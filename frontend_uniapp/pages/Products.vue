<template>
  <view class="products">
    <view class="header">
      <text class="title">商品管理</text>
      <button class="add-btn" @click="showAddModal">+ 新增</button>
    </view>

    <!-- 搜索 -->
    <view class="search-box">
      <input 
        type="text" 
        v-model="searchKeyword"
        placeholder="搜索商品名称或类别..."
        class="search-input"
      />
    </view>

    <!-- 商品列表 -->
    <view class="product-list">
      <view 
        v-for="item in filteredProducts" 
        :key="item.id"
        class="product-card"
      >
        <view class="product-info">
          <view class="product-image">
            <text class="image-placeholder">📷</text>
          </view>
          <view class="product-detail">
            <text class="product-name">{{ item.name }}</text>
            <text class="product-meta">{{ item.category }} · {{ item.material }} · {{ item.color }}</text>
            <view class="product-prices">
              <text class="cost-price">进价 ¥{{ item.cost_price }}</text>
              <text class="sale-price">售价 ¥{{ item.sale_price }}</text>
            </view>
          </view>
        </view>
        <view class="product-stock">
          <text class="stock-badge" :class="item.stock < 10 ? 'low' : 'normal'">
            库存 {{ item.stock }}
          </text>
          <view class="product-actions">
            <text class="action-edit" @click="editProduct(item)">编辑</text>
            <text class="action-delete" @click="deleteProduct(item.id)">删除</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 新增/编辑弹窗 -->
    <view v-if="modalVisible" class="modal">
      <view class="modal-mask" @click="closeModal"></view>
      <view class="modal-content">
        <view class="modal-header">
          <text class="modal-title">{{ editingProduct ? '编辑商品' : '新增商品' }}</text>
          <text class="modal-close" @click="closeModal">×</text>
        </view>
        <view class="form">
          <view class="form-item">
            <text class="label">商品名称</text>
            <input type="text" v-model="form.name" class="input" />
          </view>
          <view class="form-row">
            <view class="form-item half">
              <text class="label">类别</text>
              <picker mode="selector" :range="categories" :value="categoryIndex" @change="onCategoryChange">
                <view class="picker">{{ form.category || '请选择' }}</view>
              </picker>
            </view>
            <view class="form-item half">
              <text class="label">材质</text>
              <picker mode="selector" :range="materials" :value="materialIndex" @change="onMaterialChange">
                <view class="picker">{{ form.material || '请选择' }}</view>
              </picker>
            </view>
          </view>
          <view class="form-row">
            <view class="form-item half">
              <text class="label">进价</text>
              <input type="digit" v-model="form.cost_price" class="input" />
            </view>
            <view class="form-item half">
              <text class="label">售价</text>
              <input type="digit" v-model="form.sale_price" class="input" />
            </view>
          </view>
          <view class="form-item">
            <text class="label">颜色</text>
            <input type="text" v-model="form.color" class="input" placeholder="银色/金色/玫瑰金" />
          </view>
        </view>
        <button class="submit-btn" @click="submitForm">确认</button>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      searchKeyword: '',
      modalVisible: false,
      editingProduct: null,
      categories: ['项链', '耳环', '手链', '戒指', '发饰', '其他'],
      materials: ['钛钢', '合金', '银', '金', '珍珠', '水晶', '其他'],
      form: {
        name: '',
        category: '',
        material: '',
        color: '',
        cost_price: '',
        sale_price: ''
      },
      products: [
        { id: 1, name: '钛钢项链', category: '项链', material: '钛钢', color: '银色', cost_price: 15, sale_price: 39, stock: 45 },
        { id: 2, name: '水晶耳环', category: '耳环', material: '合金', color: '透明', cost_price: 8, sale_price: 25, stock: 23 },
        { id: 3, name: '珍珠手链', category: '手链', material: '珍珠', color: '白色', cost_price: 25, sale_price: 68, stock: 12 },
        { id: 4, name: '银戒指', category: '戒指', material: '银', color: '银色', cost_price: 20, sale_price: 55, stock: 8 },
      ]
    }
  },
  computed: {
    filteredProducts() {
      if (!this.searchKeyword) return this.products
      return this.products.filter(p => 
        p.name.includes(this.searchKeyword) || 
        p.category.includes(this.searchKeyword)
      )
    },
    categoryIndex() {
      return this.categories.indexOf(this.form.category)
    },
    materialIndex() {
      return this.materials.indexOf(this.form.material)
    }
  },
  methods: {
    showAddModal() {
      this.editingProduct = null
      this.form = { name: '', category: '', material: '', color: '', cost_price: '', sale_price: '' }
      this.modalVisible = true
    },
    editProduct(product) {
      this.editingProduct = product
      this.form = { ...product }
      this.modalVisible = true
    },
    deleteProduct(id) {
      uni.showModal({
        title: '确认删除',
        content: '确定删除此商品？',
        success: (res) => {
          if (res.confirm) {
            this.products = this.products.filter(p => p.id !== id)
          }
        }
      })
    },
    closeModal() {
      this.modalVisible = false
    },
    onCategoryChange(e) {
      this.form.category = this.categories[e.detail.value]
    },
    onMaterialChange(e) {
      this.form.material = this.materials[e.detail.value]
    },
    submitForm() {
      if (this.editingProduct) {
        const index = this.products.findIndex(p => p.id === this.editingProduct.id)
        this.products[index] = { ...this.editingProduct, ...this.form }
      } else {
        const newId = Math.max(...this.products.map(p => p.id)) + 1
        this.products.push({
          id: newId,
          ...this.form,
          stock: 0
        })
      }
      this.modalVisible = false
      uni.showToast({ title: '保存成功', icon: 'success' })
    }
  }
}
</script>

