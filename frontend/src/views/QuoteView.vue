<script setup>
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Footer from '@/components/Footer.vue'

const { t } = useI18n({
  useScope: 'global',
})

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL


// ======================================================
// FORM
// ======================================================

const form = reactive({

  // Personal
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  service: '',

  // Pickup
  pickupAddress: '',
  pickupCity: '',
  pickupZip: '',
  pickupFloor: '',
  pickupElevator: 'no',

  // Destination
  destinationAddress: '',
  destinationCity: '',
  destinationZip: '',
  destinationFloor: '',
  destinationElevator: 'no',

  // Moving details
  date: '',
  items: '',
  notes: '',

  // Consent
  consent: false,
})


// ======================================================
// STATE
// ======================================================

const loading = ref(false)

const success = ref(false)

const submitError = ref('')

const quoteId = ref(null)


// ======================================================
// FILES
// ======================================================

const files = ref([])

const fileInput = ref(null)

const dragActive = ref(false)


// ======================================================
// ERRORS
// ======================================================

const errors = reactive({
  firstName: false,
  lastName: false,
  email: false,
  phone: false,
  service: false,
  consent: false,
  files: '',
})


const resetErrors = () => {

  errors.firstName = false
  errors.lastName = false
  errors.email = false
  errors.phone = false
  errors.service = false
  errors.consent = false
  errors.files = ''

  submitError.value = ''
}


// ======================================================
// VALIDATION
// ======================================================

const validateForm = () => {

  resetErrors()

  let valid = true


  if (!form.firstName.trim()) {

    errors.firstName = true
    valid = false
  }


  if (!form.lastName.trim()) {

    errors.lastName = true
    valid = false
  }


  if (!form.email.trim()) {

    errors.email = true
    valid = false

  }
  else {

    const emailPattern =
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    if (!emailPattern.test(form.email)) {

      errors.email = true
      valid = false
    }
  }


  if (!form.phone.trim()) {

    errors.phone = true
    valid = false
  }


  if (!form.service) {

    errors.service = true
    valid = false
  }


  if (!form.consent) {

    errors.consent = true
    valid = false
  }


  return valid
}


// ======================================================
// FILE UPLOAD
// ======================================================

const openFilePicker = () => {

  fileInput.value?.click()
}


const addFiles = (newFiles) => {

  errors.files = ''


  const allowedTypes = [
    'image/jpeg',
    'image/png',
    'image/webp',
    'video/mp4',
  ]


  const maxSize =
    25 * 1024 * 1024


  for (const file of newFiles) {


    // File type validation
    if (!allowedTypes.includes(file.type)) {

      errors.files =
        `${file.name} is not a supported file type.`

      continue
    }


    // File size validation
    if (file.size > maxSize) {

      errors.files =
        `${file.name} is larger than 25 MB.`

      continue
    }


    // Avoid duplicate files
    const duplicate =
      files.value.some(
        existing =>
          existing.name === file.name &&
          existing.size === file.size
      )


    if (!duplicate) {

      files.value.push(file)
    }
  }
}


// This name matches your existing template
const handleFileSelect = (event) => {

  const selected =
    Array.from(
      event.target.files
    )


  addFiles(selected)


  event.target.value = ''
}


const handleDrop = (event) => {

  dragActive.value = false


  const droppedFiles =
    Array.from(
      event.dataTransfer.files
    )


  addFiles(droppedFiles)
}


const removeFile = (index) => {

  files.value.splice(
    index,
    1
  )
}


const formatFileSize = (bytes) => {

  const size =
    bytes / 1024 / 1024


  return `${size.toFixed(1)} MB`
}


// ======================================================
// RESET FORM
// ======================================================

const resetForm = () => {

  form.firstName = ''
  form.lastName = ''
  form.email = ''
  form.phone = ''
  form.service = ''

  form.pickupAddress = ''
  form.pickupCity = ''
  form.pickupZip = ''
  form.pickupFloor = ''
  form.pickupElevator = 'no'

  form.destinationAddress = ''
  form.destinationCity = ''
  form.destinationZip = ''
  form.destinationFloor = ''
  form.destinationElevator = 'no'

  form.date = ''
  form.items = ''
  form.notes = ''

  form.consent = false


  files.value = []

  quoteId.value = null

  success.value = false

  submitError.value = ''


  resetErrors()
}


// ======================================================
// CONVERT FRONTEND SERVICE VALUE TO DJANGO VALUE
// ======================================================

