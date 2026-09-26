import { createI18n } from 'vue-i18n'

import de from '../locales/de.json'
import en from '../locales/en.json'
import fa from '../locales/fa.json'
import ar from '../locales/ar.json'

const savedLanguage = localStorage.getItem('language') || 'de'

const i18n = createI18n({
  legacy: false,

  locale: savedLanguage,

  fallbackLocale: 'de',

  messages: {
    de,
    en,
    fa,
    ar,
  },
})

export default i18n