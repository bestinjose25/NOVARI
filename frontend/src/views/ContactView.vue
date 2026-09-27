<script setup>
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Footer from '@/components/Footer.vue'
import ServiceAreaMap from '../components/ServiceAreaMap.vue'

const { t } = useI18n({
  useScope: 'global',
})



const API_BASE_URL = import.meta.env.VITE_API_BASE_URL


const form = reactive({
  name: '',
  phone: '',
  email: '',
  message: '',
  consent: false,
})


const errors = reactive({
  name: '',
  email: '',
  message: '',
  consent: '',
})


const loading = ref(false)
const success = ref(false)
const submitError = ref('')


const resetErrors = () => {
  errors.name = ''
  errors.email = ''
  errors.message = ''
  errors.consent = ''
  submitError.value = ''
}


const validateForm = () => {
  resetErrors()

  let valid = true


  if (!form.name.trim()) {
    errors.name = t('contactPage.form.errors.name')
    valid = false
  }


  if (!form.email.trim()) {
    errors.email = t('contactPage.form.errors.email')
    valid = false
  }


  if (!form.message.trim()) {
    errors.message = t('contactPage.form.errors.message')
    valid = false
  }


  if (!form.consent) {
    errors.consent = t('contactPage.form.errors.consent')
    valid = false
  }


  return valid
}


const resetForm = () => {
  form.name = ''
  form.phone = ''
  form.email = ''
  form.message = ''
  form.consent = false
}


const submitForm = async () => {

  if (!validateForm()) {
    return
  }


  loading.value = true
  success.value = false
  submitError.value = ''


  try {

    const response = await fetch(
      `${API_BASE_URL}/api/contact/`,
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json',
        },

        body: JSON.stringify({
          name: form.name,
          phone: form.phone,
          email: form.email,
          message: form.message,

          // Vue uses "consent"
          // Django uses "consent_accepted"
          consent_accepted: form.consent,
        }),
      }
    )


    const data = await response.json()


    if (!response.ok) {

      console.error(
        'Backend validation error:',
        data
      )


      if (data.errors) {

        if (data.errors.name) {
          errors.name = data.errors.name[0]
        }


        if (data.errors.email) {
          errors.email = data.errors.email[0]
        }


        if (data.errors.message) {
          errors.message = data.errors.message[0]
        }


        if (data.errors.consent_accepted) {
          errors.consent =
            data.errors.consent_accepted[0]
        }

      }


      throw new Error(
        'Contact request failed'
      )
    }


    success.value = true

    resetForm()

  }
  catch (error) {

    console.error(
      'Contact form error:',
      error
    )


    /*
      Only show the general error if we
      don't already have field errors.
    */

    const hasFieldErrors =
      errors.name ||
      errors.email ||
      errors.message ||
      errors.consent


    if (!hasFieldErrors) {
      submitError.value =
        t('contactPage.form.submitError')
    }

  }
  finally {

    loading.value = false

  }
}
</script>

