import { readFileSync } from 'node:fs'
const business = JSON.parse(readFileSync(new URL('../src/business.json', import.meta.url)))
const missing = []
for (const key of ['legalName', 'email', 'phone', 'website', 'retentionPolicy', 'backendProvider']) {
  if (!business[key]?.trim()) missing.push(key)
}
if (!business.addressLines?.length || business.addressLines.some(line => !line.trim())) missing.push('addressLines')
if (!business.representatives?.length) missing.push('representatives')
if (!business.legalReviewed) missing.push('legalReviewed')
if (!business.privacyReviewed) missing.push('privacyReviewed')
if (missing.length) {
  console.error('Launch blocked: complete and review src/business.json: ' + missing.join(', '))
  process.exit(1)
}
console.log('Business information and review flags are complete. This check does not certify legal compliance.')
