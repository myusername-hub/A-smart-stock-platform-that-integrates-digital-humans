<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'  // 添加 auth store
import { ElMessage } from 'element-plus'     // 添加提示组件
import { stockNameMap } from '@/utils/stockMap'

const router = useRouter()
const authStore = useAuthStore()  // 初始化 auth store
const searchInput = ref('')
const stockDiscussions = ref([])

// 生成模拟的股票讨论数据
const generateMockDiscussions = () => {
  // 先检查localStorage中是否已存在数据
  const savedDiscussions = localStorage.getItem('stockDiscussions')
  if (savedDiscussions) {
    return JSON.parse(savedDiscussions)
  }

  // 如果不存在，生成新数据并保存
  const discussions = Object.entries(stockNameMap).map(([code, name]) => ({
    code,
    name,
    discussionCount: Math.floor(Math.random() * 1000),
    lastUpdateTime: new Date(Date.now() - Math.random() * 86400000 * 7).toLocaleString()
  }))
  
  // 保存到localStorage
  localStorage.setItem('stockDiscussions', JSON.stringify(discussions))
  return discussions
}

// 按讨论量排序的股票列表
const sortedStocks = computed(() => {
  if (!searchInput.value) {
    return stockDiscussions.value.sort((a, b) => b.discussionCount - a.discussionCount)
  }
  
  const query = searchInput.value.toLowerCase()
  return stockDiscussions.value
    .filter(stock => 
      stock.code.includes(query) || 
      stock.name.toLowerCase().includes(query)
    )
    .sort((a, b) => b.discussionCount - a.discussionCount)
})

// 修改跳转方法，添加登录验证
const goToDiscussion = (code) => {
  if (!authStore.user) {
    ElMessage.warning('请先登录后查看讨论')
    router.push('/login')
    return
  }
  
  router.push({
    path: `/talk/${code}`  // 修改为正确的路由路径
  })
}

// 初始化数据
onMounted(() => {
  stockDiscussions.value = generateMockDiscussions()
})

// 添加分页相关变量
const currentPage = ref(1)
const pageSize = ref(10)

// 计算分页后的股票列表
const paginatedStocks = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return sortedStocks.value.slice(start, end)
})

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(sortedStocks.value.length / pageSize.value)
})

// 分页方法
const handlePrevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const handleNextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const handleSearch = () => {
  if (!searchInput.value) return
  // 使用现有的排序和过滤逻辑
  const filtered = sortedStocks.value
  currentPage.value = 1 // 重置页码
}
</script>

<template>
  <div class="intalk-container">
    <div class="search-wrapper">
      <div class="search-bar">
        <input
          v-model="searchInput"
          type="text"
          placeholder="搜索股票代码或名称"
          class="search-input"
          @keyup.enter="handleSearch"
        >
        <button class="search-btn" @click="handleSearch">查询</button>
      </div>
    </div>

    <div class="discussions-list">
      <div v-for="stock in paginatedStocks" 
           :key="stock.code" 
           class="discussion-item"
           @click="goToDiscussion(stock.code)">
        <div class="stock-info">
          <span class="stock-name">{{ stock.name }}</span>
          <span class="stock-code">({{ stock.code }})</span>
        </div>
        <div class="discussion-info">
          <span class="count">{{ stock.discussionCount }} 讨论</span>
          <span class="time">最近更新: {{ stock.lastUpdateTime }}</span>
        </div>
      </div>
    </div>

    <!-- 添加分页控件 -->
    <div class="pagination">
      <button 
        :disabled="currentPage === 1"
        @click="handlePrevPage"
        class="page-btn"
      >
        上一页
      </button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button 
        :disabled="currentPage === totalPages"
        @click="handleNextPage"
        class="page-btn"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<style scoped>
.intalk-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
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

.search-input:focus {
  outline: none;
  border-color: #409eff;
}

.search-btn {
  padding: 8px 15px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #66b1ff;
}

.discussions-list {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.discussion-item {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.discussion-item:last-child {
  border-bottom: none;
}

.discussion-item:hover {
  background-color: #f5f7fa;
}

.stock-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stock-name {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.stock-code {
  color: #909399;
  font-size: 14px;
}

.discussion-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.count {
  color: #409eff;
  font-weight: 500;
}

.time {
  color: #909399;
  font-size: 13px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  gap: 20px;
}

.page-btn {
  padding: 8px 16px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  opacity: 0.8;
}

.page-btn:disabled {
  background-color: #909399;
  cursor: not-allowed;
  opacity: 0.7;
}

.page-info {
  color: #606266;
  font-size: 14px;
}
</style>
