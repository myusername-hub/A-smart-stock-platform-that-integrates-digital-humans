<template>
  <div class="forecast-container">
    <div class="search-bar">
      <div class="search-wrapper">
        <el-button type="primary" size="large" @click="searchStock">查询</el-button>
      </div>
    </div>
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<script>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { Search } from '@element-plus/icons-vue'

const stockData = [
  { label: '中国银行(601988)', value: '601988' },
  { label: '工商银行(601398)', value: '601398' },
  { label: '建设银行(601939)', value: '601939' },
  { label: '农业银行(601288)', value: '601288' },
  { label: '中国平安(601318)', value: '601318' },
  { label: '招商银行(600036)', value: '600036' }
]

const historicalData = [
  { value: 3.59, date: '2023-01' },
  { value: 3.61, date: '2023-02' },
  { value: 3.65, date: '2023-03' },
  { value: 3.66, date: '2023-04' },
  { value: 3.64, date: '2023-05' },
  { value: 3.61, date: '2023-06' },
  { value: 3.60, date: '2023-07' },
  { value: 3.57, date: '2023-08' },
  { value: 3.57, date: '2023-09' },
  { value: 3.59, date: '2023-10' },
  { value: 3.60, date: '2023-11' },
  { value: 3.58, date: '2023-12' }
]

const forecastData = [
  { value: 3.61, date: '2024-01' },
  { value: 3.63, date: '2024-02' },
  { value: 3.64, date: '2024-03' },
  { value: 3.64, date: '2024-04' },
  { value: 3.65, date: '2024-05' },
  { value: 3.65, date: '2024-06' },
  { value: 3.66, date: '2024-07' },
  { value: 3.66, date: '2024-08' },
  { value: 3.67, date: '2024-09' },
  { value: 3.68, date: '2024-10' }
]

export default {
  name: 'Forecast',
  components: { Search },
  setup() {
    const chartRef = ref(null)
    const keyword = ref('')
    let chart = null

    const initChart = () => {
      if (chartRef.value) {
        chart = echarts.init(chartRef.value)
        const option = {
          title: {
            text: '中国银行(601988)过去20天历史数据以及未来10天预测数据',
            left: 'center',
            top: '20px'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'line',
              lineStyle: {
                color: '#7F7F7F',
                width: 2,
                type: 'dashed'
              }
            }
          },
          legend: {
            data: ['过去20天', '未来10天'],
            top: '50px'
          },
          grid: {
            top: '100px',
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [...historicalData.map(item => item.date), ...forecastData.map(item => item.date)]
          },
          yAxis: {
            type: 'value',
            min: 3,
            max: 4,
            interval: 0.2,
            axisLabel: {
              formatter: '{value}'
            }
          },
          series: [
            {
              name: '过去20天',
              type: 'line',
              data: historicalData.map(item => item.value),
              itemStyle: {
                color: '#FF6B6B'
              },
              animationDuration: 2000,
              animationEasing: 'quadraticOut',
              smooth: true,
              effect: {
                show: true,
                period: 3,
                trailLength: 0.7
              },
              symbol: 'circle',
              symbolSize: 8,
              lineStyle: {
                width: 3,
                shadowColor: 'rgba(255,107,107,0.5)',
                shadowBlur: 10
              },
              emphasis: {
                scale: true,
                focus: 'series'
              }
            },
            {
              name: '未来10天',
              type: 'line',
              data: Array(historicalData.length).fill('-').concat(forecastData.map(item => item.value)),
              itemStyle: {
                color: '#4D96FF'
              },
              animationDuration: 2000,
              animationDelay: 1000,
              animationEasing: 'quadraticOut',
              smooth: true,
              effect: {
                show: true,
                period: 3,
                trailLength: 0.7
              },
              symbol: 'circle',
              symbolSize: 8,
              lineStyle: {
                width: 3,
                shadowColor: 'rgba(77,150,255,0.5)',
                shadowBlur: 10
              },
              emphasis: {
                scale: true,
                focus: 'series'
              }
            }
          ],
          animation: true,
          animationThreshold: 2000,
          animationDuration: 2000,
          animationEasing: 'cubicInOut',
          animationDelay: function (idx) {
            return idx * 100;
          },
          animationDurationUpdate: 1000,
          animationEasingUpdate: 'cubicInOut',
          animationDelayUpdate: function (idx) {
            return idx * 100;
          }
        }
        chart.setOption(option)
      }
    }

    const handleResize = () => {
      chart && chart.resize()
    }

    onMounted(() => {
      initChart()
      window.addEventListener('resize', handleResize)
    })

    onUnmounted(() => {
      if (chart) {
        chart.dispose()
        chart = null
      }
      window.removeEventListener('resize', handleResize)
    })

    const searchStock = () => {
      const newHistoricalData = historicalData.map(item => ({
        ...item,
        value: +(item.value + (Math.random() - 0.5) * 0.1).toFixed(2)
      }));
      
      const newForecastData = forecastData.map(item => ({
        ...item,
        value: +(item.value + (Math.random() - 0.5) * 0.1).toFixed(2)
      }));

      chart.setOption({
        series: [
          {
            data: newHistoricalData.map(item => item.value)
          },
          {
            data: Array(historicalData.length).fill('-').concat(newForecastData.map(item => item.value))
          }
        ]
      });
    }

    return {
      chartRef,
      searchStock
    }
  }
}
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
      display: flex;
      justify-content: center;
      align-items: center;
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

:deep(.suggestion-item) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .stock-code {
    color: #909399;
    font-size: 13px;
  }
}
</style>