<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n({
  useScope: 'global',
})



const benefits = [
  {
    id: 1,
    key: 'reliable',
  },
  {
    id: 2,
    key: 'careful',
  },
  {
    id: 3,
    key: 'flexible',
  },
  {
    id: 4,
    key: 'pricing',
  },
  {
    id: 5,
    key: 'shortNotice',
  },
  {
    id: 6,
    key: 'punctual',
  },
]
</script>

<template>
  <section class="bg-[#123B5D] py-16 text-white lg:py-24">

    <div class="mx-auto max-w-7xl px-6 lg:px-8">

      <!-- Section heading -->
      <div class="mb-12 max-w-2xl">

        <p
          class="
            text-sm
            font-bold
            uppercase
            tracking-widest
            text-teal-200
          "
        >
          {{ t('why.eyebrow') }}
        </p>

        <h2
          class="
            mt-4
            text-3xl
            font-black
            tracking-tight
            text-white
            sm:text-4xl
            lg:text-5xl
          "
        >
          {{ t('why.title') }}
        </h2>

        <p
          class="
            mt-5
            text-lg
            leading-8
            text-teal-100
          "
        >
          {{ t('why.description') }}
        </p>

      </div>


      <!-- Benefits grid -->
      <div
        class="
          grid
          grid-cols-1
          gap-5
          md:grid-cols-2
          lg:grid-cols-3
        "
      >

        <article
          v-for="benefit in benefits"
          :key="benefit.id"
          class="
            flex
            gap-4
            rounded-2xl
            border
            border-white/10
            bg-white/5
            p-5
            transition
            duration-300
            hover:-translate-y-1
            hover:bg-white/10
          "
        >

          <!-- Check icon -->
          <div
            class="
              flex
              h-10
              w-10
              shrink-0
              items-center
              justify-center
              rounded-xl
              bg-orange-400
              text-gray-900
            "
          >
            <svg
              class="h-5 w-5"
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


          <!-- Text -->
          <div>

            <h3
              class="
                text-lg
                font-bold
                text-white
              "
            >
              {{ t(`why.items.${benefit.key}.title`) }}
            </h3>

            <p
              class="
                mt-1
                text-sm
                leading-6
                text-teal-100
              "
            >
              {{ t(`why.items.${benefit.key}.description`) }}
            </p>

          </div>

        </article>

      </div>

    </div>

  </section>
</template>