<template>
  <div class="products-page">
    <div class="page-header">
      <h2 class="page-title">📦 商品管理</h2>
      <button class="btn-add" @click="openAddModal">+ 新增商品</button>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filters-bar">
      <input v-model="keyword" class="search-input" placeholder="搜索商品名称..." @input="fetchProducts" />
      <select v-model="filterCategory" class="filter-select" @change="fetchProducts">
        <option value="">全部分类</option>
        <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
      </select>
      <select v-model="filterMaterial" class="filter-select" @change="fetchProducts">
        <option value="">全部材质</option>
        <option v-for="m in materials" :key="m" :value="m">{{ m }}</option>
      </select>
    </div>

    <!-- 商品表格 -->
    <div class="table-container">
      <div v-if="loading" class="loading-text">加载中...</div>
      <div v-else-if="products.length === 0" class="empty-text">暂无商品，点击上方按钮添加</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>图片</th>
            <th>名称</th>
            <th>分类</th>
            <th>材质</th>
            <th>颜色</th>
            <th>进价</th>
            <th>售价</th>
            <th>库存</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id">
            <td>
              <div class="img-cell">
                <img v-if="p.image_url" :src="'http://localhost:8000' + p.image_url" class="product-img" />
                <span v-else class="no-img">无图</span>
              </div>
            </td>
            <td class="name-cell">{{ p.name }}</td>
            <td>{{ p.category }}</td>
            <td>{{ p.material || '-' }}</td>
            <td>{{ p.color || '-' }}</td>
            <td>¥{{ p.cost_price?.toFixed(2) || '0.00' }}</td>
            <td class="price-cell">¥{{ p.sale_price?.toFixed(2) || '0.00' }}</td>
            <td :class="p.quantity === 0 ? 'zero-stock' : p.quantity < p.min_stock ? 'low-stock' : ''">
              {{ p.quantity ?? 0 }}
            </td>
            <td class="actions-cell">
              <button class="btn-action upload" @click="openUploadModal(p)" title="上传图片">📷</button>
              <button class="btn-action edit" @click="openEditModal(p)" title="编辑">✏️</button>
              <button class="btn-action delete" @click="deleteProduct(p.id)" title="删除">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 新增/编辑弹窗 -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-box neon-modal">
        <h3 class="modal-title">{{ editingProduct ? '✏️ 编辑商品' : '➕ 新增商品' }}</h3>
        <form @submit.prevent="submitProduct">
          <div class="form-grid">
            <label>名称 *</label>
            <input v-model="form.name" required placeholder="商品名称" />
            <label>分类 *</label>
            <input v-model="form.category" required placeholder="如：项链、手链" />
            <label>材质</label>
            <input v-model="form.material" placeholder="如：银、金、合金" />
            <label>颜色</label>
            <input v-model="form.color" placeholder="如：金色、银色" />
            <label>单位</label>
            <input v-model="form.unit" placeholder="件" />
            <label>进价</label>
            <input v-model.number="form.cost_price" type="number" step="0.01" min="0" placeholder="0.00" />
            <label>售价</label>
            <input v-model.number="form.sale_price" type="number" step="0.01" min="0" placeholder="0.00" />
            <label>最小库存</label>
            <input v-model.number="form.min_stock" type="number" min="0" placeholder="10" />
            <label>供应商</label>
            <select v-model="form.supplier_id">
              <option value="">无</option>
              <option v-for="s in suppliers" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div class="modal-btns">
            <button type="button" class="btn-cancel" @click="closeModal">取消</button>
            <button type="submit" class="btn-confirm">确认</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 上传图片弹窗 -->
    <div v-if="showUploadModal" class="modal-overlay" @click.self="closeUploadModal">
      <div class="modal-box neon-modal">
        <h3 class="modal-title">📷 上传商品图片 - {{ uploadingProduct?.name }}</h3>
        <div class="upload-area">
          <input type="file" accept="image/jpeg,image/png,image/webp,gif" @change="onFileChange" />
          <p class="upload-hint">支持 jpg/png/webp/gif 格式</p>
        </div>
        <div class="modal-btns">
          <button type="button" class="btn-cancel" @click="closeUploadModal">取消</button>
          <button type="button" class="btn-confirm" :disabled="uploading" @click="uploadImage">
            {{ uploading ? '上传中...' : '上传' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API = 'http://localhost:8000'
const products = ref([])
const suppliers = ref([])
const categories = ref([])
const materials = ref([])
const keyword = ref('')
const filterCategory = ref('')
const filterMaterial = ref('')
const loading = ref(false)
const showModal = ref(false)
const showUploadModal = ref(false)
const editingProduct = ref(null)
const uploadingProduct = ref(null)
const uploading = ref(false)
const selectedFile = ref(null)

const form = ref({
  name: '', category: '', material: '', color: '',
  unit: '件', cost_price: 0, sale_price: 0, min_stock: 10, supplier_id: ''
})

async function fetchProducts() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (keyword.value) params.append('keyword', keyword.value)
    if (filterCategory.value) params.append('category', filterCategory.value)
    if (filterMaterial.value) params.append('material', filterMaterial.value)
    const res = await fetch(`${API}/api/products?${params}`)
    if (res.ok) {
      const data = await res.json()
      // 合并库存数量
      const stockRes = await fetch(`${API}/api/stocks`)
      const stocks = stockRes.ok ? await stockRes.json() : []
      const stockMap = {}
      stocks.forEach(s => { stockMap[s.product_id] = s.quantity })
      products.value = data.map(p => ({ ...p, quantity: stockMap[p.id] ?? 0 }))
      // 提取分类和材质选项
      const cats = [...new Set(data.map(p => p.category).filter(Boolean))]
      const mats = [...new Set(data.map(p => p.material).filter(Boolean))]
      categories.value = cats
      materials.value = mats
    }
  } catch (e) { console.error(e) }
  loading.value = false
}

