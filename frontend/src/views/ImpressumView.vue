<script setup>
import { useI18n } from 'vue-i18n'
import business from '../business.json'
import Footer from '../components/Footer.vue'

const { t } = useI18n()
</script>

<template>
  <main class="bg-gray-50">
    <section class="mx-auto max-w-4xl px-6 py-16 sm:py-24">
      <h1 class="text-4xl font-black text-gray-900">{{ t('impressumPage.title') }}</h1>
      <div class="mt-8 space-y-7 rounded-2xl border border-gray-200 bg-white p-6 sm:p-10">
        <section>
          <h2 class="text-lg font-bold">{{ t('impressumPage.company') }}</h2>
          <p class="mt-2">{{ business.legalName || business.displayName }}</p>
          <p v-for="line in business.addressLines" :key="line">{{ line }}</p>
        </section>
        <section v-if="business.representatives.length">
          <h2 class="text-lg font-bold">{{ t('impressumPage.representatives') }}</h2>
          <p v-for="name in business.representatives" :key="name">{{ name }}</p>
        </section>
        <section>
          <h2 class="text-lg font-bold">{{ t('impressumPage.contact') }}</h2>
          <a class="mt-2 block text-teal-800 underline" :href="`mailto:${business.email}`">{{ business.email }}</a>
          <a class="mt-2 block text-teal-800 underline" :href="`tel:${business.phone}`">{{ business.phone }}</a>
        </section>
        <section v-if="business.registerInfo">
          <h2 class="text-lg font-bold">{{ t('impressumPage.register') }}</h2>
          <p class="whitespace-pre-line">{{ business.registerInfo }}</p>
        </section>
        <section v-if="business.vatId">
          <h2 class="text-lg font-bold">{{ t('impressumPage.vat') }}</h2>
          <p>{{ business.vatId }}</p>
        </section>
        <p v-if="business.additionalDisclosures" class="whitespace-pre-line">{{ business.additionalDisclosures }}</p>
      </div>
    </section>
    <Footer />
  </main>
</template>