const getBackendServiceValue = () => {

  const serviceMap = {

    residential:
      'residential_move',

    business:
      'business_move',

    transport:
      'furniture_transport',

    assembly:
      'furniture_assembly',

    clearance:
      'household_clearance',

    carrying:
      'carrying_assistance',

    handyman:
      'handyman',

    unknown:
      'not_sure',
  }


  return (
    serviceMap[form.service] ||
    form.service
  )
}


// ======================================================
// SUBMIT
// ======================================================

const submitForm = async () => {


  if (!validateForm()) {

    return
  }


  loading.value = true

  success.value = false

  submitError.value = ''


  try {


    // ==================================================
    // Create multipart/form-data
    // ==================================================

    const formData =
      new FormData()


    // ---------------------------
    // Personal
    // ---------------------------

    formData.append(
      'first_name',
      form.firstName
    )


    formData.append(
      'last_name',
      form.lastName
    )


    formData.append(
      'email',
      form.email
    )


    formData.append(
      'phone',
      form.phone
    )


    formData.append(
      'service',
      getBackendServiceValue()
    )


    // ---------------------------
    // Pickup
    // ---------------------------

    formData.append(
      'pickup_address',
      form.pickupAddress
    )


    formData.append(
      'pickup_city',
      form.pickupCity
    )


    formData.append(
      'pickup_postal_code',
      form.pickupZip
    )


    formData.append(
      'pickup_floor',
      form.pickupFloor
    )


    formData.append(
      'pickup_elevator',
      form.pickupElevator === 'yes'
        ? 'true'
        : 'false'
    )


    // ---------------------------
    // Destination
    // ---------------------------

    formData.append(
      'destination_address',
      form.destinationAddress
    )


    formData.append(
      'destination_city',
      form.destinationCity
    )


    formData.append(
      'destination_postal_code',
      form.destinationZip
    )


    formData.append(
      'destination_floor',
      form.destinationFloor
    )


    formData.append(
      'destination_elevator',
      form.destinationElevator === 'yes'
        ? 'true'
        : 'false'
    )


    // ---------------------------
    // Moving details
    // ---------------------------

    if (form.date) {

      formData.append(
        'preferred_date',
        form.date
      )
    }


    formData.append(
      'items',
      form.items
    )


    formData.append(
      'notes',
      form.notes
    )


    // ---------------------------
    // Privacy
    // ---------------------------

    formData.append(
      'consent_accepted',
      form.consent
        ? 'true'
        : 'false'
    )


    // ---------------------------
    // Attachments
    // ---------------------------

    files.value.forEach(
      file => {

        formData.append(
          'files',
          file
        )
      }
    )


    // ==================================================
    // SEND TO DJANGO
    // ==================================================

    const response =
      await fetch(
        `${API_BASE_URL}/api/quote/`,
        {
          method: 'POST',

          // Do NOT manually set Content-Type
          body: formData,
        }
      )


    const data =
      await response.json()


    // ==================================================
    // DJANGO VALIDATION ERROR
    // ==================================================

    if (!response.ok) {


      console.error(
        'Quote API error:',
        data
      )


      if (data.errors) {


        if (data.errors.first_name) {

          errors.firstName = true
        }


        if (data.errors.last_name) {

          errors.lastName = true
        }


        if (data.errors.email) {

          errors.email = true
        }


        if (data.errors.phone) {

          errors.phone = true
        }


        if (data.errors.service) {

          errors.service = true
        }


        if (
          data.errors.consent_accepted
        ) {

          errors.consent = true
        }


        if (data.errors.files) {

          errors.files =
            Array.isArray(
              data.errors.files
            )
              ? data.errors.files[0]
              : String(
                  data.errors.files
                )
        }
      }


      throw new Error(
        'Quote request failed'
      )
    }


    // ==================================================
    // SUCCESS
    // ==================================================

    quoteId.value =
      data.quote_id


    success.value = true

  }
  catch (error) {


    console.error(
      'Quote submission error:',
      error
    )


    const hasFieldErrors =
      errors.firstName ||
      errors.lastName ||
      errors.email ||
      errors.phone ||
      errors.service ||
      errors.consent ||
      errors.files


    if (!hasFieldErrors) {

      submitError.value =
        'Something went wrong while sending your quote request. Please try again.'
    }

  }
  finally {

    loading.value = false
  }
}
</script>

