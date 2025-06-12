<template>
  <div class="product-card" @click="navigateToDetail">
    <div class="product-image">
      <img 
        v-if="hasValidImage"
        :src="imageUrl" 
        :alt="product.title"
        @error="handleImageError"
      >
      <div v-else class="no-image">暂无图片</div>
    </div>
    <div class="product-info">
      <h3 class="product-title">{{ product.title || '未知商品' }}</h3>
      <p class="product-price">¥{{ product.price || '0.00' }}</p>
      <p class="product-date">{{ formatDate(product.created_at) }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getImageUrl } from '../api/product'
import { ElMessage } from 'element-plus'

const props = defineProps({
  product: {
    type: Object,
    required: true,
    validator: (value) => {
      return value && typeof value === 'object' && 'id' in value
    }
  }
})

const router = useRouter()
const showNoImage = ref(false)

const hasValidImage = computed(() => {
  return !showNoImage.value && 
         props.product.images && 
         props.product.images.length > 0
})

const imageUrl = computed(() => {
  if (!hasValidImage.value) return ''
  return getImageUrl(props.product.images[0])
})

const navigateToDetail = () => {
  if (!props.product || !props.product.id) {
    console.error('无效的商品ID:', props.product)
    ElMessage.error('商品信息不完整')
    return
  }
  router.push(`/product/${props.product.id}`)
}

const handleImageError = () => {
  console.error('图片加载失败:', imageUrl.value)
  showNoImage.value = true
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return dateString
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
</script>

<style scoped>
.product-card {
  background: var(--background-white);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
  border-color: transparent;
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background-color: var(--background-light);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.no-image {
  color: var(--text-light);
  font-size: 14px;
  padding: 20px;
  text-align: center;
  background: linear-gradient(135deg, var(--background-light), var(--background-white));
}

.product-info {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--background-white);
}

.product-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
}

.product-price {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-color);
  margin: 0 0 8px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.product-date {
  font-size: 12px;
  color: var(--text-light);
  margin: 0;
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}
</style>