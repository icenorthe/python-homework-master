import { defineStore } from 'pinia'
import {
  createOrder,
  updateOrderStatus,
  getOrderDetail,
  getBuyerOrders,
  getSellerOrders,
  deleteOrder
} from '@/api/order'

export const useOrderStore = defineStore('order', {
  state: () => ({
    orderList: [],
    currentOrder: null,
    loading: false
  }),

  actions: {
    // 创建订单
    async createOrder(orderData) {
      this.loading = true
      try {
        const response = await createOrder(orderData)
        return response.data.data
      } finally {
        this.loading = false
      }
    },

    // 更新订单状态
    async updateOrderStatus({ orderId, status }) {
      if (!orderId) {
        throw new Error('订单ID不能为空')
      }
      this.loading = true
      try {
        const response = await updateOrderStatus(parseInt(orderId, 10), { status })
        return response.data.data
      } finally {
        this.loading = false
      }
    },

    // 获取订单详情
    async getOrderDetail(orderId) {
      if (!orderId) {
        throw new Error('订单ID不能为空')
      }
      this.loading = true
      try {
        const response = await getOrderDetail(parseInt(orderId, 10))
        this.currentOrder = response.data.data
        return response.data.data
      } finally {
        this.loading = false
      }
    },

    // 获取买家订单列表
    async getBuyerOrders({ buyerId, status }) {
      if (!buyerId) {
        throw new Error('买家ID不能为空')
      }
      console.log('Store: 开始获取买家订单', { buyerId, status })
      this.loading = true
      try {
        // 只在status有值时才传递
        const params = status ? { buyerId: parseInt(buyerId, 10), status } : { buyerId: parseInt(buyerId, 10) }
        const response = await getBuyerOrders(params.buyerId, params.status)
        console.log('Store: 买家订单响应', response.data)
        this.orderList = response.data.data || []
        return response.data.data
      } catch (error) {
        console.error('Store: 获取买家订单失败', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 获取卖家订单列表
    async getSellerOrders({ sellerId, status }) {
      if (!sellerId) {
        throw new Error('卖家ID不能为空')
      }
      console.log('Store: 开始获取卖家订单', { sellerId, status })
      this.loading = true
      try {
        // 只在status有值时才传递
        const params = status ? { sellerId: parseInt(sellerId, 10), status } : { sellerId: parseInt(sellerId, 10) }
        const response = await getSellerOrders(params.sellerId, params.status)
        console.log('Store: 卖家订单响应', response.data)
        this.orderList = response.data.data || []
        return response.data.data
      } catch (error) {
        console.error('Store: 获取卖家订单失败', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 删除订单
    async deleteOrder(orderId) {
      if (!orderId) {
        throw new Error('订单ID不能为空')
      }
      this.loading = true
      try {
        const response = await deleteOrder(parseInt(orderId, 10))
        return response.data.data
      } finally {
        this.loading = false
      }
    }
  }
}) 