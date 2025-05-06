<template>
  <div class="ai-container">
    <h2>AI 助手</h2>
    <div v-if="!isServerRunning" class="service-error">
      <el-alert
        title="服务未运行"
        type="warning"
        description="AI助手服务当前不可用，请稍后再试或联系管理员"
        show-icon
        :closable="false"
      />
      <el-button 
        type="primary" 
        class="retry-btn" 
        @click="checkServerStatus"
      >
        重试连接
      </el-button>
    </div>
    <div v-else id="chatbot-container"></div>
  </div>
</template>

<script>
export default {
  name: "AI",
  data() {
    return {
      isServerRunning: false,
      serviceUrl: 'http://localhost:3000'
    }
  },
  methods: {
    async checkServerStatus() {
      try {
        const response = await fetch(`${this.serviceUrl}/health`, { 
          method: 'GET',
          timeout: 5000 
        });
        this.isServerRunning = response.ok;
        if (this.isServerRunning) {
          this.initChatbot();
        }
      } catch (error) {
        this.isServerRunning = false;
        console.error('服务检测失败:', error);
      }
    },
    initChatbot() {
      const script = document.createElement("script");
      script.src = `${this.serviceUrl}/js/iframe.js`;
      // ...existing code...
    }
  },
  async mounted() {
    await this.checkServerStatus();
  }
};
</script>

<style scoped lang="scss">
.ai-container {
  padding: 20px;
  height: 100vh;

  .service-error {
    max-width: 600px;
    margin: 40px auto;
    text-align: center;

    .retry-btn {
      margin-top: 20px;
    }
  }
}
</style>

<style scoped lang="scss">
@use '@/assets/theme.scss';

.ai-container {
  padding: 20px;
  height: 100vh;
  background: theme.$primary-gradient;

  .service-error {
    max-width: 600px;
    margin: 40px auto;
    text-align: center;

    .retry-btn {
      margin-top: 20px;
      @include theme.button-blue;
    }
  }
}
</style>