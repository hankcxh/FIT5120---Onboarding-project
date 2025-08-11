import axios from 'axios'
import config from '@/config'

const api = axios.create({
  baseURL: config.apiUrl,
  timeout: 10000
})

export const parkingAPI = {
  getParkingData: () => api.get('/api/parking/'),
  getInsights: () => api.get('/api/insights/')
}

export default api