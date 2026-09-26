<script setup>
import { computed, onMounted, ref } from 'vue'
import { getJSON } from '../api'
import PatternHeightEditor from '../components/PatternHeightEditor.vue'
const items = ref([])
const rollId = ref(null)
onMounted(async () => {
  items.value = (await getJSON('/api/rolls')).items
  if (items.value.length) rollId.value = items.value[0].id
})
const selectedRoll = computed(() => items.value.find(r => r.id === rollId.value) || null)
function onSaved(updated) {
  const i = items.value.findIndex(r => r.id === updated.id)
  if (i >= 0) items.value[i] = updated
}
</script>
<template>
  <div class="page"><h1>对花说明</h1>
  <p>有花高时在墙高上加 花高/100 作为每条长度，再算每卷可裁条数与订货卷数。</p>
  <div v-if="items.length">
    <select v-model.number="rollId"><option v-for="r in items" :key="r.id" :value="r.id">{{ r.name }}</option></select>
    <div class="roll-chip" v-if="selectedRoll">
      <PatternHeightEditor :roll="selectedRoll" @saved="onSaved" />
    </div>
  </div>
  </div>
</template>
