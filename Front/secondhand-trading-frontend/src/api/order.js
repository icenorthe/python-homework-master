import axios from 'axios'
import { API_CONFIG } from '../config/api.js'

const BASE_URL = API_CONFIG.BASE_URL

// 创建新订单
export function createOrder(data) {
  return axios.post(`${BASE_URL}/api/orders`, data)
}

// 更新订单状态
export function updateOrderStatus(orderId, data) {
  return axios.put(`${BASE_URL}/api/orders/${orderId}/status`, data)
}

// 获取订单详情
export function getOrderDetail(orderId) {
  return axios.get(`${BASE_URL}/api/orders/${orderId}`)
}

// 获取买家订单列表
export function getBuyerOrders(buyerId, status) {
  console.log('调用买家订单API, buyerId:', buyerId, 'status:', status)
  return axios.get(`${BASE_URL}/api/orders/buyer/${buyerId}`, {
    params: { status }
  })
}

// 获取卖家订单列表
export function getSellerOrders(sellerId, status) {
  console.log('调用卖家订单API, sellerId:', sellerId, 'status:', status)
  return axios.get(`${BASE_URL}/api/orders/seller/${sellerId}`, {
    params: { status }
  })
}

// 删除订单
export function deleteOrder(orderId) {
  return axios.delete(`${BASE_URL}/api/orders/${orderId}`, {
    data: orderId
  })
}

export function orderApi(){
  return
}