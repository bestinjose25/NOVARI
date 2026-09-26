<script setup>
defineProps({
  category: {
    type: String,
    required: true,
  },

  title: {
    type: String,
    required: true,
  },

  description: {
    type: String,
    required: true,
  },

  tags: {
    type: Array,
    default: () => [],
  },

  image: {
    type: String,
    required: true,
  },

  reverse: {
    type: Boolean,
    default: false,
  },

  buttonText: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <article
    class="
      overflow-hidden
      rounded-3xl
      border
      border-gray-200
      bg-white
      shadow-sm
      transition
      duration-300
      hover:-translate-y-1
      hover:shadow-lg
    "
  >
    <div class="grid grid-cols-1 lg:grid-cols-2">

      <!-- CONTENT -->
      <div
        :class="[
          'flex flex-col justify-center p-7 md:p-8 lg:p-9',
          reverse ? 'lg:order-2' : 'lg:order-1',
        ]"
      >
        <span
          class="
            w-fit
            rounded-full
            bg-gray-100
            px-3
            py-1.5
            text-xs
            font-bold
            uppercase
            tracking-wider
            text-gray-700
          "
        >
          {{ category }}
        </span>

        <h2
          class="
            mt-4
            text-2xl
            font-black
            leading-tight
            text-gray-900
            md:text-3xl
          "
        >
          {{ title }}
        </h2>

        <p
          class="
            mt-3
            max-w-xl
            text-base
            leading-7
            text-gray-600
          "
        >
          {{ description }}
        </p>

        <!-- TAGS -->
        <div class="mt-5 flex flex-wrap gap-2">

          <span
            v-for="tag in tags"
            :key="tag"
            class="
              rounded-full
              border
              border-gray-300
              bg-gray-50
              px-3
              py-1.5
              text-xs
              font-medium
              text-gray-700
            "
          >
            {{ tag }}
          </span>

        </div>

        <!-- BUTTON -->
        <RouterLink
          to="/quote"
          class="
            mt-6
            w-fit
            rounded-xl
            bg-red-600
            px-5
            py-3
            text-sm
            font-semibold
            text-white
            transition
            hover:bg-red-700
          "
        >
          {{ buttonText }}
        </RouterLink>

      </div>


      <!-- IMAGE -->
      <div
        :class="[
          'relative min-h-[230px] md:min-h-[280px] lg:min-h-[310px]',
          reverse ? 'lg:order-1' : 'lg:order-2',
        ]"
      >
        <img
          :src="image"
          :alt="title"
          class="absolute inset-0 h-full w-full object-cover"
        />
      </div>

    </div>
  </article>
</template>