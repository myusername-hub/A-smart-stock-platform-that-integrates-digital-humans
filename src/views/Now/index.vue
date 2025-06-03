<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { fetchWithRetry } from '@/utils/api'
import { stockNameMap } from '@/utils/stockMap'

export default {
  setup() {
    const router = useRouter()
    // 初始化为空数组
    const stockData = ref([])
    const loading = ref(false)
    const error = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(5)
    const searchQuery = ref('')

    // 确保数据是数组
    const hasErrors = computed(() => {
      return Array.isArray(stockData.value) && 
             stockData.value.some(stock => stock?.message)
    })

    const validStockData = computed(() => {
      if (!Array.isArray(stockData.value)) return []
      if (!searchQuery.value) return stockData.value.filter(stock => !stock?.message)
      
      const query = searchQuery.value.toLowerCase()
      return stockData.value
        .filter(stock => !stock?.message)
        .filter(stock => 
          stock.code.toLowerCase().includes(query) || 
          stock.name.toLowerCase().includes(query)
        )
    })

    const paginatedStockData = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return validStockData.value.slice(start, end)
    })

    const totalPages = computed(() => {
      return Math.ceil(validStockData.value.length / pageSize.value)
    })

    const getStockName = (code) => {
      return stockNameMap[code] || '未知'
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
      }
    }

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
      }
    }

    const fetchStockData = async () => {
      try {
        loading.value = true
        error.value = null
        // 先请求后端更新数据
        await fetch('http://localhost:5000/update_stock_data', { method: 'POST' })
        // 再拉取最新数据
        console.log('开始获取数据...')
        const response = await fetchWithRetry('/api/stock_data?refresh=1')
        console.log('服务器响应:', response)
        if (response?.data?.status === 'success' && Array.isArray(response.data.data)) {
          stockData.value = response.data.data.map(item => {
            const fullCode = item.code.padStart(6, '0') // 补全股票代码为6位
            return {
              ...item.latest_data,
              code: fullCode,
              ts_code: fullCode,
              name: stockNameMap[fullCode] || '未知'
            }
          })
          console.log('处理后的数据:', stockData.value)
        } else {
          throw new Error(response?.data?.message || '数据格式不正确')
        }
      } catch (err) {
        console.error('数据获取失败:', err)
        error.value = '无法获取数据，请确保后端服务正常运行'
        stockData.value = []
      } finally {
        loading.value = false
      }
    }

    // 清理定时器
    onMounted(() => {
      fetchStockData()
      const timer = setInterval(() => {
        if (!error.value) {  // 只在没有错误时继续请求
          fetchStockData()
        }
      }, 60000)
      
      return () => clearInterval(timer)
    })

    // 添加跳转方法
    const goToStockDetail = (stock) => {
      // 统一字段名和结构
      const code = stock.code
      const name = stock.name
      const stockObj = {
        code,
        name,
        price: Number(stock.close ?? stock.price),
        change: Number(stock.change),
        changeRate: Number(stock.pct_change ?? stock.changeRate),
        preClose: stock.pre_close !== undefined ? Number(stock.pre_close) : '-',
        open: Number(stock.open),
        high: Number(stock.high),
        low: Number(stock.low)
      }
      localStorage.setItem('currentStock', JSON.stringify(stockObj))
      router.push({
        name: 'StockDetail',
        params: { code },
        query: { name }
      })
    }

    return {
      stockData,
      validStockData,
      paginatedStockData,
      loading,
      error,
      hasErrors,
      currentPage,
      totalPages,
      getStockName,
      nextPage,
      prevPage,
      searchQuery, // 保留搜索输入
      fetchStockData, // 暴露刷新方法
      goToStockDetail
    }
  }
}
</script>

