const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: 'dist',  // This forces output to 'dist' folder
  publicPath: '/',
  productionSourceMap: false
})


module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_OPTIONS_API__: JSON.stringify(true),              // keep Options API?
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false),           // devtools in prod?
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false) // silence the warning
      })
    ]
  }
}