<style scoped>
.products {
  padding: 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.title {
  font-size: 20px;
  font-weight: bold;
}

.add-btn {
  background: #ff00ff;
  color: #fff;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  border: none;
}

.search-box {
  margin-bottom: 16px;
}

.search-input {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 12px 16px;
  color: #fff;
  font-size: 14px;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-card {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 16px;
}

.product-info {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.product-image {
  width: 60px;
  height: 60px;
  background: rgba(255,0,255,0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.image-placeholder {
  font-size: 24px;
}

.product-detail {
  flex: 1;
}

.product-name {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 4px;
}

.product-meta {
  font-size: 12px;
  color: #b0b0b0;
  display: block;
  margin-bottom: 8px;
}

.product-prices {
  display: flex;
  gap: 12px;
}

.cost-price {
  font-size: 12px;
  color: #00ff88;
}

.sale-price {
  font-size: 12px;
  color: #ffaa00;
}

.product-stock {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid rgba(255,255,255,0.05);
  padding-top: 12px;
}

.stock-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.stock-badge.normal {
  background: rgba(0,255,136,0.1);
  color: #00ff88;
}

.stock-badge.low {
  background: rgba(255,51,102,0.1);
  color: #ff3366;
}

.product-actions {
  display: flex;
  gap: 16px;
}

.action-edit {
  color: #00ffff;
  font-size: 14px;
}

.action-delete {
  color: #ff3366;
  font-size: 14px;
}

/* 弹窗 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  display: flex;
  align-items: flex-end;
}

.modal-mask {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.7);
}

.modal-content {
  position: relative;
  background: #0d0518;
  border-radius: 24px 24px 0 0;
  padding: 24px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 18px;
  font-weight: bold;
}

.modal-close {
  font-size: 24px;
  color: #b0b0b0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-row {
  display: flex;
  gap: 12px;
}

.form-row .half {
  flex: 1;
}

.label {
  font-size: 14px;
  color: #b0b0b0;
}

.input, .picker {
  background: #1a0b2e;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 12px 16px;
  color: #fff;
  font-size: 14px;
}

.picker {
  line-height: 1.5;
}

.submit-btn {
  margin-top: 20px;
  background: #ff00ff;
  color: #fff;
  padding: 14px;
  border-radius: 12px;
  font-size: 16px;
  border: none;
}
</style>