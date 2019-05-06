import Vue from 'vue'
import Router from 'vue-router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import API from '@/mixins/API'


const routerOptions = [
  { path: '/', view: 'LandingPage',
    meta: { mustBeLoggedOut: true} },
  { path: '/login', view: 'LoginPage',
    meta: { mustBeLoggedOut: true} },
  { path: '/flightdetails', view: 'FlightDetailsPage',
    meta: { mustBeLoggedIn: true} },
  { path: '/newflight', view: 'NewFlightPage',
    meta: { mustBeLoggedIn: true} },
  { path: '/settings', view: 'SettingsPage',
    meta: { mustBeLoggedIn: true} },
  { path: '/homepage', view: 'HomePage',
    meta: { mustBeLoggedIn: true} },
  { path: '/drones', view: 'DronesPage',
    meta: { mustBeLoggedIn: true} },
  { path: '/flights', view: 'FlightsPage',
    meta: { mustBeLoggedIn: true} },
  { path: '/education', view: 'EducationPage',
    meta: { mustBeLoggedIn: true} },
  { path: '/dashboard', view: 'OfficialDashboardPage',
    meta: { mustBeLoggedIn: true} },
  { path: '/editflight', view: 'EditFlightPage',
    meta: { mustBeLoggedIn: true} },
  { path: '/privacy', view: 'PrivacyPage'}
]

const routes = routerOptions.map(route => {
  return {
    path: route.path,
    component: () => import(`@/views/${route.view}/${route.view}.vue`),
    meta: route.meta
  }
})

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes
})

router.beforeEach(async (to, from, next) => {
  if(to.meta.mustBeLoggedOut) {
    const access_token = window.localStorage.getItem('access_token')
    var api_data = API.data()
    var url = api_data.base_url + '/user/is_logged_in/'
    const response = await axios.get(url, {
      headers: {'Authorization': 'Bearer ' + access_token}
    });
    if (JSON.stringify(response.data) == 'true') {
      next('/homepage')
    }
  }

  if(to.meta.mustBeLoggedIn) {
    const access_token = window.localStorage.getItem('access_token')
    var api_data = API.data()
    var url = api_data.base_url + '/user/is_logged_in/'
    const response = await axios.get(url, {
      headers: {'Authorization': 'Bearer ' + access_token}
    });
    if (JSON.stringify(response.data) == 'false') {
      next('/')
    }
  }

  next()
})

export default router;
