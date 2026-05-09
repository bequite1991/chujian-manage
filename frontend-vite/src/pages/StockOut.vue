<template>
  <div class="stock-out-page">
    <h2 class="page-title">⬆️ 出库操作</h2>

    <!-- 错误提示 -->
    <div v-if="errorMsg" class="error-banner">
      ⚠️ {{ errorMsg }}
    </div>
    <!-- 成功提示 -->
    <div v-if="successMsg" class="success-banner">
      ✅ 出库成功！
    </div>

    <!-- 出库表单 -->
    <div class="form-card">
      <div class="form-title">📤 填写出库信息</div>
      <form @submit.prevent="submitStockOut">
        <div class="form-row">
          <label>商品 *</label>
          <select v-model="form.product_id" required @change="checkStock">
            <option value="">-- 选择商品 --</option>
            <option v-for="p in products" :key="p.id" :value="p.id">
              {{ p.name }} ({{ p.category }}) - 库存: {{ stockMap[p.id] ?? 0 }}
            </option>
          </select>
        </div>
        <div class="form-row">
          <label>数量 *</label>
          <input v-model.number="form.quantity" type="number" min="1" required placeholder="出库数量" />
        </div>
        <div class="form-row">
          <label>销售单价</label>
          <input v-model.number="form.sale_price" type="number" step="0.01" min="0" placeholder="元/件" />
        </div>
        <div class="form-row">
          <label>操作人</label>
          <input v-model="form.operator" type="text" placeholder="操作人姓名" />
        </div>
        <div class="form-row">
          <label>备注</label>
          <input v-model="form.note" type="text" placeholder="备注信息（可选）" />
        </div>
        <div class="form-actions">
          <button type="button" class="btn-reset" @click="resetForm">重置</button>
          <button type="submit" class="btn-submit">确认出库</button>
        </div>
      </form>
    </div>

    <!-- 最近出库记录 -->
    <div class="records-section">
      <h3 class="section-title">📋 最近出库记录</h3>
      <div v-if="loading" class="loading-text">加载中...</div>
      <div v-else-if="records.length === 0" class="empty-text">暂无出库记录</div>
      <div v-else class="records-list">
        <div v-for="r in records.slice(0, 10)" :key="r.id" class="record-item">
          <div class="record-info">
            <span class="record-product">{{ r.product_id }}</span>
            <span class="record-qty">-{{ r.quantity }}</span>
            <span class="record-price">¥{{ r.sale_price?.toFixed(2) || '-' }}</span>
          </div>
          <div class="record-meta">
            <span>{{ r.operator || '未知' }}</span>
            <span>{{ r.note || '' }}</span>
            <span class="record-time">{{ formatTime(r.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API = 'http://localhost:8000'
const products = ref([])
const records = ref([])
const stockMap = ref({})
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const form = ref({
  product_id: '', quantity: null, sale_price: null, operator: '', note: ''
})

async function fetchProducts() {
  try {
    const res = await fetch(`${API}/api/products`)
    if (res.ok) products.value = await res.json()
  } catch (e) { console.error(e) }
}

async function fetchStock() {
  try {
    const res = await fetch(`${API}/api/stocks`)
    if (res.ok) {
      const data = await res.json()
      const m = {}
      data.forEach(s => { m[s.product_id] = s.quantity })
      stockMap.value = m
    }
  } catch (e) { console.error(e) }
}

async function fetchRecords() {
  loading.value = true
  try {
    const res = await fetch(`${API}/api/out-records?limit=20`)
    if (res.ok) records.value = await res.json()
  } catch (e) { console.error(e) }
  loading.value = false
}

function checkStock() {
  errorMsg.value = ''
  if (form.value.product_id) {
    const available = stockMap.value[form.value.product_id] || 0
    if (available === 0) {
      errorMsg.value = '该商品库存为0，无法出库'
    }
  }
}

async function submitStockOut() {
  if (!form.value.product_id || !form.value.quantity) {
    alert('请填写商品和数量')
    return
  }
  errorMsg.value = ''
  successMsg.value = ''
  try {
    const res = await fetch(`${API}/api/out-records`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    const data = await res.json()
    if (res.ok) {
      successMsg.value = '出库成功'
      resetForm()
      fetchRecords()
      fetchStock()
      setTimeout(() => { successMsg.value = '' }, 3000)
    } else {
      errorMsg.value = data.detail || JSON.stringify(data)
    }
  } catch (e) { alert('请求失败：' + e) }
}

function resetForm() {
  form.value = { product_id: '', quantity: null, sale_price: null, operator: '', note: '' }
}

function formatTime(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return `${d.getMonth()+1}/${d.getDate()} ${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`
}

onMounted(() => { fetchProducts(); fetchStock(); fetchRecords() })
</script>

<style scoped>
.stock-out-page { padding-bottom: 20px; }
.page-title { font-size: 20px; color: #ff00ff; margin-bottom: 20px; text-shadow: 0 0 10px #ff00ff50; }

.error-banner { background: linear-gradient(135deg, #ff444420, #ff444440); border: 1px solid #ff444450; border-radius: 10px; padding: 14px 20px; color: #ff6b6b; font-size: 15px; margin-bottom: 16px; }
.success-banner { background: linear-gradient(135deg, #00ff8820, #00ff8840); border: 1px solid #00ff8850; border-radius: 10px; padding: 14px 20px; color: #00ff88; font-size: 15px; margin-bottom: 16px; }

.form-card { background: #0d0518; border: 1px solid #ff00ff30; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
.form-title { font-size: 16px; color: #00ffff; margin-bottom: 16px; }

.form-row { display: flex; align-items: center; gap: 16px; margin-bottom: 14px; }
.form-row label { width: 80px; font-size: 14px; color: #9ca3af; flex-shrink: 0; }
.form-row input, .form-row select { flex: 1; padding: 10px 14px; background: #1a0b2e; border: 1px solid #ff00ff30; border-radius: 8px; color: #fff; font-size: 14px; }

.form-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 20px; }
.btn-reset { padding: 10px 20px; background: transparent; border: 1px solid #ff00ff30; color: #9ca3af; border-radius: 8px; cursor: pointer; }
.btn-submit { padding: 10px 24px; background: linear-gradient(135deg, #ff00ff, #aa3bff); border: none; color: white; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 15px; }

.section-title { font-size: 16px; color: #00ffff; margin-bottom: 12px; }
.records-list { display: flex; flex-direction: column; gap: 10px; }
.record-item { background: #0d0518; border: 1px solid #ff00ff20; border-radius: 10px; padding: 14px 16px; }
.record-info { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
.record-product { color: #e0e0e0; font-weight: 600; }
.record-qty { color: #ff6b6b; font-weight: bold; font-size: 16px; }
.record-price { color: #9ca3af; }
.record-meta { display: flex; gap: 16px; font-size: 12px; color: #666; }
.record-time { margin-left: auto; }

.loading-text, .empty-text { text-align: center; padding: 20px; color: #666; }
</style>