<template>
  <div class="now-page">
    <div class="search-wrapper">
      <div class="search-bar">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="输入股票代码或名称实时搜索" 
          class="search-input"
        >
        <button class="search-btn">
          <i class="el-icon-search"></i>
          搜索
        </button>
      </div>
    </div>

    <div class="header">
      <div class="header-placeholder"></div>
      <h2>实时行情</h2>
      <div class="header-right">
        <button class="refresh-btn" @click="fetchStockData" :disabled="loading">
          <i class="el-icon-refresh" :class="{ 'is-loading': loading }"></i>
          <span>刷新</span>
        </button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="loading && !stockData.length" class="loading">
      数据加载中...
    </div>

    <div v-if="hasErrors" class="stock-table error-table">
      <div class="table-header">
        <div>股票代码</div>
        <div>状态信息</div>
      </div>
      <div v-for="stock in stockData.filter(s => s.message)" 
           :key="stock.ts_code" 
           class="stock-row error-row">
        <div class="code">{{ stock.ts_code }}</div>
        <div class="message">{{ stock.message }}</div>
      </div>
    </div>

    <div v-if="validStockData.length > 0" class="stock-table">
      <div class="table-header">
        <div>股票代码</div>
        <div>股票名称</div>
        <div>最新价</div>
        <div>涨跌幅</div>
        <div>开盘价</div>
        <div>最高价</div>
        <div>最低价</div>
        <div>昨收价</div>
      </div>

      <div v-for="stock in paginatedStockData" 
           :key="stock.code" 
           class="stock-row"
           @click="goToStockDetail(stock)">
        <div>{{ stock.code }}</div>
        <div>{{ stock.name }}</div>
        <div>{{ stock.close?.toFixed(2) }}</div>
        <div :class="[stock.change >= 0 ? 'price-up' : 'price-down']">
          {{ stock.change?.toFixed(2) }}
        </div>
        <div>{{ stock.open?.toFixed(2) }}</div>
        <div>{{ stock.high?.toFixed(2) }}</div>
        <div>{{ stock.low?.toFixed(2) }}</div>
        <div>{{ stock.pre_close?.toFixed(2) }}</div>
      </div>

      <div class="pagination">
        <button 
          :disabled="currentPage === 1"
          @click="prevPage"
          class="page-btn"
        >
          上一页
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button 
          :disabled="currentPage === totalPages"
          @click="nextPage"
          class="page-btn"
        >
          下一页
        </button>
      </div>
    </div>

    <div v-if="!loading && !error && !stockData.length" class="no-data">
      暂无股票数据
    </div>
  </div>
</template>

<style scoped>
.now-page {
  padding: 20px;
  background-color: #fff;
}

.header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
  gap: 20px;
}

.header-placeholder {
  /* 用于占位，使标题居中 */
  width: 100px;
}

.header h2 {
  text-align: center;
  margin: 0;
}

.header-right {
  display: flex;
  justify-content: flex-end;
}

.error-message {
  color: #ff6b6b;
  margin-top: 10px;
  font-weight: bold;
}

.loading, .no-data {
  text-align: center;
  padding: 20px;
  color: #1f1f1f;
  font-size: 16px;
}

.stock-table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  text-align: center;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.table-header {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  padding: 12px 8px;
  background-color: #f5f7fa;
  font-weight: 500;
  color: #606266;
  border: 1px solid #ebeef5;
}

.stock-row {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  padding: 12px 8px;
  border: 1px solid #ebeef5;
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.stock-row:hover {
  background-color: #f5f7fa;
}

.price-up {
  color: #f56c6c;
  font-weight: 500;
}

.price-down {
  color: #67c23a;
  font-weight: 500;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  gap: 20px;
  background-color: #fff;
}

.page-btn {
  padding: 8px 16px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  opacity: 0.8;
}

.page-btn:disabled {
  background-color: #909399;
  cursor: not-allowed;
  opacity: 0.7;
}

.page-info {
  font-size: 14px;
  color: #1a1a1a;
}

.error-row {
  grid-template-columns: 1fr 4fr !important;
}

.error-row .code {
  color: #3498db;
  font-weight: bold;
}

.error-row .message {
  color: #ff6b6b;
  text-align: left;
  padding-left: 20px;
  font-weight: bold;
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
  align-items: center;
}

.search-input {
  padding: 8px 12px;
  border: 2px solid #dcdfe6;
  border-radius: 5px;
  width: 300px;
}

.search-btn {
  padding: 8px 20px;
  background: linear-gradient(135deg, #4299e1, #3182ce);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s;
  height: 36px;
}

.search-btn:hover {
  background: linear-gradient(135deg, #3182ce, #2b6cb0);
  transform: scale(1.02);
}

.header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
  gap: 20px;
}

.header-placeholder {
  /* 用于占位，使标题居中 */
  width: 100px;
}

.header h2 {
  text-align: center;
  margin: 0;
}

.header-right {
  display: flex;
  justify-content: flex-end;
}

.refresh-btn {
  padding: 8px 15px 8px 10px;
  background: linear-gradient(135deg, #38b2ac, #319795);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  height: 36px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  justify-content: center;
  min-width: 80px;
}

.refresh-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #319795, #2c7a7b);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.refresh-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.refresh-btn .is-loading {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>