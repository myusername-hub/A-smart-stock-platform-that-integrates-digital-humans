<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { stockNameMap } from '@/utils/stockMap'
import axios from 'axios'

const router = useRouter()
const stockList = ref([])

// 生成预测数据
const generateRealData = async () => {
  const result = []
  
  try {
    // 获取所有股票的历史数据
    const response = await axios.get('http://localhost:5000/api/stock_daily_data')
    
    if (response.data?.status === 'success' && Array.isArray(response.data.data)) {
      for (const stock of response.data.data) {
        if (!stock.daily_data || !Array.isArray(stock.daily_data)) continue
        
        // 获取最近7天的数据
        const lastWeekData = stock.daily_data.slice(0, 7)
        if (lastWeekData.length === 0) continue
        
        // 计算周平均价
        const weekAvgPrice = lastWeekData.reduce((sum, day) => 
          sum + parseFloat(day.close || 0), 0) / lastWeekData.length
        
        // 生成预测数据
        const nextWeekAvgPrice = weekAvgPrice * (1 + (Math.random() - 0.4) * 0.15)
        const predictedChange = ((nextWeekAvgPrice - weekAvgPrice) / weekAvgPrice * 100).toFixed(2)
        
        // 使用完整的股票代码
        const fullCode = stock.code.padStart(6, '0')
        
        result.push({
          code: fullCode,
          name: stockNameMap[fullCode] || '未知',
          weekAvgPrice: weekAvgPrice.toFixed(2),
          nextWeekAvgPrice: nextWeekAvgPrice.toFixed(2),
          predictedChange
        })
      }
    }
  } catch (error) {
    console.error('获取股票数据失败:', error)
  }
  
  return result
}

// 排序后的股票列表
const sortedStocks = computed(() => {
  return [...stockList.value].sort((a, b) => parseFloat(b.predictedChange) - parseFloat(a.predictedChange))
})

// 查看详情
const viewDetails = (stock) => {
  // 保存当前股票信息到localStorage
  localStorage.setItem('currentStock', JSON.stringify({
    code: stock.code,
    name: stock.name,
    weekAvgPrice: stock.currentPrice // 使用当前价格作为周均价基准
  }))
  
  router.push({
    path: '/forecast',
    query: { code: stock.code }
  })
}

onMounted(async () => {
  try {
    const data = await generateRealData()
    stockList.value = data.filter(stock => stock.name !== '未知') // 过滤掉未知股票
    console.log('预测数据:', stockList.value) // 添加日志输出
  } catch (error) {
    console.error('数据加载失败:', error)
  }
})
</script>

<template>
  <div class="infore-container">
    <h2 class="title">股票周度预测排名</h2>
    
    <table class="stock-table">
      <thead>
        <tr>
          <th>排名</th>
          <th>股票代码</th>
          <th>股票名称</th>
          <th>本周均价</th>
          <th>下周预测均价</th>
          <th>预测涨跌幅</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(stock, index) in sortedStocks" 
            :key="stock.code">
          <td>{{ index + 1 }}</td>
          <td>{{ stock.code }}</td>
          <td>{{ stock.name }}</td>
          <td>{{ stock.weekAvgPrice }}</td>
          <td>{{ stock.nextWeekAvgPrice }}</td>
          <td :class="{ 
            'red': parseFloat(stock.predictedChange) > 0,
            'green': parseFloat(stock.predictedChange) < 0 
          }">
            {{ stock.predictedChange }}%
          </td>
          <td>
            <button class="view-btn" @click="viewDetails(stock)">
              查看详情
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.infore-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  color: #303133;
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stock-table th,
.stock-table td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ebeef5;
}

.stock-table th {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 500;
}

.red { color: #f56c6c; }
.green { color: #67c23a; }

.view-btn {
  padding: 6px 12px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.view-btn:hover {
  opacity: 0.8;
}
</style>