<template>
  <main class="contact-page">

    <!-- =========================================
         HERO
    ========================================== -->
    <section class="contact-hero">

      <div class="contact-wrap">

        <span class="eyebrow">
          {{ t('contactPage.hero.eyebrow') }}
        </span>

        <h1>
          {{ t('contactPage.hero.title') }}
        </h1>

        <p>
          {{ t('contactPage.hero.description') }}
        </p>

      </div>

    </section>


    <!-- =========================================
         CONTACT CONTENT
    ========================================== -->
    <section class="contact-section">

      <div class="contact-wrap contact-grid">


        <!-- =====================================
             LEFT SIDE
        ====================================== -->
        <div>

          <!-- QUICK CONTACT CARDS -->
          <div class="contact-cards">


            <!-- WHATSAPP -->
            <a
              class="contact-card"
              href="https://wa.me/491785129865"
              target="_blank"
              rel="noopener"
            >

              <div class="contact-icon whatsapp">

                <svg
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    d="M12 2a10 10 0 0 0-8.7 15l-1.2 4.2 4.3-1.1A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2s-1.1.2-3.6-.9-3.9-3.6-4-3.8-.9-1.2-.9-2.3.6-1.6.8-1.8.4-.3.6-.3h.5c.2 0 .4 0 .6.5l.8 1.9c0 .2.1.4 0 .6l-.4.6-.3.3c-.2.2-.3.3-.1.6a8 8 0 0 0 1.4 1.8 7 7 0 0 0 2.1 1.3c.3.1.4.1.6-.1l.7-.9c.2-.3.4-.2.6-.1l1.8.9c.3.1.5.2.5.3s0 .6-.2 1z"
                  />
                </svg>

              </div>

              <small>
                {{ t('contactPage.cards.whatsapp.label') }}
              </small>

              <b>
                0178 5129865
              </b>

              <p>
                {{ t('contactPage.cards.whatsapp.description') }}
              </p>

            </a>


            <!-- TELEPHONE -->
            <a
              class="contact-card"
              href="tel:+491739523061"
            >

              <div class="contact-icon phone">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path
                    d="M4 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L20 12l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 4 6a2 2 0 0 1 0-2z"
                    stroke-linejoin="round"
                  />
                </svg>

              </div>

              <small>
                {{ t('contactPage.cards.phone.label') }}
              </small>

              <b>
                0173 9523061
              </b>

              <p>
                {{ t('contactPage.cards.phone.description') }}
              </p>

            </a>


            <!-- EMAIL -->
            <a
              class="contact-card"
              href="mailto:Novari2026@yahoo.com"
            >

              <div class="contact-icon email">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <rect
                    x="3"
                    y="5"
                    width="18"
                    height="14"
                    rx="2"
                  />

                  <path
                    d="M4 7l8 6 8-6"
                    stroke-linecap="round"
                  />
                </svg>

              </div>

              <small>
                {{ t('contactPage.cards.email.label') }}
              </small>

              <b class="email-address">
                Novari2026@yahoo.com
              </b>

              <p>
                {{ t('contactPage.cards.email.description') }}
              </p>

            </a>


            <!-- SERVICE AREA -->
            <div class="contact-card static-card">

              <div class="contact-icon location">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path
                    d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"
                    stroke-linejoin="round"
                  />

                  <circle
                    cx="12"
                    cy="10"
                    r="2.4"
                  />
                </svg>

              </div>

              <small>
                {{ t('contactPage.cards.area.label') }}
              </small>

              <b>
                {{ t('contactPage.cards.area.title') }}
              </b>

              <p>
                {{ t('contactPage.cards.area.description') }}
              </p>

            </div>

          </div>



          <!-- =================================
              BUSINESS HOURS
          ================================== -->

          <div class="business-hours">

            <h4>

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                aria-hidden="true"
              >
                <circle
                  cx="12"
                  cy="12"
                  r="9"
                />

                <path
                  d="M12 7v5l3 2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>

              {{ t('contactPage.hours.title') }}

            </h4>


            <div class="hours-row">

              <span>
                {{ t('contactPage.hours.everyDay') }}
              </span>

              <span class="open-24">
                <span class="open-dot"></span>

                {{ t('contactPage.hours.open24') }}
              </span>

            </div>

          </div>


          <!-- =================================
                LIVE SERVICE AREA MAP
            ================================== -->

            <div class="map-strip">

              <ServiceAreaMap height="300px" />

              <div class="map-caption">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path
                    d="
                      M12 21
                      s-7-6-7-11
                      a7 7 0 0 1 14 0
                      c0 5-7 11-7 11z
                    "
                    stroke-linejoin="round"
                  />

                  <circle
                    cx="12"
                    cy="10"
                    r="2.4"
                  />
                </svg>

                {{ t('contactPage.map.caption') }}

              </div>

            </div>

        </div>


        <!-- =====================================
             RIGHT SIDE: CONTACT FORM
        ====================================== -->
        <div class="form-card">

          <!-- SUCCESS -->
          <div
            v-if="success"
            class="form-success"
          >

            <div class="success-icon">

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.6"
              >
                <path
                  d="M5 13l4 4L19 7"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>

            </div>

            <h3>
              {{ t('contactPage.success.title') }}
            </h3>

            <p>
              {{ t('contactPage.success.description') }}
            </p>

          </div>


          <!-- FORM -->
          <template v-else>

            <div class="form-heading">

              <span class="form-heading-icon">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path
                    d="M4 5h16v12H7l-3 3z"
                    stroke-linejoin="round"
                  />
                </svg>

              </span>

              <h3>
                {{ t('contactPage.form.title') }}
              </h3>

            </div>


            <form
              novalidate
              @submit.prevent="submitForm"
            >

              <!-- NAME + PHONE -->
              <div class="form-row">

                <!-- NAME -->
                <div
                  class="field"
                  :class="{ error: errors.name }"
                >

                  <label for="contact-name">

                    {{ t('contactPage.form.name') }}

                    <span class="required">
                      *
                    </span>

                  </label>

                  <input
                    id="contact-name"
                    v-model="form.name"
                    type="text"
                    @input="errors.name = ''"
                  >

                  <span
                    v-if="errors.name"
                    class="error-message"
                  >
                    {{ errors.name }}
                  </span>

                </div>


                <!-- PHONE -->
                <div class="field">

                  <label for="contact-phone">
                    {{ t('contactPage.form.phone') }}
                  </label>

                  <input
                    id="contact-phone"
                    v-model="form.phone"
                    type="tel"
                  >

                </div>

              </div>


              <!-- EMAIL -->
              <div
                class="field"
                :class="{ error: errors.email }"
              >

                <label for="contact-email">

                  {{ t('contactPage.form.email') }}

                  <span class="required">
                    *
                  </span>

                </label>

                <input
                  id="contact-email"
                  v-model="form.email"
                  type="email"
                  @input="errors.email = ''"
                >

                <span
                  v-if="errors.email"
                  class="error-message"
                >
                  {{ errors.email }}
                </span>

              </div>


              <!-- MESSAGE -->
              <div
                class="field"
                :class="{ error: errors.message }"
              >

                <label for="contact-message">

                  {{ t('contactPage.form.message') }}

                  <span class="required">
                    *
                  </span>

                </label>

                <textarea
                  id="contact-message"
                  v-model="form.message"
                  :placeholder="
                    t('contactPage.form.messagePlaceholder')
                  "
                  @input="errors.message = ''"
                ></textarea>

                <span
                  v-if="errors.message"
                  class="error-message"
                >
                 {{ errors.message }}
                </span>

              </div>


              <!-- CONSENT -->
              <div
                class="consent"
                :class="{ error: errors.consent }"
              >

                <input
                  id="contact-consent"
                  v-model="form.consent"
                  type="checkbox"
                  @change="errors.consent = ''"
                >

                <label for="contact-consent">

                  {{ t('contactPage.form.consentBefore') }}

                  <RouterLink to="/privacy">
                    {{ t('contactPage.form.privacy') }}
                  </RouterLink>

                  {{ t('contactPage.form.consentAfter') }}

                  <span class="required">
                    *
                  </span>

                </label>

              </div>
              <span
                v-if="errors.consent"
                class="error-message"
              >
                {{ errors.consent }}
              </span>

              <!-- SUBMIT -->
              <div class="submit-row">

                <button
                  type="submit"
                  class="submit-button"
                  :disabled="loading"
                >

                  <span
                    v-if="loading"
                    class="spinner"
                  ></span>

                  <span>
                    {{ t('contactPage.form.submit') }}
                  </span>

                </button>
                <p
                  v-if="submitError"
                  class="
                    mt-4
                    text-sm
                    font-semibold
                    text-red-600
                  "
                >
                  {{ submitError }}
                </p>

              </div>

            </form>

          </template>

        </div>

      </div>

    </section>
  <Footer/>
  </main>
