<template>
  <div class="forecast-container">
    <div class="search-bar">
      <div class="search-wrapper">
        <input
          v-model="searchInput"
          type="text"
          class="basic-input"
          placeholder="请输入股票代码或名称关键词"
          @input="handleInputChange"
          @focus="handleFocus"
          @keyup.down="handleKeyDown"
          @keyup.up="handleKeyUp"
          @keyup.enter="handleEnter"
        >
        <el-button 
          type="primary" 
          :loading="loading" 
          class="search-button"
          @click="handleSearch"
        >
          <el-icon class="search-icon"><Search /></el-icon>
          搜索
        </el-button>
      </div>
      <div v-if="showDropdown && filteredStocks.length" class="search-dropdown">
        <div
          v-for="(stock, index) in filteredStocks"
          :key="stock.value"
          :class="['dropdown-item', { active: currentIndex === index }]"
          @click="selectStock(stock)"
          @mouseenter="currentIndex = index"
        >
          <span class="stock-name" v-html="highlightKeyword(stock.label.split('(')[0])"></span>
          <span class="stock-code" v-html="highlightKeyword(stock.value)"></span>
        </div>
      </div>
    </div>
    <div ref="chartRef" class="chart-container"></div>
    
    <!-- 添加底部按钮组 -->
    <div class="trade-buttons">
      <button class="talk-btn" @click="goToTalk">
        <i class="iconfont icon-comment"></i>
        讨论区
      </button>
      <div class="operation-btns">
        <button class="buy-btn" @click="handleBuy">买入</button>
        <button class="sell-btn" @click="handleSell">卖出</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { stockNameMap } from '@/utils/stockMap'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Search } from '@element-plus/icons-vue'

const router = useRouter()
const chartRef = ref(null)
const searchInput = ref('')
const showDropdown = ref(false)
const filteredStocks = ref([])
const loading = ref(false)
const currentIndex = ref(-1) // 当前选中的建议项索引
const currentStockCode = ref('') // 存储当前选中的股票代码
let chart = null  // 修改为普通变量而不是 ref

const stockList = Object.entries(stockNameMap).map(([code, name]) => ({
  value: code,
  label: `${name} (${code})`
}))

// 添加初始化图表函数
const initChart = () => {
  if (!chartRef.value) return
  
  try {
    if (chart) {
      chart.dispose()
    }
    chart = echarts.init(chartRef.value)
    // 获取当前选中的股票，如果没有则使用默认股票
    const currentStock = JSON.parse(localStorage.getItem('currentStock'))
    const defaultStockCode = currentStock?.code || '688111'
    currentStockCode.value = defaultStockCode
    updateChartData(defaultStockCode)
  } catch (error) {
    console.error('初始化图表失败:', error)
    ElMessage.error('初始化图表失败')
  }
}

// 修改获取历史数据的方法
const getHistoricalData = async (stockCode) => {
  try {
    const response = await axios.get(`http://localhost:5000/api/daily_data/${stockCode}`)
    
    if (response.data?.status === 'success' && Array.isArray(response.data.data?.daily_data)) {
      // 获取最近7天的数据
      return response.data.data.daily_data
        .slice(0, 7)
        .map(item => ({
          trade_date: item.trade_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3'),
          close: parseFloat(item.close).toFixed(2)
        }))
        .reverse() // 确保日期升序排列
    }
    
    throw new Error('数据格式不正确')
  } catch (error) {
    console.error('读取历史数据失败:', error)
    ElMessage.error('获取历史数据失败')
    return []
  }
}

// 修改预测数据生成函数
const generateForecastData = (historicalData, days = 10) => {
  if (!historicalData || historicalData.length === 0) {
    return []
  }

  const lastValue = parseFloat(historicalData[historicalData.length - 1].close)
  const lastDate = new Date(historicalData[historicalData.length - 1].trade_date)
  const data = []
  
  for (let i = 1; i <= days; i++) {
    const date = new Date(lastDate)
    date.setDate(date.getDate() + i)
    // 格式化日期为YYYY-MM-DD
    const formattedDate = date.toISOString().split('T')[0]
    
    // 生成预测价格
    const predictedValue = lastValue * (1 + (Math.random() - 0.4) * 0.1)
    data.push({
      trade_date: formattedDate,
      close: predictedValue.toFixed(2)
    })
  }
  return data
}

// 计算Y轴范围
const calculateYAxisRange = (values) => {
  const minValue = Math.min(...values)
  const maxValue = Math.max(...values)
  return {
    min: Math.floor(minValue) - 20,  // 最低价向下取整后减20
    max: Math.ceil(maxValue) + 10    // 最高价向上取整后加10
  }
}

