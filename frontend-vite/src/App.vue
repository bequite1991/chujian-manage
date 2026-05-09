<template>
  <div class="app-layout">
    <nav class="nav-bar">
      <span class="nav-title">🌐 霓虹仓库</span>
      <span class="nav-subtitle">AI 库存管理</span>
    </nav>
    <div class="page-container">
      <router-view />
    </div>
    <div class="tab-bar">
      <router-link
        v-for="tab in tabs"
        :key="tab.path"
        :to="tab.path"
        class="tab-item"
        :class="{ active: $route.path === tab.path }"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-label">{{ tab.label }}</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
const tabs = [
  { path: '/dashboard', icon: '📊', label: '看板' },
  { path: '/products', icon: '📦', label: '商品' },
  { path: '/stock-in', icon: '⬇️', label: '入库' },
  { path: '/stock-out', icon: '⬆️', label: '出库' },
  { path: '/alerts', icon: '⚠️', label: '预警' },
  { path: '/suppliers', icon: '🏢', label: '供应商' },
]
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #1a0b2e;
  color: #fff;
}
.nav-bar {
  background: linear-gradient(135deg, #ff00ff20, #00ffff20);
  border-bottom: 1px solid #ff00ff30;
  padding: 12px 20px;
  display: flex;
  align-items: baseline;
  gap: 10px;
}
.nav-title { font-size: 20px; font-weight: bold; }
.nav-subtitle { font-size: 12px; color: #ff00ff; }
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
  z-index: 100;
}
.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  opacity: 0.6;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
}
.tab-item.active { opacity: 1; }
.tab-item.active .tab-label { color: #ff00ff; text-shadow: 0 0 10px #ff00ff50; }
.tab-icon { font-size: 24px; }
.tab-label { font-size: 11px; color: #b0b0b0; }
</style>
