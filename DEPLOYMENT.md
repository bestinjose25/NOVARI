# Production preparation and launch checklist

## Status

Technical preparation is implemented. Do not publish the legal pages until the
business owner supplies and reviews the missing information in
`frontend/src/business.json`. Run `npm.cmd --prefix frontend run check:release`.
This is a release checklist, not a certificate of legal compliance. Blank register
or VAT fields mean not supplied; they must be checked for applicability.
The privacy draft needs the controller address/representatives, retention policy,
applicable legal bases, actual production processors/regions and contractual
transfer safeguards, supervisory authority and any applicable additional notices
reviewed before setting privacyReviewed/legalReviewed. Never set these flags just
to bypass the check. Confirm the public email is monitored.

## Render (after account/service purchase, not performed by this change)

- Backend root: `backend`; Python 3.13.13; paid instance in Frankfurt.
- Settings: `DJANGO_SETTINGS_MODULE=config.settings_production`.
- Enter all keys in `backend/.env.production.example` privately in Render.
  This template deliberately has empty secrets and example domains.
- Web service and paid PostgreSQL in the same region. Use its internal URL;
  an external PostgreSQL connection must use `?sslmode=require`.
- Disk mount `/var/data`; set `MEDIA_ROOT=/var/data/media`.
- Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Pre-deploy: `python manage.py migrate --noinput`
- Start: `gunicorn -c gunicorn.conf.py config.wsgi:application`
- Health-check path: `/health/` (checks DB, returns only status).
- In the service shell: `python manage.py createsuperuser`.
- Apply deployment checks using `python manage.py check --deploy`.

Production refuses missing secrets, weak keys, wildcard hosts and HTTP origins.
HTTPS redirection and secure cookies are enabled. HSTS is deliberately limited to
one hour on the API hostname. The two optional check warnings about HSTS
includeSubDomains/preload remain intentional until every domain/subdomain is
verified HTTPS; do not preload an unverified deployment.

Do not use `settings_local.py` on Render. The default WSGI/ASGI entry points select
production. Local commands must continue specifying `--settings=config.settings_local`.
Local SQLite data/accounts and uploaded files are not automatically migrated.

## Netlify

- Frontend base directory: `frontend`; publish `dist`; Node 24.19+.
- Set `VITE_API_BASE_URL` to the HTTPS API origin (no path) when the backend is ready.
  It may be left unset for a frontend-only deployment; both forms show an email
  alternative and cannot submit until a backend is configured. A nonempty invalid
  origin still blocks Netlify builds.
- Build command for public launch: `npm run check:release && npm run build`.
- Rebuild after changing this variable. Never place SMTP/database secrets in VITE variables.
- `vue-i18n` and self-hosted fonts are direct frontend dependencies; frontend-only
  dependency installation now works without relying on root node_modules.
- Existing `public/_redirects` supports direct visits to client routes.

## Uploads, email and abuse limits

- Maximum 6 files, 25 MB combined; the streaming upload handler stops excess data.
- Images are checked using Pillow (type, integrity, dimensions); MP4 receives a
  container-header check, not malware scanning or full video decoding.
- No public `/media/` serving, even locally. Staff with quote/attachment view
  permissions download files using `/admin/quote-files/<id>/` and admin links.
  Downloads are attachments with private/no-store and nosniff headers.
- SMTP remains synchronous. Timeout is 120 seconds; Gunicorn allows 300 seconds.
  A durable mail queue/retries remains a future reliability improvement. Files over
  the existing 15 MB email attachment budget stay in admin rather than being attached.
- Both APIs require explicit true consent. Production anonymous requests are
  throttled at 10/hour per client IP. This is best-effort, process-local protection;
  verify Render proxy/IP handling in staging. For heavier traffic, use shared
  throttling storage and provider/WAF controls.
- Backups: verify PostgreSQL recovery, disk snapshot policy and a separate export/
  restore process. Photos may contain personal data; restrict access and retention.

## Verification before launch

1. Finish business data and review the Impressum/privacy drafts.
2. Run backend tests: `python manage.py test quotes contacts config --settings=config.settings_local`.
3. Run frontend build and release checks; audit npm and requirements again before launch.
4. Set real domains/SMTP/database/disk values; deploy backend, then frontend.
5. Test health, admin login, both forms with/without photos, both inboxes, private
   download permissions, CORS, direct client routes and a redeploy preserving files.
6. Test production database restore and decide whether existing local enquiries
   need importing. No live emails or hosting purchases are part of preparation.

References: Django deployment checklist https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/
Render deployment https://render.com/docs/deploy-django
Render disks https://render.com/docs/disks
