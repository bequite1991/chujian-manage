import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import './style.css'
import App from './App.vue'

// 页面组件
import Dashboard from './pages/Dashboard.vue'
import Products from './pages/Products.vue'
import StockIn from './pages/StockIn.vue'
import StockOut from './pages/StockOut.vue'
import Alerts from './pages/Alerts.vue'
import Suppliers from './pages/Suppliers.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard },
  { path: '/products', component: Products },
  { path: '/stock-in', component: StockIn },
  { path: '/stock-out', component: StockOut },
  { path: '/alerts', component: Alerts },
  { path: '/suppliers', component: Suppliers },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

createApp(App).use(router).mount('#app')
