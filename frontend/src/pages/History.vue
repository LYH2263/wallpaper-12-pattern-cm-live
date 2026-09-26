<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const openId = ref(null)
const detail = ref(null)
const error = ref('')
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
async function review(runId) {
  error.value = ''
  if (openId.value === runId) { openId.value = null; detail.value = null; return }
  try {
    detail.value = await getJSON(`/api/runs/${runId}`)
    openId.value = runId
  } catch (e) {
    error.value = e.message || '回看失败'
  }
}
function patternCm(result) {
  return result.pattern_cm ?? Math.round((result.pattern_m ?? 0) * 100)
}
</script>
<template>
  <div class="page"><h1>记录</h1>
  <p v-if="error" class="warn">{{ error }}</p>
  <ul>
    <li v-for="r in items" :key="r.id">
      #{{ r.id }} {{ r.wall_name }} → {{ r.result?.rolls }} 卷
      <button @click="review(r.id)">{{ openId === r.id ? '收起' : '回看' }}</button>
      <div v-if="openId === r.id && detail" class="roll-chip">
        <strong>存档回看（钉住写入当时的测算）</strong><br>
        花高 {{ patternCm(detail.result) }}cm ·
        每条 {{ detail.result.drop_len_m }}m ·
        每卷可裁 {{ detail.result.strips_per_roll }} 条 ·
        {{ detail.result.drops }} 条 ·
        订货 {{ detail.result.rolls }} 卷<br>
        卷材 {{ detail.roll_name }} · {{ detail.created_at }}<span v-if="detail.note"> · {{ detail.note }}</span>
      </div>
    </li>
  </ul>
  </div>
</template>
