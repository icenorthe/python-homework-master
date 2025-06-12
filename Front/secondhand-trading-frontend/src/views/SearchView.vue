<template>
  <div class="search-view">
    <h1 class="page-title">搜索商品</h1>
    
    <div class="search-container">
      <el-input
        v-model="keyword"
        placeholder="输入关键词搜索商品"
        class="search-input"
        clearable
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">
            搜索
          </el-button>
        </template>
      </el-input>
    </div>
    
    <div class="search-results">
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>
      
      <div v-else-if="products.length === 0" class="empty-state">
        <p v-if="hasSearched">未找到匹配的商品，请尝试其他关键词</p>
        <p v-else>请输入关键词搜索商品</p>
      </div>
      
      <template v-else>
        <h2>搜索结果 ({{ products.length }})</h2>
        <el-row :gutter="20">
          <el-col v-for="product in products" :key="product.id" :xs="24" :sm="12" :md="8" :lg="6">
            <product-card :product="product" />
          </el-col>
        </el-row>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi } from '../api/product'
import ProductCard from '../components/ProductCard.vue'

const route = useRoute()
const router = useRouter()
const keyword = ref('')
const products = ref([])
const loading = ref(false)
const hasSearched = ref(false)

const handleSearch = async () => {
  if (!keyword.value.trim()) return
  
  loading.value = true
  hasSearched.value = true
  
  try {
    // 更新URL，但不触发路由变化
    router.push({
      path: '/search',
      query: { keyword: keyword.value }
    })
    
    const response = await productApi.searchProducts(keyword.value)
    if (response.code === 200) {
      products.value = response.data.products || []
    } else {
      console.error('Search failed:', response.message)
      products.value = []
    }
  } catch (error) {
    console.error('Error during search:', error)
    products.value = []
  } finally {
    loading.value = false
  }
}

// 从URL获取初始关键词并执行搜索
const initFromQuery = () => {
  const queryKeyword = route.query.keyword
  if (queryKeyword) {
    keyword.value = queryKeyword
    handleSearch()
  }
}

onMounted(() => {
  initFromQuery()
})
</script>

<style scoped>
.search-view {
  padding: 20px 0;
}

.search-container {
  margin-bottom: 30px;
}

.search-input {
  max-width: 600px;
}

.search-results {
  min-height: 300px;
}

.search-results h2 {
  margin-bottom: 20px;
  font-size: 18px;
  color: #606266;
}

.loading-container {
  padding: 20px;
  max-width: 800px;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  background-color: #f5f7fa;
  border-radius: 8px;
  color: #909399;
}
</style>