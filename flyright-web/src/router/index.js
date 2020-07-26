import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from '../views/Landing.vue'
// import store from '../store/store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: Landing,
    meta: {
      title: 'Flyright',
    }
  }
]

const router = new VueRouter({
  routes
})

export default router
