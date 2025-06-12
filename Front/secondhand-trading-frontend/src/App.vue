<template>
  <div class="app-container">
    <header class="app-header">
      <div class="container">
        <router-link to="/" class="logo">校园二手平台</router-link>
        <nav class="main-nav">
          <router-link to="/">首页</router-link>
          <router-link to="/search">搜索</router-link>
          <router-link to="/my-products" v-if="isLoggedIn">我的商品</router-link>
          <router-link to="/my-orders" v-if="isLoggedIn">我的订单</router-link>
          <router-link to="/login" v-if="!isLoggedIn">登录</router-link>
          <router-link to="/register" v-if="!isLoggedIn">注册</router-link>
          <a href="javascript:void(0)" @click="logout" v-if="isLoggedIn">退出登录</a>
        </nav>
      </div>
    </header>
    
    <main class="app-main">
      <div class="container">
        <router-view />
      </div>
    </main>
    
    <footer class="app-footer">
      <div class="container">
        <p>© {{ new Date().getFullYear() }} 校园二手平台 - 让闲置物品流动起来</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './store/user'

const router = useRouter()
const userStore = useUserStore()

const isLoggedIn = computed(() => userStore.isLoggedIn)

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  color: white;
  padding: 15px 0;
  box-shadow: var(--shadow-md);
}

.app-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo::before {
  content: '🏪';
  font-size: 28px;
}

.main-nav {
  display: flex;
  gap: 20px;
  align-items: center;
}

.main-nav a {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.main-nav a:hover {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.main-nav a.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.app-main {
  flex: 1;
  padding: 40px 0;
  min-height: calc(100vh - 140px);
}

.app-footer {
  background-color: var(--background-white);
  padding: 30px 0;
  text-align: center;
  color: var(--text-secondary);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}
</style>