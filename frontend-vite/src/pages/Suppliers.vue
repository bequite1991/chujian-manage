<template>
  <div class="suppliers-page">
    <div class="page-header">
      <h2 class="page-title">🏢 供应商管理</h2>
      <button class="btn-add" @click="openAddModal">+ 新增供应商</button>
    </div>

    <!-- 供应商表格 -->
    <div class="table-container">
      <div v-if="loading" class="loading-text">加载中...</div>
      <div v-else-if="suppliers.length === 0" class="empty-text">暂无供应商，点击上方按钮添加</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>名称</th>
            <th>联系方式</th>
            <th>地址</th>
            <th>备注</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in suppliers" :key="s.id">
            <td class="name-cell">{{ s.name }}</td>
            <td>{{ s.contact || '-' }}</td>
            <td>{{ s.address || '-' }}</td>
            <td class="note-cell">{{ s.note || '-' }}</td>
            <td class="actions-cell">
              <button class="btn-action edit" @click="openEditModal(s)">✏️</button>
              <button class="btn-action delete" @click="deleteSupplier(s.id)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 新增/编辑弹窗 -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-box neon-modal">
        <h3 class="modal-title">{{ editingSupplier ? '✏️ 编辑供应商' : '➕ 新增供应商' }}</h3>
        <form @submit.prevent="submitSupplier">
          <div class="form-grid">
            <label>名称 *</label>
            <input v-model="form.name" required placeholder="供应商名称" />
            <label>联系方式</label>
            <input v-model="form.contact" placeholder="电话/微信" />
            <label>地址</label>
            <input v-model="form.address" placeholder="供应商地址" />
            <label>备注</label>
            <input v-model="form.note" placeholder="备注信息" />
          </div>
          <div class="modal-btns">
            <button type="button" class="btn-cancel" @click="closeModal">取消</button>
            <button type="submit" class="btn-confirm">确认</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API = 'http://localhost:8000'
const suppliers = ref([])
const loading = ref(false)
const showModal = ref(false)
const editingSupplier = ref(null)

const form = ref({ name: '', contact: '', address: '', note: '' })

async function fetchSuppliers() {
  loading.value = true
  try {
    const res = await fetch(`${API}/api/suppliers`)
    if (res.ok) suppliers.value = await res.json()
  } catch (e) { console.error(e) }
  loading.value = false
}

function openAddModal() {
  editingSupplier.value = null
  form.value = { name: '', contact: '', address: '', note: '' }
  showModal.value = true
}

function openEditModal(s) {
  editingSupplier.value = s
  form.value = { name: s.name, contact: s.contact || '', address: s.address || '', note: s.note || '' }
  showModal.value = true
}

function closeModal() { showModal.value = false }

async function submitSupplier() {
  const url = editingSupplier.value
    ? `${API}/api/suppliers/${editingSupplier.value.id}`
    : `${API}/api/suppliers`
  const method = editingSupplier.value ? 'PUT' : 'POST'
  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    if (res.ok) {
      closeModal()
      fetchSuppliers()
    } else {
      const err = await res.json()
      alert('失败：' + (err.detail || JSON.stringify(err)))
    }
  } catch (e) { alert('请求失败：' + e) }
}

async function deleteSupplier(id) {
  if (!confirm('确认删除该供应商？')) return
  try {
    const res = await fetch(`${API}/api/suppliers/${id}`, { method: 'DELETE' })
    if (res.ok) fetchSuppliers()
    else {
      const err = await res.json()
      alert(err.detail || '删除失败')
    }
  } catch (e) { alert('请求失败：' + e) }
}

onMounted(() => fetchSuppliers())
</script>

<style scoped>
.suppliers-page { padding-bottom: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.page-title { font-size: 20px; color: #ff00ff; text-shadow: 0 0 10px #ff00ff50; margin: 0; }
.btn-add { background: linear-gradient(135deg, #ff00ff, #aa3bff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: bold; }

.table-container { background: #0d0518; border: 1px solid #ff00ff20; border-radius: 12px; overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { background: linear-gradient(135deg, #ff00ff20, #00ffff20); padding: 12px; text-align: left; font-size: 12px; color: #00ffff; text-transform: uppercase; letter-spacing: 1px; }
.data-table td { padding: 14px 12px; border-top: 1px solid #ff00ff10; color: #e0e0e0; font-size: 14px; }
.data-table tr:hover td { background: #ff00ff08; }
.name-cell { color: #ff00ff; font-weight: 600; }
.note-cell { color: #666; font-size: 13px; }

.actions-cell { white-space: nowrap; }
.btn-action { background: none; border: none; cursor: pointer; font-size: 16px; padding: 4px 8px; opacity: 0.7; transition: opacity 0.2s; }
.btn-action:hover { opacity: 1; }

.loading-text, .empty-text { text-align: center; padding: 40px; color: #666; }

.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.neon-modal { background: #1a0b2e; border: 1px solid #ff00ff50; border-radius: 16px; padding: 24px; width: 90%; max-width: 480px; box-shadow: 0 0 30px #ff00ff30; }
.modal-title { font-size: 18px; color: #ff00ff; margin-bottom: 20px; text-shadow: 0 0 10px #ff00ff50; }
.form-grid { display: grid; grid-template-columns: 90px 1fr; gap: 14px; align-items: center; margin-bottom: 20px; }
.form-grid label { font-size: 13px; color: #9ca3af; text-align: right; }
.form-grid input { padding: 10px 12px; background: #0d0518; border: 1px solid #ff00ff30; border-radius: 8px; color: #fff; font-size: 14px; }
.modal-btns { display: flex; gap: 12px; justify-content: flex-end; }
.btn-cancel { padding: 10px 20px; background: transparent; border: 1px solid #ff00ff30; color: #9ca3af; border-radius: 8px; cursor: pointer; }
.btn-confirm { padding: 10px 20px; background: linear-gradient(135deg, #ff00ff, #aa3bff); border: none; color: white; border-radius: 8px; cursor: pointer; font-weight: bold; }
</style>