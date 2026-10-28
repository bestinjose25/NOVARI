import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  if (process.env.NETLIFY === 'true') {
    const apiUrl = (env.VITE_API_BASE_URL || '').trim()
    let parsed
    try { parsed = new URL(apiUrl) } catch { /* handled below */ }
    if (apiUrl && (!parsed || parsed.protocol !== 'https:' || ['localhost', '127.0.0.1', '[::1]'].includes(parsed.hostname) || parsed.pathname !== '/' || parsed.search || parsed.hash || parsed.username || parsed.password)) {
      throw new Error('Set VITE_API_BASE_URL to your HTTPS backend origin in Netlify before deploying.')
    }
    if (!apiUrl) {
      console.warn('No backend configured: publishing the frontend with online forms disabled.')
    }
  }
  return {
  plugins: [
    vue(),
    tailwindcss(),
  ],

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  }
})
