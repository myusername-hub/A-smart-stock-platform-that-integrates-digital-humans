<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { stockNameMap } from '@/utils/stockMap'
import { fetchWithRetry } from '@/utils/api'
import axios from 'axios'

const router = useRouter()
const stockList = ref([])
const stockData = ref([])
const loading = ref(false)
const error = ref(null)
const collectedStocks = ref([])

// 数据处理函数
const processStockData = (data) => {
  if (!Array.isArray(data)) return []
  
  return data.map(stock => {
    const stockCode = stock.code
    const stockInfo = stock.daily_data?.[0] || {}
    
    // 涨跌幅计算，使用原始数据中的pct_change字段
    const price = parseFloat(stockInfo.close || 0)
    const change = parseFloat(stockInfo.change || 0)
    const changeRate = parseFloat(stockInfo.pct_change || 0) // 直接使用pct_change字段

    return {
      code: stockCode,
      name: stockNameMap[stockCode] || '未知',
      price: price.toFixed(2),
      change: change.toFixed(2),
      changeRate: changeRate.toFixed(2), // 使用原始涨跌幅数据
      open: parseFloat(stockInfo.open || 0).toFixed(2),
      high: parseFloat(stockInfo.high || 0).toFixed(2),
      low: parseFloat(stockInfo.low || 0).toFixed(2),
      volume: `${(parseFloat(stockInfo.vol || 0) / 10000).toFixed(2)}`,
      amount: `${(parseFloat(stockInfo.amount || 0) / 100000000).toFixed(2)}`,
      amplitude: ((parseFloat(stockInfo.high || 0) - parseFloat(stockInfo.low || 0)) / price * 100).toFixed(2)
    }
  })
}

// 获取股票数据
const fetchStockData = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await fetchWithRetry('/api/stock_daily_data')
    console.log('原始数据:', response.data)
    
    if (response?.data?.status === 'success' && Array.isArray(response.data.data)) {
      const validData = response.data.data.filter(item => item.daily_data?.length > 0)
      stockList.value = processStockData(validData)
      console.log('处理后数据:', stockList.value)
    } else {
      throw new Error('数据格式不正确')
    }
  } catch (err) {
    console.error('数据获取失败:', err)
    error.value = '无法获取历史数据，请确保后端服务正常运行'
    stockList.value = []
  } finally {
    loading.value = false
  }
}

// 跳转到详情页
const goToDetail = (code) => {
  const currentStock = stockList.value.find(item => item.code === code)
  localStorage.setItem('currentStock', JSON.stringify(currentStock))
  router.push({
    name: 'StockDetail',
    params: { code }
  })
}

// 处理收藏
const handleCollect = (event, code) => {
  event.stopPropagation()
  const index = collectedStocks.value.indexOf(code)
  if (index > -1) {
    collectedStocks.value.splice(index, 1)
  } else {
    collectedStocks.value.push(code)
  }
  // 保存到本地存储
  localStorage.setItem('collectedStocks', JSON.stringify(collectedStocks.value))
}

// 检查是否收藏
const isCollected = (code) => {
  return collectedStocks.value.includes(code)
}

// 初始化时加载本地存储的收藏数据
onMounted(() => {
  const savedCollections = localStorage.getItem('collectedStocks')
  if (savedCollections) {
    collectedStocks.value = JSON.parse(savedCollections)
  }
  fetchStockData()
  // 每分钟更新一次数据
  const timer = setInterval(fetchStockData, 60000)
  return () => clearInterval(timer)
})
</script>

