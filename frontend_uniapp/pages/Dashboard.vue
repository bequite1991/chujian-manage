<template>
  <view class="dashboard">
    <!-- 今日数据卡片 -->
    <view class="stats-grid">
      <view class="stat-card pink">
        <text class="stat-label">今日销售额</text>
        <text class="stat-value">¥{{ todaySales }}</text>
        <text class="stat-change up">↑12%</text>
      </view>
      <view class="stat-card blue">
        <text class="stat-label">今日订单</text>
        <text class="stat-value">{{ todayOrders }}单</text>
        <text class="stat-change up">↑5%</text>
      </view>
      <view class="stat-card orange">
        <text class="stat-label">今日出库</text>
        <text class="stat-value">{{ todayOut }}件</text>
        <text class="stat-change up">↑8%</text>
      </view>
    </view>

    <!-- 库存预警 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">⚠️ 库存预警</text>
        <text class="section-count">({{ alerts.length }}条)</text>
      </view>
      <view class="alert-list">
        <view 
          v-for="alert in alerts" 
          :key="alert.id"
          class="alert-item"
          :class="alert.type"
        >
          <view class="alert-dot"></view>
          <view class="alert-content">
            <text class="alert-product">{{ alert.product }}</text>
            <text class="alert-info">{{ alert.message }}</text>
          </view>
          <button class="alert-btn" :class="alert.type">
            {{ alert.type === 'stock_low' ? '补货' : '促销' }}
          </button>
        </view>
      </view>
    </view>

    <!-- AI 补货建议 -->
    <view class="section ai-section">
      <view class="section-header">
        <text class="section-title">🤖 AI 补货建议</text>
      </view>
      <view class="ai-card">
        <text class="ai-text">
          <text class="highlight pink">{{ aiSuggestion.product }}</text>：
          近7天日均销售 <text class="highlight blue">{{ aiSuggestion.dailyAvg }}</text> 条，
          当前库存 <text class="highlight orange">{{ aiSuggestion.currentStock }}</text> 条，
          建议补货 <text class="highlight green">{{ aiSuggestion.suggest }}</text> 条
        </text>
      </view>
    </view>

    <!-- 快捷操作 -->
    <view class="quick-actions">
      <button class="action-btn pink" @click="voiceIn">
        <text class="action-icon">🎤</text>
        <text class="action-label">语音入库</text>
      </button>
      <button class="action-btn blue" @click="photoMatch">
        <text class="action-icon">📷</text>
        <text class="action-label">拍照匹配</text>
      </button>
      <button class="action-btn green" @click="goStats">
        <text class="action-icon">📊</text>
        <text class="action-label">销售统计</text>
      </button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      todaySales: 12480,
      todayOrders: 45,
      todayOut: 128,
      alerts: [
        { id: 1, product: '钛钢项链', type: 'stock_low', message: '仅剩 5 条，建议补货' },
        { id: 2, product: '银色耳环', type: 'stock_low', message: '仅剩 2 对，建议补货' },
        { id: 3, product: '合金手链', type: 'slow_selling', message: '30天无销售，建议促销' },
      ],
      aiSuggestion: {
        product: '钛钢手链',
        dailyAvg: 4,
        currentStock: 23,
        suggest: 30
      }
    }
  },
  methods: {
    voiceIn() {
      uni.navigateTo({ url: '/pages/InStock' })
    },
    photoMatch() {
      uni.showToast({ title: '拍照功能开发中', icon: 'none' })
    },
    goStats() {
      uni.navigateTo({ url: '/pages/Statistics' })
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 16px;
}

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

.stat-label {
  font-size: 12px;
  color: #b0b0b0;
  display: block;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
  display: block;
  margin: 8px 0;
}

.stat-change {
  font-size: 12px;
}

.stat-change.up {
  color: #00ff88;
}

.section {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
}

.section-count {
  font-size: 14px;
  color: #ff00ff;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-radius: 12px;
  background: rgba(255,51,102,0.1);
  border: 1px solid rgba(255,51,102,0.3);
}

.alert-item.slow_selling {
  background: rgba(255,170,0,0.1);
  border-color: rgba(255,170,0,0.3);
}

.alert-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff3366;
  flex-shrink: 0;
}

.alert-item.slow_selling .alert-dot {
  background: #ffaa00;
}

.alert-content {
  flex: 1;
}

.alert-product {
  font-size: 14px;
  font-weight: bold;
  display: block;
}

.alert-info {
  font-size: 12px;
  color: #b0b0b0;
}

.alert-btn {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  border: none;
}

.alert-btn.stock_low {
  background: rgba(255,51,102,0.2);
  color: #ff3366;
}

.alert-btn.slow_selling {
  background: rgba(255,170,0,0.2);
  color: #ffaa00;
}

.ai-section {
  background: linear-gradient(135deg, rgba(255,0,255,0.1), rgba(0,255,255,0.1));
}

.ai-card {
  background: #0d0518;
  border-radius: 12px;
  padding: 16px;
}

.ai-text {
  font-size: 14px;
  line-height: 1.6;
  color: #ccc;
}

.highlight {
  font-weight: bold;
}

.highlight.pink { color: #ff00ff; }
.highlight.blue { color: #00ffff; }
.highlight.orange { color: #ffaa00; }
.highlight.green { color: #00ff88; }

.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
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
}

.action-btn.blue {
  background: linear-gradient(135deg, rgba(0,255,255,0.15), rgba(0,255,255,0.05));
  border-color: rgba(0,255,255,0.3);
}

.action-btn.green {
  background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,255,136,0.05));
  border-color: rgba(0,255,136,0.3);
}

.action-icon {
  font-size: 32px;
}

.action-label {
  font-size: 14px;
  color: #fff;
}
</style>