import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => {
    const userJson = localStorage.getItem('user')
    const user = userJson ? JSON.parse(userJson) : null
    return {
      user: user,
      userId: user ? user.id : null
    }
  },

  getters: {
    isLoggedIn: (state) => !!state.user,
    userInfo: (state) => state.user
  },

  actions: {
    setUser(user) {
      this.user = user
      this.userId = user ? user.id : null
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
      } else {
        localStorage.removeItem('user')
      }
    },

    logout() {
      this.user = null
      this.userId = null
      localStorage.removeItem('user')
    }
  }
}) 