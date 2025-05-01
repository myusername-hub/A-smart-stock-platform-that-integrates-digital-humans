<script>
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    
    const handleRowClick = (row) => {
      router.push({
        name: 'StockDetail',
        params: { code: row.stockCode }
      })
    }

    return {
      handleRowClick
    }
  },
  data() {
    return {
      stockData: [
        {
          stockCode: '600007',
          stockName: '中国国贸',
          currentPrice: 17.61,
          dayChange: 1.09,
          threeChange: 2.09,
          fiveChange: 0.19,
          amplitude: 0.17,
          turnoverRate: 2.76,
          listDate: '19990312',
          marketValue: '10.07亿',
          totalValue: '10.07亿'
        },
        {
          stockCode: '600036',
          stockName: '招商银行',
          currentPrice: 32.45,
          dayChange: -0.89,
          threeChange: 1.56,
          fiveChange: -0.78,
          amplitude: 1.23,
          turnoverRate: 3.45,
          listDate: '20020401',
          marketValue: '8172.36亿',
          totalValue: '8172.36亿'
        },
        {
          stockCode: '601318',
          stockName: '中国平安',
          currentPrice: 45.67,
          dayChange: 2.34,
          threeChange: 3.21,
          fiveChange: 1.98,
          amplitude: 2.15,
          turnoverRate: 4.23,
          listDate: '20070301',
          marketValue: '12534.89亿',
          totalValue: '12534.89亿'
        },
        {
          stockCode: '000001',
          stockName: '平安银行',
          currentPrice: 12.89,
          dayChange: -1.23,
          threeChange: -0.56,
          fiveChange: 1.45,
          amplitude: 1.78,
          turnoverRate: 2.98,
          listDate: '19910403',
          marketValue: '2503.12亿',
          totalValue: '2503.12亿'
        },
        {
          stockCode: '000858',
          stockName: '五粮液',
          currentPrice: 167.82,
          dayChange: 0.95,
          threeChange: 2.67,
          fiveChange: 3.45,
          amplitude: 1.56,
          turnoverRate: 1.89,
          listDate: '19980427',
          marketValue: '6509.23亿',
          totalValue: '6509.23亿'
        },
        {
          stockCode: '601398',
          stockName: '工商银行',
          currentPrice: 4.56,
          dayChange: -0.45,
          threeChange: 0.78,
          fiveChange: -0.23,
          amplitude: 0.89,
          turnoverRate: 1.23,
          listDate: '20061027',
          marketValue: '16234.56亿',
          totalValue: '16234.56亿'
        },
        {
          stockCode: '600519',
          stockName: '贵州茅台',
          currentPrice: 1789.56,
          dayChange: 1.67,
          threeChange: 3.45,
          fiveChange: 2.89,
          amplitude: 2.34,
          turnoverRate: 0.78,
          listDate: '20010827',
          marketValue: '22456.78亿',
          totalValue: '22456.78亿'
        },
        {
          stockCode: '000333',
          stockName: '美的集团',
          currentPrice: 56.78,
          dayChange: -1.45,
          threeChange: -0.89,
          fiveChange: 1.23,
          amplitude: 1.67,
          turnoverRate: 2.45,
          listDate: '20130918',
          marketValue: '3967.45亿',
          totalValue: '3967.45亿'
        }
      ]
    }
  },
  methods: {
    async fetchStockData() {
      try {
        // 模拟数据刷新
        this.stockData = this.stockData.map(stock => ({
          ...stock,
          currentPrice: +(stock.currentPrice * (1 + (Math.random() - 0.5) * 0.01)).toFixed(2),
          dayChange: +(stock.dayChange + (Math.random() - 0.5)).toFixed(2),
          threeChange: +(stock.threeChange + (Math.random() - 0.5)).toFixed(2),
          fiveChange: +(stock.fiveChange + (Math.random() - 0.5)).toFixed(2),
          amplitude: +(stock.amplitude + (Math.random() - 0.5) * 0.1).toFixed(2),
          turnoverRate: +(stock.turnoverRate + (Math.random() - 0.5) * 0.1).toFixed(2)
        }))
      } catch (error) {
        console.error('获取股票数据失败:', error)
      }
    }
  },
  mounted() {
    this.fetchStockData()
    // 每5秒刷新一次数据
    this.timer = setInterval(() => {
      this.fetchStockData()
    }, 5000)
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer)
    }
  }
}
</script>

<template>
  <div class="stock-table">
    <h3>实时行情</h3>
    <el-table :data="stockData" style="width: 100%" height="800" @row-click="handleRowClick">
      <el-table-column prop="stockCode" label="股票编号" width="100" />
      <el-table-column prop="stockName" label="股票名称" width="120" />
      <el-table-column prop="currentPrice" label="最新价" width="100">
        <template #default="scope">
          <span :class="{ 'red': scope.row.currentPrice > 0, 'green': scope.row.currentPrice < 0 }">
            {{ scope.row.currentPrice }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="dayChange" label="当日涨跌幅" width="120">
        <template #default="scope">
          <span :class="{ 'red': scope.row.dayChange > 0, 'green': scope.row.dayChange < 0 }">
            {{ scope.row.dayChange }}%
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="threeChange" label="3日涨跌幅" width="120">
        <template #default="scope">
          <span :class="{ 'red': scope.row.threeChange > 0, 'green': scope.row.threeChange < 0 }">
            {{ scope.row.threeChange }}%
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="fiveChange" label="5日涨跌幅" width="120">
        <template #default="scope">
          <span :class="{ 'red': scope.row.fiveChange > 0, 'green': scope.row.fiveChange < 0 }">
            {{ scope.row.fiveChange }}%
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="amplitude" label="振幅" width="100">
        <template #default="scope">
          {{ scope.row.amplitude }}%
        </template>
      </el-table-column>
      <el-table-column prop="turnoverRate" label="换手率" width="100">
        <template #default="scope">
          {{ scope.row.turnoverRate }}%
        </template>
      </el-table-column>
      <el-table-column prop="listDate" label="上市日期" width="120" />
      <el-table-column prop="marketValue" label="市值" width="120" />
      <el-table-column prop="totalValue" label="总市值" width="120" />
    </el-table>
  </div>
</template>

<style scoped>
h3 {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
  color: #38393b;
}

.el-table tbody tr {
  cursor: pointer;
}

.el-table tbody tr:hover {
  background-color: #f5f7fa;
}

.stock-table {
  padding: 20px;
}

.red {
  color: #f56c6c;
}

.green {
  color: #67c23a;
}

:deep(.el-table) {
  --el-table-header-bg-color: #f5f7fa;
}

:deep(.el-table th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: bold;
}

:deep(.el-table td) {
  padding: 8px 0;
}
</style>