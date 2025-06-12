<template>
  <div class="product-detail-view">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!product" class="error-container">
      <h2>商品不存在或已被删除</h2>
      <router-link to="/" class="el-button el-button--primary">返回首页</router-link>
    </div>
    
    <template v-else>
      <div class="product-container">
        <div class="product-gallery">
          <el-carousel v-if="product.images && product.images.length > 0" height="400px">
            <el-carousel-item v-for="(image, index) in product.images" :key="index">
              <img 
                :src="typeof image === 'string' ? getImageUrl(image) : getImageUrl(image.url)" 
                :alt="product.title" 
                class="carousel-image"
                @error="handleImageError"
              >
            </el-carousel-item>
          </el-carousel>
          
          <div v-else class="no-image">
            <span>暂无图片</span>
          </div>
        </div>
        
        <div class="product-info">
          <h1 class="product-title">{{ product.title }}</h1>
          
          <div class="product-price">
            <span class="price-label">价格：</span>
            <span class="price-value">¥{{ product.price }}</span>
          </div>
          
          <div class="product-date">
            <span class="date-label">发布时间：</span>
            <span>{{ formatDate(product.created_at) }}</span>
          </div>
          
          <div class="product-description">
            <h3>商品描述</h3>
            <p>{{ product.description || '暂无描述' }}</p>
          </div>
          
          <div class="product-actions">
            <el-button 
              type="primary" 
              size="large" 
              @click="showBuyDialog" 
              :disabled="isOwner || !isLoggedIn"
            >
              {{ isOwner ? '这是您发布的商品' : (isLoggedIn ? '立即购买' : '登录后购买') }}
            </el-button>
            
            <div v-if="isOwner" class="owner-actions">
              <router-link :to="`/edit-product/${product.id}`" class="el-button">
                编辑商品
              </router-link>
              <el-button type="danger" @click="showDeleteConfirm">
                删除商品
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <!-- 购买对话框 -->
    <el-dialog
      v-model="buyDialogVisible"
      title="确认购买"
      width="30%"
    >
      <el-form :model="orderForm" :rules="orderRules" ref="orderFormRef">
        <p class="dialog-product-info">
          {{ product?.title }} - ¥{{ product?.price }}
        </p>
        
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="orderForm.phone" placeholder="请输入您的联系电话"></el-input>
        </el-form-item>
        
        <p class="dialog-note">
          提交订单后，卖家将通过您提供的电话与您联系。
        </p>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="buyDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmBuy" :loading="buyLoading">
            确认购买
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="30%"
    >
      <p>确定要删除商品 "{{ product?.title }}" 吗？此操作不可恢复。</p>
      
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productApi, getImageUrl } from '../api/product'
import { createOrder } from '../api/order'
import { useUserStore } from '../store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const product = ref(null)
const loading = ref(true)
const buyDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const buyLoading = ref(false)
const deleteLoading = ref(false)
const orderFormRef = ref(null)

const orderForm = ref({
  phone: ''
})

const orderRules = {
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码', trigger: 'blur' }
  ]
}

const isLoggedIn = computed(() => userStore.isLoggedIn)
const isOwner = computed(() => {
  if (!product.value || !userStore.userId) return false
  const productUserId = product.value.user_id || product.value.userId
  return productUserId === userStore.userId
})

const fetchProductDetail = async () => {
  loading.value = true
  try {
    const productId = route.params.id
    const response = await productApi.getProductDetail(productId)
    
    if (response.code === 200 && response.data) {
      product.value = processImages(response.data)
      console.log('处理后的商品数据:', product.value)
    } else {
      product.value = null
      console.error('商品不存在')
    }
  } catch (error) {
    console.error('请求失败:', error)
    product.value = null
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

const showBuyDialog = () => {
  if (!isLoggedIn.value) {
    ElMessageBox.confirm(
      '请先登录后再购买商品',
      '提示',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'info'
      }
    ).then(() => {
      router.push('/login')
    }).catch(() => {})
    return
  }
  
  buyDialogVisible.value = true
}

const confirmBuy = async () => {
  if (!orderFormRef.value) return
  
  await orderFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    buyLoading.value = true
    
    try {
      const response = await createOrder(product.value.id, orderForm.value.phone)
      
      if (response.code === 200) {
        ElMessage.success('购买成功，卖家将会联系您')
        buyDialogVisible.value = false
        orderForm.value.phone = ''
      } else {
        ElMessage.error(response.message || '购买失败，请稍后再试')
      }
    } catch (error) {
      console.error('Buy error:', error)
      ElMessage.error('购买过程中发生错误，请稍后再试')
    } finally {
      buyLoading.value = false
    }
  })
}

const showDeleteConfirm = () => {
  deleteDialogVisible.value = true
}

const confirmDelete = async () => {
  deleteLoading.value = true
  
  try {
    const response = await productApi.deleteProduct(product.value.id)
    
    if (response.code === 200) {
      ElMessage.success('商品已成功删除')
      router.push('/my-products')
    } else {
      ElMessage.error(response.message || '删除失败，请稍后再试')
    }
  } catch (error) {
    console.error('Delete error:', error)
    ElMessage.error('删除过程中发生错误，请稍后再试')
  } finally {
    deleteLoading.value = false
    deleteDialogVisible.value = false
  }
}

const handleImageError = (e) => {
  console.error('图片加载失败:', e.target.src)
  e.target.src = '/default-image.png'
}

const processImages = (productData) => {
  if (productData.images) {
    if (!Array.isArray(productData.images)) {
      productData.images = [productData.images]
    }
    productData.images = productData.images.map(img => {
      if (typeof img === 'string') return img
      return img.url || img.path || img.filename || ''
    })
  }
  return productData
}

onMounted(() => {
  fetchProductDetail()
})
</script>

<style scoped>
.product-detail-view {
  padding: 20px 0;
}

.loading-container,
.error-container {
  padding: 40px;
  text-align: center;
}

.error-container h2 {
  margin-bottom: 20px;
  color: #f56c6c;
}

.product-container {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.product-gallery {
  flex: 1;
  min-width: 300px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.no-image {
  height: 400px;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 16px;
}

.product-info {
  flex: 1;
  min-width: 300px;
}

.product-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.product-price {
  margin-bottom: 15px;
}

.price-label {
  font-size: 16px;
  color: #606266;
}

.price-value {
  font-size: 28px;
  color: #f56c6c;
  font-weight: bold;
}

.product-date {
  margin-bottom: 20px;
  color: #909399;
}

.date-label {
  color: #606266;
}

.product-description {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.product-description h3 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #303133;
}

.product-description p {
  color: #606266;
  line-height: 1.6;
}

.product-actions {
  margin-top: 30px;
}

.owner-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.dialog-product-info {
  font-size: 16px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.dialog-note {
  font-size: 12px;
  color: #909399;
  margin-top: 10px;
}
</style>