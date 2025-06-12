import axios from 'axios'
import { API_CONFIG, getApiUrl } from '../config/api.js'

// 获取图片完整URL的辅助函数
export const getImageUrl = (imageUrl) => {
  if (!imageUrl) {
    console.debug('getImageUrl: empty image URL')
    return ''
  }
  
  try {
    // 如果已经是完整URL则直接返回
    if (imageUrl.startsWith('http') || imageUrl.startsWith('https')) {
      return imageUrl
    }
    
    // 如果是 base64 数据
    if (imageUrl.startsWith('data:image')) {
      return imageUrl
    }    
    // 确保 imageUrl 不以斜杠开头
    const cleanImageUrl = imageUrl.startsWith('/') ? imageUrl.slice(1) : imageUrl
    
    // 返回完整的图片URL
    return `${API_CONFIG.BASE_URL}/${cleanImageUrl}`
    
  } catch (error) {
    console.error('Error in getImageUrl:', error)
    return ''
  }
}

// 规范化商品数据
const normalizeProduct = (product) => {
  return {
    id: product.productId,
    userId: product.userId,
    title: product.title,
    price: product.price,
    description: product.description,
    status: product.status,
    created_at: product.createdAt,
    images: product.images?.map(img => img.imageUrl) || []
  }
}

// 错误处理函数
const handleError = (error) => {
  console.error('API error:', error)
  const response = error.response || {}
  
  // 添加详细的错误日志
  if (error.response) {
    // 服务器响应了，但状态码不在 2xx 范围内
    console.error('Error response:', {
      status: error.response.status,
      data: error.response.data,
      headers: error.response.headers
    })
  } else if (error.request) {
    // 请求已经发出，但没有收到响应
    console.error('No response received:', error.request)
  } else {
    // 在设置请求时发生了错误
    console.error('Request error:', error.message)
  }

  return {
    code: response.status || 500,
    message: response.data?.message || error.message || '请求失败',
    data: null
  }
}

// 创建带基础配置的axios实例
const apiClient = axios.create({
  baseURL: getApiUrl(''),
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  // 添加超时设置
  timeout: 10000,
  // 添加重试配置
  retry: 3,
  retryDelay: 1000
})

// 请求拦截器：添加token
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// 添加请求重试拦截器
apiClient.interceptors.response.use(null, async error => {
  const config = error.config;
  
  // 如果配置了重试，且请求失败
  if (config.retry) {
    const backoff = new Promise(resolve => {
      setTimeout(() => {
        resolve();
      }, config.retryDelay || 1000);
    });
    
    // 设置重试次数
    config.retryCount = config.retryCount || 0;
    
    // 如果重试次数小于设置的重试次数
    if (config.retryCount < config.retry) {
      config.retryCount += 1;
      console.log(`Retrying request (${config.retryCount}/${config.retry})`);
      
      // 等待延迟时间后重试
      await backoff;
      return apiClient(config);
    }
  }
  
  return Promise.reject(error);
});

// 原有的响应拦截器
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const productApi = {
  // 上传商品（带多图上传）
  addProduct: async (formData) => {
    try {
      const response = await apiClient.post('/products', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return {
        code: response.data.code,
        message: response.data.message,
        data: response.data.data ? normalizeProduct(response.data.data) : null
      }
    } catch (error) {
      return handleError(error)
    }
  },

  // 获取商品列表
  getProducts: async (ids) => {
    try {
      const params = ids ? { ids: ids.join(',') } : {}
      const response = await apiClient.get('/products', { params })
      
      return {
        code: response.data.code,
        message: response.data.message,
        data: response.data.data?.map(normalizeProduct) || []
      }
    } catch (error) {
      return handleError(error)
    }
  },

  // 获取单个商品详情
  getProductDetail: async (id) => {
    try {
      const response = await apiClient.get(`/products/${id}`)
      return {
        code: response.data.code,
        message: response.data.message,
        data: response.data.data ? normalizeProduct(response.data.data) : null
      }
    } catch (error) {
      return handleError(error)
    }
  },

  // 搜索商品
  searchProducts: async (keyword) => {
    try {
      const response = await apiClient.get('/products/search', {
        params: { keyword }
      })
      
      return {
        code: response.data.code,
        message: response.data.message,
        data: {
          products: response.data.data?.map(normalizeProduct) || []
        }
      }
    } catch (error) {
      return handleError(error)
    }
  },

  // 修改商品
  updateProduct: async (id, formData) => {
    try {
      const response = await apiClient.put(`/products/${id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return {
        code: response.data.code,
        message: response.data.message,
        data: response.data.data ? normalizeProduct(response.data.data) : null
      }
    } catch (error) {
      return handleError(error)
    }
  },

  // 删除商品
  deleteProduct: async (id) => {
    try {
      const response = await apiClient.delete(`/products/${id}`, {
        params: { userId: JSON.parse(localStorage.getItem('user'))?.userId }
      })
      return response.data
    } catch (error) {
      return handleError(error)
    }
  }
}

// 获取认证头
const getAuthHeaders = () => {
  const token = localStorage.getItem('token')
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}