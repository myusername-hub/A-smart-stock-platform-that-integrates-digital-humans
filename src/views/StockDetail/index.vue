<template>
  <div class="stock-detail">
    <div class="header">
      <div class="left">
        <h2>{{ stockData?.name }} {{ stockData?.code }}</h2>
      </div>
    </div>

    <div class="price-info">
      <div class="current-price">
        <span class="price">¥ {{ priceInfo.currentPrice }}</span>
        <span class="change-rate" :class="{ 'red': priceInfo.changeRate > 0, 'green': priceInfo.changeRate < 0 }">
          {{ priceInfo.changeRate > 0 ? '▲' : '▼' }} {{ priceInfo.changeRate }}%
        </span>
      </div>
      <div class="price-details">
        <div class="detail-row">
          <span>昨收：</span><span>{{ priceInfo.prevClose }}</span>
        </div>
        <div class="detail-row">
          <span>今开：</span><span>{{ priceInfo.openPrice }}</span>
        </div>
        <div class="detail-row">
          <span>最高：</span><span>{{ priceInfo.highPrice }}</span>
        </div>
        <div class="detail-row">
          <span>最低：</span><span>{{ priceInfo.lowPrice }}</span>
        </div>
      </div>
    </div>

    <div class="trading-info">
      <h3>交易实况 (价格/成交量)</h3>
      <div v-if="tradeList.length" class="trade-rows">
        <div class="trade-row" v-for="(trade, index) in tradeList" :key="index">
          <span>买{{ index + 1 }}: {{ trade.buyPrice }} / {{ trade.buyVolume }}</span>
          <span>卖{{ index + 1 }}: {{ trade.sellPrice }} / {{ trade.sellVolume }}</span>
        </div>
      </div>
      <div v-else class="no-trade">
        暂无交易记录
      </div>
    </div>

    <div class="chart-container">
      <div class="chart-header">
        <h3>K线图</h3>
        <div class="period-buttons">
          <button 
            v-for="period in periods" 
            :key="period.value"
            :class="{ active: currentPeriod === period.value }"
            @click="changePeriod(period.value)"
          >
            {{ period.label }}
          </button>
        </div>
      </div>
      <div id="klineChart" style="width: 100%; height: 500px;"></div>
    </div>

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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import axios from 'axios'

const router = useRouter()
const stockData = ref(JSON.parse(localStorage.getItem('currentStock')))

// 使用真实数据
const priceInfo = ref({
  currentPrice: stockData.value?.price || '-',
  changeRate: stockData.value?.changeRate || 0,
  prevClose: stockData.value?.preClose || '-',
  openPrice: stockData.value?.open || '-',
  highPrice: stockData.value?.high || '-',
  lowPrice: stockData.value?.low || '-'
})

// 交易记录数据（如果没有实时数据，则显示为空）
const tradeList = ref([])

// K线周期选项
const periods = [
  { label: '年K', value: 'year' },  // 调整顺序，把年K放在最前面
  { label: '月K', value: 'month' },
  { label: '周K', value: 'week' },
  { label: '日K', value: 'day' }
]
const currentPeriod = ref('year')  // 修改默认值为'year'

// 在 fetchKLineData 函数前添加周K数据处理函数
const processWeekKLineData = (dailyData) => {
  const weekMap = new Map()
  
  // 按日期排序
  const sortedData = dailyData.sort((a, b) => new Date(a.trade_date) - new Date(b.trade_date))
  
  sortedData.forEach(dayData => {
    const date = new Date(dayData.trade_date)
    // 获取当周的周一日期作为key
    const weekStart = new Date(date)
    weekStart.setDate(date.getDate() - date.getDay() + 1)
    const weekKey = weekStart.toISOString().split('T')[0]
    
    if (!weekMap.has(weekKey)) {
      // 新的一周，初始化数据
      weekMap.set(weekKey, {
        trade_date: weekKey,
        open: parseFloat(dayData.open),
        high: parseFloat(dayData.high),
        low: parseFloat(dayData.low),
        close: parseFloat(dayData.close),
        vol: parseFloat(dayData.vol || 0)
      })
    } else {
      // 更新当周数据
      const weekData = weekMap.get(weekKey)
      weekData.high = Math.max(weekData.high, parseFloat(dayData.high))
      weekData.low = Math.min(weekData.low, parseFloat(dayData.low))
      weekData.close = parseFloat(dayData.close) // 最后一天收盘价作为周收盘价
      weekData.vol += parseFloat(dayData.vol || 0)
    }
  })
  
  return Array.from(weekMap.values())
}

