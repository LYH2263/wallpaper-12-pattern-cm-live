<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import PatternHeightEditor from '../components/PatternHeightEditor.vue'
const items = ref([])
async function load() { items.value = (await getJSON('/api/rolls')).items }
onMounted(load)
function onSaved(updated) {
  const i = items.value.findIndex(r => r.id === updated.id)
  if (i >= 0) items.value[i] = updated
}
</script>
<template>
  <div class="page"><h1>纸卷规格</h1>
  <div v-for="r in items" :key="r.id" class="roll-chip">
    {{ r.name }} · 宽{{ r.width }} · 长{{ r.length }} ·
    <PatternHeightEditor :roll="r" @saved="onSaved" />
  </div>
  </div>
</template>
