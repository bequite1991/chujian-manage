<template>
  <div class="alerts-page">
    <div class="page-header">
      <h2 class="page-title">⚠️ 预警消息</h2>
      <button class="btn-refresh" @click="refreshAlerts">🔄 扫描预警</button>
    </div>

    <!-- 筛选 -->
    <div class="filters-bar">
      <button class="filter-btn" :class="{ active: filterType === '' }" @click="filterType = ''; fetchAlerts()">全部</button>
      <button class="filter-btn" :class="{ active: filterType === 'stock_low' }" @click="filterType = 'stock_low'; fetchAlerts()">低库存</button>
      <button class="filter-btn" :class="{ active: filterType === 'slow_selling' }" @click="filterType = 'slow_selling'; fetchAlerts()">滞销</button>
      <button class="filter-btn" :class="{ active: filterType === 'unread' }" @click="filterType = 'unread'; fetchAlerts()">未读</button>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-text">加载中...</div>
    <!-- 空状态 -->
    <div v-else-if="alerts.length === 0" class="empty-state neon-card">
      <div class="empty-icon">🎉</div>
      <div class="empty-text">暂无预警，库存状态良好</div>
    </div>
    <!-- 预警列表 -->
    <div v-else class="alerts-list">
      <div
        v-for="a in filteredAlerts"
        :key="a.id"
        class="alert-item neon-card"
        :class="{ 'is-read': a.is_read, 'stock-low': a.alert_type === 'stock_low', 'slow': a.alert_type === 'slow_selling' }"
      >
        <div class="alert-icon">
          {{ a.alert_type === 'stock_low' ? '🔴' : '📉' }}
        </div>
        <div class="alert-body">
          <div class="alert-message">{{ a.message }}</div>
          <div class="alert-time">{{ formatTime(a.created_at) }}</div>
        </div>
        <div class="alert-actions">
          <button
            v-if="!a.is_read"
            class="btn-read"
            @click="markRead(a.id)"
          >✓ 已读</button>
          <span v-else class="read-tag">已读</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API = 'http://localhost:8000'
const alerts = ref([])
const loading = ref(false)
const filterType = ref('')

async function checkAlerts() {
  try {
    await fetch(`${API}/api/stocks/check-alerts`)
  } catch (e) { console.error(e) }
}

async function fetchAlerts() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filterType.value === 'unread') params.append('is_read', 'false')
    else if (filterType.value) params.append('alert_type', filterType.value)
    const res = await fetch(`${API}/api/stocks/alerts?${params}`)
    if (res.ok) alerts.value = await res.json()
  } catch (e) { console.error(e) }
  loading.value = false
}

async function markRead(id) {
  try {
    const res = await fetch(`${API}/api/stocks/alerts/${id}/read`, { method: 'PUT' })
    if (res.ok) {
      const alert = alerts.value.find(a => a.id === id)
      if (alert) alert.is_read = true
    }
  } catch (e) { console.error(e) }
}

async function refreshAlerts() {
  loading.value = true
  await checkAlerts()
  await fetchAlerts()
}

function formatTime(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return `${d.getFullYear()}-${(d.getMonth()+1).toString().padStart(2,'0')}-${d.getDate().toString().padStart(2,'0')} ${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`
}

const filteredAlerts = computed(() => {
  if (filterType.value === 'unread') return alerts.value.filter(a => !a.is_read)
  return alerts.value
})

onMounted(async () => {
  await checkAlerts()
  await fetchAlerts()
})
</script>

<style scoped>
.alerts-page { padding-bottom: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-title { font-size: 20px; color: #ff00ff; text-shadow: 0 0 10px #ff00ff50; margin: 0; }
.btn-refresh { background: linear-gradient(135deg, #00ffff30, #00ffff50); border: 1px solid #00ffff40; color: #00ffff; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 13px; }

.filters-bar { display: flex; gap: 10px; margin-bottom: 16px; }
.filter-btn { padding: 8px 16px; background: #0d0518; border: 1px solid #ff00ff30; border-radius: 20px; color: #9ca3af; cursor: pointer; font-size: 13px; transition: all 0.2s; }
.filter-btn.active { background: linear-gradient(135deg, #ff00ff30, #aa3bff30); border-color: #ff00ff60; color: #ff00ff; }
.filter-btn:hover { border-color: #ff00ff50; color: #fff; }

.loading-text { text-align: center; padding: 40px; color: #666; }

.empty-state { text-align: center; padding: 40px; }
.empty-icon { font-size: 48px; margin-bottom: 12px; }
.empty-text { color: #666; font-size: 14px; }

.alerts-list { display: flex; flex-direction: column; gap: 12px; }
.alert-item { display: flex; align-items: center; gap: 14px; padding: 16px; background: #0d0518; border-radius: 12px; border: 1px solid #ff00ff20; transition: opacity 0.3s; }
.alert-item.is-read { opacity: 0.45; }
.alert-item.stock-low { border-left: 3px solid #ff4444; }
.alert-item.slow { border-left: 3px solid #ffaa00; }

.alert-icon { font-size: 24px; flex-shrink: 0; }
.alert-body { flex: 1; }
.alert-message { color: #e0e0e0; font-size: 14px; margin-bottom: 4px; }
.alert-time { font-size: 11px; color: #666; }
.alert-actions { flex-shrink: 0; }
.btn-read { padding: 6px 14px; background: linear-gradient(135deg, #ff00ff, #aa3bff); border: none; color: white; border-radius: 16px; cursor: pointer; font-size: 12px; }
.read-tag { font-size: 12px; color: #666; padding: 6px 14px; border: 1px solid #333; border-radius: 16px; }
</style>