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
      ]
    }
  },
  methods: {
    async fetchStockData() {
      try {
        // 实现实际的数据获取逻辑
      } catch (error) {
        console.error('获取股票数据失败:', error)
      }
    }
  },
  mounted() {
    this.fetchStockData()
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
      <el-table-column prop="amplitude" label="振幅" width="100" />
      <el-table-column prop="turnoverRate" label="换手率" width="100" />
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