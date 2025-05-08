<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const stockList = ref([
  {
    code: 'SH600278',
    name: '东方创业',
    price: 7.73,
    highPrice: 7.77,
    lowPrice: 7.71,
    changeRate: -0.25,
    amplitude: 0.77,
    turnover: '1794.56万元'
  },
  {
    code: 'SH600803',
    name: '新奥股份',
    price: 18.78,
    highPrice: 19.55,
    lowPrice: 18.54,
    changeRate: -3.39,
    amplitude: 5.19,
    turnover: '39740.69万元'
  },
  // 可以添加更多数据...
])

const goToDetail = (code) => {
  const currentStock = stockList.value.find(item => item.code === code)
  // 将当前股票数据存储到 localStorage
  localStorage.setItem('currentStock', JSON.stringify(currentStock))
  router.push({
    name: 'stock',
    params: { code }
  })
}

onMounted(() => {
  // 可以在这里添加初始化逻辑，比如从API获取数据
})
</script>

<template>
  <div class="recommend-container">
    <div class="search-wrapper">
      <div class="search-bar">
        <input type="text" placeholder="输入股票编码进行查询" class="search-input">
        <button class="search-btn">查询</button>
      </div>
      
      <h2 class="title">热门股票推荐</h2>
    </div>
    
    <table class="stock-table">
      <thead>
        <tr>
          <th>股票代码</th>
          <th>股票名称</th>
          <th>最新价格</th>
          <th>最高价</th>
          <th>最低价</th>
          <th>涨跌幅</th>
          <th>振幅</th>
          <th>成交额</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in stockList" 
            :key="stock.code"
            @click="goToDetail(stock.code)"
            class="stock-row">
          <td>{{ stock.code }}</td>
          <td>{{ stock.name }}</td>
          <td :class="{ 'red': stock.price > 0, 'green': stock.price < 0 }">
            {{ stock.price }}
          </td>
          <td>{{ stock.highPrice }}</td>
          <td>{{ stock.lowPrice }}</td>
          <td :class="{ 'red': stock.changeRate > 0, 'green': stock.changeRate < 0 }">
            {{ stock.changeRate }}%
          </td>
          <td>{{ stock.amplitude }}%</td>
          <td>{{ stock.turnover }}</td>
          <td>
            <button class="detail-btn">查看详情</button>
            <button class="collect-btn">收藏</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.recommend-container {
  padding: 20px;
}

.search-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  width: 300px;
}

.search-btn {
  padding: 8px 15px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.title {
  margin-bottom: 20px;
  color: #303133;
  text-align: center;
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

.stock-table th,
.stock-table td {
  padding: 12px 8px;
  border: 1px solid #ebeef5;
}

.stock-table th {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 500;
}

.stock-table tr:hover {
  background-color: #f5f7fa;
}

.red {
  color: #f56c6c;
}

.green {
  color: #67c23a;
}

.detail-btn,
.collect-btn {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  margin: 0 4px;
}

.detail-btn {
  background-color: #409eff;
  color: white;
}

.collect-btn {
  background-color: #f56c6c;
  color: white;
}

.stock-row {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.stock-row:hover {
  background-color: #f5f7fa;
}
</style>