<template>
  <div>
    <header>
      <!-- <h1>股票量化交易系统</h1>
      <nav>
        <router-link to="/">首页</router-link>
        <router-link to="/market-info">实时行情</router-link>
        <router-link to="/stock-recommend">股票推荐</router-link>
      </nav> -->
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
nav {
  display: flex;
  gap: 1rem;
}
</style>