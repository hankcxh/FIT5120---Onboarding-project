const config = {
  apiUrl: process.env.NODE_ENV === 'production' 
    ? process.env.VUE_APP_API_URL
    : 'http://localhost:8000',  // Your Django backend
  
  environment: process.env.VUE_APP_ENVIRONMENT || 'development'
}

export default config