<template>
  <main class="quote-page">

    <!-- ======================================
         HERO
    ======================================= -->
    <section class="quote-hero">

      <div class="quote-wrap">

        <span class="eyebrow">
          {{ t('quotePage.hero.eyebrow') }}
        </span>

        <h1>
          {{ t('quotePage.hero.title') }}
        </h1>

        <p>
          {{ t('quotePage.hero.description') }}
        </p>

      </div>

    </section>


    <!-- ======================================
         QUOTE SECTION
    ======================================= -->
    <section class="quote-section">

      <div class="quote-wrap quote-grid">


        <!-- ==================================
             FORM CARD
        =================================== -->
        <div class="form-card">


          <!-- SUCCESS -->
          <div
            v-if="success"
            class="form-success"
          >

            <div class="success-tick">

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
              {{ t('quotePage.success.title') }}
            </h3>

            <p>
              {{ t('quotePage.success.description') }}
            </p>


            <div class="success-actions">

              <a
                href="https://wa.me/491739523061"
                target="_blank"
                rel="noopener"
                class="button whatsapp-button"
              >
                {{ t('quotePage.success.whatsapp') }}
              </a>

              <button
                type="button"
                class="button outline-button"
                @click="resetForm"
              >
                {{ t('quotePage.success.another') }}
              </button>

            </div>

          </div>


          <!-- =================================
               FORM
          ================================== -->
          <form
            v-else
            novalidate
            @submit.prevent="submitForm"
          >


            <!-- ===============================
                 1. PERSONAL INFORMATION
            ================================ -->
            <fieldset class="fieldset">

              <div class="fieldset-heading">

                <span class="fieldset-number">
                  1
                </span>

                <h3>
                  {{ t('quotePage.personal.title') }}
                </h3>

              </div>


              <div class="form-row">

                <!-- FIRST NAME -->
                <div
                  class="field"
                  :class="{ error: errors.firstName }"
                >

                  <label for="first-name">

                    {{ t('quotePage.personal.firstName') }}

                    <span class="required">
                      *
                    </span>

                  </label>

                  <input
                    v-model="form.firstName"
                    type="text"
                    @input="errors.firstName = ''"
                  >

                  <span
                    v-if="errors.firstName"
                    class="msg"
                  >
                    {{ errors.firstName }}
                  </span>

                </div>


                <!-- LAST NAME -->
                <div
                  class="field"
                  :class="{ error: errors.lastName }"
                >

                  <label for="last-name">

                    {{ t('quotePage.personal.lastName') }}

                    <span class="required">
                      *
                    </span>

                  </label>

                  <input
                    v-model="form.lastName"
                    type="text"
                    @input="errors.lastName = ''"
                  >

                  <span
                    v-if="errors.lastName"
                    class="msg"
                  >
                    {{ errors.lastName }}
                  </span>

                </div>

              </div>


              <div class="form-row">

                <!-- EMAIL -->
                <div
                  class="field"
                  :class="{ error: errors.email }"
                >

                  <label for="quote-email">

                    {{ t('quotePage.personal.email') }}

                    <span class="required">
                      *
                    </span>

                  </label>

                    <input
                      v-model="form.email"
                      type="email"
                      @input="errors.email = ''"
                    >

                  <span
                    v-if="errors.email"
                    class="msg"
                  >
                    {{ errors.email }}
                  </span>

                </div>


                <!-- PHONE -->
                <div
                  class="field"
                  :class="{ error: errors.phone }"
                >

                  <label for="quote-phone">

                    {{ t('quotePage.personal.phone') }}

                    <span class="required">
                      *
                    </span>

                  </label>

                  <input
                    v-model="form.phone"
                    type="tel"
                    @input="errors.phone = ''"
                  >

                  <span
                    v-if="errors.phone"
                    class="msg"
                  >
                    {{ errors.phone }}
                  </span>

                </div>

              </div>


              <!-- SERVICE TYPE -->
              <div
                class="field full"
                :class="{ error: errors.service }"
              >

                <label for="service-type">

                  {{ t('quotePage.personal.service') }}

                  <span class="required">
                    *
                  </span>

                </label>

                <select
                      id="service-type"
                      v-model="form.service"
                      @change="errors.service = false"
                    >

                      <option value="">
                        {{ t('quotePage.services.choose') }}
                      </option>


                      <option value="residential_move">
                        {{ t('quotePage.services.residential') }}
                      </option>


                      <option value="business_move">
                        {{ t('quotePage.services.business') }}
                      </option>


                      <option value="furniture_transport">
                        {{ t('quotePage.services.transport') }}
                      </option>


                      <option value="furniture_assembly">
                        {{ t('quotePage.services.assembly') }}
                      </option>


                      <option value="household_clearance">
                        {{ t('quotePage.services.clearance') }}
                      </option>


                      <option value="carrying_assistance">
                        {{ t('quotePage.services.carrying') }}
                      </option>