async function fetchSuppliers() {
  try {
    const res = await fetch(`${API}/api/suppliers`)
    if (res.ok) suppliers.value = await res.json()
  } catch (e) { console.error(e) }
}

function openAddModal() {
  editingProduct.value = null
  form.value = { name: '', category: '', material: '', color: '', unit: '件', cost_price: 0, sale_price: 0, min_stock: 10, supplier_id: '' }
  showModal.value = true
}

function openEditModal(p) {
  editingProduct.value = p
  form.value = {
    name: p.name, category: p.category, material: p.material || '',
    color: p.color || '', unit: p.unit || '件',
    cost_price: p.cost_price || 0, sale_price: p.sale_price || 0,
    min_stock: p.min_stock || 10, supplier_id: p.supplier_id || ''
  }
  showModal.value = true
}

function closeModal() { showModal.value = false }

async function submitProduct() {
  const url = editingProduct.value
    ? `${API}/api/products/${editingProduct.value.id}`
    : `${API}/api/products`
  const method = editingProduct.value ? 'PUT' : 'POST'
  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    if (res.ok) {
      closeModal()
      fetchProducts()
    } else {
      const err = await res.json()
      alert('失败：' + (err.detail || JSON.stringify(err)))
    }
  } catch (e) { alert('请求失败：' + e) }
}

async function deleteProduct(id) {
  if (!confirm('确认删除？')) return
  try {
    const res = await fetch(`${API}/api/products/${id}`, { method: 'DELETE' })
    if (res.ok) fetchProducts()
    else {
      const err = await res.json()
      alert(err.detail || '删除失败')
    }
  } catch (e) { alert('请求失败：' + e) }
}

function openUploadModal(p) {
  uploadingProduct.value = p
  selectedFile.value = null
  showUploadModal.value = true
}
function closeUploadModal() { showUploadModal.value = false }
function onFileChange(e) { selectedFile.value = e.target.files[0] }

