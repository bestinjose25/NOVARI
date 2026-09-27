<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

import homeImage from '../assets/images/HomeImage.jpeg'
</script>

<template>
  <section class="overflow-hidden bg-gray-50">
    <div
      class="
        mx-auto
        grid
        max-w-7xl
        grid-cols-1
        items-center
        gap-12
        px-6
        py-16
        lg:grid-cols-2
        lg:px-8
        lg:py-24
      "
    >

      <!-- LEFT SIDE -->
      <div>

        <!-- Small status badge -->
<!-- Quick business information -->
<div
  class="
    mb-6
    flex
    flex-wrap
    items-center
    gap-3
  "
>

  <!-- Service area -->
  <div
    class="
      inline-flex
      items-center
      gap-2.5
      rounded-full
      border
      border-gray-200
      bg-white
      px-4
      py-2
      text-sm
      font-medium
      text-gray-600
    "
  >
    <span
      class="h-2.5 w-2.5 rounded-full bg-green-500"
    ></span>

    {{ t('hero.badge') }}
  </div>


  <!-- Google Maps location -->
  <a
    href="https://maps.app.goo.gl/fvnktUbXY1mbyvBR8?g_st=iw"
    target="_blank"
    rel="noopener noreferrer"
    class="
      inline-flex
      items-center
      gap-2
      rounded-full
      border
      border-gray-200
      bg-white
      px-4
      py-2
      text-sm
      font-medium
      text-gray-600
      transition
      hover:border-teal-700
      hover:text-teal-700
    "
  >

    <!-- Location icon -->
    <svg
      class="h-4 w-4 text-teal-700"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
    >
      <path
        d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"
        stroke-linejoin="round"
      />

      <circle
        cx="12"
        cy="10"
        r="2.5"
      />
    </svg>

    {{ t('hero.location') }}

  </a>


  <!-- 24/7 service -->
  <div
    class="
      inline-flex
      items-center
      gap-2
      rounded-full
      border
      border-orange-200
      bg-orange-50
      px-4
      py-2
      text-sm
      font-bold
      text-orange-700
    "
  >

    <!-- Clock icon -->
    <svg
      class="h-4 w-4"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
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

    {{ t('hero.available24') }}

  </div>

</div>


        <!-- Main heading -->
        <h1
          class="
            max-w-2xl
            text-5xl
            font-black
            tracking-tight
            text-gray-900
            sm:text-6xl
            lg:text-7xl
          "
        >
          {{ t('hero.title') }}
          <span class="text-teal-700">
            {{ t('hero.highlight') }}
          </span>
        </h1>


        <!-- Description -->
        <h3
          class="
            mt-6
            max-w-xl
            text-lg
            leading-8
            text-gray-900
          "
        >
          {{ t('hero.mainDescription') }}
      </h3>
        <p
          class="
            mt-6
            max-w-xl
            text-lg
            leading-8
            text-gray-600
          "
        >
          {{ t('hero.description') }}
        </p>

        <!-- Buttons -->
        <div
          class="
            mt-8
            flex
            flex-col
            gap-4
            sm:flex-row
          "
        >

          <RouterLink
            to="/quote"
            class="
              inline-flex
              items-center
              justify-center
              gap-2
              rounded-full
              bg-orange-400
              px-7
              py-4
              font-bold
              text-gray-900
              transition
              hover:-translate-y-0.5
              hover:bg-orange-500
            "
          >
            {{ t('hero.quoteButton') }}

            <svg
              class="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.4"
            >
              <path
                d="M5 12h14M13 6l6 6-6 6"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>

          </RouterLink>


          <RouterLink
            to="/services"
            class="
              inline-flex
              items-center
              justify-center
              rounded-full
              border
              border-gray-300
              bg-white
              px-7
              py-4
              font-bold
              text-gray-900
              transition
              hover:border-teal-700
              hover:text-teal-700
            "
          >
            {{ t('hero.servicesButton') }}
          </RouterLink>

        </div>


        <!-- Trust information -->
        <div
          class="
            mt-10
            grid
            grid-cols-3
            gap-5
            border-t
            border-gray-200
            pt-7
          "
        >

          <div>
            <p class="text-2xl font-bold text-gray-900">
              {{ t('hero.townsNumber') }}
            </p>

            <p class="text-sm text-gray-500">
              {{ t('hero.towns') }}
            </p>
          </div>


          <div>
            <p class="text-2xl font-bold text-gray-900">
              {{ t('hero.appointmentsNumber') }}
            </p>

            <p class="text-sm text-gray-500">
              {{ t('hero.appointments') }}
            </p>
          </div>


          <div>
            <p class="text-2xl font-bold text-gray-900">
              {{ t('hero.pricingNumber') }}
            </p>

            <p class="text-sm text-gray-500">
              {{t('hero.pricing')}}
            </p>
          </div>

        </div>

      </div>


      <!-- RIGHT SIDE -->
      <div>

        <!-- Home moving image -->
        <img
          :src="homeImage"
          alt="Moving boxes and a couple preparing for a move"
          class="mx-auto h-[380px] w-full rounded-3xl object-cover"/>

      </div>

    </div>
  </section>
</template>