<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useUsersStore } from '@/store/users'
import { ElMessage } from 'element-plus'

export default {
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const usersStore = useUsersStore()
    const formData = ref({
      username: '',
      password: '',
      remember: false
    })
    const loading = ref(false)
    const showIntro = ref(true)

    // 初始化时加载数据
    usersStore.initStore()

    const handleSubmit = async () => {
      if (!formData.value.username || !formData.value.password) {
        ElMessage.warning('请填写完整信息')
        return
      }

      loading.value = true
      try {
        // 先验证用户
        await usersStore.validateLogin(
          formData.value.username,
          formData.value.password
        )
        
        // 保存记住的用户
        if (formData.value.remember) {
          localStorage.setItem('rememberedUser', JSON.stringify({
            username: formData.value.username,
            password: formData.value.password
          }))
        }

        // 登录并更新状态
        await authStore.login(formData.value.username)
        ElMessage.success('登录成功！')
        router.push('/')
      } catch (error) {
        console.error('登录失败:', error)
        ElMessage.error(error.message || '登录失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }

    const handleSkipIntro = () => {
      showIntro.value = false
      localStorage.setItem('hasSeenIntro', 'true')
    }

    onMounted(() => {
      const fromRegister = localStorage.getItem('fromRegister')
      if (fromRegister) {
        showIntro.value = true
        localStorage.removeItem('fromRegister')
        // 允许动画自动关闭，但时间缩短
        setTimeout(() => {
          showIntro.value = false
        }, 6000)
      } else {
        const hasSeenIntro = localStorage.getItem('hasSeenIntro')
        if (hasSeenIntro) {
          showIntro.value = false
        } else {
          setTimeout(() => {
            showIntro.value = false
            localStorage.setItem('hasSeenIntro', 'true')
          }, 2000)
        }
      }
    })

    return {
      formData,
      loading,
      handleSubmit,
      showIntro,
      handleSkipIntro
    }
  }
}
</script>

<template>
  <div class="signin-container">
    <div class="intro" 
         :class="{ 'intro-exit': !showIntro }"
         @click="handleSkipIntro">
      <h1>广财股票量化交易平台</h1>
      <div class="skip-hint">点击任意处跳过</div>
    </div>
    <div class="signin-box" :class="{ 'signin-enter': !showIntro }">
      <div class="signin-content">
        <h2>登录</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>
              <span class="label-text">用户名</span>
              <input 
                type="text" 
                v-model="formData.username"
                placeholder="请输入用户名"
                :disabled="loading"
              />
            </label>
          </div>
          
          <div class="form-group">
            <label>
              <span class="label-text">密码</span>
              <input 
                type="password" 
                v-model="formData.password"
                placeholder="请输入密码"
                :disabled="loading"
              />
            </label>
          </div>

          <div class="form-group remember-forgot">
            <label class="remember-me">
              <input 
                type="checkbox" 
                v-model="formData.remember"
                :disabled="loading"
              />
              <span>记住我</span>
            </label>
            <a href="#" class="forgot-password">忘记密码？</a>
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            :class="{ 'loading': loading }"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>

        <div class="register-link">
          还没有账号？ <a @click="$router.push('/register')">立即注册</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.signin-container {
  min-height: 100vh; // 修改这里，移除减去导航栏高度
  background: linear-gradient(to bottom, 
    #1a1f35 0%, 
    #2a3a5c 50%,
    #1a1f35 100%
  ); // 修改渐变
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;

  .intro {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #1a1f35 0%, #2a3a5c 100%);
    z-index: 10;
    transition: all 1s ease;

    h1 {
      font-size: 4rem;
      color: #e6f1ff;
      text-shadow: 0 0 20px rgba(100, 179, 244, 0.5);
      opacity: 1;
      transform: scale(1);
      transition: all 1s ease;
      background: linear-gradient(90deg,#ffffff 0%,
      #01506b 5%,
      #ffffff 20%,
      #d5d3d3 30%,
      #4692b3 40%,
      #ffffff 50%,
      #9ea6b6 60%,
      #376cf1 70%,
      #ffffff 80%,
      #dceef3 90%,
      #52408a 100%);
      background-size: 300% auto;
      background-clip: text; 
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: shine 4s linear infinite, titleGlow 2s ease-in-out infinite alternate;
    }

    .skip-hint {
      position: absolute;
      bottom: 40px;
      color: rgba(230, 241, 255, 0.6);
      font-size: 0.9rem;
      animation: fadeInOut 2s ease-in-out infinite;
    }

    &.intro-exit {
      transform: translateY(-90vh);
      
      h1 {
        transform: scale(0.5);
        opacity: 0.8;
      }
    }
  }

  .signin-box {
    width: 100%;
    max-width: 420px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    opacity: 0;
    transform: translateY(20px);
    transition: all 1s ease;
    transition-delay: 1s;

    &.signin-enter {
      opacity: 1;
      transform: translateY(0);
    }

    h2 {
      color: #e6f1ff;
      font-size: 2rem;
      margin-bottom: 30px;
      text-align: center;
      font-weight: 600;
    }

    .form-group {
      margin-bottom: 24px;

      label {
        display: block;
        
        .label-text {
          display: block;
          color: #e6f1ff;
          margin-bottom: 8px;
          font-size: 0.9rem;
        }
      }

      input[type="text"],
      input[type="password"] {
        width: 100%;
        padding: 12px 16px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: #e6f1ff;
        font-size: 1rem;
        transition: all 0.3s ease;

        &:focus {
          outline: none;
          border-color: #64b3f4;
          box-shadow: 0 0 0 2px rgba(100, 179, 244, 0.2);
        }

        &::placeholder {
          color: rgba(230, 241, 255, 0.5);
        }

        &:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }
      }
    }

    .remember-forgot {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .remember-me {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #e6f1ff;
        cursor: pointer;

        input[type="checkbox"] {
          accent-color: #64b3f4;
        }
      }

      .forgot-password {
        color: #64b3f4;
        text-decoration: none;
        font-size: 0.9rem;
        transition: color 0.3s ease;

        &:hover {
          color: #a8d5f9;
        }
      }
    }

    button {
      width: 100%;
      padding: 14px;
      background: linear-gradient(135deg, #0a4d8c 0%, #1b6fa8 100%);
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      cursor: pointer;
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;

      &:hover {
        background: linear-gradient(135deg, #1b6fa8 0%, #0a4d8c 100%);
      }

      &:disabled {
        opacity: 0.7;
        cursor: not-allowed;
      }

      &.loading {
        &::after {
          content: '';
          position: absolute;
          width: 20px;
          height: 20px;
          border: 2px solid #fff;
          border-top-color: transparent;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          right: 15px;
          top: 50%;
          transform: translateY(-50%);
        }
      }
    }

    .register-link {
      margin-top: 20px;
      text-align: center;
      color: #e6f1ff;

      a {
        color: #64b3f4;
        text-decoration: none;
        cursor: pointer;
        transition: color 0.3s ease;

        &:hover {
          color: #a8d5f9;
        }
      }
    }
  }
}

@keyframes spin {
  0% { transform: translateY(-50%) rotate(0deg); }
  100% { transform: translateY(-50%) rotate(360deg); }
}

@keyframes titleGlow {
  from {
    text-shadow: 0 0 20px rgba(100, 179, 244, 0.5);
  }
  to {
    text-shadow: 0 0 40px rgba(100, 179, 244, 0.8);
  }
}
@keyframes shine {
  from {
    background-position: 0% center;
  }
  to {
    background-position: -300% center;
  }
}

@keyframes fadeInOut {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}
</style>