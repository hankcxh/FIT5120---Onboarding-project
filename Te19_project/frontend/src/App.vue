<template>
  <div id="app">
    <!-- Your existing template content -->
    <router-view />
  </div>
</template>

<script>
import { parkingAPI } from '@/services/api'
import config from '@/config'

export default {
  name: 'App',
  async mounted() {
    console.log('API URL:', config.apiUrl)  // Should show http://localhost:8000
    
    try {
      const response = await parkingAPI.getParkingData()
      console.log('Data:', response.data)
    } catch (error) {
      console.error('API Error:', error)
    }
  }
}
</script>

<style>
/* Your existing styles */
</style>