// 修改更新图表数据的方法
const updateChartData = async (stockCode) => {
  try {
    loading.value = true
    const historicalData = await getHistoricalData(stockCode)
    
    if (!historicalData || historicalData.length === 0) {
      ElMessage.warning('无法获取历史数据')
      return
    }

    const currentStock = JSON.parse(localStorage.getItem('currentStock'))
    
    if (!currentStock) {
      ElMessage.warning('无法获取股票数据')
      return
    }

    // 生成预测数据
    const forecastData = generateForecastData(historicalData)
    
    // 合并历史数据和预测数据的日期和值
    const dates = [...historicalData.map(item => item.trade_date), ...forecastData.map(item => item.trade_date)]
    const historicalValues = historicalData.map(item => parseFloat(item.close))
    const forecastValues = forecastData.map(item => parseFloat(item.close))

    // 计算Y轴范围
    const allValues = [...historicalValues, ...forecastValues]
    const yAxisRange = calculateYAxisRange(allValues)
    
    const stockName = currentStock?.name || stockNameMap[stockCode] || '未知股票'

    const option = {
      title: {
        text: `${stockName} (${stockCode}) - 历史数据与预测趋势`,
        left: 'center',
        top: '20px'
      },
      tooltip: {
        trigger: 'axis',
        formatter: function(params) {
          const date = params[0].axisValue
          // 根据日期判断是否为预测数据
          const isInForecastRange = new Date(date) > new Date(historicalData[historicalData.length - 1].trade_date)
          
          if (isInForecastRange) {
            const forecastPoint = params.find(p => p.seriesName === '预测数据')
            return forecastPoint && forecastPoint.value !== null 
              ? `日期：${date}<br/>预测价格：${forecastPoint.value}` 
              : ''
          } else {
            const historyPoint = params.find(p => p.seriesName === '历史数据')
            return historyPoint && historyPoint.value !== null 
              ? `日期：${date}<br/>历史价格：${historyPoint.value}` 
              : ''
          }
        }
      },
      legend: {
        data: ['历史数据', '预测数据'],
        top: '50px'
      },
      xAxis: {
        type: 'category',
        data: dates,
        axisLabel: {
          formatter: (value) => value.substring(5) // 只显示月-日
        }
      },
      yAxis: {
        type: 'value',
        scale: true,
        min: yAxisRange.min,
        max: yAxisRange.max,
        splitLine: {
          show: true,
          lineStyle: {
            type: 'dashed'
          }
        },
        axisLabel: {
          formatter: '{value}'
        }
      },
      series: [
        {
          name: '历史数据',
          type: 'line',
          data: [...historicalValues, ...new Array(forecastValues.length).fill(null)],
          smooth: true,
          itemStyle: { color: '#FF6B6B' },
          lineStyle: { width: 3 }
        },
        {
          name: '预测数据',
          type: 'line',
          data: [...new Array(historicalValues.length).fill(null), ...forecastValues],
          smooth: true,
          itemStyle: { color: '#4D96FF' },
          lineStyle: { 
            width: 3,
            type: 'dashed'
          }
        }
      ]
    }
    chart.setOption(option, true)
  } catch (error) {
    console.error('更新图表失败:', error)
    ElMessage.error('更新图表失败')
  } finally {
    loading.value = false
  }
}

// 处理输入框获得焦点
const handleFocus = () => {
  filteredStocks.value = stockList.slice(0, 10) // 显示前10个股票作为默认建议
  showDropdown.value = true
}

// 处理键盘上下键
const handleKeyDown = () => {
  if (!showDropdown.value || !filteredStocks.value.length) return
  currentIndex.value = (currentIndex.value + 1) % filteredStocks.value.length
}

const handleKeyUp = () => {
  if (!showDropdown.value || !filteredStocks.value.length) return
  currentIndex.value = currentIndex.value <= 0 ? filteredStocks.value.length - 1 : currentIndex.value - 1
}

// 处理回车键
const handleEnter = () => {
  if (currentIndex.value > -1) {
    selectStock(filteredStocks.value[currentIndex.value])
  } else {
    handleSearch()
  }
}

// 高亮关键词
const highlightKeyword = (text) => {
  if (!searchInput.value.trim()) return text
  const keyword = searchInput.value.toLowerCase()
  const index = text.toLowerCase().indexOf(keyword)
  if (index === -1) return text
  
  const before = text.substring(0, index)
  const match = text.substring(index, index + keyword.length)
  const after = text.substring(index + keyword.length)
  
  return `${before}<span class="highlight">${match}</span>${after}`
}

