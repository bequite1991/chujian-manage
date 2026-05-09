<template>
  <view class="alerts">
    <view class="header">
      <text class="title">库存预警</text>
      <text class="read-all" @click="markAllRead">全部已读</text>
    </view>

    <!-- 统计卡片 -->
    <view class="stats-row">
      <view class="stat-card red">
        <text class="stat-num">2</text>
        <text class="stat-label">库存不足</text>
      </view>
      <view class="stat-card orange">
        <text class="stat-num">1</text>
        <text class="stat-label">滞销预警</text>
      </view>
      <view class="stat-card blue">
        <text class="stat-num">1</text>
        <text class="stat-label">临期提醒</text>
      </view>
    </view>

    <!-- 预警列表 -->
    <view class="alert-list">
      <view 
        v-for="alert in alerts" 
        :key="alert.id"
        class="alert-card"
        :class="alert.severity"
      >
        <view class="alert-header">
          <view class="alert-dot" :class="alert.severity"></view>
          <text class="alert-type">{{ getTypeLabel(alert.type) }}</text>
        </view>
        <view class="alert-body">
          <text class="alert-product">{{ alert.product }}</text>
          <text class="alert-message">{{ alert.message }}</text>
        </view>
        <button class="alert-action" @click="handleAlert(alert)">处理</button>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      alerts: [
        { id: 1, product: '钛钢项链', type: 'stock_low', message: '仅剩 5 条，建议补货', severity: 'high' },
        { id: 2, product: '银色耳环', type: 'stock_low', message: '仅剩 2 对，建议补货', severity: 'high' },
        { id: 3, product: '合金手链', type: 'slow_selling', message: '30 天无销售，建议促销', severity: 'medium' },
        { id: 4, product: '珍珠项链', type: 'expired', message: '库存超过 90 天，建议检查', severity: 'low' },
      ]
    }
  },
  methods: {
    getTypeLabel(type) {
      const labels = {
        stock_low: '库存不足',
        slow_selling: '滞销预警',
        expired: '临期提醒'
      }
      return labels[type] || type
    },
    markAllRead() {
      uni.showToast({ title: '已全部标记已读', icon: 'success' })
    },
    handleAlert(alert) {
      uni.showModal({
        title: alert.product,
        content: alert.message,
        confirmText: '去处理',
        success: (res) => {
          if (res.confirm) {
            uni.showToast({ title: '已处理', icon: 'success' })
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.alerts {
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

.read-all {
  font-size: 14px;
  color: #00ff88;
}

/* 统计卡片 */
.stats-row {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.stat-card {
  flex: 1;
  padding: 16px;
  border-radius: 16px;
  text-align: center;
}

.stat-card.red {
  background: rgba(255,51,102,0.1);
  border: 1px solid rgba(255,51,102,0.3);
}

.stat-card.orange {
  background: rgba(255,170,0,0.1);
  border: 1px solid rgba(255,170,0,0.3);
}

.stat-card.blue {
  background: rgba(0,255,255,0.1);
  border: 1px solid rgba(0,255,255,0.3);
}

.stat-num {
  font-size: 28px;
  font-weight: bold;
  display: block;
}

.stat-card.red .stat-num { color: #ff3366; }
.stat-card.orange .stat-num { color: #ffaa00; }
.stat-card.blue .stat-num { color: #00ffff; }

.stat-label {
  font-size: 12px;
  color: #b0b0b0;
  margin-top: 4px;
  display: block;
}

/* 预警列表 */
.alert-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-card {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 16px;
}

.alert-card.high {
  border-color: rgba(255,51,102,0.3);
  background: rgba(255,51,102,0.05);
}

.alert-card.medium {
  border-color: rgba(255,170,0,0.3);
  background: rgba(255,170,0,0.05);
}

.alert-card.low {
  border-color: rgba(0,255,255,0.3);
  background: rgba(0,255,255,0.05);
}

.alert-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.alert-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.alert-dot.high { background: #ff3366; }
.alert-dot.medium { background: #ffaa00; }
.alert-dot.low { background: #00ffff; }

.alert-type {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 20px;
  background: rgba(255,255,255,0.1);
}

.alert-body {
  margin-bottom: 12px;
}

.alert-product {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 4px;
}

.alert-message {
  font-size: 13px;
  color: #b0b0b0;
}

.alert-action {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  background: rgba(255,255,255,0.1);
  color: #fff;
  border: none;
  font-size: 14px;
}
</style>
