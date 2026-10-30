export function escapeHtml(value: unknown): string {
  return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");
}
const SERVICES: Record<string, string> = {
  residential_move: "Privatumzug", business_move: "Firmenumzug", furniture_transport: "Möbeltransport",
  furniture_assembly: "Möbelmontage / Demontage", household_clearance: "Haushaltsauflösung",
  carrying_assistance: "Tragehilfe", handyman: "Kleinarbeiten / Handwerkerhilfe", not_sure: "Noch nicht sicher",
};
export function renderEmail(kind: string, audience: string, data: Record<string, unknown>, files: { name: string; url: string }[]) {
  const owner = audience === "owner";
  const quote = kind === "quote";
  const name = quote ? `${data.first_name} ${data.last_name}` : String(data.name);
  const subject = owner
    ? `Neue NOVARI ${quote ? "Angebotsanfrage" : "Kontaktanfrage"} #${data.reference}`
    : `Ihre ${quote ? "Anfrage" : "Nachricht"} bei NOVARI #${data.reference} wurde erhalten`;
  const rows: [string, unknown][] = [["Anfrage-Nr.", data.reference], ["Name", name], ["E-Mail", data.email], ["Telefon", data.phone || "-"]];
  if (quote) rows.push(
    ["Dienstleistung", SERVICES[String(data.service)] || data.service],
    ["Abholadresse", data.pickup_address || "-"], ["Abholort", `${data.pickup_postal_code} ${data.pickup_city}`],
    ["Abholetage", data.pickup_floor], ["Aufzug (Abholung)", data.pickup_elevator ? "Ja" : "Nein"],
    ["Zieladresse", data.destination_address || "-"], ["Zielort", `${data.destination_postal_code} ${data.destination_city}`],
    ["Zieletage", data.destination_floor], ["Aufzug (Ziel)", data.destination_elevator ? "Ja" : "Nein"],
    ["Wunschtermin", data.preferred_date || "-"], ["Gegenstände", data.items || "-"],
    ["Zusätzliche Informationen", data.notes || "-"], ["Wie haben Sie von uns erfahren?", data.referral_source || "-"]);
  else rows.push(["Nachricht", data.message]);
  const intro = owner ? "Eine neue Anfrage wurde über die NOVARI-Website gesendet."
    : `Hallo ${name}, vielen Dank für Ihre Nachricht. Wir haben Ihre Anfrage erhalten und melden uns schnellstmöglich bei Ihnen.`;
  const fileText = owner && files.length ? "\n\nDateien (Links 7 Tage gültig):\n" + files.map(f => `${f.name}: ${f.url}`).join("\n") : "";
  const text = `${intro}\n\n${rows.map(([label, value]) => `${label}: ${value}`).join("\n\n")}${fileText}\n\nAntworten Sie auf diese E-Mail, um weitere Informationen zu ergänzen.\nNOVARI GbR`;
  const fileHtml = owner && files.length ? `<h2 style="font-size:18px">Dateien</h2><ul>${files.map(f => `<li><a href="${escapeHtml(f.url)}">${escapeHtml(f.name)}</a></li>`).join("")}</ul><p>Download-Links sind 7 Tage gültig. Die Dateien bleiben im privaten Supabase-Projekt des Unternehmens verfügbar, solange sie dort gespeichert sind.</p>` : "";
  const html = `<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><body style="margin:0;background:#f4f6f5;font-family:Arial,Helvetica,sans-serif;color:#0c272b"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:24px 12px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:680px;background:white;border:1px solid #d8e1e0;border-radius:16px;overflow:hidden"><tr><td style="background:#0c272b;padding:28px;color:white"><div style="font-size:30px;font-weight:800"><span style="color:#f52408">N</span>OVARI</div><p style="color:#b7c6c7">Umzug &amp; Möbelmontage</p></td></tr><tr><td style="padding:28px"><h1 style="font-size:25px">${escapeHtml(subject)}</h1><p style="line-height:1.7">${escapeHtml(intro)}</p><table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rows.map(([label, value]) => `<tr><td style="padding:10px 8px;border-bottom:1px solid #edf1f0;color:#526468;vertical-align:top">${escapeHtml(label)}</td><td style="padding:10px 8px;border-bottom:1px solid #edf1f0;word-break:break-word">${escapeHtml(value).replaceAll("\n", "<br>")}</td></tr>`).join("")}</table>${fileHtml}<p style="line-height:1.7">Antworten Sie auf diese E-Mail, um weitere Informationen zu ergänzen.</p></td></tr><tr><td style="padding:24px;background:#0c272b;color:#b7c6c7;text-align:center">NOVARI GbR<br>Diese E-Mail wurde automatisch versendet.</td></tr></table></td></tr></table></body></html>`;
  return { subject, html, text };
}
