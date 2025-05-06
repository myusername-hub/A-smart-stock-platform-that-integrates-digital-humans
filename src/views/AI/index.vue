<template>
  <div class="ai-container">
    <h2>AI 助手</h2>
    <div v-if="loading" class="loading-container">
      <el-spinner />
      <span>正在加载 AI 助手...</span>
    </div>
    <div v-else-if="error" class="error-container">
      <el-alert :title="error" type="error" show-icon />
      <el-button type="primary" @click="initAIAssistant" class="retry-btn">
        重试
      </el-button>
    </div>
    <div v-else class="iframe-container">
      <iframe
        :src="`${serviceUrl}/chat/share?shareId=${config.shareId}`"
        frameborder="0"
        width="100%"
        height="100%"
        ref="aiFrame"
        @load="handleIframeLoad"
        @error="handleIframeError"
      ></iframe>
    </div>
  </div>
</template>

<script>
export default {
  name: "AI",
  data() {
    return {
      loading: true,
      error: null,
      serviceUrl: 'https://cloud.fastgpt.cn',
      config: {
        shareId: 'v1jhpdkhdn3hvsuxreu5mn3b'
      }
    }
  },
  methods: {
    initAIAssistant() {
      this.loading = true;
      this.error = null;
    },
    handleIframeLoad() {
      this.loading = false;
    },
    handleIframeError() {
      this.loading = false;
      this.error = 'AI 助手加载失败，请检查网络连接或稍后重试';
    }
  },
  mounted() {
    this.initAIAssistant();
  }
};
</script>

<style scoped lang="scss">
@use '@/assets/theme' as theme;

.ai-container {
  padding: 20px;
  height: 100vh;
  background: theme.$primary-gradient;
  display: flex;
  flex-direction: column;

  .iframe-container {
    flex: 1;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }

  .loading-container,
  .error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    text-align: center;
    
    .retry-btn {
      margin-top: 20px;
    }
  }
}
</style>