<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { stockNameMap } from '@/utils/stockMap'
import axios from 'axios'

const router = useRouter()
const stockList = ref([])
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')

// 数据处理函数
const processStockData = (data) => {
  if (!Array.isArray(data)) return []
  
  return data.map(stock => {
    // 确保 ts_code 是字符串类型并补全为6位
    const stockCode = String(stock.ts_code).padStart(6, '0')
    const change = parseFloat(stock.change)  // 直接使用原始涨跌额，保留正负号
    
    return {
      code: stockCode,
      name: stockNameMap[stockCode] || '未知',
      price: parseFloat(stock.close).toFixed(2),
      change: change.toFixed(2),  // 保留正负号显示涨跌额
      changeRate: parseFloat(stock.pct_change).toFixed(2),
      open: parseFloat(stock.open).toFixed(2),
      high: parseFloat(stock.high).toFixed(2),
      low: parseFloat(stock.low).toFixed(2),
      volume: `${(parseFloat(stock.vol) / 10000).toFixed(2)}万手`,
      amount: `${(parseFloat(stock.amount) / 100000000).toFixed(2)}亿元`,
      amplitude: parseFloat(stock.amplitude).toFixed(2)
    }
  })
}

// 获取股票数据
const fetchStockData = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await axios.get('http://localhost:5000/api/stock_daily_data')  // 添加/api前缀
    stockList.value = processStockData(response.data)
  } catch (err) {
    console.error('获取数据失败:', err)
    error.value = '获取数据失败，请检查网络连接'
  } finally {
    loading.value = false
  }
}

// 搜索功能
const handleSearch = () => {
  if (!searchQuery.value) {
    fetchStockData()
    return
  }
  const query = searchQuery.value.toUpperCase()
  const filteredList = stockList.value.filter(stock => 
    stock.code.includes(query) || stock.name.includes(query)
  )
  stockList.value = filteredList
}

// 跳转到详情页
const goToDetail = (code) => {
  const currentStock = stockList.value.find(item => item.code === code)
  localStorage.setItem('currentStock', JSON.stringify(currentStock))
  router.push({
    name: 'stock',
    params: { code }
  })
}

onMounted(() => {
  fetchStockData()
  // 每分钟更新一次数据
  const timer = setInterval(fetchStockData, 60000)
  return () => clearInterval(timer)
})
</script>

<template>
  <div class="recommend-container">
    <div class="search-wrapper">
      <div class="search-bar">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="输入股票代码或名称查询" 
          class="search-input"
          @keyup.enter="handleSearch"
        >
        <button class="search-btn" @click="handleSearch">查询</button>
      </div>
      
      <h2 class="title">股票行情</h2>
    </div>

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
          <th>成交量</th>
          <th>成交额</th>
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
            <button class="collect-btn">收藏</button>
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

.search-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  width: 300px;
}

.search-btn {
  padding: 8px 15px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #66b1ff;
}

.title {
  margin-bottom: 20px;
  color: #303133;
  text-align: center;
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

.stock-table th,
.stock-table td {
  padding: 12px 8px;
  border: 1px solid #ebeef5;
}

.stock-table th {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 500;
}

.red {
  color: #f56c6c;
}

.green {
  color: #67c23a;
}

.detail-btn,
.collect-btn {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  margin: 0 4px;
}

.detail-btn {
  background-color: #409eff;
  color: white;
}

.collect-btn {
  background-color: #f56c6c;
  color: white;
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