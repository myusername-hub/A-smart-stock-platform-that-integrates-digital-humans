<template>
  <div class="ai-container">
    <div class="cloud-chat">
      <iframe
        :src="`https://robot.chaoxing.com/coze?unitId=${config.unitId}&robotId=${config.robotId}`"
        frameborder="0"
        width="100%"
        height="100%"
        allow="camera; microphone; fullscreen; clipboard-write"
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals allow-downloads allow-presentation allow-pointer-lock"
        allowfullscreen
        webkitallowfullscreen
        mozallowfullscreen
      ></iframe>
    </div>
  </div>
</template>

<script>
export default {
  name: "AI",
  data() {
    return {
      config: {
        unitId: '329528',
        robotId: 'bc58d329855745239915afa08c3cb47e'  // 更新为正确的robotId
      }
    }
  }
}
</script>

<style scoped lang="scss">
.ai-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  
  .cloud-chat {
    width: 100vw;
    height: 100vh;
    margin: 0;
    padding: 0;
    
    iframe {
      width: 100vw;
      height: 100vh;
      border: none;
      margin: 0;
      padding: 0;
    }
  }
}
</style>