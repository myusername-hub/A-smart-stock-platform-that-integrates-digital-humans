<template>
  <div class="app">
    <TheHeader />
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import TheHeader from '@/views/Home/TheHeader.vue'
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
</style>