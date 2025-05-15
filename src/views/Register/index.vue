<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const formData = ref({
      username: '',
      password: '',
      confirmPassword: '', // 添加确认密码字段
      remember: false
    })
    const loading = ref(false)

    const handleSubmit = async () => {
      if (!formData.value.username || !formData.value.password) {
        alert('请填写完整信息')
        return
      }

      if (formData.value.password !== formData.value.confirmPassword) {
        alert('两次输入的密码不一致')
        return
      }

      if (formData.value.password.length < 6) {
        alert('密码长度不能少于6位')
        return
      }

      loading.value = true
      try {
        await authStore.register(formData.value.username, formData.value.password)
        localStorage.setItem('fromRegister', 'true')
        alert('注册成功，正在为您自动跳转到登录页面')
        router.push('/login')
      } catch (error) {
        console.error('注册失败:', error)
        let errorMessage = '注册失败：'
        if (error.message === '用户已存在') {
          errorMessage += '该用户名已被注册'
        } else if (error.message.includes('password')) {
          errorMessage += '密码格式不正确，请使用6-20位字符'
        } else if (error.message.includes('username')) {
          errorMessage += '用户名不合法，请使用3-20位字符'
        } else {
          errorMessage += '服务器错误，请稍后重试'
        }
        alert(errorMessage)
      } finally {
        loading.value = false
      }
    }

    // 确保返回模板中使用的所有数据和方法
    return {
      formData,
      loading,
      handleSubmit
    }
  }
}
</script>

<template>
  <div class="register-container">
    <div class="register-box">
      <h2>用户注册</h2>
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

        <div class="form-group">
          <label>
            <span class="label-text">确认密码</span>
            <input 
              type="password" 
              v-model="formData.confirmPassword"
              placeholder="请再次输入密码"
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
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped lang="scss">
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1f35 0%, #2a3a5c 100%);
  padding: 20px;

  .register-box {
    width: 100%;
    max-width: 420px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);

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

      &:hover {
        background: linear-gradient(135deg, #1b6fa8 0%, #0a4d8c 100%);
      }

      &:disabled {
        opacity: 0.7;
        cursor: not-allowed;
      }

      &.loading {
        position: relative;
        
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
  }
}

@keyframes spin {
  0% { transform: translateY(-50%) rotate(0deg); }
  100% { transform: translateY(-50%) rotate(360deg); }
}
</style>