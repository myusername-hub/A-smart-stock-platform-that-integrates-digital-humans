<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { stockNameMap } from '@/utils/stockMap'

export default {
  setup() {
    const stockData = ref([])
    const loading = ref(false)
    const error = ref(null)
    const currentPage = ref(1)
    const pageSize = ref(5)  // 每页显示5条数据

    const hasErrors = computed(() => {
      return stockData.value.some(stock => stock.message);
    });

    const validStockData = computed(() => {
      return stockData.value.filter(stock => !stock.message);
    });

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
        const response = await axios.get('http://localhost:5000/stock_data')
        stockData.value = response.data
      } catch (err) {
        console.error('获取数据失败:', err)
        error.value = '连接服务器失败，请检查后端服务是否启动'
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchStockData()
      const timer = setInterval(fetchStockData, 30000)
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
      prevPage
    }
  }
}
</script>

<template>
  <div class="now-page">
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
           :key="stock.ts_code" 
           class="stock-row">
        <div>{{ stock.ts_code }}</div>
        <div>{{ getStockName(stock.ts_code) }}</div>
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
  color: #1b1a1a;  
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
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.table-header,
.stock-row {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  padding: 15px;
  align-items: center;
}

.table-header {
  background: #f5f5f5;
  font-weight: bold;
  color: #252424;
}

.stock-row {
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s;
}

.stock-row:hover {
  background: rgba(0, 0, 0, 0.05);
}

.price-up {
  color: #00c853;
  font-weight: bold;
}

.price-down {
  color: #ff4d4f;
  font-weight: bold;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  gap: 20px;
  border-top: 1px solid #eee;
}

.page-btn {
  padding: 8px 16px;
  background: #1a1a1a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.page-btn:hover:not(:disabled) {
  background: #333;
}

.page-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
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
</style>