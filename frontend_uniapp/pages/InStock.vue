<template>
  <view class="in-stock">
    <view class="header">
      <text class="title">入库管理</text>
    </view>

    <!-- 语音录入区域 -->
    <view class="voice-section">
      <view 
        class="voice-btn"
        :class="{ recording: isRecording }"
        @click="toggleRecording"
      >
        <text class="voice-icon">{{ isRecording ? '🔴' : '🎤' }}</text>
        <text class="voice-text">{{ isRecording ? '点击结束' : '点击说话' }}</text>
      </view>
      
      <view v-if="isRecording" class="voice-waves">
        <view v-for="i in 5" :key="i" class="wave" :style="{ animationDelay: i * 0.1 + 's' }"></view>
      </view>

      <text class="voice-hint">例如："入库50条钛钢项链，银色，批发价15，售价39"</text>
    </view>

    <!-- 识别结果 -->
    <view v-if="parsedData" class="result-section">
      <view class="result-header">
        <text class="result-title">识别结果</text>
        <text class="result-text">{{ voiceText }}</text>
      </view>

      <view class="form">
        <view class="form-item">
          <text class="label">品名</text>
          <input type="text" v-model="parsedData.name" class="input" />
        </view>
        <view class="form-row">
          <view class="form-item half">
            <text class="label">类别</text>
            <input type="text" v-model="parsedData.category" class="input" />
          </view>
          <view class="form-item half">
            <text class="label">材质</text>
            <input type="text" v-model="parsedData.material" class="input" />
          </view>
        </view>
        <view class="form-row">
          <view class="form-item half">
            <text class="label">数量</text>
            <input type="number" v-model="parsedData.quantity" class="input" />
          </view>
          <view class="form-item half">
            <text class="label">颜色</text>
            <input type="text" v-model="parsedData.color" class="input" />
          </view>
        </view>
        <view class="form-row">
          <view class="form-item half">
            <text class="label">进价</text>
            <input type="digit" v-model="parsedData.cost_price" class="input" />
          </view>
          <view class="form-item half">
            <text class="label">售价</text>
            <input type="digit" v-model="parsedData.sale_price" class="input" />
          </view>
        </view>
      </view>

      <view class="actions">
        <button class="btn-secondary" @click="reset">重新识别</button>
        <button class="btn-primary" @click="confirmIn">确认入库</button>
      </view>
    </view>

    <!-- 最近入库记录 -->
    <view class="records-section">
      <text class="section-title">最近入库</text>
      <view class="record-list">
        <view v-for="record in recentRecords" :key="record.id" class="record-item">
          <view class="record-icon">📦</view>
          <view class="record-info">
            <text class="record-product">{{ record.product }}</text>
            <text class="record-meta">{{ record.time }} · {{ record.operator }}</text>
          </view>
          <text class="record-quantity">+{{ record.quantity }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      isRecording: false,
      voiceText: '',
      parsedData: null,
      recentRecords: [
        { id: 1, product: '钛钢项链', quantity: 50, time: '2026-05-08 14:30', operator: '店主' },
        { id: 2, product: '水晶耳环', quantity: 30, time: '2026-05-08 11:20', operator: '店员' },
        { id: 3, product: '珍珠手链', quantity: 20, time: '2026-05-07 16:45', operator: '店主' },
      ]
    }
  },
  methods: {
    toggleRecording() {
      if (this.isRecording) {
        // 停止录音，模拟识别结果
        this.isRecording = false
        this.voiceText = '入库50条钛钢项链，银色，批发价15，售价39'
        this.parsedData = {
          name: '钛钢项链',
          category: '项链',
          material: '钛钢',
          color: '银色',
          quantity: 50,
          cost_price: 15,
          sale_price: 39
        }
      } else {
        // 开始录音
        this.isRecording = true
        this.voiceText = ''
        this.parsedData = null
        
        // 模拟5秒后自动停止
        setTimeout(() => {
          if (this.isRecording) {
            this.toggleRecording()
          }
        }, 5000)
      }
    },
    reset() {
      this.voiceText = ''
      this.parsedData = null
    },
    confirmIn() {
      uni.showToast({ title: '入库成功', icon: 'success' })
      this.recentRecords.unshift({
        id: Date.now(),
        product: this.parsedData.name,
        quantity: this.parsedData.quantity,
        time: new Date().toLocaleString('zh-CN'),
        operator: '店主'
      })
      this.reset()
    }
  }
}
</script>

<style scoped>
.in-stock {
  padding: 16px;
}

.header {
  margin-bottom: 20px;
}

.title {
  font-size: 20px;
  font-weight: bold;
}

/* 语音区域 */
.voice-section {
  background: linear-gradient(135deg, rgba(255,0,255,0.1), rgba(0,255,255,0.1));
  border: 1px solid rgba(255,0,255,0.2);
  border-radius: 20px;
  padding: 30px 20px;
  text-align: center;
  margin-bottom: 20px;
}

.voice-btn {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff00ff, #00ffff);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 0 30px rgba(255,0,255,0.3);
}

.voice-btn.recording {
  background: linear-gradient(135deg, #ff3366, #ff00ff);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.voice-icon {
  font-size: 36px;
}

.voice-text {
  font-size: 12px;
  color: #fff;
  margin-top: 4px;
}

.voice-waves {
  display: flex;
  justify-content: center;
  gap: 4px;
  margin-bottom: 12px;
}

.wave {
  width: 4px;
  height: 20px;
  background: #ff00ff;
  border-radius: 2px;
  animation: wave 1s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% { transform: scaleY(0.5); }
  50% { transform: scaleY(1); }
}

.voice-hint {
  font-size: 12px;
  color: #b0b0b0;
}

/* 识别结果 */
.result-section {
  background: #0d0518;
  border: 1px solid rgba(255,0,255,0.2);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.result-header {
  margin-bottom: 16px;
}

.result-title {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 8px;
}

.result-text {
  font-size: 14px;
  color: #b0b0b0;
  background: #1a0b2e;
  padding: 12px;
  border-radius: 8px;
  display: block;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-row {
  display: flex;
  gap: 12px;
}

.form-row .half {
  flex: 1;
}

.label {
  font-size: 13px;
  color: #b0b0b0;
}

.input {
  background: #1a0b2e;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 10px 14px;
  color: #fff;
  font-size: 14px;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.btn-secondary {
  flex: 1;
  background: rgba(255,255,255,0.1);
  color: #b0b0b0;
  padding: 12px;
  border-radius: 10px;
  border: none;
  font-size: 14px;
}

.btn-primary {
  flex: 2;
  background: #00ff88;
  color: #000;
  padding: 12px;
  border-radius: 10px;
  border: none;
  font-size: 14px;
  font-weight: bold;
}

/* 记录列表 */
.records-section {
  background: #0d0518;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 16px;
}

.record-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #1a0b2e;
  border-radius: 12px;
}

.record-icon {
  font-size: 24px;
}

.record-info {
  flex: 1;
}

.record-product {
  font-size: 14px;
  font-weight: bold;
  display: block;
}

.record-meta {
  font-size: 12px;
  color: #b0b0b0;
}

.record-quantity {
  font-size: 16px;
  font-weight: bold;
  color: #00ff88;
}
</style>