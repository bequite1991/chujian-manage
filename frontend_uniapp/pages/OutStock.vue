<template>
  <view class="out-stock">
    <view class="header">
      <text class="title">出库管理</text>
      <button class="scan-btn" @click="toggleScan">{{ scanMode ? '退出' : '扫码' }}</button>
    </view>

    <!-- 扫码区域 -->
    <view v-if="scanMode" class="scan-section">
      <view class="scan-frame">
        <view class="scan-line"></view>
        <text class="scan-text">对准商品条码</text>
      </view>
    </view>

    <!-- 商品选择 -->
    <view class="products-section">
      <text class="section-title">选择商品</text>
      <view class="product-grid">
        <view 
          v-for="item in products" 
          :key="item.id"
          class="product-item"
          @click="addToCart(item)"
        >
          <view class="product-image">📷</view>
          <text class="product-name">{{ item.name }}</text>
          <text class="product-price">¥{{ item.sale_price }}</text>
          <text class="product-stock">库存 {{ item.stock }}</text>
        </view>
      </view>
    </view>

    <!-- 购物车 -->
    <view v-if="cart.length > 0" class="cart-section">
      <view class="cart-header">
        <text class="cart-title">出库清单 ({{ cart.length }})</text>
        <text class="cart-total">¥{{ cartTotal }}</text>
      </view>
      <view class="cart-list">
        <view v-for="(item, index) in cart" :key="index" class="cart-item">
          <view class="cart-info">
            <text class="cart-name">{{ item.name }}</text>
            <text class="cart-price">¥{{ item.sale_price }}</text>
          </view>
          <view class="cart-quantity">
            <button class="qty-btn" @click="changeQty(index, -1)">-</button>
            <text class="qty-value">{{ item.quantity }}</text>
            <button class="qty-btn" @click="changeQty(index, 1)">+</button>
            <text class="remove-btn" @click="removeFromCart(index)">×</text>
          </view>
        </view>
      </view>
      <button class="checkout-btn" @click="checkout">确认出库</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      scanMode: false,
      products: [
        { id: 1, name: '钛钢项链', stock: 45, sale_price: 39 },
        { id: 2, name: '水晶耳环', stock: 23, sale_price: 25 },
        { id: 3, name: '珍珠手链', stock: 12, sale_price: 68 },
        { id: 4, name: '银戒指', stock: 8, sale_price: 55 },
        { id: 5, name: '发夹套装', stock: 34, sale_price: 15 },
        { id: 6, name: '合金手链', stock: 56, sale_price: 29 },
      ],
      cart: []
    }
  },
  computed: {
    cartTotal() {
      return this.cart.reduce((sum, item) => sum + item.sale_price * item.quantity, 0)
    }
  },
  methods: {
    toggleScan() {
      this.scanMode = !this.scanMode
      if (this.scanMode) {
        uni.showToast({ title: '扫码功能开发中', icon: 'none' })
      }
    },
    addToCart(product) {
      const existing = this.cart.find(item => item.id === product.id)
      if (existing) {
        if (existing.quantity < product.stock) {
          existing.quantity++
        } else {
          uni.showToast({ title: '库存不足', icon: 'none' })
        }
      } else {
        this.cart.push({ ...product, quantity: 1 })
      }
    },
    changeQty(index, delta) {
      const item = this.cart[index]
      const newQty = item.quantity + delta
      if (newQty > 0 && newQty <= item.stock) {
        item.quantity = newQty
      }
    },
    removeFromCart(index) {
      this.cart.splice(index, 1)
    },
    checkout() {
      uni.showModal({
        title: '确认出库',
        content: `总计 ¥${this.cartTotal}，确认出库？`,
        success: (res) => {
          if (res.confirm) {
            uni.showToast({ title: '出库成功', icon: 'success' })
            this.cart = []
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.out-stock {
  padding: 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  font-size: 20px;
  font-weight: bold;
}

.scan-btn {
  background: #00ffff;
  color: #000;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  border: none;
  font-weight: bold;
}

/* 扫码区域 */
.scan-section {
  background: #0d0518;
  border: 2px dashed #00ffff;
  border-radius: 16px;
  padding: 40px 20px;
  text-align: center;
  margin-bottom: 20px;
}

.scan-frame {
  width: 200px;
  height: 200px;
  border: 2px solid #00ffff;
  border-radius: 12px;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #00ffff;
  box-shadow: 0 0 10px #00ffff;
  animation: scan 2s linear infinite;
}

@keyframes scan {
  0% { top: 0; }
  100% { top: 100%; }
}

.scan-text {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  color: #00ffff;
  font-size: 14px;
}

/* 商品网格 */
.products-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 12px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.product-item {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 16px 12px;
  text-align: center;
}

.product-image {
  width: 50px;
  height: 50px;
  background: rgba(255,0,255,0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 8px;
  font-size: 24px;
}

.product-name {
  font-size: 13px;
  font-weight: bold;
  display: block;
  margin-bottom: 4px;
}

.product-price {
  font-size: 14px;
  color: #ffaa00;
  font-weight: bold;
  display: block;
}

.product-stock {
  font-size: 11px;
  color: #b0b0b0;
}

/* 购物车 */
.cart-section {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 20px;
  position: fixed;
  bottom: 80px;
  left: 16px;
  right: 16px;
  max-height: 50vh;
  overflow-y: auto;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 12px;
}

.cart-title {
  font-size: 16px;
  font-weight: bold;
}

.cart-total {
  font-size: 20px;
  font-weight: bold;
  color: #ffaa00;
}

.cart-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #1a0b2e;
  border-radius: 10px;
}

.cart-info {
  flex: 1;
}

.cart-name {
  font-size: 14px;
  display: block;
}

.cart-price {
  font-size: 12px;
  color: #ffaa00;
}

.cart-quantity {
  display: flex;
  align-items: center;
  gap: 8px;
}

.qty-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  color: #fff;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.qty-value {
  width: 30px;
  text-align: center;
  font-size: 14px;
}

.remove-btn {
  color: #ff3366;
  font-size: 20px;
  margin-left: 8px;
}

.checkout-btn {
  width: 100%;
  background: #00ff88;
  color: #000;
  padding: 14px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: bold;
  border: none;
}
</style>