<template>
  <div class="recommend-container">
    <h2 class="title">今日推荐股票</h2>

    <!-- 错误提示 -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- 加载提示 -->
    <div v-if="loading" class="loading-message">
      数据加载中...
    </div>

    <!-- 数据展示 -->
    <table v-if="!loading && !error && stockList.length" class="stock-table">
      <thead>
        <tr>
          <th>股票代码</th>
          <th>股票名称</th>
          <th>最新价</th>
          <th>涨跌额</th>
          <th>涨跌幅</th>
          <th>开盘价</th>
          <th>最高价</th>
          <th>最低价</th>
          <th>成交量（万手）</th>
          <th>成交额（亿元）</th>
          <th>振幅</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in stockList" 
            :key="stock.code"
            @click="goToDetail(stock.code)"
            class="stock-row">
          <td>{{ stock.code }}</td>
          <td>{{ stock.name }}</td>
          <td :class="{ 
            'red': parseFloat(stock.change) > 0, 
            'green': parseFloat(stock.change) < 0 
          }">{{ stock.price }}</td>
          <td :class="{ 
            'red': parseFloat(stock.change) > 0, 
            'green': parseFloat(stock.change) < 0 
          }">{{ stock.change }}</td>
          <td :class="{ 
            'red': parseFloat(stock.changeRate) > 0, 
            'green': parseFloat(stock.changeRate) < 0 
          }">{{ stock.changeRate }}%</td>
          <td>{{ stock.open }}</td>
          <td>{{ stock.high }}</td>
          <td>{{ stock.low }}</td>
          <td>{{ stock.volume }}</td>
          <td>{{ stock.amount }}</td>
          <td>{{ stock.amplitude }}%</td>
          <td>
            <button class="detail-btn">查看详情</button>
            <button 
              class="collect-btn"
              @click="handleCollect($event, stock.code)"
              :class="{ 'collected': isCollected(stock.code) }"
            >
              {{ isCollected(stock.code) ? '取消收藏' : '收藏' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 无数据提示 -->
    <div v-if="!loading && !error && !stockList.length" class="empty-message">
      暂无股票数据
    </div>
  </div>
</template>

<style scoped>
.recommend-container {
  padding: 20px;
}

.title {
  margin-bottom: 20px;
  color: #303133;
  text-align: center;
}

.stock-table {
  width: 100%;
  table-layout: fixed; /* 添加固定布局 */
  border-collapse: collapse;
  text-align: center;
}

.stock-table th,
.stock-table td {
  padding: 12px 8px;
  border: 1px solid #ebeef5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 设置各列宽度 */
.stock-table th:nth-child(1),
.stock-table td:nth-child(1) { width: 8%; }  /* 股票代码 */

.stock-table th:nth-child(2),
.stock-table td:nth-child(2) { width: 8%; }  /* 股票名称 */

.stock-table th:nth-child(3),
.stock-table td:nth-child(3) { width: 7%; }  /* 最新价 */

.stock-table th:nth-child(4),
.stock-table td:nth-child(4) { width: 7%; }  /* 涨跌额 */

.stock-table th:nth-child(5),
.stock-table td:nth-child(5) { width: 7%; }  /* 涨跌幅 */

.stock-table th:nth-child(6),
.stock-table td:nth-child(6) { width: 7%; }  /* 开盘价 */

.stock-table th:nth-child(7),
.stock-table td:nth-child(7) { width: 7%; }  /* 最高价 */

.stock-table th:nth-child(8),
.stock-table td:nth-child(8) { width: 7%; }  /* 最低价 */

.stock-table th:nth-child(9),
.stock-table td:nth-child(9) { width: 10%; } /* 成交量 */

.stock-table th:nth-child(10),
.stock-table td:nth-child(10) { width: 10%; } /* 成交额 */

.stock-table th:nth-child(11),
.stock-table td:nth-child(11) { width: 7%; } /* 振幅 */

.stock-table th:nth-child(12),
.stock-table td:nth-child(12) { 
  width: 15%;
  white-space: nowrap;  /* 添加这行确保按钮不会换行 */
  padding: 4px;  /* 调整padding让按钮有足够空间 */
}

.red {
  color: #f56c6c;
}

.green {
  color: #67c23a;
}

.detail-btn,
.collect-btn {
  display: inline-block;
  padding: 4px 8px;  /* 减小padding */
  min-width: 60px;   /* 减小最小宽度 */
  font-size: 13px;   /* 稍微减小字体 */
  margin: 0 2px;     /* 减小间距 */
  border-radius: 4px;
  border: none;
  cursor: pointer;
  line-height: 1.5;
  text-align: center;
  transition: all 0.3s;
}

.detail-btn {
  background-color: #409eff;
  color: white;
}

.collect-btn {
  background-color: #f56c6c;
  color: white;
  transition: all 0.3s;
}

.collect-btn:hover {
  background-color: #ff7875;
}

.collect-btn.collected {
  background-color: #909399;
  opacity: 0.8;
}

.stock-row {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.stock-row:hover {
  background-color: #f5f7fa;
}

.error-message {
  color: #f56c6c;
  text-align: center;
  padding: 20px;
  background-color: #fef0f0;
  border-radius: 4px;
  margin-bottom: 20px;
}

.loading-message,
.empty-message {
  text-align: center;
  padding: 40px;
  color: #909399;
  font-size: 14px;
}
</style>