</template>


<style scoped>
.contact-page {
  background: var(--paper);
  color: var(--ink);
  font-family: var(--body);
}


/* =========================================
   WRAPPER
========================================= */

.contact-wrap {
  width: 100%;
  max-width: 1180px;

  margin-inline: auto;

  padding-inline:
    clamp(18px, 4vw, 32px);
}


/* =========================================
   HERO
========================================= */

.contact-hero {
  background:
    linear-gradient(
      165deg,
      var(--teal),
      var(--teal-deep)
    );

  color: white;

  padding-block:
    clamp(48px, 7vw, 84px);
}


.eyebrow {
  display: inline-flex;

  align-items: center;

  gap: 9px;

  font-family: var(--display);

  font-stretch: 112%;

  font-weight: 700;

  font-size: 12.5px;

  letter-spacing: 0.16em;

  text-transform: uppercase;

  color: #BFE0DF;
}


.eyebrow::before {
  content: "";

  width: 26px;
  height: 2px;

  background: var(--amber);

  border-radius: 2px;
}


.contact-hero h1 {
  margin-top: 14px;

  color: white;

  font-family: var(--display);

  font-size:
    clamp(38px, 6vw, 68px);

  font-weight: 900;

  font-stretch: 118%;

  line-height: 1.03;

  letter-spacing: -0.01em;
}


.contact-hero p {
  max-width: 56ch;

  margin-top: 18px;

  color: #C7E0DF;

  font-size: 19px;
}


/* =========================================
   MAIN SECTION
========================================= */

.contact-section {
  padding-block:
    clamp(58px, 8vw, 104px);

  background: var(--paper-2);
}


