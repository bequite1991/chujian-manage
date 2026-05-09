<template>
  <div>
    <!-- 今日数据 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">今日销售额</div>
        <div class="stat-value">¥{{ today.today_sales || 0 }}</div>
        <div class="stat-change" :style="{ color: (today.sales_change || 0) >= 0 ? '#00ff88' : '#ff3366' }">
          {{ (today.sales_change || 0) >= 0 ? '↑' : '↓' }}{{ Math.abs(today.sales_change || 0) }}%
        </div>
      </div>
      <div class="stat-card blue">
        <div class="stat-label">今日订单</div>
        <div class="stat-value">{{ today.today_orders || 0 }}单</div>
        <div class="stat-change" :style="{ color: (today.orders_change || 0) >= 0 ? '#00ff88' : '#ff3366' }">
          {{ (today.orders_change || 0) >= 0 ? '↑' : '↓' }}{{ Math.abs(today.orders_change || 0) }}%
        </div>
      </div>
      <div class="stat-card orange">
        <div class="stat-label">今日出库</div>
        <div class="stat-value">{{ today.today_out || 0 }}件</div>
        <div class="stat-change" :style="{ color: (today.out_change || 0) >= 0 ? '#00ff88' : '#ff3366' }">
          {{ (today.out_change || 0) >= 0 ? '↑' : '↓' }}{{ Math.abs(today.out_change || 0) }}%
        </div>
      </div>
    </div>

    <!-- 预警概览 -->
    <div class="section">
      <div class="section-title">⚠️ 库存预警</div>
      <div v-if="alerts.length === 0" style="color:#888;font-size:13px;">暂无预警</div>
      <div v-for="alert in alerts.slice(0, 5)" :key="alert.id" :class="['alert-item', alert.alert_type === 'slow_selling' ? 'slow' : '']">
        <div class="alert-dot"></div>
        <div class="alert-content">
          <div class="alert-product">{{ alert.message }}</div>
          <div class="alert-info">{{ alert.created_at ? new Date(alert.created_at).toLocaleString() : '' }}</div>
        </div>
        <button class="alert-btn" @click="markRead(alert.id)">已读</button>
      </div>
      <div v-if="alerts.length > 5" style="text-align:center;margin-top:8px;">
        <router-link to="/alerts" style="color:#ff00ff;font-size:13px;">查看全部 →</router-link>
      </div>
    </div>

    <!-- 畅销TOP5 -->
    <div class="section">
      <div class="section-title">🔥 畅销商品 TOP5</div>
      <div v-if="stats.top_selling.length === 0" style="color:#888;font-size:13px;">暂无数据</div>
      <div v-for="(item, idx) in stats.top_selling" :key="idx" class="rank-item">
        <div :class="['rank-num', idx < 3 ? ['gold','silver','bronze'][idx] : 'gray']">{{ idx + 1 }}</div>
        <div class="rank-info">
          <div class="rank-name">{{ item.name }}</div>
          <div class="rank-sales">销量 {{ item.sales || 0 }} 件</div>
        </div>
        <div class="rank-revenue">¥{{ item.revenue || 0 }}</div>
      </div>
    </div>

    <!-- 滞销TOP5 -->
    <div class="section">
      <div class="section-title">❄️ 滞销商品 TOP5</div>
      <div v-if="stats.slow_selling.length === 0" style="color:#888;font-size:13px;">暂无数据</div>
      <div v-for="(item, idx) in stats.slow_selling" :key="idx" class="rank-item">
        <div class="rank-num gray">{{ idx + 1 }}</div>
        <div class="rank-info">
          <div class="rank-name">{{ item.name }}</div>
          <div class="rank-sales">库存 {{ item.stock || 0 }} 件 · 7天销量 {{ item.sales_7d || 0 }}</div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <router-link to="/stock-in" class="action-btn">
        <span class="action-icon">⬇️</span>
        <span class="action-label">入库</span>
      </router-link>
      <router-link to="/stock-out" class="action-btn blue">
        <span class="action-icon">⬆️</span>
        <span class="action-label">出库</span>
      </router-link>
      <router-link to="/products" class="action-btn green">
        <span class="action-icon">📦</span>
        <span class="action-label">商品</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://localhost:8000/api'

