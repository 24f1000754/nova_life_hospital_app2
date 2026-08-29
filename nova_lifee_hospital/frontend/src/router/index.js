import { createRouter, createWebHistory } from 'vue-router'

import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import DoctorDashboard from '../components/DoctorDashboard.vue'
import PatientDashboard from '../components/PatientDashboard.vue'
import EditProfile from '../components/EditProfile.vue'



const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  

  { path: '/edit-profile', component: EditProfile },

  { path: '/admin', component: AdminDashboard },
  { path: '/doctor', component: DoctorDashboard },
  { path: '/patient', component: PatientDashboard },

  {
    path: "/doctor/treatment/:id",
    name: "DoctorTreatment",
    component: () => import("../components/DoctorTreatment.vue")
  },

  {
    path:"/doctor/edit-profile",
    component:()=>import("../components/DoctorEditProfile.vue")
  }


]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
