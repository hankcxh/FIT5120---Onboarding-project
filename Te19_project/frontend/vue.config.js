const { defineConfig } = require('@vue/cli-service')

const path = require('path')

module.exports = {
  outputDir: path.resolve(__dirname, '../backend/static'),

  indexPath: path.resolve(__dirname, '../backend/templates/index.html'),

  publicPath: '/static/'
}
