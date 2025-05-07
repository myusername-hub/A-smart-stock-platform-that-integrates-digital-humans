<template>
  <div class="now-page">
    <div class="header">
      <h2>实时行情</h2>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>

    <div v-if="loading" class="loading">
      数据加载中...
    </div>

    <div v-if="hasErrors" class="stock-table">
      <div class="table-header">
        <div>股票代码</div>
        <div>状态信息</div>
      </div>
      <div v-for="stock in stockData" 
           :key="stock.ts_code" 
           class="stock-row error-row">
        <div class="code">{{ stock.ts_code }}</div>
        <div class="message">{{ stock.message }}</div>
      </div>
    </div>

    <div v-else-if="stockData.length > 0" class="stock-table">
      <div class="table-header">
        <div>股票代码</div>
        <div>收盘价</div>
        <div>涨跌幅(%)</div>
        <div>成交量</div>
        <div>成交额(万)</div>
      </div>

      <div v-for="stock in stockData" 
           :key="stock.ts_code" 
           class="stock-row">
        <div>{{ stock.ts_code }}</div>
        <div>{{ stock.close }}</div>
        <div :class="[stock.pct_chg >= 0 ? 'price-up' : 'price-down']">
          {{ stock.pct_chg?.toFixed(2) }}%
        </div>
        <div>{{ (stock.vol / 1000)?.toFixed(2) }}K</div>
        <div>{{ (stock.amount / 10000)?.toFixed(2) }}</div>
      </div>
    </div>

    <div v-else-if="!loading && !error" class="no-data">
      暂无股票数据
    </div>
  </div>
</template>

<script>
<<<<<<< HEAD
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const stockData = ref([])
    const loading = ref(false)
    const error = ref(null)

    const hasErrors = computed(() => {
      return stockData.value.length > 0 && stockData.value.every(stock => stock.message);
    });

    const fetchStockData = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await axios.get('http://localhost:5000/stock_data')
        console.log('API响应数据:', response.data) // 调试用
        stockData.value = response.data
      } catch (err) {
        console.error('获取数据失败:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchStockData()
      // 每30秒刷新一次数据
      const timer = setInterval(fetchStockData, 30000)
      return () => clearInterval(timer)
    })

    return {
      stockData,
      loading,
      error,
      hasErrors
=======
export default {
  name: 'NowView',
  data() {
    return {
      // 您的数据
>>>>>>> df14a350e61311da1daaed85c387f5a33293a8f8
    }
  }
}
</script>

<style scoped>
<<<<<<< HEAD
.now-page {
  padding: 20px;
  color: #e6f1ff;
}

.header {
  margin-bottom: 20px;
}

.error-message {
  color: #ff4d4f;
  margin-top: 10px;
}

.loading, .no-data {
  text-align: center;
  padding: 20px;
  color: #a8b2d1;
}

.stock-table {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.table-header {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  font-weight: bold;
}

.stock-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  padding: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: background-color 0.3s;
}

.stock-row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.price-up {
  color: #52c41a;
}

.price-down {
  color: #ff4d4f;
}

.error-row {
  grid-template-columns: 1fr 4fr !important;
}

.error-row .code {
  color: #1890ff;
  font-weight: bold;
}

.error-row .message {
  color: #ff4d4f;
  text-align: left;
  padding-left: 20px;
}
=======
.now-container {
  padding: 20px;
}
>>>>>>> df14a350e61311da1daaed85c387f5a33293a8f8
</style>