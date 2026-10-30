import { resolveApiBaseUrl } from './apiConfig'

const provider = import.meta.env.VITE_BACKEND_PROVIDER || 'django'
const djangoUrl = resolveApiBaseUrl(import.meta.env.VITE_API_BASE_URL, import.meta.env.DEV)
const supabaseUrl = resolveApiBaseUrl(import.meta.env.VITE_SUPABASE_URL, import.meta.env.DEV)
export const usesSupabase = provider === 'supabase'
export const turnstileSiteKey = import.meta.env.VITE_TURNSTILE_SITE_KEY || ''
export const formsAvailable = usesSupabase ? Boolean(supabaseUrl && turnstileSiteKey) : Boolean(djangoUrl)
const attempts = new Map()
export function clearEnquiryAttempt() { attempts.clear() }

export async function compressPhoto(file) {
  if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) return file
  // Avoid decoding decompression bombs in the browser; server uploads are
  // still constrained by the declared/bucket limits and signature checks.
  const bitmap = await createImageBitmap(file)
  try {
    const scale = Math.min(1, 1920 / Math.max(bitmap.width, bitmap.height))
    const canvas = document.createElement('canvas')
    canvas.width = Math.max(1, Math.round(bitmap.width * scale))
    canvas.height = Math.max(1, Math.round(bitmap.height * scale))
    const context = canvas.getContext('2d')
    if (!context) throw new Error('Image conversion unavailable')
    context.fillStyle = '#fff'
    context.fillRect(0, 0, canvas.width, canvas.height)
    context.drawImage(bitmap, 0, 0, canvas.width, canvas.height)
    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.8))
    if (!blob || blob.size >= file.size) return file
    return new File([blob], file.name.replace(/\.[^.]+$/, '') + '.jpg', { type: 'image/jpeg', lastModified: file.lastModified })
  } finally { bitmap.close() }
}

async function endpoint(route, body) {
  return fetch(`${supabaseUrl}/functions/v1/novari-enquiries/${route}`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  })
}
export async function submitEnquiry(kind, input, captcha) {
  if (!formsAvailable) throw new Error('Forms unavailable')
  if (!usesSupabase) {
    return fetch(`${djangoUrl}/api/${kind}/`, input instanceof FormData
      ? { method: 'POST', body: input }
      : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(input) })
  }
  const data = input instanceof FormData ? Object.fromEntries([...input.entries()].filter(([key]) => key !== 'files')) : { ...input }
  for (const key of ['consent_accepted', 'pickup_elevator', 'destination_elevator']) {
    if (key in data) data[key] = data[key] === true || data[key] === 'true'
  }
  const originals = input instanceof FormData ? input.getAll('files') : []
  const fingerprint = JSON.stringify({ kind, data, files: originals.map(file => [file.name, file.size, file.lastModified]) })
  // In-memory only: no names, messages or upload tokens are saved in localStorage.
  let attempt = attempts.get(fingerprint)
  if (!attempt || Date.now() - attempt.created > 18 * 60_000) {
    const files = []
    for (const file of originals) files.push(await compressPhoto(file))
    attempt = { request_id: crypto.randomUUID(), token: crypto.randomUUID(), files, created: Date.now() }
    attempts.clear()
    attempts.set(fingerprint, attempt)
  }
  const { request_id, token, files } = attempt
  const started = await endpoint('start', {
    request_id, token, kind, data, captcha,
    files: files.map(file => ({ name: file.name, size: file.size, type: file.type })),
  })
  if (!started.ok) return started
  const result = await started.json()
  if (result.email_status === 'queued') return new Response(JSON.stringify(result), { status: 201 })
  for (let i = 0; i < files.length; i++) {
    const upload = result.uploads[i]
    if (upload.uploaded) continue
    const response = await fetch(upload.url, {
      method: 'PUT', headers: { 'Content-Type': files[i].type, 'x-upsert': 'false' }, body: files[i],
    })
    if (!response.ok) throw new Error('Photo upload failed. Retry without closing the page.')
  }
  return endpoint('complete', { request_id, token })
}
