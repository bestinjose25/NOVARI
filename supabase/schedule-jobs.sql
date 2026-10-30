-- Run ONLY after deploying the Edge Function and creating the job secret.
-- Put the SAME random 32+ character value in:
-- 1. Edge Functions -> Secrets -> NOVARI_JOB_SECRET
-- 2. Supabase Vault -> secret named novari_job_secret
-- Never replace this with your database password, service key or Resend key.

create extension if not exists pg_cron;
create extension if not exists pg_net;

do $$ begin
  if not exists (select 1 from vault.decrypted_secrets where name='novari_job_secret' and length(decrypted_secret)>=32) then
    raise exception 'Create the 32+ character novari_job_secret in Vault first';
  end if;
end $$;

select cron.schedule('novari-email-dispatch', '* * * * *', $job$
  select net.http_post(
    url := 'https://vdlkltslnsgggwmqgyfu.supabase.co/functions/v1/novari-enquiries/dispatch',
    headers := jsonb_build_object('Content-Type','application/json',
      'x-job-secret',(select decrypted_secret from vault.decrypted_secrets where name='novari_job_secret' limit 1)),
    body := '{}'::jsonb,
    timeout_milliseconds := 60000
  );
$job$);

select cron.schedule('novari-abandoned-uploads', '17 * * * *', $job$
  select net.http_post(
    url := 'https://vdlkltslnsgggwmqgyfu.supabase.co/functions/v1/novari-enquiries/maintenance',
    headers := jsonb_build_object('Content-Type','application/json',
      'x-job-secret',(select decrypted_secret from vault.decrypted_secrets where name='novari_job_secret' limit 1)),
    body := '{}'::jsonb,
    timeout_milliseconds := 60000
  );
$job$);