async function uploadImage() {
  if (!selectedFile.value || !uploadingProduct.value) return
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    const res = await fetch(`${API}/api/products/upload-image/${uploadingProduct.value.id}`, {
      method: 'POST',
      body: formData
    })
    if (res.ok) {
      closeUploadModal()
      fetchProducts()
    } else {
      const err = await res.json()
      alert('上传失败：' + (err.detail || JSON.stringify(err)))
    }
  } catch (e) { alert('请求失败：' + e) }
  uploading.value = false
}

onMounted(() => { fetchProducts(); fetchSuppliers() })
</script>

<style scoped>
.products-page { padding-bottom: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-title { font-size: 20px; color: #ff00ff; text-shadow: 0 0 10px #ff00ff50; margin: 0; }
.btn-add { background: linear-gradient(135deg, #ff00ff, #aa3bff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: bold; }

.filters-bar { display: flex; gap: 10px; margin-bottom: 16px; }
.search-input { flex: 1; padding: 10px 14px; background: #0d0518; border: 1px solid #ff00ff30; border-radius: 8px; color: #fff; font-size: 14px; }
.search-input::placeholder { color: #666; }
.filter-select { padding: 10px 14px; background: #0d0518; border: 1px solid #ff00ff30; border-radius: 8px; color: #fff; font-size: 14px; cursor: pointer; }

.table-container { background: #0d0518; border: 1px solid #ff00ff20; border-radius: 12px; overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { background: linear-gradient(135deg, #ff00ff20, #00ffff20); padding: 12px; text-align: left; font-size: 12px; color: #00ffff; text-transform: uppercase; letter-spacing: 1px; }
.data-table td { padding: 12px; border-top: 1px solid #ff00ff10; color: #e0e0e0; font-size: 14px; }
.data-table tr:hover td { background: #ff00ff08; }

.img-cell { width: 40px; height: 40px; }
.product-img { width: 40px; height: 40px; object-fit: cover; border-radius: 6px; border: 1px solid #ff00ff30; }
.no-img { display: block; width: 40px; height: 40px; background: #1a0b2e; border-radius: 6px; text-align: center; line-height: 40px; font-size: 10px; color: #666; }
.name-cell { color: #ff00ff; font-weight: 600; }
.price-cell { color: #00ffff; font-weight: bold; }
.zero-stock { color: #666 !important; }
.low-stock { color: #ff6b6b !important; }

.actions-cell { white-space: nowrap; }
.btn-action { background: none; border: none; cursor: pointer; font-size: 16px; padding: 4px 8px; opacity: 0.7; transition: opacity 0.2s; }
.btn-action:hover { opacity: 1; }
.btn-action.delete:hover { filter: hue-rotate(180deg) saturate(3); }

.loading-text, .empty-text { text-align: center; padding: 40px; color: #666; }

.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.neon-modal { background: #1a0b2e; border: 1px solid #ff00ff50; border-radius: 16px; padding: 24px; width: 90%; max-width: 500px; box-shadow: 0 0 30px #ff00ff30; }
.modal-title { font-size: 18px; color: #ff00ff; margin-bottom: 20px; text-shadow: 0 0 10px #ff00ff50; }
.form-grid { display: grid; grid-template-columns: 100px 1fr; gap: 12px; align-items: center; margin-bottom: 20px; }
.form-grid label { font-size: 13px; color: #9ca3af; text-align: right; }
.form-grid input, .form-grid select { padding: 10px 12px; background: #0d0518; border: 1px solid #ff00ff30; border-radius: 8px; color: #fff; font-size: 14px; }
.modal-btns { display: flex; gap: 12px; justify-content: flex-end; }
.btn-cancel { padding: 10px 20px; background: transparent; border: 1px solid #ff00ff30; color: #9ca3af; border-radius: 8px; cursor: pointer; }
.btn-confirm { padding: 10px 20px; background: linear-gradient(135deg, #ff00ff, #aa3bff); border: none; color: white; border-radius: 8px; cursor: pointer; font-weight: bold; }
.btn-confirm:disabled { opacity: 0.5; cursor: not-allowed; }

.upload-area { margin-bottom: 20px; }
.upload-area input { color: #fff; }
.upload-hint { font-size: 12px; color: #666; margin-top: 8px; }
</style>