const today = ref({ sales: 0, orders: 0, out_count: 0, sales_change: 0, orders_change: 0, out_change: 0 })
const stats = ref({ top_selling: [], slow_selling: [] })
const alerts = ref([])

async function fetchToday() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/today`)
    const data = await res.json()
    today.value = data || {}
  } catch (e) { console.error(e) }
}

async function fetchStats() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/stats`)
    const data = await res.json()
    stats.value = {
      top_selling: data.top_products || [],
      slow_selling: data.slow_products || []
    }
  } catch (e) { console.error(e) }
}

async function fetchAlerts() {
  try {
    const res = await fetch(`${API_BASE}/stocks/alerts?limit=20`)
    const data = await res.json()
    alerts.value = Array.isArray(data) ? data : (data.items || [])
  } catch (e) { console.error(e) }
}

async function markRead(id) {
  try {
    await fetch(`${API_BASE}/stocks/alerts/${id}/read`, { method: 'PUT' })
    alerts.value = alerts.value.filter(a => a.id !== id)
  } catch (e) { console.error(e) }
}

onMounted(() => {
  fetchToday()
  fetchStats()
  fetchAlerts()
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.stat-card {
  background: linear-gradient(135deg, rgba(255,0,255,0.15), rgba(255,0,255,0.05));
  border: 1px solid rgba(255,0,255,0.3);
  border-radius: 16px;
  padding: 16px;
}
.stat-card.blue {
  background: linear-gradient(135deg, rgba(0,255,255,0.15), rgba(0,255,255,0.05));
  border-color: rgba(0,255,255,0.3);
}
.stat-card.orange {
  background: linear-gradient(135deg, rgba(255,170,0,0.15), rgba(255,170,0,0.05));
  border-color: rgba(255,170,0,0.3);
}
.stat-label { font-size: 12px; color: #b0b0b0; }
.stat-value { font-size: 20px; font-weight: bold; margin: 8px 0; }
.stat-change { font-size: 12px; }
.section {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
}
.section-title { font-size: 16px; font-weight: bold; margin-bottom: 12px; }
.alert-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-radius: 12px;
  background: rgba(255,51,102,0.1);
  border: 1px solid rgba(255,51,102,0.3);
  margin-bottom: 10px;
}
.alert-item.slow {
  background: rgba(255,170,0,0.1);
  border-color: rgba(255,170,0,0.3);
}
.alert-dot { width: 8px; height: 8px; border-radius: 50%; background: #ff3366; }
.alert-item.slow .alert-dot { background: #ffaa00; }
.alert-content { flex: 1; }
.alert-product { font-size: 14px; font-weight: bold; }
.alert-info { font-size: 12px; color: #b0b0b0; }
.alert-btn {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  border: none;
  background: rgba(255,51,102,0.2);
  color: #ff3366;
  cursor: pointer;
}
.alert-item.slow .alert-btn {
  background: rgba(255,170,0,0.2);
  color: #ffaa00;
}
.rank-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #1a0b2e;
  border-radius: 12px;
  margin-bottom: 10px;
}
.rank-num {
  width: 28px; height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
}
.rank-num.gold { background: #ffaa00; color: #000; }
.rank-num.silver { background: #c0c0c0; color: #000; }
.rank-num.bronze { background: #cd7f32; color: #000; }
.rank-num.gray { background: rgba(255,255,255,0.1); color: #b0b0b0; }
.rank-info { flex: 1; }
.rank-name { font-size: 14px; font-weight: bold; }
.rank-sales { font-size: 12px; color: #b0b0b0; }
.rank-revenue { font-size: 14px; color: #ffaa00; font-weight: bold; }
.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}
.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border-radius: 16px;
  border: none;
  background: linear-gradient(135deg, rgba(255,0,255,0.15), rgba(255,0,255,0.05));
  border: 1px solid rgba(255,0,255,0.3);
  color: #fff;
  cursor: pointer;
  text-decoration: none;
}
.action-btn.blue {
  background: linear-gradient(135deg, rgba(0,255,255,0.15), rgba(0,255,255,0.05));
  border-color: rgba(0,255,255,0.3);
}
.action-btn.green {
  background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,255,136,0.05));
  border-color: rgba(0,255,136,0.3);
}
.action-icon { font-size: 32px; }
.action-label { font-size: 14px; }
</style>