<!-- 
                      <option value="handyman">
                        {{ t('quotePage.services.handyman') }}
                      </option> -->


                      <option value="not_sure">
                        {{ t('quotePage.services.unknown') }}
                      </option>

                    </select>

                <span
                  v-if="errors.service"
                  class="error-message"
                >
                  {{ t('quotePage.errors.service') }}
                </span>

              </div>

            </fieldset>



            <!-- ===============================
                 2. PICKUP
            ================================ -->
            <fieldset class="fieldset">

              <div class="fieldset-heading">

                <span class="fieldset-number">
                  2
                </span>

                <h3>
                  {{ t('quotePage.pickup.title') }}
                </h3>

              </div>


              <div class="field full">

                <label for="pickup-address">
                  {{ t('quotePage.pickup.address') }}
                </label>

                <input
                  id="pickup-address"
                  v-model="form.pickupAddress"
                  type="text"
                  :placeholder="
                    t('quotePage.common.streetPlaceholder')
                  "
                >

              </div>


              <div class="form-row thirds">

                <div class="field">

                  <label for="pickup-city">
                    {{ t('quotePage.common.city') }}
                  </label>

                  <input
                    id="pickup-city"
                    v-model="form.pickupCity"
                    type="text"
                  >

                </div>


                <div class="field">

                  <label for="pickup-zip">
                    {{ t('quotePage.common.postalCode') }}
                  </label>

                  <input
                    id="pickup-zip"
                    v-model="form.pickupZip"
                    type="text"
                  >

                </div>


                <div class="field">

                  <label for="pickup-floor">
                    {{ t('quotePage.common.floor') }}
                  </label>

                  <input
                    id="pickup-floor"
                    v-model="form.pickupFloor"
                    type="text"
                    :placeholder="
                      t('quotePage.common.floorPlaceholder')
                    "
                  >

                </div>

              </div>


              <!-- PICKUP ELEVATOR -->
              <div class="field">

                <label>
                  {{ t('quotePage.common.elevator') }}
                </label>

                <div class="segment">

                  <button
                    type="button"
                    :class="{
                      active:
                        form.pickupElevator === 'yes',
                    }"
                    @click="
                      form.pickupElevator = 'yes'
                    "
                  >
                    {{ t('quotePage.common.yes') }}
                  </button>

                  <button
                    type="button"
                    :class="{
                      active:
                        form.pickupElevator === 'no',
                    }"
                    @click="
                      form.pickupElevator = 'no'
                    "
                  >
                    {{ t('quotePage.common.no') }}
                  </button>

                </div>

              </div>

            </fieldset>



            <!-- ===============================
                 3. DESTINATION
            ================================ -->
            <fieldset class="fieldset">

              <div class="fieldset-heading">

                <span class="fieldset-number">
                  3
                </span>

                <h3>
                  {{ t('quotePage.destination.title') }}
                </h3>

              </div>


              <div class="field full">

                <label for="destination-address">
                  {{ t('quotePage.destination.address') }}
                </label>

                <input
                  id="destination-address"
                  v-model="form.destinationAddress"
                  type="text"
                  :placeholder="
                    t('quotePage.common.streetPlaceholder')
                  "
                >

              </div>


              <div class="form-row thirds">

                <div class="field">

                  <label for="destination-city">
                    {{ t('quotePage.common.city') }}
                  </label>

                  <input
                    id="destination-city"
                    v-model="form.destinationCity"
                    type="text"
                  >

                </div>


                <div class="field">

                  <label for="destination-zip">
                    {{ t('quotePage.common.postalCode') }}
                  </label>

                  <input
                    id="destination-zip"
                    v-model="form.destinationZip"
                    type="text"
                  >

                </div>


                <div class="field">

                  <label for="destination-floor">
                    {{ t('quotePage.common.floor') }}
                  </label>

                  <input
                    id="destination-floor"
                    v-model="form.destinationFloor"
                    type="text"
                    :placeholder="
                      t('quotePage.common.floorPlaceholderDestination')
                    "
                  >

                </div>

              </div>


              <!-- DESTINATION ELEVATOR -->
              <div class="field">

                <label>
                  {{ t('quotePage.common.elevator') }}
                </label>

                <div class="segment">

                  <button
                    type="button"
                    :class="{
                      active:
                        form.destinationElevator === 'yes',
                    }"
                    @click="
                      form.destinationElevator = 'yes'
                    "
                  >
                    {{ t('quotePage.common.yes') }}
                  </button>

                  <button
                    type="button"
                    :class="{
                      active:
                        form.destinationElevator === 'no',
                    }"
                    @click="
                      form.destinationElevator = 'no'
                    "
                  >
                    {{ t('quotePage.common.no') }}
                  </button>

                </div>

              </div>

            </fieldset>



            <!-- ===============================
                 4. MOVING DETAILS
            ================================ -->
            <fieldset class="fieldset">

              <div class="fieldset-heading">

                <span class="fieldset-number">
                  4
                </span>

                <h3>
                  {{ t('quotePage.details.title') }}
                </h3>

              </div>


              <div class="form-row">

                <div class="field">

                  <label for="preferred-date">
                    {{ t('quotePage.details.date') }}
                  </label>

                  <input
                    id="preferred-date"
                    v-model="form.date"
                    type="date"
                  >

                </div>


                <div class="field">

                  <label for="items">
                    {{ t('quotePage.details.items') }}
                  </label>

                  <input
                    id="items"
                    v-model="form.items"
                    type="text"
                    :placeholder="
                      t('quotePage.details.itemsPlaceholder')
                    "
                  >

                </div>

              </div>


              <div class="field full">

                <label for="notes">
                  {{ t('quotePage.details.additional') }}
                </label>

                <textarea
                  id="notes"
                  v-model="form.notes"
                  :placeholder="
                    t('quotePage.details.additionalPlaceholder')
                  "
                ></textarea>

              </div>

            </fieldset>



            <!-- ===============================
                 5. PHOTOS
            ================================ -->
            <fieldset class="fieldset">

              <div class="fieldset-heading">

                <span class="fieldset-number">
                  5
                </span>

                <h3>
                  {{ t('quotePage.photos.title') }}
                </h3>

              </div>


              <!-- UPLOAD BOX -->
              <div
                class="upload-box"
                :class="{
                  dragover: dragActive,
                }"
                tabindex="0"
                role="button"
                @click="openFilePicker"
                @keydown.enter="openFilePicker"
                @keydown.space.prevent="openFilePicker"
                @dragenter.prevent="
                  dragActive = true
                "
                @dragover.prevent="
                  dragActive = true
                "
                @dragleave.prevent="
                  dragActive = false
                "
                @drop.prevent="handleDrop"
              >

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.8"
                >
                  <path
                    d="M12 16V6M8 10l4-4 4 4"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />

                  <path
                    d="M5 18h14"
                    stroke-linecap="round"
                  />
                </svg>


                <b>
                  {{ t('quotePage.photos.upload') }}
                </b>

                <span>
                  {{ t('quotePage.photos.description') }}
                </span>


                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept="image/jpeg,image/png,image/webp,video/mp4"
                  hidden
                  @change="handleFileSelect"
                >

              </div>


              <!-- FILE LIST -->
              <div
                v-if="files.length"
                class="file-list"
              >

                <div
                  v-for="(file, index) in files"
                  :key="`${file.name}-${index}`"
                  class="file-item"
                >

                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path d="M4 5h16v14H4z" />

                    <path
                      d="M8 13l3-3 3 4 2-2 2 3"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>


                  <span class="file-name">
                    {{ file.name }}
                  </span>

                  <span class="file-size">
                    {{ formatFileSize(file.size) }}
                  </span>


                  <button
                    type="button"
                    class="remove-file"
                    :aria-label="
                      t('quotePage.photos.remove')
                    "
                    @click="removeFile(index)"
                  >
                    ×
                  </button>

                </div>

              </div>
              <p
                v-if="errors.files"
                class="error-message"
              >
                {{ errors.files }}
              </p>

            </fieldset>



            <!-- ===============================
                 CONSENT
            ================================ -->
            <div
              class="consent"
              :class="{
                error: errors.consent,
              }"
            >

              <input
                id="quote-consent"
                v-model="form.consent"
                type="checkbox"
                @change="
                  errors.consent = false
                "
              >

              <label for="quote-consent">

                {{ t('quotePage.consent.before') }}

                <RouterLink to="/privacy">
                  {{ t('quotePage.consent.privacy') }}
                </RouterLink>

                {{ t('quotePage.consent.after') }}

                <span class="required">
                  *
                </span>

              </label>

            </div>
            <p
              v-if="errors.consent"
              class="error-message"
            >
              {{ t('quotePage.errors.consent') }}
            </p>


            <!-- ===============================
                 SUBMIT
            ================================ -->
            <div class="submit-row">

              <button
                type="submit"
                class="primary-button"
                :disabled="loading"
              >

                <span
                  v-if="loading"
                  class="spinner"
                ></span>

                <span>
                  {{ t('quotePage.submit.button') }}
                </span>

              </button>


              <span class="form-note">
                {{ t('quotePage.submit.note') }}
              </span>

            </div>
            <p
              v-if="submitError"
              class="error-message submit-error"
            >
              {{ submitError }}
            </p>

          </form>

        </div>



        <!-- ==================================
             SIDE CARD
        =================================== -->
        <aside class="aside-card">

          <h3>
            {{ t('quotePage.aside.title') }}
          </h3>

          <p>
            {{ t('quotePage.aside.description') }}
          </p>


          <ul class="aside-list">

            <li>

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.4"
              >
                <path
                  d="M5 13l4 4L19 7"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>

              {{ t('quotePage.aside.quote') }}

            </li>


            <li>

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.4"
              >
                <path
                  d="M5 13l4 4L19 7"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>

              {{ t('quotePage.aside.flexible') }}

            </li>


            <li>

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.4"
              >
                <path
                  d="M5 13l4 4L19 7"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>

              {{ t('quotePage.aside.transport') }}

            </li>


            <li>

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.4"
              >
                <path
                  d="M5 13l4 4L19 7"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>

              {{ t('quotePage.aside.clearance') }}

            </li>


            <li>

              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.4"
              >
                <path
                  d="M5 13l4 4L19 7"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>

              {{ t('quotePage.aside.carrying') }}

            </li>

          </ul>



          <!-- CONTACT OPTIONS -->
          <div class="aside-contact">

            <!-- WHATSAPP -->
            <a
              href="https://wa.me/491785129865"
              target="_blank"
              rel="noopener"
            >

              <span class="contact-icon whatsapp">

                <svg
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M12 2a10 10 0 0 0-8.7 15l-1.2 4.2 4.3-1.1A10 10 0 1 0 12 2z"
                  />
                </svg>

              </span>

              <span>

                <small>
                  WhatsApp
                </small>

                <b>
                  0178 5129865
                </b>

              </span>

            </a>


            <!-- PHONE -->
            <a href="tel:+491785129865">

              <span class="contact-icon phone">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M4 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L20 12l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 4 6a2 2 0 0 1 0-2z"
                    stroke-linejoin="round"
                  />
                </svg>

              </span>

              <span>

                <small>
                  {{ t('quotePage.aside.phone') }}
                </small>

                <b>
                  0178 5129865
                </b>

              </span>

            </a>


            <!-- EMAIL -->
            <a href="mailto:Novari2026@yahoo.com">

              <span class="contact-icon email">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
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

              </span>

              <span>

                <small>
                  {{ t('quotePage.aside.email') }}
                </small>

                <b class="email-value">
                  Novari2026@yahoo.com
                </b>

              </span>

            </a>

          </div>

        </aside>

      </div>

    </section>
    <Footer />
  </main>
