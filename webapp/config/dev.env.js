'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  CLIENT_ID: '"client_id"',
  VUE_APP_BUSINESS_LOGIC_HOST:'"http://127.0.0.1:8000"',
  CLIENT_SECRET: '"client_secret"'
})
