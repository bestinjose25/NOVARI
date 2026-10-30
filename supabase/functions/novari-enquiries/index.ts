import { createClient } from "npm:@supabase/supabase-js@2.118.0";
import { BUCKET, InputError, matchesSignature, sha256, validateData, validateUploads, validUuid, type Kind, type Upload } from "./validation.ts";
import { renderEmail } from "./email.ts";

const env = (name: string) => {
  const value = Deno.env.get(name)?.trim();
  if (!value) throw new Error(`Missing configuration: ${name}`);
  return value;
};
function database() {
  const keys = JSON.parse(Deno.env.get("SUPABASE_SECRET_KEYS") || "{}");
  return createClient(env("SUPABASE_URL"), keys.default || env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false, autoRefreshToken: false } });
}
type DB = ReturnType<typeof database>;
function checked<T>(result: { data: T; error: unknown }): T {
  if (result.error) throw result.error;
  return result.data;
}
async function smallJson(req: Request) {
  const reader = req.body?.getReader();
  if (!reader) throw new InputError({ form: ["Missing body."] });
  let length = 0;
  const chunks: Uint8Array[] = [];
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    length += value.length;
    if (length > 65536) { await reader.cancel(); throw new InputError({ form: ["Request too large."] }, 413); }
    chunks.push(value);
  }
  const bytes = new Uint8Array(length); let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
  try {
    const value = JSON.parse(new TextDecoder().decode(bytes));
    if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("Expected object");
    return value;
  }
  catch { throw new InputError({ form: ["Invalid JSON."] }); }
}
async function captcha(token: unknown, origin: string, action: string) {
  if (typeof token !== "string" || token.length > 2048) throw new InputError({ captcha: ["Complete the security check."] });
  const result = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST", body: new URLSearchParams({ secret: env("TURNSTILE_SECRET_KEY"), response: token }),
    signal: AbortSignal.timeout(10000),
  });
  if (!result.ok) throw new Error("CAPTCHA service unavailable");
  const value = await result.json();
  const hosts = env("TURNSTILE_HOSTNAMES").split(",").map(s => s.trim());
  if (!value.success || !hosts.includes(value.hostname) || value.hostname !== new URL(origin).hostname || value.action !== action) throw new InputError({ captcha: ["Security check expired. Please try again."] });
}
async function authorizedSession(db: DB, body: Record<string, unknown>) {
  if (!validUuid(body.request_id) || !validUuid(body.token)) throw new InputError({ form: ["Invalid session."] });
  const hash = await sha256(body.token);
  const session = checked(await db.from("novari_submission_sessions").select("*").eq("id", body.request_id).maybeSingle());
  if (!session || session.token_hash !== hash) throw new InputError({ form: ["Invalid session."] }, 403);
  if (!session.completed_at && Date.parse(session.expires_at) < Date.now()) throw new InputError({ form: ["Upload session expired. Reload and try again."] }, 410);
  return session;
}
async function start(db: DB, body: Record<string, unknown>, origin: string) {
  if (!validUuid(body.request_id) || !validUuid(body.token) || !["quote", "contact"].includes(String(body.kind))) throw new InputError({ form: ["Invalid request."] });
  if (body.website) throw new InputError({ form: ["Submission rejected."] });
  const kind = body.kind as Kind;
  const data = validateData(kind, body.data);
  const files = validateUploads(body.files ?? [], body.request_id);
  if (kind === "contact" && files.length) throw new InputError({ files: ["Contact messages do not accept files."] });
  const tokenHash = await sha256(body.token);
  const payloadHash = await sha256(JSON.stringify({ kind, data, files }));
  const existing = checked(await db.from("novari_submission_sessions").select("id,token_hash,payload_hash").eq("id", body.request_id).maybeSingle());
  if (existing) {
    if (existing.token_hash !== tokenHash || existing.payload_hash !== payloadHash) throw new InputError({ form: ["Session conflict. Reload and try again."] }, 409);
  } else {
    await captcha(body.captcha, origin, kind);
    checked(await db.rpc("novari_start_session", {
      p_id: body.request_id, p_kind: kind, p_token: tokenHash, p_hash: payloadHash,
      p_payload: data, p_files: files, p_email_hash: await sha256(String(data.email).toLowerCase()),
    }));
  }
  const session = await authorizedSession(db, body);
  if (session.completed_at) return checked(await db.rpc("novari_complete_session", { p_id: session.id, p_token: tokenHash }));
  const uploads = [];
  for (const file of files) {
    const info = await db.storage.from(BUCKET).info(file.path);
    if (!info.error) { uploads.push({ ...file, uploaded: true }); continue; }
    const signed = checked(await db.storage.from(BUCKET).createSignedUploadUrl(file.path, { upsert: false }))!;
    uploads.push({ ...file, url: signed.signedUrl, uploaded: false });
  }
  return { success: true, uploads };
}
async function verifyFiles(db: DB, files: Upload[]) {
  for (const file of files) {
    const info = checked(await db.storage.from(BUCKET).info(file.path))!;
    if (info.size !== file.size || info.contentType !== file.type) throw new InputError({ files: ["Uploaded file does not match the declared size/type."] });
    const signed = checked(await db.storage.from(BUCKET).createSignedUrl(file.path, 60))!;
    const response = await fetch(signed.signedUrl, { headers: { Range: "bytes=0-63" }, signal: AbortSignal.timeout(15000) });
    if (!response.ok) throw new Error("Storage read unavailable");
    const reader = response.body?.getReader();
    const prefix: number[] = [];
    try {
      while (reader && prefix.length < 64) {
        const chunk = await reader.read();
        if (chunk.done) break;
        prefix.push(...chunk.value.slice(0, 64 - prefix.length));
      }
    } finally { await reader?.cancel(); }
    if (!matchesSignature(file.type, new Uint8Array(prefix))) throw new InputError({ files: ["The file content is not a supported image or MP4."] });
  }
}
async function complete(db: DB, body: Record<string, unknown>) {
  const session = await authorizedSession(db, body);
  if (!session.completed_at) await verifyFiles(db, session.files);
  return checked(await db.rpc("novari_complete_session", { p_id: session.id, p_token: session.token_hash }));
}

