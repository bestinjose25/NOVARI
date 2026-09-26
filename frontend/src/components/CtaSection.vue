<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n({
  useScope: 'global',
})
</script>


<template>
  <section
    class="
      relative
      overflow-hidden
      bg-[#E8DFD1]
      py-16
      text-[#0C272B]
      lg:py-20
    "
  >

    <!-- Decorative background -->
    <div
      class="
        absolute
        -right-20
        -top-20
        h-80
        w-80
        rounded-full
        bg-orange-400/20
        blur-3xl
      "
    ></div>


    <div
      class="
        relative
        mx-auto
        flex
        max-w-7xl
        flex-col
        items-start
        justify-between
        gap-8
        px-6
        lg:flex-row
        lg:items-center
        lg:px-8
      "
    >

      <!-- Heading -->
      <h2
        class="
          max-w-xl
          text-3xl
          font-black
          tracking-tight
          text-[#0C272B]
          sm:text-4xl
          lg:text-5xl
        "
      >
        {{ t('cta.title') }}
      </h2>


      <!-- Buttons -->
      <div
        class="
          flex
          w-full
          flex-col
          gap-3
          sm:w-auto
          sm:flex-row
          sm:flex-wrap
        "
      >

        <!-- Quote -->
        <RouterLink
          to="/quote"
          class="
            inline-flex
            items-center
            justify-center
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
          {{ t('cta.quote') }}
        </RouterLink>


        <!-- WhatsApp -->
        <a
          href="https://wa.me/491785129865"
          target="_blank"
          rel="noopener noreferrer"
          class="
            inline-flex
            items-center
            justify-center
            gap-2
            rounded-full
            bg-[#25D366]
            px-7
            py-4
            font-bold
            text-[#053d1b]
            transition
            duration-300
            hover:-translate-y-0.5
            hover:bg-[#20bd5a]
          "
        >

          <svg
            class="h-5 w-5"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path
              d="M12 2a10 10 0 0 0-8.7 15l-1.2 4.2 4.3-1.1A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2s-1.1.2-3.6-.9-3.9-3.6-4-3.8-.9-1.2-.9-2.3.6-1.6.8-1.8.4-.3.6-.3h.5c.2 0 .4 0 .6.5l.8 1.9c0 .2.1.4 0 .6l-.4.6-.3.3c-.2.2-.3.3-.1.6a8 8 0 0 0 1.4 1.8 7 7 0 0 0 2.1 1.3c.3.1.4.1.6-.1l.7-.9c.2-.3.4-.2.6-.1l1.8.9c.3.1.5.2.5.3s0 .6-.2 1z"
            />
          </svg>

          {{ t('cta.whatsapp') }}

        </a>


        <!-- Phone -->
        <a
          href="tel:+491739523061"
          class="
            inline-flex
            items-center
            justify-center
            gap-2
            rounded-full
            border
            border-[#0C272B]/20
            bg-white/60
            px-7
            py-4
            font-bold
            text-[#0C272B]
            transition
            duration-300
            hover:-translate-y-0.5
            hover:bg-white
          "
        >

          <svg
            class="h-5 w-5"
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

          {{ t('cta.call') }}

        </a>

      </div>

    </div>
  </section>
</template>