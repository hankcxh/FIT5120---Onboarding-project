<template>
  <div class="parking-view">
    <HeaderBar />

    <main class="container">
      <h1 class="title">Real-time parking information</h1>
      <p class="subtitle">Search by street name or zone number.</p>

      <!-- Search row -->
      <div class="search-card">
        <label class="search-label">Search parking (Street or Zone)</label>
        <div class="search-row">
          <input
            v-model="searchStreet"
            type="text"
            :maxlength="20"
            @input="validateLength"
            @keyup.enter="searchParking"
            class="input"
            placeholder="e.g. Collins, Bourke, Spencer, or 7084"
          />

          <button
            class="btn"
            :disabled="loading || lengthError"
            @click="searchParking"
          >
            {{ loading ? 'Searching...' : 'Search' }}
          </button>
        </div>

        <p v-if="lengthError" class="error">
          Input too long ({{ searchStreet.length }}/20). Please shorten.
        </p>
        <p v-if="error" class="error">{{ error }}</p>
      </div>

      <!-- Map -->
      <section class="map-card">
        <h3 class="map-title">Melbourne Parking Map ({{ spotCount }} available spots)</h3>
        <div id="parking-map" ref="mapEl" class="map"></div>
      </section>
    </main>
  </div>
</template>

<script>
import HeaderBar from '@/components/HeaderBar.vue'
import * as L from 'leaflet'

