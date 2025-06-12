<template>
  <div class="edit-product-view">
    <h1 class="page-title">编辑商品</h1>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="!product" class="error-container">
      <h2>商品不存在或已被删除</h2>
      <router-link to="/my-products" class="el-button el-button--primary">返回我的商品</router-link>
    </div>
    
    <el-form 
      v-else
      ref="productForm" 
      :model="formData" 
      :rules="formRules" 
      label-position="top"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="商品标题" prop="title">
        <el-input v-model="formData.title" placeholder="请输入商品标题"></el-input>
      </el-form-item>
      
      <el-form-item label="商品价格" prop="price">
        <el-input-number 
          v-model="formData.price" 
          :min="0.01" 
          :precision="2" 
          :step="0.01"
          style="width: 100%;"
        ></el-input-number>
      </el-form-item>
      
      <el-form-item label="商品描述" prop="description">
        <el-input 
          v-model="formData.description" 
          type="textarea" 
          :rows="4"
          placeholder="请详细描述商品的情况、成色等信息"
        ></el-input>
      </el-form-item>
      
      <el-form-item label="当前商品图片">
        <div class="current-images" v-if="product.images && product.images.length > 0">
          <div v-for="(image, index) in product.images" :key="index" class="current-image-item">
            <img :src="image" :alt="`商品图片${index + 1}`" class="current-image" />
          </div>
        </div>
        <div v-else class="no-images">暂无图片</div>
      </el-form-item>
      
      <el-form-item label="上传新图片（如需更换）" prop="images">
        <el-upload
          class="product-uploader"
          action="#"
          list-type="picture-card"
          :auto-upload="false"
          :limit="5"
          :on-change="handleImageChange"
          :on-remove="handleImageRemove"
        >
          <el-icon><Plus /></el-icon>
          <template #tip>
            <div class="el-upload__tip">
              上传新图片将替换原有图片，最多5张，每张不超过5MB
            </div>
          </template>
        </el-upload>
      </el-form-item>
      
      <div class="form-actions">
        <el-button @click="$router.go(-1)">取消</el-button>
        <el-button type="primary" native-type="submit" :loading="submitting">
          保存修改
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { productApi } from '../api/product'
import { useUserStore } from '../store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const productForm = ref(null)
const loading = ref(true)
const submitting = ref(false)
const product = ref(null)
const imageFiles = ref([])

const formData = reactive({
  title: '',
  price: 0,
  description: '',
  images: []
})

const formRules = {
  title: [
    { required: true, message: '请输入商品标题', trigger: 'blur' },
    { min: 2, max: 50, message: '标题长度应为2-50个字符', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入商品价格', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '价格必须大于0', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入商品描述', trigger: 'blur' },
    { min: 10, max: 1000, message: '描述长度应为10-1000个字符', trigger: 'blur' }
  ]
}

const fetchProductDetail = async () => {
  loading.value = true
  try {
    // 检查用户登录状态
    if (!userStore.isLoggedIn || !userStore.userId) {
      ElMessage.error('请先登录')
      router.push('/login')
      return
    }

    const productId = route.params.id
    const response = await productApi.getProductDetail(productId)
    
    if (response.code === 200 && response.data) {
      product.value = response.data
      
      // 检查是否是当前用户的商品
      const productUserId = product.value.userId || product.value.user_id
      if (productUserId !== userStore.userId) {
        ElMessage.error('您没有权限修改此商品')
        router.push('/my-products')
        return
      }
      
      // 填充表单数据
      formData.title = product.value.title || ''
      formData.price = product.value.price || 0
      formData.description = product.value.description || ''

      console.log('获取到的商品数据:', {
        product: product.value,
        currentUserId: userStore.userId,
        productUserId
      })
    } else {
      product.value = null
      ElMessage.error('商品不存在或已被删除')
      router.push('/my-products')
    }
  } catch (error) {
    console.error('Error fetching product:', error)
    product.value = null
    ElMessage.error('获取商品信息失败')
    router.push('/my-products')
  } finally {
    loading.value = false
  }
}

const handleImageChange = (file, fileList) => {
  // 更新图片文件列表
  imageFiles.value = fileList.map(item => item.raw)
  formData.images = fileList
}

const handleImageRemove = (file, fileList) => {
  // 更新图片文件列表
  imageFiles.value = fileList.map(item => item.raw)
  formData.images = fileList
}

const handleSubmit = async () => {
  if (!productForm.value) return
  
  // 检查用户登录状态和用户ID
  if (!userStore.isLoggedIn || !userStore.userId) {
    ElMessage.error('请先登录后再修改商品')
    router.push('/login')
    return
  }
  
  await productForm.value.validate(async (valid) => {
    if (!valid) return
    
    submitting.value = true
    
    try {
      const formDataToSend = new FormData()
      
      // 创建商品数据对象，确保使用原始商品的userId
      const productDto = {
        id: product.value.id,
        title: formData.title,
        price: Number(formData.price).toFixed(2),
        description: formData.description,
        userId: product.value.userId, // 使用原始商品的userId
        user_id: product.value.userId, // 后端可能使用user_id
        status: product.value.status || 'available' // 保持原有状态
      }
      
      // 将商品数据作为JSON字符串添加到FormData
      formDataToSend.append('productDto', new Blob([JSON.stringify(productDto)], {
        type: 'application/json'
      }))
      
      // 如果有新上传的图片，添加到表单数据中
      if (imageFiles.value.length > 0) {
        imageFiles.value.forEach(file => {
          formDataToSend.append('images', file)
        })
      }
      
      console.log('发送的数据:', {
        productDto,
        imageCount: imageFiles.value.length,
        originalUserId: product.value.userId,
        currentUserId: userStore.userId
      })
      
      const response = await productApi.updateProduct(product.value.id, formDataToSend)
      
      if (response.code === 200) {
        ElMessage.success('商品修改成功')
        router.push('/my-products')
      } else {
        ElMessage.error(response.message || '修改失败，请稍后再试')
      }
    } catch (error) {
      console.error('Update product error:', error)
      ElMessage.error('修改过程中发生错误，请稍后再试')
    } finally {
      submitting.value = false
    }
  })
}

onMounted(() => {
  fetchProductDetail()
})
</script>

<style scoped>
.edit-product-view {
  padding: 20px 0;
  max-width: 800px;
  margin: 0 auto;
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

.current-images {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.current-image-item {
  width: 120px;
  height: 120px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  overflow: hidden;
}

.current-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-images {
  color: #909399;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 6px;
  text-align: center;
}

.product-uploader {
  width: 100%;
}

.product-uploader :deep(.el-upload--picture-card) {
  width: 120px;
  height: 120px;
  line-height: 120px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 30px;
}
</style>