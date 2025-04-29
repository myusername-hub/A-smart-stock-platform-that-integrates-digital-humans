<template>
  <div class="ai-container">
    <h2>AI 助手</h2>
    <!-- Chatbot 容器 -->
    <div id="chatbot-container"></div>
  </div>
</template>

<script>
export default {
  name: "AI",
  mounted() {
    // 动态加载脚本
    const script = document.createElement("script");
    script.src = "http://localhost:3000/js/iframe.js";
    script.id = "chatbot-iframe";
    script.defer = true;

    // 设置 data-* 属性
    script.setAttribute(
      "data-bot-src",
      "http://localhost:3000/chat/share?shareId=gie670t7d0efkdzawnr2bkff"
    );
    script.setAttribute("data-default-open", "true");
    script.setAttribute("data-drag", "true");
    script.setAttribute(
      "data-open-icon",
      "data:image/svg+xml;base64,PHN2ZyBOPSIxNiKWNTMyNzg1NjYOliBjbGFzcz0iadata-close-icon=data:image/svg+xml;base64,PHN2ZVBOPSIxNiKWNTM1NDQxNTI2liBibGFzcz0idefer"
    );

    // 将脚本添加到页面
    document.getElementById("chatbot-container").appendChild(script);
  },
};
</script>

<style scoped>
.ai-container {
  padding: 20px;
}
</style>