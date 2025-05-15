<script>
import { ref, onMounted, computed } from 'vue'
import { fetchWithRetry } from '@/utils/api'
import { stockNameMap } from '@/utils/stockMap'

export default {
  setup() {
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
      return stockData.value.filter(stock => !stock?.message)
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
        console.log('开始获取数据...')
        
        const response = await fetchWithRetry('/api/stock_data')
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

    const handleSearch = () => {
      if (!searchQuery.value) {
        fetchStockData()
        return
      }
      const query = searchQuery.value.toUpperCase()
      const filteredList = validStockData.value.filter(stock => 
        stock.ts_code.includes(query) || getStockName(stock.ts_code).includes(query)
      )
      stockData.value = filteredList
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
      searchQuery,
      handleSearch
    }
  }
}
</script>

<template>
  <div class="now-page">
    <!-- 添加搜索栏 -->
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
    </div>

    <div class="header">
      <h2>实时行情</h2>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
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
           class="stock-row">
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
  margin-bottom: 20px;
  text-align: center;
}

.header h2 {
  color: #171717;
  font-size: 24px;
  font-weight: bold;
  display: inline-block;
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
</style>