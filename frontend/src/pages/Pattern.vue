<script setup>
import { computed, onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const items = ref([])
const selectedId = ref(null)
const draft = ref(0)
const errorMsg = ref('')
const selected = computed(() => items.value.find(r => r.id === selectedId.value))
onMounted(async () => {
  items.value = (await getJSON('/api/rolls')).items
  if (items.value.length) {
    selectedId.value = items.value[0].id
    draft.value = items.value[0].pattern_cm
  }
})
function pick() {
  errorMsg.value = ''
  if (selected.value) draft.value = selected.value.pattern_cm
}
async function save() {
  errorMsg.value = ''
  try {
    const updated = await patchJSON(`/api/rolls/${selectedId.value}`, { pattern_cm: Number(draft.value) })
    const row = items.value.find(r => r.id === selectedId.value)
    if (row) row.pattern_cm = updated.pattern_cm
    draft.value = updated.pattern_cm
  } catch (e) {
    errorMsg.value = e.message
  }
}
</script>
<template>
  <div class="page"><h1>花匹配</h1>
  <p>有花高时在墙高上加花高/100（米）作为每条长度，再算每卷可裁条数与订货卷数。</p>
  <select v-if="items.length" v-model.number="selectedId" @change="pick">
    <option v-for="r in items" :key="r.id" :value="r.id">{{ r.name }}</option>
  </select>
  <div v-if="selected" class="roll-chip">
    {{ selected.name }} · 宽{{ selected.width }}m · 长{{ selected.length }}m ·
    <label>花高（cm）<input type="number" step="0.1" min="0" v-model.number="draft"></label>
    <button @click="save">保存</button>
    <span v-if="errorMsg" class="warn">{{ errorMsg }}</span>
  </div>
  </div>
</template>
