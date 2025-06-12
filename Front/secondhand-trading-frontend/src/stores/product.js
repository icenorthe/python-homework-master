import { defineStore } from 'pinia'
import { productApi } from '../api/product'

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [],
    currentProduct: null,
    loading: false,
    error: null
  }),

  actions: {
    async searchProducts(keyword) {
      this.loading = true
      this.error = null
      try {
        const response = await productApi.searchProducts(keyword)
        if (response.code === 200) {
          return response.data || []
        }
        throw new Error(response.message)
      } catch (error) {
        this.error = error.message
        return []
      } finally {
        this.loading = false
      }
    },

    async getProductDetail(productId) {
      this.loading = true
      this.error = null
      try {
        const response = await productApi.getProductDetail(productId)
        if (response.code === 200) {
          this.currentProduct = response.data
          return response.data
        }
        throw new Error(response.message)
      } catch (error) {
        this.error = error.message
        return null
      } finally {
        this.loading = false
      }
    },

    async getUserProducts(userId) {
      this.loading = true
      this.error = null
      try {
        const response = await productApi.getUserProducts(userId)
        if (response.code === 200) {
          this.products = response.data || []
          return this.products
        }
        throw new Error(response.message)
      } catch (error) {
        this.error = error.message
        this.products = []
        return []
      } finally {
        this.loading = false
      }
    }
  }
}) 