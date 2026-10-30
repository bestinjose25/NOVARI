-- Run once in this project's Supabase SQL Editor, or with Supabase migrations.
-- Customer data is service-side only: no anonymous/public read or write policies.
begin;

create table if not exists public.novari_quote_requests (
  id uuid primary key default gen_random_uuid(),
  reference bigint generated always as identity unique,
  request_id uuid not null unique,
  first_name varchar(100) not null check (length(btrim(first_name)) > 0),
  last_name varchar(100) not null check (length(btrim(last_name)) > 0),
  email varchar(254) not null check (length(btrim(email)) > 0),
  phone varchar(50) not null check (length(btrim(phone)) > 0),
  service varchar(50) not null check (service in (
    'residential_move', 'business_move', 'furniture_transport', 'furniture_assembly',
    'household_clearance', 'carrying_assistance', 'handyman', 'not_sure'
  )),
  pickup_address varchar(255) not null default '',
  pickup_city varchar(100) not null check (length(btrim(pickup_city)) > 0),
  pickup_postal_code varchar(20) not null check (length(btrim(pickup_postal_code)) > 0),
  pickup_floor varchar(30) not null check (length(btrim(pickup_floor)) > 0),
  pickup_elevator boolean not null default false,
  destination_address varchar(255) not null default '',
  destination_city varchar(100) not null check (length(btrim(destination_city)) > 0),
  destination_postal_code varchar(20) not null check (length(btrim(destination_postal_code)) > 0),
  destination_floor varchar(30) not null check (length(btrim(destination_floor)) > 0),
  destination_elevator boolean not null default false,
  preferred_date date,
  items varchar(500) not null default '',
  notes text not null default '' check (length(notes) <= 10000),
  referral_source varchar(255) not null default '',
  consent_accepted boolean not null check (consent_accepted = true),
  consent_version text not null default '2026-10',
  status text not null default 'new' check (status in ('new', 'contacted', 'quoted', 'closed')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.novari_contact_requests (
  id uuid primary key default gen_random_uuid(),
  reference bigint generated always as identity unique,
  request_id uuid not null unique,
  name varchar(150) not null check (length(btrim(name)) > 0),
  email varchar(254) not null check (length(btrim(email)) > 0),
  phone varchar(50) not null default '',
  message text not null check (length(btrim(message)) between 1 and 10000),
  consent_accepted boolean not null check (consent_accepted = true),
  consent_version text not null default '2026-10',
  is_read boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.novari_quote_attachments (
  id uuid primary key default gen_random_uuid(),
  quote_id uuid not null references public.novari_quote_requests(id) on delete cascade,
  storage_path text not null unique,
  original_name varchar(255) not null,
  content_type text not null check (content_type in ('image/jpeg', 'image/png', 'image/webp', 'video/mp4')),
  file_size bigint not null check (file_size > 0 and file_size <= 26214400),
  created_at timestamptz not null default now()
);

-- Durable email jobs: successful form storage must not depend on email speed.
-- Delivery functions and retry scheduling are configured in the next stage.
create table if not exists public.novari_email_outbox (
  id uuid primary key default gen_random_uuid(),
  quote_id uuid references public.novari_quote_requests(id) on delete cascade,
  contact_id uuid references public.novari_contact_requests(id) on delete cascade,
  audience text not null check (audience in ('owner', 'customer')),
  status text not null default 'pending' check (status in ('pending', 'processing', 'sent', 'failed')),
  attempts integer not null default 0 check (attempts >= 0),
  next_attempt_at timestamptz not null default now(),
  locked_until timestamptz,
  provider_message_id text,
  last_error_code text,
  sent_at timestamptz,
  created_at timestamptz not null default now(),
  check (num_nonnulls(quote_id, contact_id) = 1)
);

create unique index if not exists novari_email_quote_audience
  on public.novari_email_outbox(quote_id, audience) where quote_id is not null;
create unique index if not exists novari_email_contact_audience
  on public.novari_email_outbox(contact_id, audience) where contact_id is not null;
create index if not exists novari_email_pending
  on public.novari_email_outbox(status, next_attempt_at);
create index if not exists novari_quote_created on public.novari_quote_requests(created_at desc);
create index if not exists novari_contact_created on public.novari_contact_requests(created_at desc);
create index if not exists novari_attachment_quote on public.novari_quote_attachments(quote_id);

create or replace function public.novari_touch_updated_at()
returns trigger language plpgsql set search_path = '' as $$
begin
  new.updated_at = pg_catalog.now();
  return new;
end;
$$;
revoke all on function public.novari_touch_updated_at() from public, anon, authenticated;

drop trigger if exists novari_quote_updated on public.novari_quote_requests;
create trigger novari_quote_updated before update on public.novari_quote_requests
  for each row execute function public.novari_touch_updated_at();
drop trigger if exists novari_contact_updated on public.novari_contact_requests;
create trigger novari_contact_updated before update on public.novari_contact_requests
  for each row execute function public.novari_touch_updated_at();

alter table public.novari_quote_requests enable row level security;
alter table public.novari_contact_requests enable row level security;
alter table public.novari_quote_attachments enable row level security;
alter table public.novari_email_outbox enable row level security;

revoke all on public.novari_quote_requests, public.novari_contact_requests,
  public.novari_quote_attachments, public.novari_email_outbox from public, anon, authenticated;
grant all on public.novari_quote_requests, public.novari_contact_requests,
  public.novari_quote_attachments, public.novari_email_outbox to service_role;
revoke all on sequence public.novari_quote_requests_reference_seq,
  public.novari_contact_requests_reference_seq from public, anon, authenticated;
grant usage, select on sequence public.novari_quote_requests_reference_seq,
  public.novari_contact_requests_reference_seq to service_role;

insert into storage.buckets(id, name, public, file_size_limit, allowed_mime_types)
values ('novari-quote-uploads', 'novari-quote-uploads', false, 26214400,
  array['image/jpeg', 'image/png', 'image/webp', 'video/mp4'])
on conflict (id) do nothing;

-- Do not silently reuse an existing public or differently configured bucket.
do $$
begin
  if exists (
    select 1 from storage.buckets where id = 'novari-quote-uploads'
      and (public or file_size_limit is distinct from 26214400
           or allowed_mime_types is distinct from array['image/jpeg', 'image/png', 'image/webp', 'video/mp4']::text[])
  ) then
    raise exception 'The novari-quote-uploads bucket already exists with different settings. Review it before continuing.';
  end if;
end;
$$;

-- No storage.objects policies are added. Signed, server-authorized uploads and
-- downloads will be issued by functions; the browser cannot list private files.
commit;
