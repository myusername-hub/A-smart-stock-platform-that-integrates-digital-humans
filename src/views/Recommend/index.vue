<script>
export default {
  name: 'Recommend',
  data() {
    return {
      searchQuery: '', // 搜索框输入内容
      stocks: [
        {
          stockCode: 'sh600278',
          stockName: '东方创业',
          currentPrice: 7.73,
          highPrice: 7.77,
          lowPrice: 7.71,
          priceChange: -0.25,
          amplitude: 0.77,
          turnover: '1794.56万元'
        },
        {
          stockCode: 'sh600083',
          stockName: '新钢股份',
          currentPrice: 18.78,
          highPrice: 19.55,
          lowPrice: 18.54,
          priceChange: -3.39,
          amplitude: 5.19,
          turnover: '39740.69万元'
        },
        {
          stockCode: 'sh603236',
          stockName: '移动通信',
          currentPrice: 191.18,
          highPrice: 198.69,
          lowPrice: 189.7,
          priceChange: -2.95,
          amplitude: 4.56,
          turnover: '37964.73万元'
        },
        {
          stockCode: 'sh600597',
          stockName: '光明乳业',
          currentPrice: 14.63,
          highPrice: 14.63,
          lowPrice: 14.45,
          priceChange: 0.82,
          amplitude: 2.54,
          turnover: '40595.49万元'
        },
        {
          stockCode: 'sh601211',
          stockName: '国泰君安',
          currentPrice: 17.62,
          highPrice: 17.87,
          lowPrice: 17.35,
          priceChange: 1.03,
          amplitude: 2.96,
          turnover: '108265.24万元'
        }
      ]
    }
  },
  computed: {
    filteredStocks() {
      if (!this.searchQuery) {
        return this.stocks
      }
      return this.stocks.filter((stock) =>
        stock.stockName.includes(this.searchQuery) || stock.stockCode.includes(this.searchQuery)
      )
    }
  },
  methods: {
    searchStock() {
      console.log('搜索股票:', this.searchQuery)
    },
    viewDetails(stock) {
      console.log('查看详情:', stock)
      this.$router.push({ name: 'StockDetail', params: { code: stock.stockCode } })
    },
    collectStock(stock) {
      console.log('收藏股票:', stock)
      alert(`已收藏股票：${stock.stockName}`)
    }
  }
}
</script>

<template>
  <div class="recommend-container">
    <!-- 搜索框 -->
    <div class="search-bar">
      <input v-model="searchQuery" placeholder="输入股票名称进行查询" />
      <button @click="searchStock">查询</button>
    </div>

    <!-- 表格标题 -->
    <h2>热门股票推荐</h2>

    <!-- 股票推荐表格 -->
    <el-table :data="filteredStocks" style="width: 100%" border>
      <el-table-column prop="stockCode" label="股票代码" width="120" />
      <el-table-column prop="stockName" label="股票名称" width="150" />
      <el-table-column prop="currentPrice" label="最新价格" width="120" />
      <el-table-column prop="highPrice" label="最高价" width="120" />
      <el-table-column prop="lowPrice" label="最低价" width="120" />
      <el-table-column prop="priceChange" label="涨跌幅" width="120">
        <template #default="scope">
          <span :class="{ 'red': scope.row.priceChange > 0, 'green': scope.row.priceChange < 0 }">
            {{ scope.row.priceChange }}%
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="amplitude" label="振幅" width="120" />
      <el-table-column prop="turnover" label="成交额" width="150" />
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <button @click="viewDetails(scope.row)" class="btn btn-blue">查看详情</button>
          <button @click="collectStock(scope.row)" class="btn btn-red">收藏</button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped>
.recommend-container {
  padding: 20px;
}

.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.search-bar input {
  width: 300px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
}

.search-bar button {
  padding: 8px 16px;
  background-color: #1b8eda;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-bar button:hover {
  background-color: #0f6299;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-blue {
  background-color: #1b8eda;
  color: white;
  margin-right: 10px;
}

.btn-blue:hover {
  background-color: #0f6299;
}

.btn-red {
  background-color: #f56c6c;
  color: white;
}

.btn-red:hover {
  background-color: #d93030;
}

.red {
  color: #f56c6c;
}

.green {
  color: #67c23a;
}
</style>