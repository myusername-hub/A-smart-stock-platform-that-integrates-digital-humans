<template>
  <div class="header">
    <div class="nav">
      <div class="logo">广财股票量化交易平台</div> <!-- 添加logo -->
      <div class="right-section">
        <div class="search-box" @click="showSuggestions = true">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="搜索股票代码或名称..." 
            class="search-input"
            @keyup.enter="handleSearch()"
          />
          <button class="search-btn" @click.stop="handleSearch()">
            <i class="iconfont icon-sousuo"></i>
          </button>
          
          <!-- 搜索建议下拉框 -->
          <div v-if="showSuggestions" class="suggestions-box">
            <!-- 搜索建议 -->
            <div v-if="searchSuggestions.length > 0" class="suggestion-group">
              <div class="group-title">搜索建议</div>
              <div
                v-for="[code, name] in searchSuggestions"
                :key="code"
                class="suggestion-item"
                @click="selectSuggestion(code, name)"
              >
                <span class="stock-code">{{ code }}</span>
                <span class="stock-name">{{ name }}</span>
              </div>
            </div>
            
            <!-- 搜索历史 -->
            <div v-if="searchHistory.length > 0" class="suggestion-group">
              <div class="group-title">
                搜索历史
                <span class="clear-history" @click.stop="clearHistory">清空</span>
              </div>
              <div
                v-for="item in searchHistory"
                :key="item"
                class="suggestion-item"
                @click="handleSearch(item)"
              >
                <i class="iconfont icon-history"></i>
                <span>{{ item }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="auth-links">
          <template v-if="isLoggedIn">
            <span class="welcome-message">欢迎您，{{ username }}</span>
            <a @click="logout" class="auth-link">退出登录</a>
          </template>
          <template v-else>
            <a @click="goToPage('/login')" class="auth-link">登录</a>
            <span class="divider">|</span>
            <a @click="goToPage('/register')" class="auth-link">注册</a>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import "../../assets/iconfont.css"  // 添加图标引用
import { ElMessage } from 'element-plus' // 引入 ElMessage 组件
import { stockNameMap } from '@/utils/stockMap'

const router = useRouter()
const authStore = useAuthStore()
const searchQuery = ref('')
const showSuggestions = ref(false)
const searchHistory = ref(JSON.parse(localStorage.getItem('searchHistory') || '[]'))

// 计算属性获取登录状态
const isLoggedIn = computed(() => authStore.isLoggedIn)
const username = computed(() => authStore.currentUser)

// 页面跳转
const goToPage = (path) => {
  router.push(path)
}

// 用户注销
const logout = () => {
  authStore.logout()
  ElMessage.success('已退出登录')  // 添加提示消息
}

// 搜索建议列表
const searchSuggestions = computed(() => {
  if (!searchQuery.value) return []
  const query = searchQuery.value.toLowerCase()
  return Object.entries(stockNameMap)
    .filter(([code, name]) => 
      code.includes(query) || 
      name.toLowerCase().includes(query)
    )
    .slice(0, 5)
})

// 添加到搜索历史
const addToHistory = (query) => {
  if (!query) return
  const history = searchHistory.value
  // 移除重复项
  const index = history.indexOf(query)
  if (index > -1) {
    history.splice(index, 1)
  }
  // 添加到开头
  history.unshift(query)
  // 限制历史记录数量
  if (history.length > 5) {
    history.pop()
  }
  searchHistory.value = history
  localStorage.setItem('searchHistory', JSON.stringify(history))
}

// 处理搜索
const handleSearch = (query = searchQuery.value) => {
  if (!query.trim()) {
    ElMessage.warning('请输入股票代码或名称')
    return
  }
  // 查找股票对象
  let code = query.split(' ')[0]
  let name = ''
  if (stockNameMap[code]) {
    name = stockNameMap[code]
  } else {
    // 支持用名称查找
    const found = Object.entries(stockNameMap).find(([c, n]) => n === query.trim())
    if (found) {
      code = found[0]
      name = found[1]
    }
  }
  if (!code || !stockNameMap[code]) {
    ElMessage.warning('未找到该股票')
    return
  }
  addToHistory(query)
  showSuggestions.value = false
  // 存储完整对象
  localStorage.setItem('currentStock', JSON.stringify({ code, name }))
  router.push({
    name: 'StockDetail',
    params: { code },
    query: { name }
  })
}

// 清空搜索历史
const clearHistory = () => {
  searchHistory.value = []
  localStorage.removeItem('searchHistory')
}

// 选择建议项
const selectSuggestion = (code, name) => {
  addToHistory(`${code} ${name}`)
  showSuggestions.value = false
  // 存储完整对象
  localStorage.setItem('currentStock', JSON.stringify({ code, name }))
  router.push({
    name: 'StockDetail',
    params: { code },
    query: { name }
  })
}

// 关闭建议框
onMounted(() => {
  document.addEventListener('click', (e) => {
    const target = e.target
    if (!target.closest('.search-box')) {
      showSuggestions.value = false
    }
  })
})
</script>

<style scoped lang="scss">
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: rgba(26, 31, 53, 0.95);
  backdrop-filter: blur(10px);
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  width: 100%;

  .nav {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    padding: 0 40px;

    .logo {
      color: #e6f1ff;
      font-size: 1.2rem;
      font-weight: 500;
    }

    .right-section {
      display: flex;
      align-items: center;
      gap: 30px;

      .search-box {
        display: flex;
        align-items: center;
        margin-right: 30px;
        position: relative;

        .search-input {
          width: 250px;
          height: 36px;
          padding: 0 15px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 8px;
          background: rgba(255, 255, 255, 0.1);
          color: #e6f1ff;
          font-size: 14px;
          transition: all 0.3s ease;
          margin-right: 20px;
          padding-right: 40px;

          &::placeholder {
            color: rgba(230, 241, 255, 0.5);
          }

          &:focus {
            outline: none;
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
          }
        }

        .search-btn {
          position: absolute;
          right: 25px;
          top: 50%;
          transform: translateY(-50%);
          background: transparent;
          color: #e6f1ff;
          border: none;
          cursor: pointer;
          transition: all 0.3s ease;
          padding: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          
          &:hover {
            color: #64b3f4;
          }

          i {
            font-size: 18px;
          }
        }
      }

      .auth-links {
        display: flex;
        align-items: center;
        gap: 15px;

        .auth-link {
          color: #e6f1ff;
          text-decoration: none;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.3s ease;
          padding: 6px 0;
          border-radius: 6px;

          &:hover {
            color: #64b3f4;
          }
        }

        .divider {
          color: rgba(230, 241, 255, 0.3);
        }

        .welcome-message {
          color: #e6f1ff;
          font-size: 14px;
        }
      }
    }
  }

  .suggestions-box {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    margin-top: 5px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    z-index: 1000;

    .suggestion-group {
      padding: 8px 0;
      
      &:not(:last-child) {
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
      }

      .group-title {
        padding: 8px 16px;
        color: #909399;
        font-size: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .clear-history {
          color: #409EFF;
          cursor: pointer;
          &:hover { text-decoration: underline; }
        }
      }

      .suggestion-item {
        padding: 8px 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #303133;

        &:hover {
          background: rgba(64, 158, 255, 0.1);
        }

        .stock-code {
          color: #409EFF;
          font-weight: 500;
        }

        .stock-name {
          color: #606266;
        }

        i {
          color: #909399;
          font-size: 14px;
        }
      }
    }
  }
}
</style>