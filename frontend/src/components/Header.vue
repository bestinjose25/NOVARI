<script setup>
import { ref, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import logo from '../assets/images/NovariLogo.png'

const router = useRouter()

const { locale, t } = useI18n({
  useScope: 'global',
})

const mobileOpen = ref(false)

const languages = [
  {
    code: 'de',
    name: 'DE',
  },
  {
    code: 'en',
    name: 'EN',
  },
  {
    code: 'fa',
    name: 'FA',
  },
  {
    code: 'ar',
    name: 'AR',
  },
]


watch(
  locale,
  (newLocale) => {
    localStorage.setItem('language', newLocale)

    document.documentElement.lang = newLocale

    document.documentElement.dir =
      newLocale === 'fa' || newLocale === 'ar'
        ? 'rtl'
        : 'ltr'
  },
  {
    immediate: true,
  }
)


const closeMobile = () => {
  mobileOpen.value = false
}
</script>


<template>

  <!-- =====================================
       NAVBAR
  ====================================== -->

  <header
    class="
      sticky
      top-0
      z-[60]
      border-b
      border-[#D8E1E0]/70
      bg-[#F4F6F5]/90
      backdrop-blur-xl
      shadow-sm
    "
  >

    <nav
      class="
        mx-auto
        flex
        h-[74px]
        max-w-[1180px]
        items-center
        gap-5
        px-[clamp(18px,4vw,32px)]
      "
    >

      <!-- =================================
           LOGO
      ================================== -->

      <RouterLink
        to="/"
        class="
          flex
          shrink-0
          items-center
          gap-3
        "
        @click="closeMobile"
      >

        <img
          :src="logo"
          alt="NOVARI"
          class="
            h-[42px]
            w-auto
            object-contain
          "
        >

      </RouterLink>



      <!-- =================================
           DESKTOP NAVIGATION
      ================================== -->

      <div
        class="
          ml-auto
          hidden
          items-center
          gap-1
          lg:flex
        "
      >

        <!-- HOME -->
        <RouterLink
          to="/"
          class="
            rounded-lg
            px-3
            py-2
            text-[15px]
            font-semibold
            text-[#0C272B]
            transition
            hover:bg-[#EAEFEE]
            hover:text-[#0E5A63]
          "
          active-class="!text-[#0E5A63]"
        >
          {{ t('header.home') }}
        </RouterLink>


        <!-- SERVICES -->
        <RouterLink
          to="/services"
          class="
            rounded-lg
            px-3
            py-2
            text-[15px]
            font-semibold
            text-[#0C272B]
            transition
            hover:bg-[#EAEFEE]
            hover:text-[#0E5A63]
          "
          active-class="!text-[#0E5A63]"
        >
          {{ t('header.services') }}
        </RouterLink>


        <!-- HOW IT WORKS -->
                    <RouterLink
              :to="{
                name: 'home',
                hash: '#how-it-works'
              }"
              class="
                rounded-lg
                px-3
                py-2
                text-[15px]
                font-semibold
                text-[#0C272B]
                transition
                hover:bg-[#EAEFEE]
                hover:text-[#0E5A63]
              "
            >
              {{ t('header.howItWorks') }}
            </RouterLink>


                    <!-- SERVICE AREA -->
            <RouterLink
              :to="{
                name: 'home',
                hash: '#service-area'
              }"
              class="
                rounded-lg
                px-3
                py-2
                text-[15px]
                font-semibold
                text-[#0C272B]
                transition
                hover:bg-[#EAEFEE]
                hover:text-[#0E5A63]
              "
            >
              {{ t('header.serviceArea') }}
            </RouterLink>


        <!-- CONTACT -->
        <RouterLink
          to="/contact"
          class="
            rounded-lg
            px-3
            py-2
            text-[15px]
            font-semibold
            text-[#0C272B]
            transition
            hover:bg-[#EAEFEE]
            hover:text-[#0E5A63]
          "
          active-class="!text-[#0E5A63]"
        >
          {{ t('header.contact') }}
        </RouterLink>

      </div>



      <!-- =================================
           LANGUAGE
      ================================== -->

      <select
        v-model="locale"
        aria-label="Language"
        class="
          ml-auto
          hidden
          rounded-lg
          border
          border-[#D8E1E0]
          bg-white
          px-2.5
          py-2
          text-sm
          font-bold
          text-[#0C272B]
          outline-none
          transition
          focus:border-[#0E5A63]
          lg:block
          lg:ml-2
        "
      >

        <option
          v-for="language in languages"
          :key="language.code"
          :value="language.code"
        >
          {{ language.name }}
        </option>

      </select>



      <!-- =================================
           REQUEST QUOTE
      ================================== -->

      <RouterLink
        to="/quote"
        class="
          hidden
          shrink-0
          items-center
          justify-center
          rounded-full
          bg-[#F49B1C]
          px-5
          py-2.5
          text-[14px]
          font-bold
          text-[#3A2500]
          shadow-sm
          transition
          hover:-translate-y-0.5
          hover:bg-[#E08A08]
          lg:inline-flex
        "
      >
        {{ t('header.quote') }}
      </RouterLink>



      <!-- =================================
           MOBILE HAMBURGER
      ================================== -->

      <button
        type="button"
        aria-label="Open menu"
        class="
          ml-auto
          flex
          h-11
          w-11
          items-center
          justify-center
          rounded-xl
          border
          border-[#D8E1E0]
          bg-white
          text-[#0C272B]
          lg:hidden
        "
        @click="mobileOpen = true"
      >

        <svg
          class="h-5 w-5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.2"
        >
          <path
            d="M3 6h18M3 12h18M3 18h18"
            stroke-linecap="round"
          />
        </svg>

      </button>

    </nav>

  </header>



  <!-- =====================================
       MOBILE MENU OVERLAY
  ====================================== -->

  <div
    v-if="mobileOpen"
    class="
      fixed
      inset-0
      z-[70]
      bg-[#0C272B]/50
    "
    @click.self="closeMobile"
  >

    <div
      class="
        absolute
        right-0
        top-0
        flex
        h-full
        w-[min(340px,86vw)]
        flex-col
        bg-[#F4F6F5]
        p-6
        shadow-2xl
      "
    >

      <!-- MOBILE TOP -->
      <div
        class="
          mb-6
          flex
          items-center
          justify-between
        "
      >

        <img
          :src="logo"
          alt="NOVARI"
          class="h-10 w-auto"
        >


        <button
          type="button"
          aria-label="Close menu"
          class="
            flex
            h-11
            w-11
            items-center
            justify-center
            rounded-xl
            border
            border-[#D8E1E0]
            bg-white
          "
          @click="closeMobile"
        >

          <svg
            class="h-5 w-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.2"
          >
            <path
              d="M6 6l12 12M18 6L6 18"
              stroke-linecap="round"
            />
          </svg>

        </button>

      </div>



      <!-- MOBILE LINKS -->

      <div
        class="
          flex
          flex-col
          gap-1
        "
      >

        <RouterLink
          to="/"
          class="mobile-link"
          @click="closeMobile"
        >
          {{ t('header.home') }}
        </RouterLink>


        <RouterLink
          to="/services"
          class="mobile-link"
          @click="closeMobile"
        >
          {{ t('header.services') }}
        </RouterLink>


          <RouterLink
          :to="{
          name: 'home',
          hash: '#how-it-works'
          }"
          class="mobile-link"
          @click="closeMobile"
          >
          {{ t('header.howItWorks') }}
          </RouterLink>


          <RouterLink
           :to="{
           name: 'home',
           hash: '#service-area'
           }"
           class="mobile-link"
            @click="closeMobile">
            {{ t('header.serviceArea') }}
          </RouterLink>


        <RouterLink
          to="/contact"
          class="mobile-link"
          @click="closeMobile"
        >
          {{ t('header.contact') }}
        </RouterLink>

      </div>



      <!-- MOBILE LANGUAGE -->

      <div
        class="
          mt-5
          border-t
          border-[#D8E1E0]
          pt-5
        "
      >

        <label
          class="
            mb-2
            block
            text-sm
            font-bold
            text-[#526468]
          "
        >
          {{ t('header.language') }}
        </label>


        <select
          v-model="locale"
          class="
            w-full
            rounded-xl
            border
            border-[#D8E1E0]
            bg-white
            px-4
            py-3
            font-semibold
            text-[#0C272B]
            outline-none
            focus:border-[#0E5A63]
          "
        >

          <option
            v-for="language in languages"
            :key="language.code"
            :value="language.code"
          >
            {{ language.name }}
          </option>

        </select>

      </div>



      <!-- MOBILE QUOTE -->

      <RouterLink
        to="/quote"
        class="
          mt-5
          inline-flex
          w-full
          items-center
          justify-center
          rounded-full
          bg-[#F49B1C]
          px-6
          py-4
          font-bold
          text-[#3A2500]
          transition
          hover:bg-[#E08A08]
        "
        @click="closeMobile"
      >
        {{ t('header.quote') }}
      </RouterLink>

    </div>

  </div>

</template>


<style scoped>
nav,
button,
a,
select {
  font-family: var(--display);
}


.mobile-link {
  width: 100%;

  padding: 14px 12px;

  border: 0;

  border-radius: 12px;

  background: transparent;

  color: var(--ink);

  font-family: var(--display);

  font-size: 18px;

  font-weight: 700;

  text-decoration: none;

  transition:
    background 0.15s,
    color 0.15s;
}


.mobile-link:hover {
  background: var(--paper-2);

  color: var(--teal);
}
</style>