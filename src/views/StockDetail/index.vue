<template>
  <div class="stock-detail">
    <div class="header">
      <div class="left">
        <button class="back-btn" @click="goBack">
          <i class="iconfont icon-fanhui"></i> 返回
        </button>
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
      <div class="trade-rows">
        <div class="trade-row" v-for="(trade, index) in tradeList" :key="index">
          <span>买{{ index + 1 }}: {{ trade.buyPrice }} / {{ trade.buyVolume }}</span>
          <span>卖{{ index + 1 }}: {{ trade.sellPrice }} / {{ trade.sellVolume }}</span>
        </div>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()
const stockData = ref(JSON.parse(localStorage.getItem('currentStock')))

// 返回上一页
const goBack = () => {
  router.back()
}

// 模拟数据
const priceInfo = ref({
  currentPrice: '10.600',
  changeRate: 3.62,
  prevClose: '10.230',
  openPrice: '10.550',
  highPrice: '10.750',
  lowPrice: '10.500'
})

const tradeList = ref([
  { buyPrice: '10.590', buyVolume: '3720', sellPrice: '10.600', sellVolume: '8129' },
  { buyPrice: '10.580', buyVolume: '3282', sellPrice: '10.610', sellVolume: '9769' },
  { buyPrice: '10.570', buyVolume: '6211', sellPrice: '10.620', sellVolume: '12619' },
  { buyPrice: '10.560', buyVolume: '12083', sellPrice: '10.630', sellVolume: '9550' },
  { buyPrice: '10.550', buyVolume: '18880', sellPrice: '10.640', sellVolume: '11234' }
])

// K线周期选项
const periods = [
  { label: '日K', value: 'day' },
  { label: '周K', value: 'week' },
  { label: '月K', value: 'month' },
  { label: '年K', value: 'year' }
]
const currentPeriod = ref('day')

// 生成不同周期的K线数据
const generateKLineData = (period) => {
  const basePrice = 10
  const data = []
  const now = new Date()
  
  // 根据不同周期生成对应的数据点数量和时间间隔
  const getTimePoints = () => {
    switch(period) {
      case 'day':
        // 一天内每半小时一个数据点，交易时间9:30-15:00
        return Array.from({ length: 12 }, (_, i) => {
          const time = new Date(now)
          time.setHours(9, 30 + i * 30, 0, 0)
          return time
        })
      case 'week':
        // 一周内每天的数据
        return Array.from({ length: 7 }, (_, i) => {
          const time = new Date(now)
          time.setDate(time.getDate() - i)
          return time
        })
      case 'month':
        // 一个月内每天的数据
        return Array.from({ length: 30 }, (_, i) => {
          const time = new Date(now)
          time.setDate(time.getDate() - i)
          return time
        })
      case 'year':
        // 一年内每天的数据
        return Array.from({ length: 365 }, (_, i) => {
          const time = new Date(now)
          time.setDate(time.getDate() - i)
          return time
        })
    }
  }

  const timePoints = getTimePoints()
  
  // 生成每个时间点的数据
  timePoints.forEach(time => {
    const volatility = period === 'day' ? 0.5 : 
                      period === 'week' ? 1 :
                      period === 'month' ? 2 : 3
    
    const open = basePrice + Math.random() * volatility - volatility/2
    const close = open + Math.random() * volatility - volatility/2
    const low = Math.min(open, close) - Math.random() * volatility/2
    const high = Math.max(open, close) + Math.random() * volatility/2
    const volume = Math.round(Math.random() * 10000)
    
    // 根据不同周期格式化日期
    const dateStr = period === 'day' ? 
      `${time.getHours()}:${time.getMinutes().toString().padStart(2, '0')}` :
      time.toISOString().split('T')[0]
    
    data.unshift([dateStr, open, close, low, high, volume])
  })
  
  return data
}

const changePeriod = (period) => {
  currentPeriod.value = period
  updateChart()
}

const updateChart = () => {
  const chartDom = document.getElementById('klineChart')
  if (!chartDom) return
  
  const myChart = echarts.getInstanceByDom(chartDom) || echarts.init(chartDom)
  const klineData = generateKLineData(currentPeriod.value)
  
  // 计算价格范围
  const prices = klineData.reduce((acc, item) => {
    acc.push(item[1], item[2], item[3], item[4])
    return acc
  }, [])
  const minPrice = Math.min(...prices)
  const maxPrice = Math.max(...prices)
  const priceRange = maxPrice - minPrice
  
  const option = {
    title: {
      show: false  // 隐藏echarts的标题
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['K线', 'MA5', 'MA10', 'MA20']
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
      top: '10%',
      height: 'auto'
    },
    xAxis: {
      type: 'category',
      data: klineData.map(item => item[0]),
      scale: true,
      boundaryGap: true,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: 'dataMin',
      max: 'dataMax'
    },
    yAxis: {
      scale: true,
      splitArea: { show: true },
      min: minPrice - priceRange * 0.1,
      max: maxPrice + priceRange * 0.1
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,  // 修改为0，显示全部数据
        end: 100
      },
      {
        show: true,
        type: 'slider',
        top: '90%',
        start: 0,  // 修改为0，显示全部数据
        end: 100
      }
    ],
    series: [{
      name: 'K线',
      type: 'candlestick',
      data: klineData.map(item => item.slice(1, 5)),
      itemStyle: {
        color: '#ef232a',
        color0: '#14b143',
        borderColor: '#ef232a',
        borderColor0: '#14b143'
      },
      barWidth: '70%'  // 控制K线宽度
    }]
  }

  myChart.setOption(option, true)  // 添加 true 参数来强制更新
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

.back-btn {
  padding: 8px 16px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.back-btn:hover {
  background-color: #66b1ff;
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
</style>