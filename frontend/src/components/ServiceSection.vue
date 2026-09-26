<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n({
  useScope: 'global',
})

const services = [
  {
    id: 1,
    key: 'moving',
    icon: 'M3 7h11v9H3V7Zm11 3h4l3 3v3h-7v-6Z',
  },
  {
    id: 2,
    key: 'transport',
    icon: 'M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3M3 11h18v6H3v-6Z',
  },
  {
    id: 3,
    key: 'assembly',
    icon: 'M14 7l3-3 3 3-3 3M14 7l-8 8-2 5 5-2 8-8',
  },
  {
    id: 4,
    key: 'clearance',
    icon: 'M4 8h16l-1.5 12H5.5L4 8Zm4 0V6a4 4 0 0 1 8 0v2',
  },
  {
    id: 5,
    key: 'carrying',
    icon: 'M6 11V6a1.5 1.5 0 0 1 3 0v4M9 10V4.5a1.5 1.5 0 0 1 3 0V10M12 10V6a1.5 1.5 0 0 1 3 0v5',
  },
]
</script>

<template>
  <section class="bg-white py-16 lg:py-24">

    <div class="mx-auto max-w-7xl px-6 lg:px-8">

      <!-- Section heading -->
      <div class="mx-auto mb-12 max-w-2xl text-center">

        <p
          class="
            text-sm
            font-bold
            uppercase
            tracking-widest
            text-teal-700
          "
        >
          {{ t('services.eyebrow') }}
        </p>

        <h2
          class="
            mt-4
            text-3xl
            font-black
            tracking-tight
            text-gray-900
            sm:text-4xl
            lg:text-5xl
          "
        >
          {{ t('services.title') }}
        </h2>

        <p
          class="
            mt-5
            text-lg
            leading-8
            text-gray-600
          "
        >
          {{ t('services.description') }}
        </p>

      </div>


      <!-- Services grid -->
      <div
        class="
          grid
          grid-cols-1
          gap-6
          md:grid-cols-2
          lg:grid-cols-3
        "
      >

        <article
          v-for="service in services"
          :key="service.id"
          class="
            group
            relative
            overflow-hidden
            rounded-2xl
            border
            border-gray-200
            bg-white
            p-7
            transition
            duration-300
            hover:-translate-y-1
            hover:border-transparent
            hover:shadow-lg
          "
        >

          <!-- Orange hover line -->
          <div
            class="
              absolute
              left-0
              top-0
              h-1
              w-full
              origin-left
              scale-x-0
              bg-orange-400
              transition-transform
              duration-300
              group-hover:scale-x-100
            "
          ></div>


          <!-- Icon -->
          <div
            class="
              mb-5
              flex
              h-14
              w-14
              items-center
              justify-center
              rounded-xl
              bg-gray-100
              text-teal-700
              transition
              duration-300
              group-hover:bg-teal-700
              group-hover:text-white
            "
          >

            <svg
              class="h-7 w-7"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path :d="service.icon" />
            </svg>

          </div>


          <!-- Service title -->
          <h3 class="text-xl font-bold text-gray-900">
            {{ t(`services.items.${service.key}.title`) }}
          </h3>


          <!-- Description -->
          <p class="mt-3 leading-7 text-gray-600">
            {{ t(`services.items.${service.key}.description`) }}
          </p>


          <!-- Learn more -->
          <RouterLink
            to="/services"
            class="
              mt-5
              inline-flex
              items-center
              gap-2
              font-bold
              text-teal-700
            "
          >
            {{ t('services.learnMore') }}

            <svg
              class="
                h-4
                w-4
                transition
                group-hover:translate-x-1
              "
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

        </article>

      </div>

    </div>

  </section>
</template>