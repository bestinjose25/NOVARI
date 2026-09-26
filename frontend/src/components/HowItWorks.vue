<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n({
  useScope: 'global',
})

const steps = [
  {
    id: 1,
    key: 'photos',
  },
  {
    id: 2,
    key: 'destination',
  },
  {
    id: 3,
    key: 'access',
    hasTags: true,
  },
  {
    id: 4,
    key: 'date',
  },
  {
    id: 5,
    key: 'quote',
    completed: true,
  },
]
</script>


<template>
  <section
    id="how-it-works"
    class="bg-white py-16 lg:py-24"
  >
    <div class="mx-auto max-w-7xl px-6 lg:px-8">

      <!-- Section heading -->
      <div class="mx-auto mb-14 max-w-2xl text-center">

        <p
          class="
            text-sm
            font-bold
            uppercase
            tracking-widest
            text-teal-700
          "
        >
          {{ t('how.eyebrow') }}
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
          {{ t('how.title') }}
        </h2>


        <p
          class="
            mt-5
            text-lg
            leading-8
            text-gray-600
          "
        >
          {{ t('how.description') }}
        </p>

      </div>


      <!-- Steps -->
      <div class="relative">

        <!-- Dotted route line -->
        <div
          class="
            absolute
            left-[8%]
            right-[8%]
            top-8
            hidden
            border-t-2
            border-dashed
            border-teal-700
            lg:block
          "
        ></div>


        <div
          class="
            relative
            grid
            grid-cols-1
            gap-10
            sm:grid-cols-2
            lg:grid-cols-5
            lg:gap-5
          "
        >

          <article
            v-for="step in steps"
            :key="step.id"
            class="text-center"
          >

            <!-- Step circle -->
            <div
              class="
                relative
                z-10
                mx-auto
                mb-5
                flex
                h-16
                w-16
                items-center
                justify-center
                rounded-full
                border-4
                text-xl
                font-black
                shadow-sm
              "
              :class="
                step.completed
                  ? 'border-orange-400 bg-orange-400 text-gray-900'
                  : 'border-teal-700 bg-white text-teal-700'
              "
            >

              <!-- Numbers 1 - 4 -->
              <span v-if="!step.completed">
                {{ step.id }}
              </span>


              <!-- Final checkmark -->
              <svg
                v-else
                class="h-7 w-7"
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


            <!-- Step title -->
            <h3
              class="
                text-lg
                font-bold
                text-gray-900
              "
            >
              {{ t(`how.steps.${step.key}.title`) }}
            </h3>


            <!-- Step description -->
            <p
              class="
                mt-2
                text-sm
                leading-6
                text-gray-600
              "
            >
              {{ t(`how.steps.${step.key}.description`) }}
            </p>


            <!-- Floor + Elevator tags -->
            <div
              v-if="step.hasTags"
              class="
                mt-3
                flex
                flex-wrap
                justify-center
                gap-2
              "
            >

              <span
                class="
                  rounded-md
                  bg-gray-100
                  px-3
                  py-1
                  text-xs
                  font-semibold
                  text-teal-700
                "
              >
                {{ t('how.steps.access.floor') }}
              </span>


              <span
                class="
                  rounded-md
                  bg-gray-100
                  px-3
                  py-1
                  text-xs
                  font-semibold
                  text-teal-700
                "
              >
                {{ t('how.steps.access.elevator') }}
              </span>

            </div>

          </article>

        </div>

      </div>


      <!-- CTA -->
      <div class="mt-14 text-center">

        <RouterLink
          to="/quote"
          class="
            inline-flex
            items-center
            gap-2
            rounded-full
            bg-orange-400
            px-7
            py-4
            font-bold
            text-gray-900
            transition
            duration-300
            hover:-translate-y-0.5
            hover:bg-orange-500
          "
        >
          {{ t('how.startQuote') }}

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

      </div>

    </div>
  </section>
</template>