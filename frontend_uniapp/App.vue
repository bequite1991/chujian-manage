<template>
  <view class="app">
    <!-- 自定义导航栏 -->
    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <text class="nav-title">🌐 霓虹仓库</text>
        <text class="nav-subtitle">AI 库存管理</text>
      </view>
    </view>
    
    <!-- 页面内容 -->
    <view class="page-container">
      <Dashboard v-if="currentPage === 'dashboard'" />
      <Products v-if="currentPage === 'products'" />
      <InStock v-if="currentPage === 'in'" />
      <OutStock v-if="currentPage === 'out'" />
      <Alerts v-if="currentPage === 'alerts'" />
      <Statistics v-if="currentPage === 'stats'" />
    </view>
    
    <!-- 底部导航 -->
    <view class="tab-bar">
      <view 
        v-for="item in tabs" 
        :key="item.page"
        class="tab-item"
        :class="{ active: currentPage === item.page }"
        @click="switchPage(item.page)"
      >
        <text class="tab-icon">{{ item.icon }}</text>
        <text class="tab-label">{{ item.label }}</text>
      </view>
    </view>
  </view>
</template>

<script>
import Dashboard from './pages/Dashboard.vue'
import Products from './pages/Products.vue'
import InStock from './pages/InStock.vue'
import OutStock from './pages/OutStock.vue'
import Alerts from './pages/Alerts.vue'
import Statistics from './pages/Statistics.vue'

export default {
  components: {
    Dashboard, Products, InStock, OutStock, Alerts, Statistics
  },
  data() {
    return {
      statusBarHeight: 0,
      currentPage: 'dashboard',
      tabs: [
        { page: 'dashboard', label: '看板', icon: '📊' },
        { page: 'products', label: '商品', icon: '📦' },
        { page: 'in', label: '入库', icon: '⬇️' },
        { page: 'out', label: '出库', icon: '⬆️' },
        { page: 'alerts', label: '预警', icon: '⚠️' },
      ]
    }
  },
  onLoad() {
    // 获取状态栏高度
    const systemInfo = uni.getSystemInfoSync()
    this.statusBarHeight = systemInfo.statusBarHeight
  },
  methods: {
    switchPage(page) {
      this.currentPage = page
    }
  }
}
</script>

<style>
.app {
  min-height: 100vh;
  background: #1a0b2e;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.nav-bar {
  background: linear-gradient(135deg, #ff00ff20, #00ffff20);
  border-bottom: 1px solid #ff00ff30;
}

.nav-content {
  padding: 12px 20px;
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.nav-title {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
}

.nav-subtitle {
  font-size: 12px;
  color: #ff00ff;
}

.page-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 80px;
}

.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 70px;
  background: #0d0518;
  border-top: 1px solid #ff00ff20;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding-bottom: env(safe-area-inset-bottom);
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  opacity: 0.6;
  transition: all 0.3s;
}

.tab-item.active {
  opacity: 1;
}

.tab-item.active .tab-label {
  color: #ff00ff;
  text-shadow: 0 0 10px #ff00ff50;
}

.tab-icon {
  font-size: 24px;
}

.tab-label {
  font-size: 11px;
  color: #b0b0b0;
}
</style>