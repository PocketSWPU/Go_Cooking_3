import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import DishDetail from '@/views/DishDetail.vue'
import AddDish from '@/views/AddDish.vue'
import Materials from '@/views/Materials.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/dish/:id',
    name: 'DishDetail',
    component: DishDetail,
    props: true
  },
  {
    path: '/add',
    name: 'AddDish',
    component: AddDish
  },
  {
    path: '/materials',
    name: 'Materials',
    component: Materials
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router