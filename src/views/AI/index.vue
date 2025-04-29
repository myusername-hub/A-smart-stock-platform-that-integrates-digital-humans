<template>
  <div class="ai-container">
    <h2>AI 助手</h2>
    <div id="chatbot-container"></div>
  </div>
</template>

<script>
export default {
  name: "AI",
  mounted() {
    const script = document.createElement("script");
    script.src = "http://localhost:3000/js/iframe.js";
    script.id = "chatbot-iframe";
    script.defer = true;

    // 添加必要的配置
    script.setAttribute(
      "data-bot-src",
      "http://localhost:3000/chat/share?shareId=gie670t7d0efkdzawnr2bkff"
    );
    script.setAttribute("data-default-open", "true");
    script.setAttribute("data-drag", "true");

    // 添加加载事件监听
    script.onload = () => {
      console.log("Chatbot 脚本加载成功");
    };

    script.onerror = (error) => {
      console.error("Chatbot 脚本加载失败:", error);
    };

    document.getElementById("chatbot-container").appendChild(script);
  },
};
</script>

<style scoped>
.ai-container {
  padding: 20px;
  height: 100vh;
}
</style>