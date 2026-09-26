<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const queryId = ref('')
const pinned = ref(null)
const lookupError = ref('')
onMounted(load)
async function load() {
  items.value = (await getJSON('/api/runs')).items
}
async function lookup() {
  pinned.value = null
  lookupError.value = ''
  const id = Number(queryId.value)
  if (!Number.isInteger(id) || id <= 0) {
    lookupError.value = '请输入历史编号'
    return
  }
  try {
    pinned.value = await getJSON(`/api/runs/${id}`)
  } catch (e) {
    lookupError.value = e.message
  }
}
function dash(v) {
  return v === null || v === undefined || v === '' ? '—' : v
}
</script>
<template>
  <div class="page"><h1>记录</h1>
  <div>
    <label>编号<input type="number" min="1" v-model.number="queryId" @keyup.enter="lookup"></label>
    <button @click="lookup">回看</button>
    <span v-if="lookupError" class="warn">{{ lookupError }}</span>
  </div>
  <div v-if="pinned" class="roll-chip">
    #{{ pinned.id}} {{ pinned.wall_name }} → {{ pinned.roll_name }}：
    花高 {{ dash(pinned.result?.pattern_cm) }}cm · 条长 {{ dash(pinned.result?.drop_len_m) }}m ·
    每卷可裁 {{ dash(pinned.result?.strips_per_roll) }} 条 · 订货 <strong>{{ dash(pinned.result?.rolls) }}</strong> 卷
  </div>
  <ul><li v-for="r in items" :key="r.id">
    #{{ r.id }} {{ r.wall_name }} → {{ r.roll_name }}：
    花高 {{ dash(r.result?.pattern_cm) }}cm · 条长 {{ dash(r.result?.drop_len_m) }}m ·
    每卷可裁 {{ dash(r.result?.strips_per_roll) }} 条 · 订货 <strong>{{ dash(r.result?.rolls) }}</strong> 卷
  </li></ul>
  </div>
</template>
