import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ServicesView from '../views/ServicesView.vue'
import QuoteView from '../views/QuoteView.vue'
import ContactView from '../views/ContactView.vue'
import PrivacyView from '../views/PrivacyView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },

  {
    path: '/services',
    name: 'services',
    component: ServicesView,
  },

  {
    path: '/quote',
    name: 'quote',
    component: QuoteView,
  },

  {
    path: '/contact',
    name: 'contact',
    component: ContactView,
  },

    {
    path: '/privacy',
    name: 'privacy',
    component: PrivacyView,
  },
]


const router = createRouter({
  history: createWebHistory(),
  routes,

  scrollBehavior(to, from, savedPosition) {

    // Browser back / forward
    if (savedPosition) {
      return savedPosition
    }

    // Go directly to a section
    if (to.hash) {
      return {
        el: to.hash,
        top: 80,
        behavior: 'smooth',
      }
    }

    // Normal page navigation
    return {
      top: 0,
      left: 0,
    }
  },
})

export default router