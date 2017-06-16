import Vue from 'vue'
import App from './App'
import VueResource from 'vue-resource'

Vue.use(VueResource)

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
