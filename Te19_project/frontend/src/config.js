const config = {
  apiUrl: process.env.NODE_ENV === 'production' 
    ? process.env.VUE_APP_API_URL  // For Vercel
    : 'http://127.0.0.1:8000',     // Your Django backend
  
  environment: process.env.VUE_APP_ENVIRONMENT || 'development'
}

export default config