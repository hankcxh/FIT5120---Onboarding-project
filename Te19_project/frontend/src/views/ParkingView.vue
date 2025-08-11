<template>
  <div class="parking-view">
    <!-- Header -->
    <HeaderBar />
    
    <!-- Main Content -->
    <main class="mx-auto max-w-6xl px-4 py-12">
      <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight text-gray-900 mb-6">
        Real-time parking information
      </h1>
      
      <p class="text-lg text-gray-600 max-w-3xl mb-10">
        View live parking availability and guidance for Melbourne CBD. 
        We use real-time sensors and traffic data to help drivers find 
        the nearest parking spots quickly, reducing congestion and emissions.
      </p>

      <!-- Search Input -->
      <div class="mb-8">
        <div class="flex gap-4 max-w-md">
          <input
            v-model="searchStreet"
            @keyup.enter="searchParking"
            type="text"
            placeholder="Enter street name or zone (e.g., 7394)"
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            @click="searchParking"
            :disabled="loading || !searchStreet.trim()"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? 'Searching...' : 'Search' }}
          </button>
        </div>
      </div>

      <!-- Map Container - ALWAYS VISIBLE -->
      <div class="rounded-xl border bg-white p-4 min-h-[500px] mb-6">
        <h3 class="text-lg font-semibold mb-4">Melbourne Parking Map</h3>
        
        <!-- Map - ALWAYS SHOW -->
        <div 
          id="parking-map" 
          ref="mapContainer"
          class="w-full rounded-lg border-2 border-gray-400"
          style="height: 500px; background-color: #f3f4f6; position: relative;"
        >
          <!-- Fallback content if map doesn't load -->
          <div class="absolute inset-0 flex items-center justify-center text-gray-500">
            Loading map...
          </div>
        </div>
        
        <!-- Debug Info -->
        <div class="mt-4 p-2 bg-gray-100 rounded text-sm">
          <p><strong>Debug:</strong> Map status: {{ map ? 'Initialized' : 'Not initialized' }}</p>
          <p><strong>Leaflet:</strong> {{ leafletLoaded ? 'Loaded' : 'Not loaded' }}</p>
          <p><strong>API URL:</strong> {{ apiUrl }}</p>
        </div>
      </div>

      <!-- Search and Results Section -->
      <div v-if="searchResults" class="mb-6">
        <div class="bg-green-50 border border-green-200 rounded-lg p-4">
          <h3 class="text-lg font-semibold text-green-800 mb-2">
            Search Results for "{{ searchResults.searchTerm }}"
          </h3>
          <p class="text-green-700">
            <span class="font-bold">{{ searchResults.availableSpots }}</span> available spots 
            out of <span class="font-bold">{{ searchResults.totalSpots }}</span> total spots
          </p>
          <p v-if="searchResults.note" class="text-blue-600 text-sm mt-2">
            {{ searchResults.note }}
          </p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="mb-6">
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex items-center">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
            <p class="text-blue-700">Loading parking data...</p>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="mb-6">
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
          <h3 class="text-lg font-semibold text-red-800 mb-2">Error</h3>
          <p class="text-red-700">{{ error }}</p>
          <p class="text-sm text-gray-600 mt-2">API URL: {{ apiUrl }}</p>
        </div>
      </div>

      <!-- Parking Spots List -->
      <div v-if="searchResults && searchResults.data.spots && searchResults.data.spots.length > 0" class="bg-white rounded-lg p-4 border">
        <h4 class="font-semibold mb-3 text-lg">Available Parking Spots ({{ searchResults.data.spots.length }})</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-60 overflow-y-auto">
          <div 
            v-for="spot in searchResults.data.spots" 
            :key="spot.kerbsideId"
            class="bg-gray-50 p-3 rounded border text-sm hover:bg-gray-100 cursor-pointer"
            @click="focusOnSpot(spot)"
          >
            <div class="font-medium text-blue-600">Spot ID: {{ spot.kerbsideId }}</div>
            <div class="text-gray-600">Zone: {{ spot.zoneNumber }}</div>
            <div class="text-gray-600 text-xs">{{ spot.lat?.toFixed(6) }}, {{ spot.lng?.toFixed(6) }}</div>
            <div class="text-green-600 font-medium">✓ {{ spot.status }}</div>
          </div>
        </div>
        <p class="text-sm text-gray-500 mt-3">
          Click on a parking spot to focus on it on the map
        </p>
      </div>
    </main>
  </div>
