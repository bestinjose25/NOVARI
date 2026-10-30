<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { loadTurnstile } from '../turnstile'
import { turnstileSiteKey } from '../enquiries'
const props = defineProps({ action: { type: String, required: true } })
const emit = defineEmits(['update:modelValue'])
const { t } = useI18n()
const element = ref(null)
const failed = ref(false)
let id
let active = true
onMounted(async () => {
  try {
    const api = await loadTurnstile()
    if (!active) return
    id = api.render(element.value, {
      sitekey: turnstileSiteKey, action: props.action,
      callback: token => { failed.value = false; emit('update:modelValue', token) },
      'expired-callback': () => emit('update:modelValue', ''),
      'error-callback': () => { failed.value = true; emit('update:modelValue', '') },
    })
  } catch { failed.value = true }
})
function reset() {
  emit('update:modelValue', '')
  if (id !== undefined) window.turnstile?.reset(id)
}
defineExpose({ reset })
onUnmounted(() => { active = false; if (id !== undefined) window.turnstile?.remove(id) })
</script>
<template>
  <div class="my-5">
    <div ref="element"></div>
    <p v-if="failed" role="alert" class="text-sm text-red-700">{{ t('securityCheckError') }}</p>
  </div>
</template>
