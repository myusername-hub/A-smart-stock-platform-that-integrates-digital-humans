<template>
  <div class="now-container">
    <table class="stock-table">
      <thead>
        <tr>
          <th>股票编号</th>
          <th>股票名称</th>
          <th>最新价</th>
          <th>单日涨跌幅</th>
          <th>3日涨跌幅</th>
          <th>5日涨跌幅</th>
          <th>涨跌额</th>
          <th>换手率</th>
          <th>振幅</th>
          <th>上市日期</th>
          <th>流通股本</th>
          <th>总股本</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in stockList" 
            :key="item.code"
            @click="handleRowClick(item.code)"
            class="table-row">
          <td>{{ item.code }}</td>
          <td>{{ item.name }}</td>
          <td :class="{ 'red': item.price > 0, 'green': item.price < 0 }">{{ item.price }}</td>
          <td :class="{ 'red': item.dayChange > 0, 'green': item.dayChange < 0 }">{{ item.dayChange }}%</td>
          <td :class="{ 'red': item.threeChange > 0, 'green': item.threeChange < 0 }">{{ item.threeChange }}%</td>
          <td :class="{ 'red': item.fiveChange > 0, 'green': item.fiveChange < 0 }">{{ item.fiveChange }}%</td>
          <td :class="{ 'red': item.changeAmount > 0, 'green': item.changeAmount < 0 }">{{ item.changeAmount }}</td>
          <td>{{ item.turnoverRate }}%</td>
          <td>{{ item.amplitude }}%</td>
          <td>{{ item.listDate }}</td>
          <td>{{ item.floatShares }}</td>
          <td>{{ item.totalShares }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'NowView',
  data() {
    return {
      stockList: [
        {
          code: '600007',
          name: '中国国贸',
          price: 17.61,
          dayChange: 1.09,
          threeChange: 0.92,
          fiveChange: 2.09,
          changeAmount: 0.19,
          turnoverRate: 0.17,
          amplitude: 2.76,
          listDate: '19990312',
          floatShares: '10.07亿',
          totalShares: '10.07亿',
          detailUrl: 'c:/Users/lenovo/Documents/WeChat Files/wxid_v1bro0hwlpfq22/FileStorage/Temp/992c5b2207edee39fb007a68f2120a0.png'
        },
        // 添加更多股票数据...
      ]
    }
  },
  methods: {
    handleRowClick(code) {
      this.$router.push({
        path: '/stock/:code',
        query: { code: code }  // 传递股票代码作为参数
      });
    }
  }
}
</script>

<style scoped>
.now-container {
  padding: 20px;
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

.stock-table th,
.stock-table td {
  padding: 8px;
  border: 1px solid #eee;
}

.stock-table th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.table-row {
  cursor: pointer;
  transition: background-color 0.3s;
}

.table-row:hover {
  background-color: #f5f7fa;
}

.red {
  color: #f56c6c;
}

.green {
  color: #67c23a;
}
</style>