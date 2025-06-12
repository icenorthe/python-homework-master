import axios from 'axios'
import { getApiUrl } from '../config/api.js'

// 创建axios实例
const apiClient = axios.create({
  baseURL: getApiUrl(''),
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
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

// 响应拦截器：处理token过期
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

export const userApi = {
  // 用户注册
  register: async (data) => {
    try {
      const response = await apiClient.post('/auth/register', data)
      return response.data
    } catch (error) {
      console.error('Register API error:', error)
      return { code: 400, message: error.response?.data?.message || '注册失败，请稍后再试' }
    }
  },

  // 用户登录
  login: async (username, password) => {
    try {
      const response = await apiClient.post('/auth/login', {
        username,
        password
      })
      return response.data
    } catch (error) {
      console.error('Login API error:', error)
      return { code: 400, message: error.response?.data?.message || '登录失败，请稍后再试' }
    }
  }
}