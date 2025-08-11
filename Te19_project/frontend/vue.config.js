const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: 'dist',  // This forces output to 'dist' folder
  publicPath: '/',
  productionSourceMap: false
})