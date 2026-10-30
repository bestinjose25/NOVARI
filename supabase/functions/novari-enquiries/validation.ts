export const MAX_FILES = 6;
export const MAX_BYTES = 25 * 1024 * 1024;
export const BUCKET = "novari-quote-uploads";
export type Kind = "quote" | "contact";
export type Upload = { path: string; name: string; type: string; size: number };
export class InputError extends Error {
  constructor(public errors: Record<string, string[]>, public status = 400) {
    super("Invalid request");
  }
}
export function validUuid(value: unknown): value is string {
  return typeof value === "string" && /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}
export async function sha256(value: string) {
  const hash = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(hash), (b) => b.toString(16).padStart(2, "0")).join("");
}
export function validateData(kind: Kind, input: unknown): Record<string, unknown> {
  if (!input || typeof input !== "object" || Array.isArray(input)) throw new InputError({ form: ["Invalid form."] });
  const raw = input as Record<string, unknown>;
  const data: Record<string, unknown> = {};
  const errors: Record<string, string[]> = {};
  function text(key: string, max: number, required = false) {
    const value = raw[key] ?? "";
    if (typeof value !== "string" || value.trim().length > max || (required && !value.trim())) {
      errors[key] = [`Enter a valid value (maximum ${max} characters).`];
    } else data[key] = value.trim();
  }
  text("email", 254, true);
  if (typeof data.email !== "string" || !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(data.email)) errors.email = ["Enter a valid email address."];
  text("phone", 50, kind === "quote");
  if (raw.consent_accepted !== true) errors.consent_accepted = ["Please accept the privacy policy."];
  data.consent_accepted = true;
  if (kind === "contact") {
    text("name", 150, true);
    text("message", 10000, true);
  } else {
    text("first_name", 100, true); text("last_name", 100, true);
    const services = ["residential_move", "business_move", "furniture_transport", "furniture_assembly", "household_clearance", "carrying_assistance", "handyman", "not_sure"];
    if (!services.includes(String(raw.service))) errors.service = ["Choose a service."];
    else data.service = raw.service;
    for (const prefix of ["pickup", "destination"]) {
      text(`${prefix}_address`, 255);
      text(`${prefix}_city`, 100, true);
      text(`${prefix}_postal_code`, 20, true);
      text(`${prefix}_floor`, 30, true);
      const elevator = raw[`${prefix}_elevator`] ?? false;
      if (typeof elevator !== "boolean") errors[`${prefix}_elevator`] = ["Invalid elevator value."];
      else data[`${prefix}_elevator`] = elevator;
    }
    text("items", 500); text("notes", 10000); text("referral_source", 255);
    if (raw.preferred_date) {
      const date = String(raw.preferred_date);
      const parsed = new Date(`${date}T00:00:00Z`);
      if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !Number.isFinite(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== date) errors.preferred_date = ["Enter a valid date."];
      else data.preferred_date = date;
    } else data.preferred_date = null;
  }
  if (Object.keys(errors).length) throw new InputError(errors);
  return data;
}
export function validateUploads(input: unknown, session: string): Upload[] {
  if (!Array.isArray(input) || input.length > MAX_FILES) throw new InputError({ files: ["Upload at most 6 files."] });
  let total = 0;
  const extensions: Record<string, string> = { "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "video/mp4": "mp4" };
  return input.map((item, index) => {
    if (!item || typeof item.name !== "string" || !item.name.trim() || item.name.length > 255 || /[\r\n\0]/.test(item.name) || !Object.hasOwn(extensions, item.type) || !Number.isSafeInteger(item.size) || item.size <= 0 || item.size > MAX_BYTES) throw new InputError({ files: ["Invalid file name, type or size."] });
    total += item.size;
    if (total > MAX_BYTES) throw new InputError({ files: ["The combined upload size must not exceed 25 MB."] });
    return { path: `${session}/${index}.${extensions[item.type]}`, name: item.name.replaceAll("\\", "/").split("/").pop()!, type: item.type, size: item.size };
  });
}
// Basic signature check. This is not a malware scan or a full image/video decode.
export function matchesSignature(type: string, b: Uint8Array) {
  if (type === "image/jpeg") return b.length >= 3 && b[0] === 255 && b[1] === 216 && b[2] === 255;
  if (type === "image/png") return [137,80,78,71,13,10,26,10].every((v, i) => b[i] === v);
  const ascii = (start: number, end: number) => new TextDecoder().decode(b.slice(start, end));
  if (type === "image/webp") return b.length >= 12 && ascii(0,4) === "RIFF" && ascii(8,12) === "WEBP";
  if (type === "video/mp4") return b.length >= 16 && ascii(4,8) === "ftyp";
  return false;
}