</template>

<style scoped>
.quote-page {
  background: var(--paper);
  color: var(--ink);
  font-family: var(--body);
}


/* =========================================
   WRAPPER
========================================= */

.quote-wrap {
  width: 100%;
  max-width: 1180px;
  margin-inline: auto;
  padding-inline: clamp(18px, 4vw, 32px);
}


/* =========================================
   HERO
========================================= */

.quote-hero {
  padding-block: clamp(48px, 7vw, 84px);

  background:
    linear-gradient(
      165deg,
      var(--teal),
      var(--teal-deep)
    );

  color: white;
}


.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 9px;

  color: #BFE0DF;

  font-family: var(--display);
  font-stretch: 112%;
  font-weight: 700;
  font-size: 12.5px;

  letter-spacing: 0.16em;
  text-transform: uppercase;
}


.eyebrow::before {
  content: "";

  width: 26px;
  height: 2px;

  background: var(--amber);

  border-radius: 2px;
}


.quote-hero h1 {
  margin-top: 14px;

  color: white;

  font-family: var(--display);
  font-size: clamp(38px, 6vw, 68px);
  font-weight: 900;

  line-height: 1.03;
}


.quote-hero p {
  max-width: 56ch;

  margin-top: 18px;

  color: #C7E0DF;

  font-size: 19px;
}


