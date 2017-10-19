import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App'
import VueResource from 'vue-resource'
import VueWebsocket from "vue-websocket"
import VueUploader from "vue-uploader"
Vue.use(VueWebsocket)

Vue.use(VueResource)
Vue.use(VueRouter)

/* eslint-disable no-new */
new Vue({
  el: 'body',
  components: { App }
})

try {
  Vue.http.options.root = require('../.config').backendServer
} catch(err) {
  Vue.http.options.root = ''
  console.log('kkkkkk')
}


var router = new VueRouter({
  hashbang: false,
  history: true,
  saveScrollPosition: true,
  transitionOnLoad: true
})