export default {
  name: 'ParkingView',
  components: { HeaderBar },
  data() {
    return {
      searchStreet: '',
      lengthError: false,
      loading: false,
      error: '',
      spotCount: 0,
      apiUrl: 'https://ccj3gsn6fl.execute-api.ap-southeast-2.amazonaws.com/prod/parking',
      map: null,
      markers: []
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initMap()
      this.loadAllParking() // Load all parking spots on page load
    })
  },
  methods: {
    validateLength() {
      this.lengthError =
        (this.searchStreet && this.searchStreet.length > 20) ? true : false
    },

    initMap() {
      if (this.map) return
      this.map = L.map(this.$refs.mapEl, {
        center: [-37.8136, 144.9631], // Melbourne CBD
        zoom: 14
      })
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
      }).addTo(this.map)
    },

    // Load all available parking spots when page loads
    async loadAllParking() {
      this.loading = true
      this.error = ''
      
      try {
        console.log('Loading all available parking spots...')
        console.log('API URL:', this.apiUrl)
        
        const response = await fetch(this.apiUrl, { 
          method: 'GET',
          headers: { 
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          mode: 'cors'
        })

        console.log('Response status:', response.status)
        console.log('Response headers:', response.headers)

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }

        const data = await response.json()
        console.log('Received data:', data)
        
        if (data && data.success) {
          this.displayParkingSpots(data.spots || [], 'All available parking spots')
          this.spotCount = data.total_spots || 0
        } else {
          this.error = data?.message || 'Failed to load parking data'
          this.spotCount = 0
        }
      } catch (e) {
        console.error('Load all parking error:', e)
        this.error = `Unable to load parking information at the moment. Please try again.`
        this.spotCount = 0
      } finally {
        this.loading = false
      }
    },

    async searchParking() {
      this.validateLength()
      if (this.lengthError) return

      const street = (this.searchStreet || '').trim()
      if (!street) {
        // If search is empty, load all parking spots
        this.loadAllParking()
        return
      }

      this.error = ''
      this.loading = true
      
      try {
        console.log(`Searching for: ${street}`)
        const url = `${this.apiUrl}?street=${encodeURIComponent(street)}`
        console.log('Search URL:', url)
        
        const response = await fetch(url, { 
          method: 'GET',
          headers: { 
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          mode: 'cors'
        })

        console.log('Search response status:', response.status)

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }

        const data = await response.json()
        console.log('Search data received:', data)

        if (data && data.success) {
          this.displayParkingSpots(data.spots || [], `${data.street_name || street}`)
          this.spotCount = data.total_available_spots || 0
          
          // Center map on search results if bounds provided
          if (data.map_bounds) {
            const bounds = data.map_bounds
            this.map.fitBounds([
              [bounds.southwest.lat, bounds.southwest.lon],
              [bounds.northeast.lat, bounds.northeast.lon]
            ], { padding: [20, 20] })
          }
        } else {
          this.error = `No available parking spots found for "${street}"`
          this.clearMarkers()
          this.spotCount = 0
        }
      } catch (e) {
        console.error('Search error:', e)
        // Handle different types of errors with user-friendly messages
        if (e.message.includes('404')) {
          this.error = `No available parking spots found for "${street}". Try: Collins, Bourke, Russell, Spencer, or Queen.`
        } else if (e.message.includes('403')) {
          this.error = `No available parking spots found for "${street}"`
        } else if (e.message.includes('500')) {
          this.error = `No available parking spots found for "${street}"`
        } else {
          this.error = `No available parking spots found for "${street}"`
        }
        this.clearMarkers()
        this.spotCount = 0
      } finally {
        this.loading = false
      }
    },

    displayParkingSpots(spots, title) {
      console.log(`Displaying ${spots.length} parking spots for: ${title}`)
      
      // Clear existing markers
      this.clearMarkers()

      if (!spots || spots.length === 0) {
        this.error = `No available parking spots found`
        return
      }

      // Add markers for each parking spot
      spots.forEach((spot, index) => {
        if (spot.latitude && spot.longitude) {
          // Create green marker for available parking
          const marker = L.marker([spot.latitude, spot.longitude], {
            icon: L.divIcon({
              className: 'parking-marker',
              html: '<div class="marker-icon">P</div>',
              iconSize: [30, 30],
              iconAnchor: [15, 15]
            })
          }).addTo(this.map)

          // Add popup with parking info
          const popupContent = `
            <div class="parking-popup">
              <h4>Zone ${spot.zone_number}</h4>
              <p><strong>Status:</strong> Available</p>
              <p><strong>Kerbside ID:</strong> ${spot.kerbsideid}</p>
              <p><strong>Last Updated:</strong><br>${this.formatDateTime(spot.status_timestamp)}</p>
            </div>
          `
          marker.bindPopup(popupContent)
          this.markers.push(marker)
        } else {
          console.warn(`Spot ${index} missing coordinates:`, spot)
        }
      })

      // Fit map to show all markers if we have any
      if (this.markers.length > 0) {
        const group = L.featureGroup(this.markers)
        this.map.fitBounds(group.getBounds(), { padding: [20, 20] })
      } else {
        // Reset to Melbourne CBD view
        this.map.setView([-37.8136, 144.9631], 14)
      }
    },

    clearMarkers() {
      this.markers.forEach(m => this.map.removeLayer(m))
      this.markers = []
    },

    formatDateTime(dateString) {
      if (!dateString) return 'Unknown'
      try {
        return new Date(dateString).toLocaleString('en-AU', {
          year: 'numeric',
          month: 'short', 
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch {
        return 'Invalid date'
      }
    }
  }
}
</script>

<style scoped>
.container { max-width: 1100px; margin: 0 auto; padding: 40px 16px; }
.title { font-size: 32px; font-weight: 800; margin-bottom: 8px; }
.subtitle { color: #555; margin-bottom: 16px; }

.search-card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}
.search-label { display: block; font-size: 14px; color: #666; margin-bottom: 8px; }
.search-row { display: flex; gap: 10px; flex-wrap: wrap; }

.input {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 10px;
  font-size: 14px;
  min-width: 220px;
  flex: 1;
}
.btn {
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
  cursor: pointer;
}
.btn:disabled { opacity: .5; cursor: not-allowed; }
.error { color: #b91c1c; font-size: 13px; margin-top: 6px; }

.map-card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 16px;
}
.map-title { font-weight: 600; margin-bottom: 8px; }
.map { width: 100%; height: 500px; background: #f3f4f6; border-radius: 8px; z-index: 10; }

/* Custom parking marker styles */
:deep(.parking-marker) {
  background: #22c55e;
  border: 3px solid white;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.marker-icon) {
  color: white;
  font-weight: bold;
  font-size: 14px;
}

:deep(.parking-popup h4) {
  margin: 0 0 8px 0;
  color: #2563eb;
  font-size: 16px;
}

:deep(.parking-popup p) {
  margin: 4px 0;
  font-size: 14px;
  line-height: 1.4;
}

@media (max-width: 640px) {
  .container { padding: 24px 12px; }
  .title { font-size: 24px; }
  .search-row { flex-direction: column; align-items: stretch; }
  .btn { width: 100%; }
}
</style>