const fetchKLineData = async () => {
  try {
    const code = (stockData.value?.code || '688111').split('.')[0].padStart(6, '0')
    console.log('请求K线数据，代码:', code, '周期:', currentPeriod.value)
    
    if (currentPeriod.value === 'week') {
      // 先获取日K数据，再合并成周K
      const url = `http://localhost:5000/api/stock_kline_data/${code}?period=day`
      const response = await axios.get(url)
      console.log('[DEBUG] 日K响应:', response.data)
      
      if (response.data?.status === 'success' && Array.isArray(response.data.data)) {
        // 处理日K数据
        const dailyData = response.data.data
          .filter(item => item.trade_date && item.open && item.high && item.low && item.close)
          .map(item => ({
            trade_date: typeof item.trade_date === 'string' ? item.trade_date.split('T')[0] : new Date(item.trade_date).toISOString().split('T')[0],
            open: Number(item.open),
            close: Number(item.close),
            high: Number(item.high),
            low: Number(item.low),
            vol: Number(item.vol || 0)
          }))
          .sort((a, b) => new Date(b.trade_date) - new Date(a.trade_date))
          .slice(0, 7)
          .sort((a, b) => new Date(a.trade_date) - new Date(b.trade_date))

        console.log('[DEBUG] 处理后的日K数据:', dailyData)
        return dailyData
      }
      return []
    } else {
      const url = `http://localhost:5000/api/stock_kline_data/${code}?period=${currentPeriod.value}`
      const response = await axios.get(url)
      if (response.data?.status === 'success' && Array.isArray(response.data.data)) {
        const processedData = response.data.data
          .filter(item => item.trade_date && item.open && item.high && item.low && item.close)
          .map(item => ({
            ...item,
            trade_date: item.trade_date.toString(),  // 直接转字符串，避免日期解析错误
            open: parseFloat(item.open),
            close: parseFloat(item.close),
            high: parseFloat(item.high),
            low: parseFloat(item.low),
            vol: parseFloat(item.vol || 0)
          }))
        return processedData
      }
    }
    
    console.error('响应格式错误')
    return []
  } catch (error) {
    console.error('获取K线数据失败:', error)
    return []
  }
}

const updateChart = async () => {
  const chartDom = document.getElementById('klineChart')
  if (!chartDom) return
  
  const myChart = echarts.getInstanceByDom(chartDom) || echarts.init(chartDom)
  myChart.showLoading() // 添加加载提示
  
  const klineData = await fetchKLineData()
  
  if (!klineData || klineData.length === 0) {
    console.error('未获取到K线数据')
    myChart.hideLoading()
    return
  }

  const option = {
    title: { 
      text: `${stockData.value?.name} - ${
        currentPeriod.value === 'day' ? '日K线' : 
        currentPeriod.value === 'week' ? '周K线' : 
        currentPeriod.value === 'month' ? '月K线' : '年K线'
      }`,
      subtext: '右上角切换周期',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      formatter: function (params) {
        const data = params[0].data
        return `日期：${params[0].name}<br/>
                开盘：${data[0]}<br/>
                收盘：${data[1]}<br/>
                最低：${data[2]}<br/>
                最高：${data[3]}<br/>
                ${currentPeriod.value !== 'day' ? `成交量：${data[4]}<br/>` : ''}`
      }
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
      top: '10%'
    },
    xAxis: {
      type: 'category',
      data: klineData.map(item => item.trade_date.toString()),
      boundaryGap: true,
      axisLine: { onZero: false },
      splitLine: { show: false }
    },
    yAxis: {
      scale: true,
      splitArea: { show: true }
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      },
      {
        show: true,
        type: 'slider',
        bottom: 0,
        start: 0,
        end: 100
      }
    ],
    series: [
      {
        name: '价格区间',
        type: 'candlestick',
        data: klineData.map(item => ([
          parseFloat(item.open),
          parseFloat(item.close),
          parseFloat(item.low),
          parseFloat(item.high)
        ])),
        itemStyle: {
          color: '#ef232a',
          color0: '#14b143',
          borderColor: '#ef232a',
          borderColor0: '#14b143'
        }
      }
    ]
  }

  try {
    myChart.hideLoading() // 隐藏加载提示
    myChart.setOption(option, true)
    console.log('图表已更新:', currentPeriod.value)
  } catch (error) {
    console.error('图表更新失败:', error)
    myChart.hideLoading()
  }
}

const changePeriod = (period) => {
  if (currentPeriod.value === period) return
  currentPeriod.value = period
  updateChart()
}

const goToTalk = () => {
  router.push({
    name: 'talk',
    params: { code: stockData.value.code }
  })
}

onMounted(() => {
  updateChart()
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    const chartDom = document.getElementById('klineChart')
    const chart = echarts.getInstanceByDom(chartDom)
    if (chart) chart.resize()
  })
})
</script>

<style scoped>
.stock-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.price-info {
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.current-price {
  font-size: 32px;
  margin-bottom: 20px;
}

.price {
  margin-right: 15px;
}

.change-rate {
  font-size: 24px;
}

.price-details {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.trading-info {
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.trade-rows {
  display: grid;
  gap: 10px;
}

.trade-row {
  display: flex;
  justify-content: space-between;
}

.mock-chart {
  width: 100%;
  height: 400px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.chart-container {
  margin-top: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.red {
  color: #f56c6c;
}

.green {
  color: #67c23a;
}

.period-buttons {
  display: flex;
  gap: 10px;
}

.period-buttons button {
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  background-color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.period-buttons button.active {
  background-color: #409eff;
  color: white;
  border-color: #409eff;
}

.period-buttons button:hover {
  border-color: #409eff;
}

.no-trade {
  text-align: center;
  padding: 20px;
  color: #909399;
  font-size: 14px;
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
}

.operation-btns {
  display: flex;
  gap: 10px;
}

.buy-btn,
.sell-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.buy-btn:hover,
.sell-btn:hover {
  opacity: 0.8;
}

.buy-btn {
  background-color: #f56c6c;
  color: white;
}

.sell-btn {
  background-color: #67c23a;
  color: white;
}

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
}

.talk-btn:hover {
  opacity: 0.8;
}
</style>