/* =========================================
   QUOTE SECTION
========================================= */

.quote-section {
  padding-block: clamp(58px, 8vw, 104px);

  background: var(--paper-2);
}


.quote-grid {
  display: grid;

  grid-template-columns:
    1.4fr 0.95fr;

  gap:
    clamp(24px, 3.5vw, 44px);

  align-items: start;
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


/* =========================================
   FIELDSET
========================================= */

.fieldset {
  margin: 0 0 30px;
  padding: 0;

  border: 0;
}


.fieldset:last-of-type {
  margin-bottom: 0;
}


.fieldset-heading {
  display: flex;

  align-items: center;

  gap: 12px;

  margin-bottom: 18px;

  padding-bottom: 14px;

  border-bottom:
    1px solid var(--line);
}


.fieldset-number {
  display: flex;

  flex: none;

  align-items: center;
  justify-content: center;

  width: 30px;
  height: 30px;

  border-radius: 8px;

  background: var(--teal);

  color: white;

  font-family: var(--display);

  font-weight: 800;

  font-size: 15px;
}


.fieldset-heading h3 {
  font-size: 19px;
  font-weight: 800;
}


/* =========================================
   FORM GRID
========================================= */

.form-row {
  display: grid;

  grid-template-columns:
    1fr 1fr;

  gap: 16px;
}


.form-row.thirds {
  grid-template-columns:
    2fr 1fr 1fr;
}


/* =========================================
   FIELD
========================================= */

.field {
  display: flex;

  flex-direction: column;

  gap: 7px;

  margin-bottom: 16px;
}


.field.full {
  grid-column: 1 / -1;
}


.field label {
  color: var(--ink);

  font-family: var(--display);

  font-stretch: 104%;

  font-weight: 700;

  font-size: 13.5px;
}


.required {
  color: var(--err);
}


.field input,
.field select,
.field textarea {
  width: 100%;

  padding: 12px 14px;

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
.field select:hover,
.field textarea:hover {
  border-color: var(--slate-2);
}


.field input:focus,
.field select:focus,
.field textarea:focus {
  outline: none;

  border-color: var(--teal);

  background: white;

  box-shadow:
    0 0 0 4px
    rgba(14, 90, 99, 0.12);
}


.field.error input,
.field.error select,
.field.error textarea {
  border-color: var(--err);

  background: #FDF3F2;
}


.error-message {
  color: var(--err);

  font-size: 12.5px;
}


/* =========================================
   YES / NO
========================================= */

.segment {
  display: inline-flex;

  width: fit-content;

  gap: 4px;

  padding: 4px;

  border:
    1.5px solid var(--line);

  border-radius: 10px;

  background: var(--paper);
}


.segment button {
  padding: 9px 20px;

  border: 0;

  border-radius: 7px;

  background: transparent;

  color: var(--slate);

  font-family: var(--display);

  font-weight: 700;

  font-size: 14px;

  cursor: pointer;

  transition: 0.15s;
}


.segment button.active {
  background: var(--teal);

  color: white;
}


/* =========================================
   UPLOAD
========================================= */

.upload-box {
  padding: 26px;

  border:
    2px dashed var(--line);

  border-radius: 14px;

  background: var(--paper);

  text-align: center;

  cursor: pointer;

  transition: 0.15s;
}


.upload-box:hover {
  border-color: var(--teal);

  background: white;
}


.upload-box.dragover {
  border-color: var(--amber);

  background: #FFF9EF;
}


.upload-box svg {
  width: 34px;
  height: 34px;

  margin:
    0 auto 10px;

  color: var(--teal);
}


.upload-box b {
  display: block;

  font-family: var(--display);

  font-stretch: 106%;

  font-weight: 700;

  font-size: 15px;
}


.upload-box > span {
  display: block;

  margin-top: 4px;

  color: var(--slate-2);

  font-size: 13px;
}


/* =========================================
   FILE LIST
========================================= */

.file-list {
  display: flex;

  flex-direction: column;

  gap: 8px;

  margin-top: 14px;
}


.file-item {
  display: flex;

  align-items: center;

  gap: 10px;

  padding: 9px 12px;

  border:
    1px solid var(--line);

  border-radius: 8px;

  background: var(--paper);

  font-size: 13.5px;
}


.file-item svg {
  flex: none;

  width: 16px;
  height: 16px;

  color: var(--teal);
}


.file-name {
  min-width: 0;

  overflow: hidden;

  text-overflow: ellipsis;

  white-space: nowrap;
}


.file-size {
  margin-left: auto;

  color: var(--slate-2);

  white-space: nowrap;
}


.remove-file {
  border: 0;

  background: none;

  color: var(--slate-2);

  font-size: 18px;

  cursor: pointer;
}


.remove-file:hover {
  color: var(--err);
}


/* =========================================
   CONSENT
========================================= */

.consent {
  display: flex;

  gap: 12px;

  align-items: flex-start;

  margin: 22px 0;
}


.consent input {
  flex: none;

  width: 20px;
  height: 20px;

  margin-top: 2px;

  accent-color: var(--teal);
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
   SUBMIT
========================================= */

.submit-row {
  display: flex;

  align-items: center;

  flex-wrap: wrap;

  gap: 16px;
}


.primary-button,
.button {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  gap: 10px;

  padding: 14px 24px;

  border:
    2px solid transparent;

  border-radius: 999px;

  font-family: var(--display);

  font-stretch: 108%;

  font-weight: 700;

  font-size: 15.5px;

  cursor: pointer;

  transition:
    transform 0.16s,
    background 0.16s,
    box-shadow 0.16s;
}


.primary-button {
  padding: 17px 30px;

  background: var(--amber);

  color: #3A2500;

  font-size: 16.5px;

  box-shadow:
    0 6px 16px
    rgba(244, 155, 28, 0.35);
}


.primary-button:hover {
  background:
    var(--amber-dark);

  transform:
    translateY(-2px);
}


.primary-button:disabled {
  opacity: 0.75;

  cursor: wait;
}


.form-note {
  color: var(--slate-2);

  font-size: 13px;
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
    transform: rotate(360deg);
  }
}


/* =========================================
   SUCCESS
========================================= */

.form-success {
  padding: 26px 10px;

  text-align: center;
}


.success-tick {
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


.success-tick svg {
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


.success-actions {
  display: flex;

  justify-content: center;

  flex-wrap: wrap;

  gap: 12px;

  margin-top: 20px;
}


.whatsapp-button {
  background: #25D366;

  color: #053D1B;
}


.outline-button {
  border-color: var(--line);

  background: transparent;

  color: var(--ink);
}


/* =========================================
   ASIDE
========================================= */

.aside-card {
  position: sticky;

  top: 96px;

  padding:
    clamp(24px, 3vw, 34px);

  border-radius: 20px;

  background:
    linear-gradient(
      165deg,
      var(--teal),
      var(--teal-deep)
    );

  color: white;
}


.aside-card h3 {
  color: white;

  font-size: 26px;

  font-weight: 800;
}


.aside-card > p {
  margin-top: 12px;

  color: #C7E0DF;

  font-size: 15.5px;
}


.aside-list {
  display: flex;

  flex-direction: column;

  gap: 13px;

  margin:
    22px 0;

  padding: 0;

  list-style: none;
}


.aside-list li {
  display: flex;

  align-items: center;

  gap: 11px;

  font-size: 15px;
}


.aside-list li svg {
  flex: none;

  width: 20px;
  height: 20px;

  color: var(--amber);
}


/* =========================================
   ASIDE CONTACT
========================================= */

.aside-contact {
  display: flex;

  flex-direction: column;

  gap: 11px;

  margin-top: 24px;

  padding-top: 22px;

  border-top:
    1px solid rgba(255, 255, 255, 0.16);
}


.aside-contact a {
  display: flex;

  align-items: center;

  gap: 12px;

  padding: 13px 16px;

  border:
    1px solid rgba(255, 255, 255, 0.14);

  border-radius: 10px;

  background:
    rgba(255, 255, 255, 0.08);

  color: white;

  text-decoration: none;

  transition:
    background 0.15s;
}


.aside-contact a:hover {
  background:
    rgba(255, 255, 255, 0.16);
}


.contact-icon {
  display: flex;

  flex: none;

  align-items: center;
  justify-content: center;

  width: 36px;
  height: 36px;

  border-radius: 9px;
}


.contact-icon svg {
  width: 19px;
  height: 19px;
}


.contact-icon.whatsapp {
  background: #25D366;

  color: #053D1B;
}


.contact-icon.phone {
  background: var(--amber);

  color: #3A2500;
}


.contact-icon.email {
  background: white;

  color: var(--teal);
}


.aside-contact small {
  display: block;

  color: #A9C8C7;

  font-size: 12px;
}


.aside-contact b {
  font-family: var(--display);

  font-stretch: 106%;

  font-weight: 700;

  font-size: 16px;
}


.email-value {
  overflow-wrap: anywhere;
}


/* =========================================
   RESPONSIVE
========================================= */

@media (max-width: 960px) {

  .quote-grid {
    grid-template-columns:
      1fr;
  }


  .aside-card {
    position: static;
  }

}


@media (max-width: 600px) {

  .form-row,
  .form-row.thirds {
    grid-template-columns:
      1fr;
  }


  .quote-hero p {
    font-size: 17px;
  }


  .primary-button {
    width: 100%;
  }


  .submit-row {
    align-items: stretch;
  }


  .file-item {
    flex-wrap: wrap;
  }

}
</style>