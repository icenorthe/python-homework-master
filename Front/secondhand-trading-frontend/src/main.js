import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/main.css'

const app = createApp(App)

// 全局挂载$http (Vue 3方式)

// 使用插件
app.use(router)
app.use(createPinia())
app.use(ElementPlus)

// 挂载应用
app.mount('#app')