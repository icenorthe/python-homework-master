<template>
  <div class="my-products-view">
    <div class="page-header">
      <h1 class="page-title">我的商品</h1>
      <router-link to="/add-product" class="el-button el-button--primary">
        发布新商品
      </router-link>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="products.length === 0" class="empty-state">
      <p>您还没有发布任何商品</p>
      <router-link to="/add-product" class="el-button el-button--primary">
        立即发布
      </router-link>
    </div>
    
    <div v-else class="products-list">
      <el-table :data="products" style="width: 100%">
        <el-table-column label="商品图片" width="120">
          <template #default="scope">
            <div class="product-image">
              <img 
                v-if="scope.row.images && scope.row.images.length > 0" 
                :src="getImageUrl(scope.row.images[0])" 
                :alt="scope.row.title"
                @error="handleImageError"
              >
              <div v-else class="no-image">无图片</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="title" label="商品名称" min-width="180" />
        
        <el-table-column prop="price" label="价格" width="120">
          <template #default="scope">
            ¥{{ scope.row.price }}
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="发布时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <router-link :to="`/product/${scope.row.id}`" class="el-button el-button--text">
              查看
            </router-link>
            <router-link :to="`/edit-product/${scope.row.id}`" class="el-button el-button--text">
              编辑
            </router-link>
            <el-button 
              type="text" 
              @click="handleDelete(scope.row)" 
              class="delete-button"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="30%"
    >
      <p>确定要删除商品 "{{ currentProduct?.title }}" 吗？此操作不可恢复。</p>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="confirmDelete" :loading="deleteLoading">
            确认删除
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { productApi, getImageUrl } from '../api/product'
import { useUserStore } from '../store/user'

const userStore = useUserStore()
const products = ref([])
const loading = ref(true)
const deleteDialogVisible = ref(false)
const deleteLoading = ref(false)
const currentProduct = ref(null)

const handleImageError = (e) => {
  e.target.src = ''
  e.target.parentElement.innerHTML = '<div class="no-image">图片加载失败</div>'
}

const fetchMyProducts = async () => {
  loading.value = true
  
  try {
    const response = await productApi.getProducts()
    
    if (response.code === 200) {
      // 过滤出属于当前用户的商品，同时处理可能的 user_id 或 userId 字段
      products.value = response.data.filter(product => {
        const productUserId = product.user_id || product.userId
        return productUserId === userStore.userId
      })
      
      if (products.value.length === 0) {
        console.log('未找到当前用户的商品，用户ID:', userStore.userId)
      }
    } else {
      console.error('获取商品列表失败:', response.message)
      products.value = []
    }
  } catch (error) {
    console.error('获取商品列表时发生错误:', error)
    products.value = []
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

const handleDelete = (product) => {
  currentProduct.value = product
  deleteDialogVisible.value = true
}

const confirmDelete = async () => {
  if (!currentProduct.value) return
  
  deleteLoading.value = true
  
  try {
    const response = await productApi.deleteProduct(currentProduct.value.id)
    
    if (response.code === 200) {
      ElMessage.success('商品已成功删除')
      // 从列表中移除已删除的商品
      products.value = products.value.filter(p => p.id !== currentProduct.value.id)
      deleteDialogVisible.value = false
    } else {
      ElMessage.error(response.message || '删除失败，请稍后再试')
    }
  } catch (error) {
    console.error('Delete error:', error)
    ElMessage.error('删除过程中发生错误，请稍后再试')
  } finally {
    deleteLoading.value = false
  }
}

onMounted(() => {
  fetchMyProducts()
})
</script>

<style scoped>
.my-products-view {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
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

.delete-button {
  color: #f56c6c;
}

.delete-button:hover {
  color: #f78989;
}
</style>