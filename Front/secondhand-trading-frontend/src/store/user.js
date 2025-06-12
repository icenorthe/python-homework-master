import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '../api/user'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  
  // 计算属性
  const isLoggedIn = computed(() => !!user.value)
  const userId = computed(() => {
    if (!user.value) return null
    // 确保返回正确的用户ID，优先使用user_id
    return user.value.user_id || user.value.userId || user.value.id
  })
  
  // 方法
  const login = async (username, password) => {
    try {
      const response = await userApi.login(username, password)
      if (response.code === 200) {
        const userData = {
          ...response.data,
          // 确保同时设置user_id和userId
          user_id: response.data.user_id || response.data.userId || response.data.id,
          userId: response.data.user_id || response.data.userId || response.data.id
        }
        user.value = userData
        localStorage.setItem('user', JSON.stringify(userData))
        return { success: true }
      } else {
        return { success: false, message: response.message }
      }
    } catch (error) {
      console.error('Login error:', error)
      return { success: false, message: '登录失败，请稍后再试' }
    }
  }
  
  const register = async (data) => {
    try {
      const response = await userApi.register(data)
      return { 
        success: response.code === 200, 
        message: response.message 
      }
    } catch (error) {
      console.error('Register error:', error)
      return { success: false, message: '注册失败，请稍后再试' }
    }
  }
  
  const logout = () => {
    user.value = null
    localStorage.removeItem('user')
  }
  
  return {
    user,
    isLoggedIn,
    userId,
    login,
    register,
    logout
  }
})