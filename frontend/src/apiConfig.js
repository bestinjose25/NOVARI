// A missing backend must never produce requests to /undefined/api/... .
export function resolveApiBaseUrl(value, development = false) {
  const input = (value || '').trim()
  if (!input) return ''
  try {
    const url = new URL(input)
    const local = ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)
    if (url.username || url.password || url.search || url.hash || url.pathname !== '/') return ''
    if (url.protocol !== 'https:' && !(development && local && url.protocol === 'http:')) return ''
    if (local && !development) return ''
    return url.origin
  } catch {
    return ''
  }
}
