<script>
import * as echarts from 'echarts'

export default {
  name: 'StockDetail',
  data() {
    return {
      stockCode: '',
      stockName: '',
      currentPrice: 10.6,
      priceChange: 3.62,
      prevClose: 10.23,
      openPrice: 10.55,
      highPrice: 10.75,
      lowPrice: 10.5,
      buy1Price: 10.59,
      buy1Volume: 3720,
      sell1Price: 10.6,
      sell1Volume: 8129,
      buy2Price: 10.58,
      buy2Volume: 3282,
      sell2Price: 10.62,
      sell2Volume: 12619,
      buy3Price: 10.57,
      buy3Volume: 6211,
      sell3Price: 10.63,
      sell3Volume: 9550
    }
  },
  created() {
    // 从路由参数获取股票代码
    this.stockCode = this.$route.params.code

    // 模拟根据股票代码获取股票名称
    this.fetchStockName(this.stockCode)
  },
  mounted() {
    this.initChart()
  },
  methods: {
    fetchStockName(code) {
      // 模拟一个股票代码到名称的映射
      const stockMap = {
        '000001': '平安银行',
        '600007': '中国国贸',
        '600005': '武钢股份'
      }

      // 根据代码设置股票名称
      this.stockName = stockMap[code] || '未知股票'
    },
    initChart() {
      const chart = echarts.init(document.getElementById('chart'))
      const option = {
        xAxis: {
          type: 'category',
          data: ['09:30', '10:00', '10:30', '11:00', '13:00', '13:30', '14:00', '14:30']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11.0],
            type: 'line',
            smooth: true
          }
        ]
      }
      chart.setOption(option)
    }
  }
}
</script>

<template>
  <div class="stock-detail">
    <!-- 股票标题 -->
    <div class="stock-header">
      <h2>{{ stockName }} ({{ stockCode }})</h2>
      <div class="price-info">
        <span class="current-price" :class="{ 'red': priceChange > 0, 'green': priceChange < 0 }">
          ¥ {{ currentPrice }}
        </span>
        <span class="price-change" :class="{ 'red': priceChange > 0, 'green': priceChange < 0 }">
          {{ priceChange }}%
        </span>
      </div>
    </div>

    <!-- 股票价格详情 -->
    <div class="price-details">
      <div class="detail-item">昨收：{{ prevClose }}</div>
      <div class="detail-item">今开：{{ openPrice }}</div>
      <div class="detail-item">最高：{{ highPrice }}</div>
      <div class="detail-item">最低：{{ lowPrice }}</div>
    </div>

    <!-- 交易情况 -->
    <div class="trading-info">
      <h3>交易情况（价格 / 成交量）</h3>
      <div class="trade-details">
        <div class="trade-row">
          <span>买一：{{ buy1Price }} / {{ buy1Volume }}</span>
          <span>卖一：{{ sell1Price }} / {{ sell1Volume }}</span>
        </div>
        <div class="trade-row">
          <span>买二：{{ buy2Price }} / {{ buy2Volume }}</span>
          <span>卖二：{{ sell2Price }} / {{ sell2Volume }}</span>
        </div>
        <div class="trade-row">
          <span>买三：{{ buy3Price }} / {{ buy3Volume }}</span>
          <span>卖三：{{ sell3Price }} / {{ sell3Volume }}</span>
        </div>
      </div>
    </div>

    <!-- 实时行情图表 -->
    <div class="stock-chart">
      <h3>实时行情</h3>
      <div id="chart" style="height: 400px;"></div>
    </div>
  </div>
</template>

<style scoped>
@use '@/assets/theme' as theme;
.stock-detail {
  padding: 20px;
}

.stock-header {
  margin-bottom: 20px;
}

.price-info {
  margin-top: 10px;
}

.current-price {
  font-size: 24px;
  font-weight: bold;
  margin-right: 10px;
}

.price-change {
  font-size: 18px;
}

.red {
  color: #f56c6c;
}

.green {
  color: #67c23a;
}

.price-details {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.detail-item {
  font-size: 16px;
}

.trading-info {
  margin-top: 20px;
}

.trade-details {
  margin-top: 10px;
}

.trade-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.stock-chart {
  margin-top: 20px;
}
</style>