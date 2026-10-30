# NOVARI Supabase migration

Branch: `codex/supabase-migration`. Django and the live `main` branch are preserved.

## Project

- Reference: `vdlkltslnsgggwmqgyfu`
- Standard API URL: `https://vdlkltslnsgggwmqgyfu.supabase.co`
- No credentials are stored in this repository.

## Stage 1: database and private bucket

1. Open this project in Supabase and choose SQL Editor -> New query.
2. Paste all of `migrations/202610280001_novari_enquiries.sql` and Run.
3. Table Editor should show four `novari_` tables.
4. Storage should show `novari-quote-uploads`, marked private.
5. Do not add public read/write policies or disable RLS to connect the frontend.

The SQL is transactional. It adds no customer data and no email is sent. The
outbox is only a job table at this stage; it does not send emails by itself.
It can be rerun for an interrupted initial setup, but subsequent schema changes
must use new migrations. Existing unrelated tables/buckets are not modified.

Customer-facing functions will use a server-side secret key. Browser publishable
keys must not be granted access to enquiries or uploaded photos. The Supabase
owner can manage records through the dashboard; no custom owner UI exists yet.

## Remaining stages

- Validated form endpoints, anti-spam protection and upload sessions.
- Direct private uploads with short-lived permissions and image compression.
- HTML owner/customer emails through an email provider; durable outbox dispatch,
  idempotency and retries; verification of the `novari-gbr.de` sender domain.
- Frontend provider switch on the migration branch, with Django fallback intact.
- Cleanup of abandoned uploads and an owner-approved retention policy.
- Live preview tests of submissions, email delivery, access policies, backup/
  exports and failure recovery. Import local Django records only if requested.

Do not merge or change Netlify production variables until live tests pass.
Free project inactivity pausing, storage and email quotas need monitoring.

## Stage 2: submission workflow (prepared locally)

Run `migrations/202610300002_submission_workflow.sql` once in SQL Editor after
stage 1. This adds private upload sessions, rate limits and transactional email
jobs. It does not send emails. Do not rerun after successful completion.

## Stage 3: spam protection and secrets

Create a free Cloudflare Turnstile Managed widget for `novari-gbr.de`,
`www.novari-gbr.de` and your exact Netlify preview hostname. This does not require
changing nameservers. Keep the site key for frontend configuration; put the
secret key only in Supabase Edge Functions Secrets.

Set the names in `functions/.env.example` in Supabase:

- `RESEND_API_KEY`, `RESEND_FROM_EMAIL`, `NOVARI_NOTIFICATION_EMAIL`.
- `TURNSTILE_SECRET_KEY` and comma-separated `TURNSTILE_HOSTNAMES`.
- `ALLOWED_ORIGINS`: comma-separated exact HTTPS origins including preview.
- `NOVARI_JOB_SECRET`: a separate random secret of at least 32 characters.

Do not add API secrets to Vite variables, Git or chat. Supabase provides its
server-side database credentials automatically. Verify the sender domain in
Resend before sending from `info@novari-gbr.de`.

## Stage 4: deploy and schedule

From the repository root, with Node installed:

```powershell
npx supabase login
npx supabase functions deploy novari-enquiries --project-ref vdlkltslnsgggwmqgyfu
```

`config.toml` disables gateway JWT verification because these are public enquiry
endpoints; the application verifies Turnstile and restricts origins. Internal
jobs require the separate job secret. Do not expose privileged database keys.

Create a Vault secret named `novari_job_secret` with the SAME value as
`NOVARI_JOB_SECRET`, then run `schedule-jobs.sql`. The cron dispatcher retries
queued emails every minute; maintenance clears abandoned uploads after three
hours. Inspect Cron run history and Edge Function logs after deployment.

## Stage 5: Netlify branch preview

Configure these variables for the migration branch preview first:

```text
VITE_BACKEND_PROVIDER=supabase
VITE_SUPABASE_URL=https://vdlkltslnsgggwmqgyfu.supabase.co
VITE_TURNSTILE_SITE_KEY=<public site key>
```

Use the preview hostname in Turnstile and the Edge Function allowlists. Redeploy
after changing Vite variables. Leave production configuration and Django intact
until preview tests pass. Omitting the provider keeps the Django path.

## Delivery behavior and acceptance checks

Both forms save the enquiry and two outbox jobs in one database transaction.
Successful submission means saved/queued, not confirmed inbox delivery. Inspect
`novari_email_outbox` for `sent` or `failed`, and Resend delivery logs separately.
Retries use the same provider idempotency key and cached payload; automatic
retries stop after eight attempts or twenty hours. Failed jobs require review.

Images are compressed in the browser when possible. Up to six files and 25 MiB
combined are accepted, with metadata and header checks server-side. These are
not antivirus scans. Files stay in a private bucket. Owner emails include
seven-day signed links and attach files when the combined size is at most
10 MiB. Customer acknowledgements do not contain photo links. Forwarding an
owner email shares its temporary links.

The current conservative limits allow 40 submission sessions per UTC day and
three per email per hour, and reserve storage below 800 MiB. Free service quotas
can change; review current provider limits before launch. Saved enquiries and
completed uploads have no automatic business retention policy yet. Review and
delete/export old data through the dashboard to avoid filling storage.

Before switching production, test contact and quote submissions (including a
phone photo), owner and customer inbox delivery, required fields, spam checks,
repeated completion, denied private access, and queue retries. Get authorization
before sending real test emails. Existing Django records are not imported.

Local verification: frontend production build, Deno validation/email tests and
Deno type check. Database workflow was checked with local PGlite and a mocked
Storage catalog; live Supabase Storage, Cron and delivery still require preview
verification. No live deployment or email sending was performed locally.
