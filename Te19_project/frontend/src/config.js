const config = {
  apiUrl: process.env.VUE_APP_API_URL || 'http://localhost:5000',
  environment: process.env.VUE_APP_ENVIRONMENT || 'development',
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production'
}

export default config

