<template>
  <div class="sell-container">
    <h2>卖出股票</h2>
    <div v-if="stockCode">
      <p>股票代码：{{ stockCode }}</p>
      <p>股票名称：{{ stockName }}</p>
    </div>
    <form @submit.prevent="handleSell">
      <label>卖出数量：</label>
      <input v-model.number="quantity" type="number" min="1" required />
      <button type="submit">确认卖出</button>
    </form>
    <div v-if="message" class="message">{{ message }}</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { stockNameMap } from '@/utils/stockMap'

const route = useRoute()
const stockCode = route.query.code || ''
const stockName = computed(() => stockNameMap[stockCode] || '未知')
const quantity = ref(100)
const message = ref('')

const handleSell = () => {
  message.value = `已成功卖出 ${quantity.value} 股 ${stockName.value}（${stockCode}）！`
}
</script>

<style scoped>
.sell-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 30px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.sell-container h2 {
  text-align: center;
  margin-bottom: 20px;
}
.sell-container form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.sell-container .message {
  margin-top: 20px;
  color: #f56c6c;
  text-align: center;
}
</style>
