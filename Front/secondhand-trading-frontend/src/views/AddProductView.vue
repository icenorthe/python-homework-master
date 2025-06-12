<template>
  <div class="add-product-view">
    <h1 class="page-title">发布新商品</h1>
    
    <el-form 
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
      
      <el-form-item label="商品图片" prop="images">
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
              请上传商品图片，最多5张，每张不超过5MB
            </div>
          </template>
        </el-upload>
      </el-form-item>
      
      <div class="form-actions">
        <el-button @click="$router.go(-1)">取消</el-button>
        <el-button type="primary" native-type="submit" :loading="loading">
          发布商品
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { productApi } from '../api/product'
import { useUserStore } from '../store/user'

const router = useRouter()
const userStore = useUserStore()
const productForm = ref(null)
const loading = ref(false)
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
  ],
  images: [
    { required: true, message: '请上传至少一张商品图片', trigger: 'change' }
  ]
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
    ElMessage.error('请先登录后再发布商品')
    router.push('/login')
    return
  }
  
  await productForm.value.validate(async (valid) => {
    if (!valid) return
    
    if (imageFiles.value.length === 0) {
      ElMessage.warning('请上传至少一张商品图片')
      return
    }
    
    loading.value = true
    
    try {
      const formDataToSend = new FormData()
      
      // 创建商品数据对象
      const productDto = {
        title: formData.title,
        price: Number(formData.price).toFixed(2),
        description: formData.description,
        // 同时设置user_id和userId以确保兼容性
        user_id: userStore.userId,
        // userId: userStore.userId
      }
      
      console.log('发送的商品数据:', productDto)
      
      // 将商品数据作为JSON字符串添加到FormData
      formDataToSend.append('productDto', new Blob([JSON.stringify(productDto)], {
        type: 'application/json'
      }))
      
      // 添加所有图片文件
      if (imageFiles.value.length > 0) {
        imageFiles.value.forEach(file => {
          formDataToSend.append('images', file)
        })
      }
      
      console.log('发送的数据:', {
        productDto,
        imageCount: imageFiles.value.length
      })
      
      const response = await productApi.addProduct(formDataToSend)
      
      if (response.code === 200) {
        ElMessage.success('商品发布成功')
        router.push('/my-products')
      } else {
        ElMessage.error(response.message || '发布失败，请稍后再试')
      }
    } catch (error) {
      console.error('Add product error:', error)
      ElMessage.error('发布过程中发生错误，请稍后再试')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.add-product-view {
  padding: 20px 0;
  max-width: 800px;
  margin: 0 auto;
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