// 处理输入变化
const handleInputChange = () => {
  const query = searchInput.value.trim().toLowerCase()
  currentIndex.value = -1
  
  if (!query) {
    filteredStocks.value = stockList.slice(0, 10) // 显示前10个股票作为默认建议
    showDropdown.value = true
    return
  }

  filteredStocks.value = stockList
    .filter(item => {
      const stockName = item.label.toLowerCase()
      const stockCode = item.value
      return stockName.includes(query) || stockCode.includes(query)
    })
    .slice(0, 10)
  
  showDropdown.value = true
}

// 点击选择股票
const selectStock = (stock) => {
  searchInput.value = stock.label
  showDropdown.value = false
  currentStockCode.value = stock.value
  updateChartData(stock.value)
}

// 处理搜索按钮点击
const handleSearch = () => {
  const query = searchInput.value.trim()
  if (!query) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  if (filteredStocks.value.length > 0) {
    // 默认选择第一个匹配的股票
    selectStock(filteredStocks.value[0])
  } else {
    ElMessage.warning('未找到匹配的股票')
  }
}

// 添加点击外部关闭下拉框
const handleClickOutside = (event) => {
  const wrapper = document.querySelector('.search-wrapper')
  if (wrapper && !wrapper.contains(event.target)) {
    showDropdown.value = false
  }
}

const handleResize = () => {
  chart && chart.resize()
}

// 添加按钮处理函数
const goToTalk = () => {
  if (!currentStockCode.value) {
    ElMessage.warning('请先选择股票')
    return
  }
  
  router.push({
    name: 'talk',
    params: { code: currentStockCode.value }
  })
}

const handleBuy = () => {
  ElMessage.success('买入功能待实现')
}

const handleSell = () => {
  ElMessage.warning('卖出功能待实现')
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  if (chart) {
    chart.dispose()
    chart = null
  }
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped lang="scss">
.forecast-container {
  padding: 20px;
  background-color: #f5f7fa;

  .search-bar {
    display: flex;
    justify-content: center;
    padding: 20px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;

    .search-wrapper {
      position: relative;
      display: flex;
      gap: 10px;
      width: 100%;
      max-width: 600px;

      .basic-input {
        flex: 1;
        min-width: 300px;
        padding: 8px 12px;
        border: 1px solid #dcdfe6;
        border-radius: 4px;
        font-size: 14px;
        transition: all 0.3s;

        &:focus {
          outline: none;
          border-color: #409eff;
        }
      }

      .search-button {
        min-width: 80px;
        height: 40px;
        padding: 0 15px 0 10px;
        border-radius: 5px;
        font-size: 15px;
        font-weight: 500;
        background: linear-gradient(45deg, #409eff, #36cf9f);
        border: none;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        line-height: 1;

        .search-icon {
          margin-right: 2px;
          font-size: 20px;
          display: flex;
          align-items: center;
        }

        span {
          display: inline-block;
          vertical-align: middle;
        }

        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
        }

        &:active {
          transform: translateY(0);
        }
      }
    }
  }

  .search-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    max-height: 300px;
    overflow-y: auto;
    background: white;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    z-index: 1000;

    .dropdown-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 15px;
      cursor: pointer;

      .stock-name {
        font-weight: 500;
      }

      .stock-code {
        color: #909399;
        font-size: 13px;
      }

      &:hover {
        background-color: #f5f7fa;
      }

      &.active {
        background-color: #f5f7fa;
      }

      .highlight {
        color: #409eff;
        font-weight: bold;
      }
    }
  }

  .chart-container {
    width: 100%;
    height: 500px;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
}

.trade-buttons {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #fff;
  box-shadow: 0 -2px 12px 0 rgba(0,0,0,0.1);
  z-index: 100;

  .talk-btn {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    background-color: #409eff;
    color: white;
    cursor: pointer;
    transition: opacity 0.3s;

    &:hover {
      opacity: 0.8;
    }
  }

  .operation-btns {
    display: flex;
    gap: 10px;

    .buy-btn,
    .sell-btn {
      padding: 8px 20px;
      border: none;
      border-radius: 4px;
      font-size: 14px;
      cursor: pointer;
      transition: opacity 0.3s;

      &:hover {
        opacity: 0.8;
      }
    }

    .buy-btn {
      background-color: #f56c6c;
      color: white;
    }

    .sell-btn {
      background-color: #67c23a;
      color: white;
    }
  }
}

.suggestion-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;

  .stock-code {
    color: #909399;
    font-size: 13px;
  }
}

:deep(.el-select-dropdown__item) {
  padding: 0 20px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>