.contact-grid {
  display: grid;

  grid-template-columns:
    1fr 1fr;

  gap:
    clamp(24px, 3.5vw, 44px);

  align-items: start;
}


/* =========================================
   CONTACT CARDS
========================================= */

.contact-cards {
  display: grid;

  grid-template-columns:
    1fr 1fr;

  gap: 16px;
}


.contact-card {
  display: block;

  padding: 24px;

  background: white;

  border:
    1px solid var(--line);

  border-radius: 14px;

  color: inherit;

  text-decoration: none;

  transition:
    transform 0.16s,
    box-shadow 0.16s,
    border-color 0.16s;
}


.contact-card:not(.static-card):hover {
  transform:
    translateY(-3px);

  border-color:
    transparent;

  box-shadow:
    0 6px 18px rgba(12, 39, 43, 0.08),
    0 2px 6px rgba(12, 39, 43, 0.05);
}


.contact-icon {
  display: flex;

  align-items: center;
  justify-content: center;

  width: 48px;
  height: 48px;

  margin-bottom: 15px;

  border-radius: 12px;
}


.contact-icon svg {
  width: 24px;
  height: 24px;
}


.contact-icon.whatsapp {
  color: #1F9E4E;

  background: #E7FBEE;
}


.contact-icon.phone {
  color: var(--amber-dark);

  background: #FFF3E0;
}


.contact-icon.email,
.contact-icon.location {
  color: var(--teal);

  background: var(--paper-2);
}


.contact-card small {
  font-family:
    var(--display);

  font-stretch: 104%;

  font-weight: 700;

  font-size: 12px;

  letter-spacing: 0.1em;

  text-transform: uppercase;

  color: var(--slate-2);
}


.contact-card b {
  display: block;

  margin-top: 5px;

  font-family:
    var(--display);

  font-stretch: 110%;

  font-weight: 800;

  font-size: 19px;
}


.contact-card p {
  margin-top: 6px;

  color: var(--slate);

  font-size: 14px;
}


.email-address {
  overflow-wrap: anywhere;
}


/* =========================================
   HOURS
========================================= */

.business-hours {
  margin-top: 16px;

  padding: 24px;

  background: white;

  border:
    1px solid var(--line);

  border-radius: 14px;
}


.business-hours h4 {
  display: flex;

  align-items: center;

  gap: 10px;

  margin-bottom: 14px;

  font-size: 17px;

  font-weight: 800;
}


.business-hours h4 svg {
  width: 20px;
  height: 20px;

  color: var(--teal);
}


.hours-row {
  display: flex;

  justify-content: space-between;

  gap: 20px;

  padding: 9px 0;

  border-bottom:
    1px solid var(--line);

  font-size: 15px;
}


.hours-row:last-child {
  border-bottom: 0;
}


.hours-row span:last-child {
  font-weight: 600;
}


.hours-row.closed
span:last-child {
  color: var(--slate-2);
}


/* =========================================
   MAP STRIP
========================================= */

.map-strip {
  overflow: hidden;

  margin-top: 16px;

  background: white;

  border:
    1px solid var(--line);

  border-radius: 14px;
}


.map-strip > svg {
  display: block;

  width: 100%;

  height: auto;
}


.map-caption {
  display: flex;

  align-items: center;

  gap: 10px;

  padding:
    14px 18px;

  color: var(--slate);

  font-size: 14px;
}


.map-caption svg {
  flex: none;

  width: 18px;
  height: 18px;

  color: var(--amber);
}


/* =========================================
   FORM CARD
========================================= */

.form-card {
  padding:
    clamp(22px, 3vw, 36px);

  background: white;

  border:
    1px solid var(--line);

  border-radius: 20px;

  box-shadow:
    0 1px 2px rgba(12, 39, 43, 0.06),
    0 2px 6px rgba(12, 39, 43, 0.05);
}


.form-heading {
  display: flex;

  align-items: center;

  gap: 12px;

  margin-bottom: 22px;

  padding-bottom: 14px;

  border-bottom:
    1px solid var(--line);
}


.form-heading-icon {
  display: flex;

  flex: none;

  align-items: center;
  justify-content: center;

  width: 30px;
  height: 30px;

  border-radius: 8px;

  background: var(--teal);

  color: white;
}


.form-heading-icon svg {
  width: 17px;
  height: 17px;
}


.form-heading h3 {
  font-size: 19px;

  font-weight: 800;
}


/* =========================================
   FORM
========================================= */

