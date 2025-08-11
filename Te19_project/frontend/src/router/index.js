import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomeView.vue'
import Insights from '../views/InsightsView.vue'
import Parking from '../views/ParkingView.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/insights', name: 'Insights', component: Insights },
  { path: '/parking', name: 'Parking', component: Parking }
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
    