</template>

<script>
import HeaderBar from '../components/HeaderBar.vue'

// Dynamic Leaflet import for better build compatibility
let L = null;

export default {
  name: 'ParkingView',
  components: { HeaderBar },
  data() {
    return {
      searchStreet: '',
      loading: false,
      searchResults: null,
      error: null,
      map: null,
      markers: [],
      leafletLoaded: false,
      apiUrl: 'https://ccj3gsn6fl.execute-api.ap-southeast-2.amazonaws.com/prod'
    }
  },
  async mounted() {
    console.log('=== COMPONENT DEBUG ===');
    console.log('API URL:', this.apiUrl);
    
    // Load Leaflet dynamically
    await this.loadLeaflet();
    
    // Wait for DOM to be fully rendered
    this.$nextTick(() => {
      this.initializeMap();
    });
  },
  beforeUnmount() {
    if (this.map) {
      this.map.remove();
    }
  },
  methods: {
    async loadLeaflet() {
      try {
        // Dynamic import of Leaflet
        const leafletModule = await import('leaflet');
        L = leafletModule.default;
        
        // Import CSS
        await import('leaflet/dist/leaflet.css');
        
        // Fix for default markers
        delete L.Icon.Default.prototype._getIconUrl;
        L.Icon.Default.mergeOptions({
          iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
          iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
        });
        
        this.leafletLoaded = true;
        console.log('Leaflet loaded successfully');
        
      } catch (error) {
        console.error('Failed to load Leaflet:', error);
        this.leafletLoaded = false;
      }
    },
    initializeMap() {
      console.log('=== MAP INITIALIZATION DEBUG ===');
      
      if (!L || !this.leafletLoaded) {
        console.error('Leaflet not loaded yet');
        return;
      }
      
      try {
        const container = this.$refs.mapContainer;
        console.log('Container element:', container);
        
        if (!container) {
          console.error('MAP CONTAINER NOT FOUND!');
          return;
        }
        
        // Clear any existing content
        container.innerHTML = '';
        
        console.log('Creating Leaflet map...');
        
        // Create map with explicit options
        this.map = L.map(container, {
          center: [-37.8136, 144.9631],
          zoom: 13,
          scrollWheelZoom: true,
          zoomControl: true,
          attributionControl: true
        });
        
        console.log('Map object created:', this.map);
        
        // Add tile layer
        const tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors',
          maxZoom: 19
        });
        
        tileLayer.addTo(this.map);
        console.log('Tile layer added');
        
        // Add test marker
        // eslint-disable-next-line no-unused-vars
        const marker = L.marker([-37.8136, 144.9631])
          .addTo(this.map)
          .bindPopup('MAP IS WORKING!<br>Melbourne CBD<br>Search for parking above');
        
        console.log('Test marker added');
        
        // Force resize
        setTimeout(() => {
          if (this.map) {
            this.map.invalidateSize();
            console.log('MAP INITIALIZED SUCCESSFULLY!');
          }
        }, 200);
        
      } catch (error) {
        console.error('MAP INITIALIZATION FAILED:', error);
        this.leafletLoaded = false;
      }
    },
    
    async searchParking() {
      if (!this.searchStreet.trim()) return;
      
      this.loading = true;
      this.error = null;
      this.searchResults = null;
      this.clearMarkers();
      
      try {
        console.log('Searching for:', this.searchStreet);
        
        // FIXED: Use correct Lambda endpoint
        const apiCall = `${this.apiUrl}?street=${encodeURIComponent(this.searchStreet)}`;
        console.log('API Call:', apiCall);
        
        const response = await fetch(apiCall, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
          throw new Error(`API request failed: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('API Response:', data);
        
        if (data.success) {
          this.searchResults = data;
          
          // Center map and add markers
          if (data.data.lat && data.data.lng) {
            this.centerMap(data.data.lat, data.data.lng);
          }
          
          // Add parking spot markers
          if (data.data.spots && data.data.spots.length > 0) {
            this.addParkingMarkers(data.data.spots);
          }
        } else {
          this.error = data.error || 'Failed to fetch parking data';
        }
        
      } catch (err) {
        console.error('Search error:', err);
        this.error = `Failed to connect to parking service: ${err.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    centerMap(lat, lng) {
      if (this.map) {
        this.map.setView([lat, lng], 16);
        
        // Add a center marker for the search area
        const centerMarker = L.marker([lat, lng], {
          icon: L.divIcon({
            html: '<div style="background-color: #3b82f6; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white;"></div>',
            iconSize: [20, 20],
            className: 'custom-div-icon'
          })
        }).addTo(this.map);
        
        centerMarker.bindPopup(`Search Center: ${this.searchStreet}`);
        this.markers.push(centerMarker);
      }
    },
    
    addParkingMarkers(spots) {
      if (!this.map) return;
      
      spots.forEach(spot => {
        // Create custom icon for available parking spots
        const parkingIcon = L.divIcon({
          html: `
            <div style="
              background-color: #10b981; 
              color: white; 
              width: 30px; 
              height: 30px; 
              border-radius: 50%; 
              border: 2px solid white;
              display: flex;
              align-items: center;
              justify-content: center;
              font-weight: bold;
              font-size: 12px;
              box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            ">P</div>
          `,
          iconSize: [30, 30],
          className: 'parking-spot-icon'
        });
        
        const marker = L.marker([spot.lat, spot.lng], { icon: parkingIcon })
          .addTo(this.map);
        
        // Create popup content
        const popupContent = `
          <div style="font-family: sans-serif;">
            <h4 style="margin: 0 0 8px 0; color: #1f2937;">Parking Spot</h4>
            <p style="margin: 4px 0;"><strong>Spot ID:</strong> ${spot.kerbsideId}</p>
            <p style="margin: 4px 0;"><strong>Zone:</strong> ${spot.zoneNumber}</p>
            <p style="margin: 4px 0;"><strong>Status:</strong> <span style="color: #10b981; font-weight: bold;">${spot.status}</span></p>
            <p style="margin: 4px 0; font-size: 12px; color: #6b7280;">
              📍 ${spot.lat.toFixed(6)}, ${spot.lng.toFixed(6)}
            </p>
          </div>
        `;
        
        marker.bindPopup(popupContent);
        this.markers.push(marker);
      });
      
      console.log(`Added ${spots.length} parking markers to map`);
    },
    
    clearMarkers() {
      this.markers.forEach(marker => {
        this.map.removeLayer(marker);
      });
      this.markers = [];
    },
    
    focusOnSpot(spot) {
      if (this.map) {
        this.map.setView([spot.lat, spot.lng], 18);
        
        // Find and open the popup for this spot
        this.markers.forEach(marker => {
          const markerLatLng = marker.getLatLng();
          if (Math.abs(markerLatLng.lat - spot.lat) < 0.0001 && 
              Math.abs(markerLatLng.lng - spot.lng) < 0.0001) {
            marker.openPopup();
          }
        });
      }
    }
  }
}
</script>

<style scoped>
.parking-view {
  min-height: 100vh;
  background-color: #ffffff;
}

/* Ensure Leaflet map has proper dimensions */
#parking-map {
  height: 500px !important;
  width: 100% !important;
  position: relative;
  z-index: 1;
}

/* Import Leaflet CSS globally */
@import 'leaflet/dist/leaflet.css';

/* Fix for Leaflet markers */
:deep(.leaflet-div-icon) {
  background: transparent !important;
  border: none !important;
}

:deep(.custom-div-icon) {
  background: transparent !important;
  border: none !important;
}

:deep(.parking-spot-icon) {
  background: transparent !important;
  border: none !important;
}

/* Ensure Leaflet controls are visible */
:deep(.leaflet-control-zoom) {
  box-shadow: 0 1px 5px rgba(0,0,0,0.65);
}

:deep(.leaflet-control-attribution) {
  background: rgba(255, 255, 255, 0.7);
}

/* Force map container sizing */
:deep(.leaflet-container) {
  height: 500px !important;
  width: 100% !important;
}
</style>