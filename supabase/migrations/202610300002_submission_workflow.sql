begin;

create table public.novari_submission_sessions (
  id uuid primary key,
  kind text not null check (kind in ('quote', 'contact')),
  token_hash text not null,
  payload_hash text not null,
  payload jsonb not null,
  files jsonb not null default '[]',
  completed_at timestamptz,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null default now() + interval '20 minutes'
);
create table public.novari_rate_limits (
  key text primary key,
  hits integer not null default 0,
  expires_at timestamptz not null
);
alter table public.novari_email_outbox add column email_payload jsonb;
alter table public.novari_email_outbox add column lock_token uuid;

alter table public.novari_submission_sessions enable row level security;
alter table public.novari_rate_limits enable row level security;
revoke all on public.novari_submission_sessions, public.novari_rate_limits from public, anon, authenticated;
grant all on public.novari_submission_sessions, public.novari_rate_limits to service_role;

-- The function is service-only. CAPTCHA and application validation happen before
-- this transaction. The global daily cap keeps two emails per enquiry below the
-- provider's 100/day free allowance; abandoned uploads also count conservatively.
create function public.novari_start_session(
  p_id uuid, p_kind text, p_token text, p_hash text, p_payload jsonb,
  p_files jsonb, p_email_hash text
) returns void language plpgsql security definer set search_path = '' as $$
declare
  v_existing public.novari_submission_sessions;
  v_key text;
  v_limit integer;
  v_hits integer;
  v_used bigint;
  v_reserved bigint;
begin
  perform pg_catalog.pg_advisory_xact_lock(828301);
  select * into v_existing from public.novari_submission_sessions where id = p_id;
  if found then
    if v_existing.token_hash <> p_token or v_existing.payload_hash <> p_hash then
      raise exception 'SESSION_CONFLICT';
    end if;
    return;
  end if;
  if p_kind not in ('quote', 'contact') or jsonb_array_length(p_files) > 6 then raise exception 'INVALID_SESSION'; end if;
  foreach v_key in array array[
    'day:' || to_char(now() at time zone 'UTC', 'YYYY-MM-DD'),
    'email:' || p_email_hash || ':' || to_char(now() at time zone 'UTC', 'YYYY-MM-DD-HH')
  ] loop
    v_limit := case when v_key like 'day:%' then 40 else 3 end;
    insert into public.novari_rate_limits(key, hits, expires_at)
    values(v_key, 1, now() + interval '2 days')
    on conflict(key) do update set hits = public.novari_rate_limits.hits + 1
    returning hits into v_hits;
    if v_hits > v_limit then raise exception 'RATE_LIMIT'; end if;
  end loop;
  -- Reserve the bucket's maximum per signed path, not the client-declared size.
  -- Signed upload URLs remain valid for two hours. Reserve for three hours.
  select coalesce(sum((metadata->>'size')::bigint), 0) into v_used
    from storage.objects where bucket_id = 'novari-quote-uploads';
  select coalesce(sum(jsonb_array_length(files)::bigint * 26214400), 0) into v_reserved
    from public.novari_submission_sessions where created_at > now() - interval '3 hours';
  if jsonb_array_length(p_files) > 0 and v_used + v_reserved + jsonb_array_length(p_files)::bigint * 26214400 > 838860800 then
    raise exception 'STORAGE_BUDGET';
  end if;
  insert into public.novari_submission_sessions(id, kind, token_hash, payload_hash, payload, files)
    values(p_id, p_kind, p_token, p_hash, p_payload, p_files);
end;
$$;

-- Save enquiry, attachments and both email jobs atomically. Repeat completion
-- requests return the same reference instead of creating duplicate enquiries.
create function public.novari_complete_session(p_id uuid, p_token text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare
  s public.novari_submission_sessions;
  q public.novari_quote_requests;
  c public.novari_contact_requests;
  f jsonb;
  v_reference bigint;
begin
  select * into s from public.novari_submission_sessions where id = p_id for update;
  if not found or s.token_hash <> p_token then raise exception 'INVALID_SESSION'; end if;
  if s.completed_at is null then
    if s.expires_at < now() then raise exception 'EXPIRED_SESSION'; end if;
    if s.kind = 'quote' then
      q := jsonb_populate_record(null::public.novari_quote_requests, s.payload);
      insert into public.novari_quote_requests(
        id,request_id,first_name,last_name,email,phone,service,
        pickup_address,pickup_city,pickup_postal_code,pickup_floor,pickup_elevator,
        destination_address,destination_city,destination_postal_code,destination_floor,destination_elevator,
        preferred_date,items,notes,referral_source,consent_accepted
      ) values(p_id,p_id,q.first_name,q.last_name,q.email,q.phone,q.service,
        q.pickup_address,q.pickup_city,q.pickup_postal_code,q.pickup_floor,q.pickup_elevator,
        q.destination_address,q.destination_city,q.destination_postal_code,q.destination_floor,q.destination_elevator,
        q.preferred_date,q.items,q.notes,q.referral_source,q.consent_accepted);
      for f in select value from jsonb_array_elements(s.files) loop
        insert into public.novari_quote_attachments(quote_id,storage_path,original_name,content_type,file_size)
          values(p_id,f->>'path',f->>'name',f->>'type',(f->>'size')::bigint);
      end loop;
      insert into public.novari_email_outbox(quote_id,audience) values(p_id,'owner'),(p_id,'customer');
    else
      c := jsonb_populate_record(null::public.novari_contact_requests, s.payload);
      insert into public.novari_contact_requests(id,request_id,name,email,phone,message,consent_accepted)
        values(p_id,p_id,c.name,c.email,c.phone,c.message,c.consent_accepted);
      insert into public.novari_email_outbox(contact_id,audience) values(p_id,'owner'),(p_id,'customer');
    end if;
    update public.novari_submission_sessions set completed_at=now() where id=p_id;
  end if;
  if s.kind='quote' then select reference into v_reference from public.novari_quote_requests where id=p_id;
  else select reference into v_reference from public.novari_contact_requests where id=p_id; end if;
  return jsonb_build_object('success',true,'quote_id',case when s.kind='quote' then v_reference else null end,'reference',v_reference,'email_status','queued');
end;
$$;

create function public.novari_claim_email(p_lock uuid)
returns setof public.novari_email_outbox language sql security definer set search_path = '' as $$
  update public.novari_email_outbox
  set status='processing', lock_token=p_lock, locked_until=now()+interval '10 minutes', attempts=attempts+1
  where id=(select id from public.novari_email_outbox
    where (status='pending' or (status='processing' and locked_until < now()))
      and next_attempt_at<=now() and attempts<8 and created_at>now()-interval '20 hours'
    order by created_at for update skip locked limit 1)
  returning *;
$$;

revoke all on function public.novari_start_session(uuid,text,text,text,jsonb,jsonb,text) from public,anon,authenticated;
revoke all on function public.novari_complete_session(uuid,text) from public,anon,authenticated;
revoke all on function public.novari_claim_email(uuid) from public,anon,authenticated;
grant execute on function public.novari_start_session(uuid,text,text,text,jsonb,jsonb,text) to service_role;
grant execute on function public.novari_complete_session(uuid,text) to service_role;
grant execute on function public.novari_claim_email(uuid) to service_role;

commit;