async function emailEnvelope(db: DB, job: Record<string, any>) {
  const kind = job.quote_id ? "quote" : "contact";
  const table = job.quote_id ? "novari_quote_requests" : "novari_contact_requests";
  const data = checked(await db.from(table).select("*").eq("id", job.quote_id || job.contact_id).single());
  const owner = job.audience === "owner";
  const files = job.quote_id && owner ? checked(await db.from("novari_quote_attachments").select("*").eq("quote_id", job.quote_id)) : [];
  const links = [];
  const attachments = [];
  let attachmentBytes = 0;
  for (const file of files || []) {
    // Allow browsers to display supported images instead of forcing a download.
    const signed = checked(await db.storage.from(BUCKET).createSignedUrl(file.storage_path, 7 * 86400))!;
    links.push({ name: file.original_name, url: signed.signedUrl });
    if (attachmentBytes + file.file_size <= 10 * 1024 * 1024) {
      attachments.push({ filename: file.original_name, path: signed.signedUrl });
      attachmentBytes += file.file_size;
    }
  }
  return {
    from: env("RESEND_FROM_EMAIL"),
    to: [owner ? env("NOVARI_NOTIFICATION_EMAIL") : data.email],
    reply_to: owner ? data.email : env("NOVARI_NOTIFICATION_EMAIL"),
    ...renderEmail(kind, job.audience, data, links),
    ...(attachments.length ? { attachments } : {}),
  };
}
// Stable, persisted envelopes and idempotency keys prevent duplicates after a
// timeout. Automatic retries stop before Resend's 24-hour deduplication expires.
export async function dispatch(db: DB) {
  let sent = 0;
  for (let index = 0; index < 2; index++) {
    const lease = crypto.randomUUID();
    const jobs = checked(await db.rpc("novari_claim_email", { p_lock: lease }));
    if (!jobs?.length) break;
    const job = jobs[0];
    let errorCode = "SEND_FAILED";
    let permanent = false;
    try {
      let payload = job.email_payload;
      if (!payload) {
        payload = await emailEnvelope(db, job);
        checked(await db.from("novari_email_outbox").update({ email_payload: payload }).eq("id", job.id).eq("lock_token", lease).select("id").single());
      }
      const response = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${env("RESEND_API_KEY")}`, "Content-Type": "application/json", "Idempotency-Key": `novari-${job.id}` },
        body: JSON.stringify(payload), signal: AbortSignal.timeout(25000),
      });
      if (!response.ok) {
        errorCode = `EMAIL_HTTP_${response.status}`;
        permanent = response.status >= 400 && response.status < 500 && ![408,409,429].includes(response.status);
        throw new Error(errorCode);
      }
      const result = await response.json();
      if (typeof result.id !== "string") throw new Error("Invalid email provider response");
      checked(await db.from("novari_email_outbox").update({ status: "sent", sent_at: new Date().toISOString(), provider_message_id: result.id, last_error_code: null, lock_token: null, locked_until: null }).eq("id", job.id).eq("lock_token", lease));
      sent++;
    } catch {
      const failed = permanent || job.attempts >= 8;
      checked(await db.from("novari_email_outbox").update({
        status: failed ? "failed" : "pending", last_error_code: errorCode,
        next_attempt_at: new Date(Date.now() + Math.min(3600, 60 * 2 ** job.attempts) * 1000).toISOString(),
        lock_token: null, locked_until: null,
      }).eq("id", job.id).eq("lock_token", lease));
      console.warn("Email job not sent", job.id, errorCode);
    }
  }
  return { sent };
}
async function maintenance(db: DB) {
  const cutoff = new Date(Date.now() - 3 * 3600_000).toISOString();
  const sessions = checked(await db.from("novari_submission_sessions").select("id,files").is("completed_at", null).lt("created_at", cutoff).limit(20));
  for (const session of sessions || []) {
    const paths = session.files.map((file: Upload) => file.path);
    if (paths.length) checked(await db.storage.from(BUCKET).remove(paths));
    checked(await db.from("novari_submission_sessions").delete().eq("id", session.id).is("completed_at", null));
  }
  checked(await db.from("novari_submission_sessions").delete().not("completed_at", "is", null).lt("completed_at", new Date(Date.now() - 7 * 86400_000).toISOString()));
  checked(await db.from("novari_rate_limits").delete().lt("expires_at", new Date().toISOString()));
  checked(await db.from("novari_email_outbox").update({ status: "failed", last_error_code: "RETRY_WINDOW_EXPIRED" }).in("status", ["pending", "processing"]).lt("created_at", new Date(Date.now() - 20 * 3600_000).toISOString()));
  return { cleaned: sessions?.length || 0 };
}
export async function handler(req: Request) {
  const origin = req.headers.get("Origin") || "";
  const allow = (Deno.env.get("ALLOWED_ORIGINS") || "").split(",").map(s => s.trim()).filter(Boolean);
  const cors: Record<string, string> = allow.includes(origin) ? { "Access-Control-Allow-Origin": origin, "Access-Control-Allow-Headers": "content-type", "Access-Control-Allow-Methods": "POST, OPTIONS", "Vary": "Origin" } : {};
  const json = (value: unknown, status = 200) => new Response(JSON.stringify(value), { status, headers: { ...cors, "Content-Type": "application/json", "Cache-Control": "no-store" } });
  try {
    const route = new URL(req.url).pathname.split("/").filter(Boolean).pop();
    if (route === "dispatch" || route === "maintenance") {
      if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);
      if (await sha256(req.headers.get("x-job-secret") || "") !== await sha256(env("NOVARI_JOB_SECRET"))) return json({ error: "Unauthorized" }, 401);
      return json(route === "dispatch" ? await dispatch(database()) : await maintenance(database()));
    }
    if (!allow.includes(origin)) return json({ error: "Origin not allowed" }, 403);
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);
    const body = await smallJson(req);
    const db = database();
    if (route === "start") return json(await start(db, body, origin));
    if (route === "complete") {
      const result = await complete(db, body);
      const work = dispatch(db).catch(() => console.error("Email dispatcher unavailable; queued jobs remain for cron."));
      const runtime = (globalThis as unknown as { EdgeRuntime?: { waitUntil: (p: Promise<unknown>) => void } }).EdgeRuntime;
      if (runtime) runtime.waitUntil(work); else await work;
      return json(result, 201);
    }
    return json({ error: "Not found" }, 404);
  } catch (error) {
    if (error instanceof InputError) return json({ success: false, errors: error.errors }, error.status);
    const message = error && typeof error === "object" && "message" in error ? String(error.message) : "";
    if (message.includes("RATE_LIMIT")) return json({ errors: { form: ["Too many submissions. Please try later or email us."] } }, 429);
    if (message.includes("STORAGE_BUDGET")) return json({ errors: { files: ["Photo storage is temporarily full. Please email your photos."] } }, 503);
    if (/SESSION/.test(message)) return json({ errors: { form: ["Session expired or invalid. Reload and try again."] } }, 409);
    console.error("Enquiry request failed", error instanceof Error ? error.name : "BackendError");
    return json({ errors: { form: ["Submission unavailable. Please retry or email us."] } }, 503);
  }
}
Deno.serve(handler);
