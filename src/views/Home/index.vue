<template>
  <div class="home">
    <TheHeader />
    <div class="content">
      <!-- 主页内容 -->
    </div>
  </div>
</template>

<script setup>
import TheHeader from './TheHeader.vue'
</script>

<style scoped lang="scss">
.home {
  min-height: 100vh;
  padding-top: 60px; // 为header留出空间
}

.content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}
</style>
