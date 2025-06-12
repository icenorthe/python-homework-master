<template>
  <div class="home-view">
     <!-- 新增装饰性渐变背景 -->
    <div class="background-gradient"></div>
    <h1 class="page-title">
      <span class="title-text">校园二手市场</span>
      <span class="title-decoration">♻️</span>
    </h1>
    

    <!-- 优化后的banner -->
    <div class="banner">
      <div class="banner-content">
        <h2 class="banner-title">
          <span class="gradient-text">让闲置物品流动起来</span>
        </h2>
        <p class="banner-subtitle">买卖二手物品，为校园生活增添便利</p>
        <div class="banner-actions">
          <router-link to="/search" class="action-btn primary">
            <i class="el-icon-search"></i>
            浏览商品
          </router-link>
          <router-link 
            v-if="isLoggedIn" 
            to="/add-product" 
            class="action-btn secondary"
          >
            <i class="el-icon-upload2"></i>
            发布商品
          </router-link>
          <router-link v-else to="/login" class="action-btn secondary">
            <i class="el-icon-user"></i>
            登录发布
          </router-link>
        </div>
      </div>
    </div>

    
    <div class="latest-products">
      <h2>最新上架</h2>
      <el-row :gutter="20">
        <el-col v-for="product in latestProducts" :key="product.id" :xs="24" :sm="12" :md="8" :lg="6">
          <product-card :product="product" />
        </el-col>
      </el-row>
      
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>
      
      <div v-if="!loading && latestProducts.length === 0" class="empty-state">
        <p>暂无商品，快来发布第一个商品吧！</p>
      </div>
    </div>
    
    <div class="categories">
      <h2>商品分类</h2>
      <div class="category-list">
        <div class="category-item" @click="searchByCategory('书籍')">
          <i class="el-icon-reading"></i>
          <span>书籍教材</span>
        </div>
        <div class="category-item" @click="searchByCategory('电子')">
          <i class="el-icon-mobile"></i>
          <span>电子产品</span>
        </div>
        <div class="category-item" @click="searchByCategory('服装')">
          <i class="el-icon-shopping-bag-1"></i>
          <span>服装鞋包</span>
        </div>
        <div class="category-item" @click="searchByCategory('生活')">
          <i class="el-icon-house"></i>
          <span>生活用品</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { productApi } from '../api/product'
import ProductCard from '../components/ProductCard.vue'

const router = useRouter()
const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)

const latestProducts = ref([])
const loading = ref(true)

const fetchLatestProducts = async () => {
  loading.value = true
  try {
    const response = await productApi.getProducts()
    console.log('获取到的商品数据:', response)
    
    if (response.code === 200 && Array.isArray(response.data)) {
      // 只显示最新的8个商品
      latestProducts.value = response.data
        .filter(product => product.status === 'available')
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 8)
      
      console.log('处理后的商品数据:', latestProducts.value)
    } else {
      console.error('商品数据格式不正确:', response)
      latestProducts.value = []
    }
  } catch (error) {
    console.error('获取商品列表失败:', error)
    latestProducts.value = []
  } finally {
    loading.value = false
  }
}

const searchByCategory = (category) => {
  router.push({
    path: '/search',
    query: { keyword: category }
  })
}

onMounted(() => {
  fetchLatestProducts()
})
</script>

<style scoped>
.home-view {
  position: relative;
  padding: 20px 0;
}

.background-gradient {
  position: absolute;
  top: -40px;
  left: 0;
  right: 0;
  height: 500px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(16, 185, 129, 0.1));
  z-index: -1;
  transform: skewY(-6deg);
  transform-origin: top left;
}

.banner {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  padding: 60px 20px;
  border-radius: 16px;
  text-align: center;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="0" cy="0" r="20" fill="rgba(255,255,255,0.1)"/></svg>') 0 0/50px 50px;
  opacity: 0.5;
}

.banner-title {
  font-size: 36px;
  margin-bottom: 16px;
  font-weight: 700;
}

.banner-subtitle {
  font-size: 18px;
  margin-bottom: 32px;
  opacity: 0.9;
}

.banner-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 25px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background-color: white;
  color: var(--primary-color);
}

.action-btn.secondary {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.latest-products {
  margin-bottom: 60px;
}

.latest-products h2,
.categories h2 {
  font-size: 28px;
  margin-bottom: 24px;
  color: var(--text-primary);
  position: relative;
  display: inline-block;
}

.latest-products h2::after,
.categories h2::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
  border-radius: 3px;
}

.category-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.category-item {
  background-color: var(--background-white);
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.category-item:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
  border-color: transparent;
}

.category-item i {
  font-size: 32px;
  margin-bottom: 12px;
  color: var(--primary-color);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-text-fill-color: transparent;
}

.category-item span {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-primary);
}

.empty-state {
  background-color: var(--background-white);
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  color: var(--text-light);
  border: 2px dashed rgba(0, 0, 0, 0.1);
}
</style>