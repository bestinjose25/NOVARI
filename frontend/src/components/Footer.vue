<script setup>
import { useI18n } from 'vue-i18n'
import logo from '../assets/images/NovariLogo.png'


const { t } = useI18n({
  useScope: 'global',
})

const currentYear = new Date().getFullYear()

const footerServices = [
  'moving',
  'transport',
  'assembly',
  'clearance',
  'carrying',
]
</script>


<template>
  <footer class="bg-[#081f22] text-gray-300">

    <div
      class="
        mx-auto
        max-w-7xl
        px-6
        py-16
        lg:px-8
      "
    >

      <!-- Main footer -->
      <div
        class="
          grid
          grid-cols-1
          gap-10
          sm:grid-cols-2
          lg:grid-cols-[1.6fr_1fr_1fr_1.2fr]
        "
      >

        <!-- ================= -->
        <!-- BRAND -->
        <!-- ================= -->
<div>

  <RouterLink
    to="/"
    class="inline-block"
  >
    <div
      class="
        inline-flex
        rounded-xl
        bg-white
        p-2
      "
    >
      <img
        :src="logo"
        alt="NOVARI Umzug und Möbelmontage"
        class="
          w-[220px]
          max-w-full
          object-contain
        "
      >
    </div>
  </RouterLink>


  <p
    class="
      mt-4
      max-w-sm
      text-sm
      leading-6
      text-gray-400
    "
  >
    {{ t('footer.description') }}
  </p>

</div>


        <!-- ================= -->
        <!-- NAVIGATION -->
        <!-- ================= -->
        <div>

          <h3
            class="
              mb-5
              text-sm
              font-bold
              uppercase
              tracking-widest
              text-white
            "
          >
            {{ t('footer.navigation') }}
          </h3>


          <ul class="space-y-3 text-sm">

            <li>
              <RouterLink
                to="/"
                class="transition hover:text-orange-400"
              >
                {{ t('header.home') }}
              </RouterLink>
            </li>


            <li>
              <RouterLink
                to="/services"
                class="transition hover:text-orange-400"
              >
                {{ t('header.services') }}
              </RouterLink>
            </li>


            <li>
              <RouterLink
                :to="{ path: '/', hash: '#how-it-works' }"
                class="transition hover:text-orange-400"
              >
                {{ t('header.howItWorks') }}
              </RouterLink>
            </li>


            <li>
              <RouterLink
                :to="{ path: '/', hash: '#service-area' }"
                class="transition hover:text-orange-400"
              >
                {{ t('header.serviceArea') }}
              </RouterLink>
            </li>


            <li>
              <RouterLink
                to="/contact"
                class="transition hover:text-orange-400"
              >
                {{ t('header.contact') }}
              </RouterLink>
            </li>


            <li>
              <RouterLink
                to="/quote"
                class="transition hover:text-orange-400"
              >
                {{ t('header.quote') }}
              </RouterLink>
            </li>

          </ul>

        </div>


        <!-- ================= -->
        <!-- SERVICES -->
        <!-- ================= -->
        <div>

          <h3
            class="
              mb-5
              text-sm
              font-bold
              uppercase
              tracking-widest
              text-white
            "
          >
            {{ t('footer.services') }}
          </h3>


          <ul class="space-y-3 text-sm">

            <li
              v-for="service in footerServices"
              :key="service"
            >

              <RouterLink
                to="/services"
                class="
                  transition
                  hover:text-orange-400
                "
              >
                {{ t(`services.items.${service}.title`) }}
              </RouterLink>

            </li>

          </ul>

        </div>


        <!-- ================= -->
        <!-- CONTACT -->
        <!-- ================= -->
        <div>

          <h3
            class="
              mb-5
              text-sm
              font-bold
              uppercase
              tracking-widest
              text-white
            "
          >
            {{ t('footer.contact') }}
          </h3>


          <div class="space-y-5">

            <!-- WhatsApp -->
            <a
              href="https://wa.me/491785129865"
              target="_blank"
              rel="noopener noreferrer"
              class="
                flex
                items-start
                gap-3
                transition
                hover:text-orange-400
              "
            >

              <svg
                class="
                  mt-0.5
                  h-5
                  w-5
                  shrink-0
                  text-orange-400
                "
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M12 2a10 10 0 0 0-8.7 15l-1.2 4.2 4.3-1.1A10 10 0 1 0 12 2z"
                />
              </svg>


              <div class="text-sm">

                <span class="text-gray-400">
                  {{ t('footer.whatsapp') }}
                </span>

                <p class="font-semibold text-white">
                  0178 5129865
                </p>

              </div>

            </a>


            <!-- Phone -->
            <a
              href="tel:+491739523061"
              class="
                flex
                items-start
                gap-3
                transition
                hover:text-orange-400
              "
            >

              <svg
                class="
                  mt-0.5
                  h-5
                  w-5
                  shrink-0
                  text-orange-400
                "
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


              <div class="text-sm">

                <span class="text-gray-400">
                  {{ t('footer.phone') }}
                </span>

                <p class="font-semibold text-white">
                  0173 9523061
                </p>

              </div>

            </a>


            <!-- Email -->
            <a
              href="mailto:Novari2026@yahoo.com"
              class="
                flex
                items-start
                gap-3
                transition
                hover:text-orange-400
              "
            >

              <svg
                class="
                  mt-0.5
                  h-5
                  w-5
                  shrink-0
                  text-orange-400
                "
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


              <div class="text-sm">

                <span class="text-gray-400">
                  {{ t('footer.email') }}
                </span>

                <p
                  class="
                    break-all
                    font-semibold
                    text-white
                  "
                >
                  Novari2026@yahoo.com
                </p>

              </div>

            </a>

          </div>

        </div>

      </div>


      <!-- ================= -->
      <!-- FOOTER BOTTOM -->
      <!-- ================= -->

      <div
        class="
          mt-12
          flex
          flex-col
          gap-4
          border-t
          border-white/10
          pt-6
          text-sm
          text-gray-500
          sm:flex-row
          sm:items-center
          sm:justify-between
        "
      >

        <p>
          © {{ currentYear }} {{ t('footer.copyright') }}
        </p>


        <div class="flex flex-wrap gap-2">

          <RouterLink
            to="/impressum"
            class="
              transition
              hover:text-orange-400
            "
          >
            {{ t('footer.impressum') }}
          </RouterLink>


          <span>·</span>


          <RouterLink
            to="/privacy"
            class="
              transition
              hover:text-orange-400
            "
          >
            {{ t('footer.privacy') }}
          </RouterLink>

        </div>

      </div>

    </div>

  </footer>
</template>