<template>
  <div class="parking-view">
    <HeaderBar />

    <main class="container">
      <h1 class="title">Real-time parking information</h1>
      <p class="subtitle">
        View live parking availability and guidance for Melbourne CBD.
      </p>

      <!-- Search row -->
      <div class="search-card">
        <label class="search-label">Search parking</label>
        <div class="search-row">
          <select v-model="searchType" class="select">
            <option value="street">Street</option>
            <option value="zone">Zone ID</option>
            <option value="suburb">Suburb</option>
          </select>

          <input
            v-model="searchStreet"
            type="text"
            :maxlength="20"
            @input="validateLength"
            @keyup.enter="searchParking"
            class="input"
            placeholder="Enter term (max 20 chars)"
          />

          <button
            class="btn"
            :disabled="loading || !searchStreet.trim() || lengthError"
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
        <h3 class="map-title">Melbourne Parking Map</h3>
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
      searchType: 'street',
      searchStreet: '',
      lengthError: false,
      loading: false,
      error: '',
      apiUrl: import.meta?.env?.VUE_APP_API_URL || process.env.VUE_APP_API_URL,
      map: null,
      markers: []
    }
  },
  mounted() {
    this.$nextTick(this.initMap)
  },
  methods: {
    validateLength() {
      this.lengthError =
        (this.searchStreet && this.searchStreet.length > 20) ? true : false
    },
    initMap() {
      if (this.map) return
      this.map = L.map(this.$refs.mapEl, {
        center: [-37.8136, 144.9631], // Melbourne
        zoom: 14
      })
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
      }).addTo(this.map)
    },
    async searchParking() {
      this.validateLength()
      if (this.lengthError || !this.searchStreet.trim()) return

      this.error = ''
      this.loading = true
      try {
        const url = `${this.apiUrl}?type=${encodeURIComponent(
          this.searchType
        )}&q=${encodeURIComponent(this.searchStreet)}`
        const res = await fetch(url, {
          headers: { Accept: 'application/json' }
        })
        if (!res.ok) throw new Error(`API request failed: ${res.status}`)
        const data = await res.json()

        // Clear old markers
        this.markers.forEach(m => this.map.removeLayer(m))
        this.markers = []

        // Draw new markers if the API provides coords
        if (data && Array.isArray(data.spots)) {
          data.spots.forEach(s => {
            if (s.lat && s.lng) {
              const m = L.marker([s.lat, s.lng]).addTo(this.map)
              if (s.name || s.zone) {
                m.bindPopup(
                  `<strong>${s.name || 'Spot'}</strong><br/>Zone: ${s.zone ?? '—'}`
                )
              }
              this.markers.push(m)
            }
          })
          // Fit bounds if any markers
          if (this.markers.length) {
            const group = L.featureGroup(this.markers)
            this.map.fitBounds(group.getBounds(), { padding: [20, 20] })
          }
        }
      } catch (e) {
        this.error = e.message || 'Search failed'
        // Keep map visible and usable
      } finally {
        this.loading = false
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

.select, .input {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 10px;
  font-size: 14px;
}
.input { min-width: 220px; flex: 1; }
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
.map { width: 100%; height: 500px; background: #f3f4f6; border-radius: 8px; }

@media (max-width: 640px) {
  .container { padding: 24px 12px; }
  .title { font-size: 24px; }
  .search-row { flex-direction: column; align-items: stretch; }
  .btn { width: 100%; }
}
</style>
