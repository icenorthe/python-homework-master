import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue')
    },
    {
      path: '/product/:id',
      name: 'product-detail',
      component: () => import('../views/ProductDetailView.vue')
    },
    {
      path: '/my-products',
      name: 'my-products',
      component: () => import('../views/MyProductsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/add-product',
      name: 'add-product',
      component: () => import('../views/AddProductView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/edit-product/:id',
      name: 'edit-product',
      component: () => import('../views/EditProductView.vue'),
      meta: { requiresAuth: true }
    },
    // 订单相关路由
    {
      path: '/my-orders',
      name: 'my-orders',
      component: () => import('@/views/order/OrderList.vue'),
      meta: { title: '我的订单', requiresAuth: true }
    },
    {
      path: '/order/detail/:id',
      name: 'OrderDetail',
      component: () => import('@/views/order/OrderDetail.vue'),
      meta: { title: '订单详情', requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = JSON.parse(localStorage.getItem('user'))
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !userStore) {
    next('/login')
  } else {
    next()
  }
})

export default router