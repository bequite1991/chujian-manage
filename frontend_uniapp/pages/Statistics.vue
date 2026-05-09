<template>
  <view class="statistics">
    <view class="header">
      <text class="title">销售统计</text>
      <view class="period-tabs">
        <text 
          v-for="p in periods" 
          :key="p.value"
          class="tab"
          :class="{ active: period === p.value }"
          @click="period = p.value"
        >{{ p.label }}</text>
      </view>
    </view>

    <!-- 统计卡片 -->
    <view class="stats-grid">
      <view class="stat-card pink">
        <text class="stat-icon">💰</text>
        <text class="stat-label">本周销售额</text>
        <text class="stat-value">¥18,500</text>
        <text class="stat-change up">↑15%</text>
      </view>
      <view class="stat-card blue">
        <text class="stat-icon">📦</text>
        <text class="stat-label">本周订单</text>
        <text class="stat-value">208单</text>
        <text class="stat-change up">↑8%</text>
      </view>
      <view class="stat-card green">
        <text class="stat-icon">📊</text>
        <text class="stat-label">客单价</text>
        <text class="stat-value">¥89</text>
        <text class="stat-change up">↑5%</text>
      </view>
      <view class="stat-card orange">
        <text class="stat-icon">↩️</text>
        <text class="stat-label">退货率</text>
        <text class="stat-value">2.3%</text>
        <text class="stat-change down">↓0.5%</text>
      </view>
    </view>

    <!-- 销售趋势 -->
    <view class="chart-section">
      <text class="section-title">销售趋势</text>
      <view class="chart-placeholder">
        <text class="chart-text">📈 柱状图区域</text>
        <text class="chart-sub">周一 ¥1200 | 周二 ¥1800 | 周三 ¥2400 | 周四 ¥1600 | 周五 ¥3200 | 周六 ¥4500 | 周日 ¥3800</text>
      </view>
    </view>

    <!-- 热销排行 -->
    <view class="rank-section">
      <text class="section-title">🔥 热销排行</text>
      <view class="rank-list">
        <view v-for="(item, index) in topProducts" :key="index" class="rank-item">
          <text class="rank-num" :class="getRankClass(index)">{{ index + 1 }}</text>
          <view class="rank-info">
            <text class="rank-name">{{ item.name }}</text>
            <text class="rank-sales">销量 {{ item.sales }}</text>
          </view>
          <text class="rank-revenue">¥{{ item.revenue }}</text>
        </view>
      </view>
    </view>

    <!-- 滞销商品 -->
    <view class="rank-section">
      <text class="section-title">⚠️ 滞销商品</text>
      <view class="rank-list">
        <view v-for="(item, index) in slowProducts" :key="index" class="rank-item slow">
          <text class="rank-num gray">{{ index + 1 }}</text>
          <view class="rank-info">
            <text class="rank-name">{{ item.name }}</text>
            <text class="rank-sales">库存 {{ item.stock }}</text>
          </view>
          <text class="rank-days">{{ item.days }}天无销售</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      period: 'week',
      periods: [
        { label: '本周', value: 'week' },
        { label: '本月', value: 'month' },
        { label: '本年', value: 'year' }
      ],
      topProducts: [
        { name: '钛钢项链', sales: 156, revenue: 6084 },
        { name: '水晶耳环', sales: 132, revenue: 3300 },
        { name: '珍珠手链', sales: 98, revenue: 6664 },
        { name: '银戒指', sales: 87, revenue: 4350 },
        { name: '发夹套装', sales: 76, revenue: 1900 }
      ],
      slowProducts: [
        { name: '合金手链', days: 30, stock: 45 },
        { name: '古铜项链', days: 25, stock: 32 },
        { name: '塑料耳环', days: 22, stock: 67 }
      ]
    }
  },
  methods: {
    getRankClass(index) {
      if (index === 0) return 'gold'
      if (index === 1) return 'silver'
      if (index === 2) return 'bronze'
      return 'gray'
    }
  }
}
</script>

<style scoped>
.statistics {
  padding: 16px;
}

.header {
  margin-bottom: 20px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  display: block;
  margin-bottom: 12px;
}

.period-tabs {
  display: flex;
  gap: 8px;
}

.tab {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  background: rgba(255,255,255,0.1);
  color: #b0b0b0;
}

.tab.active {
  background: #ff00ff;
  color: #fff;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.stat-card {
  padding: 16px;
  border-radius: 16px;
}

.stat-card.pink {
  background: linear-gradient(135deg, rgba(255,0,255,0.15), rgba(255,0,255,0.05));
  border: 1px solid rgba(255,0,255,0.3);
}

.stat-card.blue {
  background: linear-gradient(135deg, rgba(0,255,255,0.15), rgba(0,255,255,0.05));
  border: 1px solid rgba(0,255,255,0.3);
}

.stat-card.green {
  background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,255,136,0.05));
  border: 1px solid rgba(0,255,136,0.3);
}

.stat-card.orange {
  background: linear-gradient(135deg, rgba(255,170,0,0.15), rgba(255,170,0,0.05));
  border: 1px solid rgba(255,170,0,0.3);
}

.stat-icon {
  font-size: 24px;
  display: block;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 12px;
  color: #b0b0b0;
  display: block;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  display: block;
  margin: 4px 0;
}

.stat-change {
  font-size: 12px;
}

.stat-change.up {
  color: #00ff88;
}

.stat-change.down {
  color: #ff3366;
}

/* 图表区域 */
.chart-section {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 16px;
}

.chart-placeholder {
  background: #1a0b2e;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
}

.chart-text {
  font-size: 18px;
  display: block;
  margin-bottom: 12px;
}

.chart-sub {
  font-size: 12px;
  color: #b0b0b0;
  line-height: 1.8;
}

/* 排行 */
.rank-section {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.rank-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rank-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #1a0b2e;
  border-radius: 12px;
}

.rank-item.slow {
  background: rgba(255,170,0,0.05);
}

.rank-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  flex-shrink: 0;
}

.rank-num.gold {
  background: #ffaa00;
  color: #000;
}

.rank-num.silver {
  background: #c0c0c0;
  color: #000;
}

.rank-num.bronze {
  background: #cd7f32;
  color: #000;
}

.rank-num.gray {
  background: rgba(255,255,255,0.1);
  color: #b0b0b0;
}

.rank-info {
  flex: 1;
}

.rank-name {
  font-size: 14px;
  font-weight: bold;
  display: block;
}

.rank-sales {
  font-size: 12px;
  color: #b0b0b0;
}

.rank-revenue {
  font-size: 14px;
  color: #ffaa00;
  font-weight: bold;
}

.rank-days {
  font-size: 12px;
  color: #ff3366;
}
</style>