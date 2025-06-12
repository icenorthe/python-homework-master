<template>
  <div class="my-orders-view">
    <h1 class="page-title">我的订单</h1>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="orders.length === 0" class="empty-state">
      <p>您还没有任何订单</p>
      <router-link to="/search" class="el-button el-button--primary">
        去购物
      </router-link>
    </div>
    
    <div v-else class="orders-list">
      <el-table :data="orders" style="width: 100%">
        <el-table-column label="商品图片" width="120">
          <template #default="scope">
            <div class="product-image">
              <img 
                v-if="scope.row.product && scope.row.product.images && scope.row.product.images.length > 0" 
                :src="scope.row.product.images[0]" 
                :alt="scope.row.product.title"
              >
              <div v-else class="no-image">无图片</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="商品名称" min-width="180">
          <template #default="scope">
            <router-link 
              :to="`/product/${scope.row.product_id}`" 
              class="product-link"
            >
              {{ scope.row.product ? scope.row.product.title : '商品已删除' }}
            </router-link>
          </template>
        </el-table-column>
        
        <el-table-column label="价格" width="120">
          <template #default="scope">
            <span v-if="scope.row.product">¥{{ scope.row.product.price }}</span>
            <span v-else>--</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="购买时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="phone" label="联系电话" width="150" />
        
        <el-table-column label="卖家" width="150">
          <template #default="scope">
            <span v-if="scope.row.product && scope.row.product.user">
              {{ scope.row.product.user.username }}
            </span>
            <span v-else>--</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { orderApi } from '../api/order'

const orders = ref([])
const loading = ref(true)

const fetchMyOrders = async () => {
  loading.value = true
  
  try {
    const response = await orderApi.getMyOrders()
    
    if (response.code === 200) {
      orders.value = response.data || []
    } else {
      console.error('Failed to fetch orders:', response.message)
      orders.value = []
    }
  } catch (error) {
    console.error('Error fetching orders:', error)
    orders.value = []
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return dateString
  
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchMyOrders()
})
</script>

<style scoped>
.my-orders-view {
  padding: 20px 0;
}

.loading-container {
  padding: 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.empty-state p {
  margin-bottom: 20px;
  color: #909399;
  font-size: 16px;
}

.product-image {
  width: 80px;
  height: 80px;
  overflow: hidden;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  color: #909399;
  font-size: 12px;
}

.product-link {
  color: #409EFF;
  text-decoration: none;
}

.product-link:hover {
  text-decoration: underline;
}
</style>