let loading
export function loadTurnstile() {
  if (window.turnstile) return Promise.resolve(window.turnstile)
  if (!loading) {
    loading = new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit'
      script.async = true
      script.onload = () => resolve(window.turnstile)
      script.onerror = () => { loading = undefined; script.remove(); reject(new Error('Security check unavailable')) }
      document.head.appendChild(script)
    })
  }
  return loading
}
