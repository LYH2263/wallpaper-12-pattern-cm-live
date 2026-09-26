<script setup>
import { onMounted, reactive, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const items = ref([])
const drafts = reactive({})
const errors = reactive({})
onMounted(load)
async function load() {
  items.value = (await getJSON('/api/rolls')).items
  for (const r of items.value) drafts[r.id] = r.pattern_cm
}
async function save(r) {
  errors[r.id] = ''
  try {
    const updated = await patchJSON(`/api/rolls/${r.id}`, { pattern_cm: Number(drafts[r.id]) })
    r.pattern_cm = updated.pattern_cm
    drafts[r.id] = updated.pattern_cm
  } catch (e) {
    errors[r.id] = e.message
  }
}
</script>
<template>
  <div class="page"><h1>纸卷规格</h1>
  <div v-for="r in items" :key="r.id" class="roll-chip">
    {{ r.name }} · 宽{{ r.width }}m · 长{{ r.length }}m ·
    <label>花高（cm）<input type="number" step="0.1" min="0" v-model.number="drafts[r.id]"></label>
    <button @click="save(r)">保存</button>
    <span v-if="errors[r.id]" class="warn">{{ errors[r.id] }}</span>
  </div>
  </div>
</template>
