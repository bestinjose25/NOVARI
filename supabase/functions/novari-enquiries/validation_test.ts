import assert from "node:assert/strict";
import { InputError, matchesSignature, validateData, validateUploads } from "./validation.ts";
import { renderEmail } from "./email.ts";

const quote = {
  first_name: "Test", last_name: "Customer", email: "test@example.com", phone: "123456",
  service: "residential_move", consent_accepted: true,
  pickup_city: "Koblenz", pickup_postal_code: "01234", pickup_floor: "0",
  destination_city: "Neuwied", destination_postal_code: "56564", destination_floor: "EG",
};
Deno.test("required quote locations preserve postal zeros and ground floor", () => {
  assert.equal(validateData("quote", quote).pickup_postal_code, "01234");
  assert.equal(validateData("quote", quote).pickup_floor, "0");
  for (const field of ["pickup_city", "pickup_postal_code", "pickup_floor", "destination_city", "destination_postal_code", "destination_floor"]) {
    for (const value of [undefined, "", "   "]) assert.throws(() => validateData("quote", { ...quote, [field]: value }), InputError);
  }
});
Deno.test("both forms require explicit boolean consent and a valid email", () => {
  for (const consent of [undefined, false, "true", null]) {
    assert.throws(() => validateData("quote", { ...quote, consent_accepted: consent }), InputError);
    assert.throws(() => validateData("contact", { name: "Test", email: "test@example.com", message: "Hello", consent_accepted: consent }), InputError);
  }
  assert.throws(() => validateData("quote", { ...quote, email: "bad\r\nBcc: a@example.com" }), InputError);
});
Deno.test("date and field lengths are checked", () => {
  assert.throws(() => validateData("quote", { ...quote, preferred_date: "2026-02-30" }), InputError);
  assert.equal(validateData("quote", { ...quote, preferred_date: "2028-02-29" }, new Date("2028-02-28T12:00:00Z")).preferred_date, "2028-02-29");
  assert.throws(() => validateData("contact", { name: "x", email: "a@example.com", consent_accepted: true, message: "x".repeat(10001) }), InputError);
});

Deno.test("preferred dates use the Berlin calendar day and allow today", () => {
  const now = new Date("2026-10-30T23:30:00Z");
  assert.throws(() => validateData("quote", { ...quote, preferred_date: "2026-10-30" }, now), InputError);
  for (const date of ["2026-10-31", "2026-11-01"]) {
    assert.equal(validateData("quote", { ...quote, preferred_date: date }, now).preferred_date, date);
  }
  assert.equal(validateData("quote", quote, now).preferred_date, null);
});
Deno.test("upload manifest rejects unsafe types, size/count excess and header injection", () => {
  const file = { name: "photo.jpg", type: "image/jpeg", size: 1024 };
  const id = "b8709734-0463-438f-8090-67262c597e49";
  assert.equal(validateUploads([file], id)[0].path, `${id}/0.jpg`);
  for (const type of ["text/html", "toString", "constructor"]) assert.throws(() => validateUploads([{ ...file, type }], id), InputError);
  assert.throws(() => validateUploads(Array(7).fill(file), id), InputError);
  assert.throws(() => validateUploads([{ ...file, size: 14 * 1024 ** 2 }, { ...file, size: 14 * 1024 ** 2 }], id), InputError);
  assert.throws(() => validateUploads([{ ...file, name: "photo\r\n.jpg" }], id), InputError);
});
Deno.test("file signatures distinguish supported headers", () => {
  assert.ok(matchesSignature("image/jpeg", new Uint8Array([255,216,255,224])));
  assert.ok(matchesSignature("image/png", new Uint8Array([137,80,78,71,13,10,26,10])));
  assert.ok(matchesSignature("image/webp", new TextEncoder().encode("RIFF1234WEBP")));
  assert.ok(matchesSignature("video/mp4", new TextEncoder().encode("1234ftypisom1234")));
  assert.equal(matchesSignature("image/jpeg", new TextEncoder().encode("<script>bad</script>")), false);
});
Deno.test("emails escape customer content and include referral/locations", () => {
  const data = { ...quote, reference: 42, notes: '<script>alert("bad")</script>', referral_source: "Google & friends" };
  const owner = renderEmail("quote", "owner", data, [{ name: '<img src=x>', url: "https://example.com/file?x=1&y=2" }]);
  assert.ok(owner.html.includes("&lt;script&gt;"));
  assert.ok(!owner.html.includes('<script>'));
  assert.ok(owner.html.includes("Google &amp; friends"));
  assert.ok(owner.html.includes("01234 Koblenz"));
  assert.ok(owner.html.includes("&lt;img src=x&gt;"));
  const customer = renderEmail("quote", "customer", data, [{ name: "private.jpg", url: "https://private.example.com" }]);
  assert.ok(!customer.html.includes("private.example.com"));
  for (const kind of ["quote", "contact"]) {
    const acknowledgement = renderEmail(kind, "customer", { ...data, name: "Test" }, []);
    assert.ok(!acknowledgement.subject.includes("#42"));
    assert.ok(!acknowledgement.html.includes("Anfrage-Nr."));
    assert.ok(!acknowledgement.text.includes("Anfrage-Nr."));
    const notification = renderEmail(kind, "owner", { ...data, name: "Test" }, []);
    assert.ok(notification.subject.includes("#42"));
    assert.ok(notification.text.includes("Anfrage-Nr.: 42"));
  }
  assert.ok(renderEmail("contact", "owner", { name: "Test", reference: 7, email: "a@example.com", message: "Hello\nWorld" }, []).html.includes("Hello<br>World"));
});
