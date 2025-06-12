export const API_CONFIG = {
  BASE_URL: 'http://localhost:8081',
  API_PREFIX: '/api',
  FRONTEND_URL: 'http://localhost:3000'
}

// 获取完整的API URL
export const getApiUrl = (path) => {
  // 如果path已经包含/api前缀，则不再添加
  const prefix = path.startsWith('/api') ? '' : API_CONFIG.API_PREFIX
  return `${API_CONFIG.BASE_URL}${prefix}${path}`
} 