var path = require('path')
var express = require('express')
var webpack = require('webpack')
var config = require('../config')
var proxyMiddleware = require('http-proxy-middleware')
var webpackConfig = process.env.NODE_ENV === 'testing'
  ? require('./webpack.prod.conf')
  : require('./webpack.dev.conf')

// default port where dev server listens for incoming traffic
var port = process.env.PORT || config.dev.port
// Define HTTP proxies to your custom API backend
// https://github.com/chimurai/http-proxy-middleware
var proxyTable = config.dev.proxyTable

var app = express()
var compiler = webpack(webpackConfig)

var devMiddleware = require('webpack-dev-middleware')(compiler, {
  publicPath: webpackConfig.output.publicPath,
  stats: {
    colors: true,
    chunks: false
  }
})

var hotMiddleware = require('webpack-hot-middleware')(compiler)
// force page reload when html-webpack-plugin template changes
compiler.plugin('compilation', function (compilation) {
  compilation.plugin('html-webpack-plugin-after-emit', function (data, cb) {
    hotMiddleware.publish({ action: 'reload' })
    cb()
  })
})

// proxy api requests
Object.keys(proxyTable).forEach(function (context) {
  var options = proxyTable[context]
  if (typeof options === 'string') {
    options = { target: options }
  }
  app.use(proxyMiddleware(context, options))
})



// handle fallback for HTML5 history API
app.use(require('connect-history-api-fallback')())

// serve webpack bundle output
app.use(devMiddleware)

// enable hot-reload and state-preserving
// compilation error display
app.use(hotMiddleware)

// serve pure static assets
var staticPath = path.posix.join(config.dev.assetsPublicPath, config.dev.assetsSubDirectory)
app.use(staticPath, express.static('./static'))

// 支持api代理解决跨域问题
app.use(express.static('public'));

var httpProxy = require('http-proxy');
var apiProxy = httpProxy.createProxyServer();
var apiServer = ''

try {
  apiServer = require('../.config').apiServer
  console.log(apiServer)
  console.log('api')
} catch(err) {
  apiServer = 'http://127.0.0.1:18000/'
}

if (!apiServer) {apiServer = 'http://127.0.0.1:18000/'}
var apiServerHost = /http:\/\/=?(\S*)(?=\/)/.exec(apiServer)[1]
console.log(apiServerHost)


app.all('/book12/*', function(req, res){
  apiProxy.web(req, res, {target: apiServer}, function(e) {
      console.log('Proxy server error: "' + e + '"')
    })
})

apiProxy.on('proxyReq', function (proxyReq, req, res) {
  proxyReq.setHeader('Host', apiServerHost);
});


module.exports = app.listen(port, function (err) {
  if (err) {
    console.log(err)
    return
  }
  console.log('Listening at http://localhost:' + port + '\n')
})
