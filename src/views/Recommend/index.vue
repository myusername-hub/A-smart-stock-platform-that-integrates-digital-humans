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
    <h3>热门股票推荐</h3>

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

<style scoped lang="scss">
@use '@/assets/theme' as theme;
.recommend-container {
  padding: 20px;
  background: linear-gradient(135deg, #e8f1f8 0%, #d2e4f3 100%);  // 改为淡蓝色背景
  min-height: 100vh;

  h3 {
    color: #2c3e50;  // 深色文字
    margin-bottom: 20px;
    font-size: 1.3rem;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .search-bar {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;

    input {
      width: 300px;
      padding: 12px;
      background: rgba(255, 255, 255, 0.8);  // 半透明白色背景
      border: 1px solid #a8c6df;
      border-radius: 8px;
      color: #2c3e50;  // 深色文字
      margin-right: 10px;
      transition: all 0.3s ease;

      &::placeholder {
        color: #7f8c8d;
      }

      &:focus {
        outline: none;
        border-color: #3498db;
        background: #ffffff;
      }
    }

    button {
      padding: 8px 24px;
      background: #3498db;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        background: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      }
    }
  }

  :deep(.el-table) {
    background: rgba(127, 180, 242, 0.9);  // 半透明白色背景
    border: 1px solid #a8c6df;
    border-radius: 8px;
    overflow: hidden;

    th {
      background: #cde6fa;  // 淡蓝色表头
      border-bottom: 1px solid #99bfde;
      color: #2c3e50;  // 深色文字
      font-weight: 500;
    }

    td {
      background: transparent;
      border-bottom: 1px solid #e8f1f8;
      color: #2c3e50;  // 深色文字
    }

    tr {
      &:hover > td {
        background: #f4f9fd;  // 淡蓝色悬停效果
      }
    }
  }

  .btn {
    padding: 6px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 14px;
  }

  .btn-blue {
    background: #3498db;
    color: white;
    margin-right: 10px;

    &:hover {
      background: #2980b9;
      transform: translateY(-2px);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
  }

  .btn-red {
    background: #e74c3c;
    color: white;

    &:hover {
      background: #c0392b;
      transform: translateY(-2px);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
  }

  .red {
    color: #e74c3c;
    &:hover {
      color: #c0392b;
    }
  }

  .green {
    color: #27ae60;
    &:hover {
      color: #219a52;
    }
  }
}
</style>