.form-row {
  display: grid;

  grid-template-columns:
    1fr 1fr;

  gap: 16px;
}


.field {
  display: flex;

  flex-direction: column;

  gap: 7px;

  margin-bottom: 16px;
}


.field label {
  font-family:
    var(--display);

  font-stretch: 104%;

  font-weight: 700;

  font-size: 13.5px;

  color: var(--ink);
}


.required {
  color: var(--err);
}


.field input,
.field textarea {
  width: 100%;

  padding:
    12px 14px;

  border:
    1.5px solid var(--line);

  border-radius: 10px;

  background: var(--paper);

  color: var(--ink);

  font-family: var(--body);

  font-size: 15.5px;

  transition:
    border-color 0.15s,
    background 0.15s,
    box-shadow 0.15s;
}


.field textarea {
  min-height: 96px;

  resize: vertical;
}


.field input:hover,
.field textarea:hover {
  border-color:
    var(--slate-2);
}


.field input:focus,
.field textarea:focus {
  outline: none;

  border-color:
    var(--teal);

  background: white;

  box-shadow:
    0 0 0 4px
    rgba(14, 90, 99, 0.12);
}


.field.error input,
.field.error textarea {
  border-color:
    var(--err);

  background: #FDF3F2;
}


.error-message {
  color: var(--err);

  font-size: 12.5px;
}


/* =========================================
   CONSENT
========================================= */

.consent {
  display: flex;

  align-items: flex-start;

  gap: 12px;

  margin:
    22px 0;
}


.consent input {
  flex: none;

  width: 20px;
  height: 20px;

  margin-top: 2px;

  accent-color:
    var(--teal);
}


.consent label {
  color: var(--slate);

  font-size: 14px;
}


.consent a {
  color: var(--teal);

  text-decoration: underline;
}


.consent.error label {
  color: var(--err);
}


/* =========================================
   BUTTON
========================================= */

.submit-row {
  display: flex;

  align-items: center;

  gap: 16px;

  flex-wrap: wrap;
}


.submit-button {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  gap: 10px;

  padding:
    17px 30px;

  border: 2px solid transparent;

  border-radius: 999px;

  background: var(--amber);

  color: #3A2500;

  font-family:
    var(--display);

  font-stretch: 108%;

  font-weight: 700;

  font-size: 16.5px;

  cursor: pointer;

  box-shadow:
    0 6px 16px
    rgba(244, 155, 28, 0.35);

  transition:
    transform 0.16s,
    background 0.16s,
    box-shadow 0.16s;
}


.submit-button:hover {
  background:
    var(--amber-dark);

  transform:
    translateY(-2px);
}


.submit-button:disabled {
  cursor: wait;

  opacity: 0.8;
}


/* =========================================
   SPINNER
========================================= */

.spinner {
  width: 19px;
  height: 19px;

  border:
    2.5px solid
    rgba(58, 37, 0, 0.3);

  border-top-color:
    #3A2500;

  border-radius: 50%;

  animation:
    spin 0.7s linear infinite;
}


@keyframes spin {
  to {
    transform:
      rotate(360deg);
  }
}


/* =========================================
   SUCCESS
========================================= */

.form-success {
  padding:
    26px 10px;

  text-align: center;
}


.success-icon {
  display: flex;

  align-items: center;
  justify-content: center;

  width: 72px;
  height: 72px;

  margin:
    0 auto 20px;

  border-radius: 50%;

  background: var(--ok);

  color: white;
}


.success-icon svg {
  width: 38px;
  height: 38px;
}


.form-success h3 {
  font-size: 26px;

  font-weight: 800;
}


.form-success p {
  max-width: 44ch;

  margin:
    12px auto 0;

  color: var(--slate);
}


.open-24 {
  display: inline-flex;
  align-items: center;
  gap: 8px;

  font-weight: 700;
  color: #1e8a5b;
}

.open-dot {
  width: 9px;
  height: 9px;

  flex-shrink: 0;

  border-radius: 999px;

  background: #1e8a5b;

  box-shadow:
    0 0 0 4px rgba(30, 138, 91, 0.12);
}

/* =========================================
   RESPONSIVE
========================================= */

@media (max-width: 960px) {

  .contact-grid {
    grid-template-columns:
      1fr;
  }

}


@media (max-width: 600px) {

  .contact-cards,
  .form-row {
    grid-template-columns:
      1fr;
  }

  .contact-hero p {
    font-size: 17px;
  }

  .submit-button {
    width: 100%;
  }

  .hours-row {
    align-items: flex-start;
  }

}
</style>