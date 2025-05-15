<template>
  <div class="header">
    <div class="nav">
      <div class="logo">广财股票量化交易平台</div> <!-- 添加logo -->
      <div class="right-section">
        <div class="search-box">
          <input 
            type="text" 
            placeholder="搜索股票..." 
            class="search-input" 
            v-model="searchQuery" 
            @keypress="handleKeyPress" 
          />
          <button class="search-btn" @click="handleSearch">
            <i class="iconfont icon-sousuo"></i>
          </button>
        </div>
        <div class="auth-links">
          <template v-if="isLoggedIn">
            <span class="welcome-message">欢迎您，{{ username }}</span>
            <a @click="logout" class="auth-link">注销</a>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import "../../assets/iconfont.css"  // 添加图标引用

const router = useRouter()
const searchQuery = ref('')
const isLoggedIn = ref(false)
const username = ref('')

// 页面跳转
const goToPage = (path) => {
  router.push(path)
}

// 检查登录状态
const checkLoginStatus = () => {
  const user = JSON.parse(localStorage.getItem('user'))
  if (user && user.username) {
    isLoggedIn.value = true
    username.value = user.username
  } else {
    isLoggedIn.value = false
    username.value = ''
  }
}

// 用户注销
const logout = () => {
  localStorage.removeItem('user')
  checkLoginStatus()
}

// 搜索功能
const handleSearch = () => {
  if (!searchQuery.value.trim()) {
    alert('请输入股票代码或名称')
    return
  }
  router.push({
    path: '/search',
    query: { q: searchQuery.value }
  })
}

const handleKeyPress = (event) => {
  if (event.key === 'Enter') {
    handleSearch()
  }
}

onMounted(() => {
  checkLoginStatus()
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
}
</style>