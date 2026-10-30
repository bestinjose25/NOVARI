import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  if (process.env.NETLIFY === 'true') {
    const provider = env.VITE_BACKEND_PROVIDER || 'django'
    if (!['django', 'supabase'].includes(provider)) throw new Error('VITE_BACKEND_PROVIDER must be django or supabase.')
    const apiUrl = (provider === 'supabase' ? env.VITE_SUPABASE_URL || '' : env.VITE_API_BASE_URL || '').trim()
    let parsed
    try { parsed = new URL(apiUrl) } catch { /* handled below */ }
    if (apiUrl && (!parsed || parsed.protocol !== 'https:' || ['localhost', '127.0.0.1', '[::1]'].includes(parsed.hostname) || parsed.pathname !== '/' || parsed.search || parsed.hash || parsed.username || parsed.password)) {
      throw new Error('Set the selected backend URL to a valid HTTPS origin in Netlify.')
    }
    if (provider === 'supabase' && (!apiUrl || !env.VITE_TURNSTILE_SITE_KEY)) throw new Error('Supabase previews require VITE_SUPABASE_URL and VITE_TURNSTILE_SITE_KEY.')
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
