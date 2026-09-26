<script setup>
import { useI18n } from 'vue-i18n'
import ServiceAreaMap from './ServiceAreaMap.vue'

const { t } = useI18n({
  useScope: 'global',
})

const cities = [
  { id: 1, key: 'koblenz' },
  { id: 2, key: 'andernach' },
  { id: 3, key: 'neuwied' },
  { id: 4, key: 'mayen' },
  { id: 5, key: 'bendorf' },
  { id: 6, key: 'weissenthurm' },
  { id: 7, key: 'muelheimKaerlich' },
]
</script>


<template>
  <section
    id="service-area"
    class="scroll-mt-24 bg-gray-100 py-16 lg:py-24"
  >
    <div
      class="
        mx-auto
        grid
        max-w-7xl
        grid-cols-1
        items-center
        gap-12
        px-6
        lg:grid-cols-2
        lg:px-8
      "
    >

      <!-- ===================== -->
      <!-- LEFT SIDE: LIVE MAP -->
      <!-- ===================== -->

      <div
        class="
          overflow-hidden
          rounded-3xl
          border
          border-gray-200
          bg-white
          p-2
          shadow-md
        "
      >
        <ServiceAreaMap />
      </div>


      <!-- ===================== -->
      <!-- RIGHT SIDE -->
      <!-- ===================== -->

      <div>

        <!-- Eyebrow -->
        <div class="flex items-center gap-3">

          <span class="h-0.5 w-7 bg-orange-400"></span>

          <p
            class="
              text-sm
              font-bold
              uppercase
              tracking-widest
              text-teal-700
            "
          >
            {{ t('area.eyebrow') }}
          </p>

        </div>


        <!-- Heading -->
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
          {{ t('area.title') }}
        </h2>


        <!-- Description -->
        <p
          class="
            mt-5
            text-lg
            leading-8
            text-gray-600
          "
        >
          {{ t('area.description') }}
        </p>


        <!-- ===================== -->
        <!-- CITY LIST -->
        <!-- ===================== -->

        <div
          class="
            mt-8
            grid
            grid-cols-1
            gap-3
            sm:grid-cols-2
          "
        >

          <div
            v-for="city in cities"
            :key="city.id"
            class="
              flex
              items-center
              gap-3
              rounded-xl
              border
              border-gray-200
              bg-white
              px-4
              py-3
              font-bold
              text-gray-800
              transition
              duration-300
              hover:border-teal-700
              hover:shadow-sm
            "
          >

            <span
              class="
                h-3
                w-3
                shrink-0
                rounded-full
                bg-orange-400
              "
            ></span>

            {{ t(`area.cities.${city.key}`) }}

          </div>

        </div>


        <!-- ===================== -->
        <!-- NOTE -->
        <!-- ===================== -->

        <div
          class="
            mt-6
            flex
            items-start
            gap-3
            text-gray-600
          "
        >

          <svg
            class="mt-1 h-6 w-6 shrink-0 text-teal-700"
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
              r="2.4"
            />
          </svg>


          <p>
            {{ t('area.note') }}
          </p>

        </div>

      </div>

    </div>
  </section>
</template>