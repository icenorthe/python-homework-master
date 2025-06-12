import {
  createOrder,
  updateOrderStatus,
  getOrderDetail,
  getBuyerOrders,
  getSellerOrders,
  deleteOrder
} from '@/api/order'

const state = {
  orderList: [],
  currentOrder: null,
  loading: false
}

const mutations = {
  SET_ORDER_LIST(state, orders) {
    state.orderList = orders
  },
  SET_CURRENT_ORDER(state, order) {
    state.currentOrder = order
  },
  SET_LOADING(state, status) {
    state.loading = status
  }
}

const actions = {
  // 创建订单
  async createOrder({ commit }, orderData) {
    try {
      commit('SET_LOADING', true)
      const response = await createOrder(orderData)
      return response
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 更新订单状态
  async updateOrderStatus({ commit }, { orderId, status }) {
    try {
      commit('SET_LOADING', true)
      const response = await updateOrderStatus(orderId, { status })
      return response
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取订单详情
  async getOrderDetail({ commit }, orderId) {
    try {
      commit('SET_LOADING', true)
      const response = await getOrderDetail(orderId)
      commit('SET_CURRENT_ORDER', response.data)
      return response
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取买家订单列表
  async getBuyerOrders({ commit }, { buyerId, status }) {
    try {
      commit('SET_LOADING', true)
      const response = await getBuyerOrders(buyerId, status)
      commit('SET_ORDER_LIST', response.data)
      return response
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 获取卖家订单列表
  async getSellerOrders({ commit }, { sellerId, status }) {
    try {
      commit('SET_LOADING', true)
      const response = await getSellerOrders(sellerId, status)
      commit('SET_ORDER_LIST', response.data)
      return response
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 删除订单
  async deleteOrder({ commit }, orderId) {
    try {
      commit('SET_LOADING', true)
      const response = await deleteOrder(orderId)
      return response
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const getters = {
  orderList: state => state.orderList,
  currentOrder: state => state.currentOrder,
  loading: state => state.loading
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 