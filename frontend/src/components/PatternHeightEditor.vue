<script setup>
import { ref, watch } from 'vue'
import { patchJSON } from '../api'
const props = defineProps({ roll: { type: Object, required: true } })
const emit = defineEmits(['saved'])
const draft = ref('0')
const error = ref('')
const saving = ref(false)

watch(() => props.roll?.pattern_cm, v => { draft.value = String(v ?? 0) }, { immediate: true })

async function save() {
  error.value = ''
  const n = Number(draft.value)
  if (draft.value === '' || !Number.isFinite(n) || n < 0) {
    error.value = '花高不能为负'
    return
  }
  saving.value = true
  try {
    const updated = await patchJSON(`/api/rolls/${props.roll.id}/pattern`, { pattern_cm: n })
    emit('saved', updated)
  } catch (e) {
    error.value = e.message || '保存失败'
  } finally {
    saving.value = false
  }
}
</script>
<template>
  <span class="pattern-editor">
    花高 <input type="number" min="0" step="0.1" v-model="draft" @keyup.enter="save"> cm
    <button :disabled="saving" @click="save">保存</button>
    <span v-if="error" class="warn">{{ error }}</span>
  </span>
</template>
