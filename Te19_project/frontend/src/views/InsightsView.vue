<template>
  <div class="insights-page">
    <HeaderBar />
    <main class="container">
      <h1>Let Data tell Melbourne's traffic situation</h1>

      <div class="card-grid">
        <!-- Vehicles: chart + text -->
        <section class="card">
          <div class="card-header">
            <span class="small-text">Melbourne Car Ownership</span>
          </div>
          <div class="card-body split-grid">
            <div class="chart-wrap">
              <!-- force canvas to remount whenever key changes -->
              <canvas :key="vehicleKey" ref="vehicleChart" aria-label="Vehicles over time" role="img"></canvas>
            </div>
            <div class="insight-list">
              <h2>Vehicle Insights</h2>
              <ul>
                <li><strong>High Vehicle Count</strong> — Victoria has the second-highest number of passenger vehicles in Australia, and it keeps growing year-on-year.</li>
                <li><strong>Fewer Cars Leaving the Roads</strong> — Attrition (deregistration) is decreasing, so older vehicles stay in use longer.</li>
                <li><strong>Old and New Cars Together</strong> — A mix of older and newer cars keeps total numbers consistently high.</li>
                <li><strong>Impact on Daily Life</strong> — More vehicles → heavier traffic and fewer parking spots, especially at peak times.</li>
              </ul>
            </div>
          </div>
        </section>

        <!-- Population: chart + text -->
        <section class="card">
          <div class="card-header">
            <span class="small-text">CBD Population</span>
          </div>
          <div class="card-body split-grid">
            <div class="chart-wrap">
              <canvas :key="popKey" ref="popChart" aria-label="CBD population over time" role="img"></canvas>
            </div>
            <div class="insight-list">
              <h2>Population Insights</h2>
              <ul>
                <li><strong>Population Growth</strong> — Victoria has added 1.7M+ people since 2001, driven largely by Greater Melbourne.</li>
                <li><strong>Melbourne’s Domination</strong> — ~75% of Victorians live in Melbourne, competing for the same urban space and resources.</li>
                <li><strong>CBD Pressure Rising</strong> — More people in/around the CBD increases demand for parking, housing, and transport.</li>
                <li><strong>Pandemic Pause, Not a Stop</strong> — COVID slowed growth briefly; long-term trends point upward, bringing back pressure.</li>
                <li><strong>Shared Challenge</strong> — Parking difficulty isn’t “bad luck”; it’s a shared, city-wide challenge.</li>
              </ul>
            </div>
          </div>
        </section>
        <div class="bottom-button">
        <router-link to="/parking" class="btn-link">
          Want to Parking Information?
        </router-link>
      </div>
      </div>
    </main>
  </div>
</template>

<script>
import {
  Chart,
  LineController, LineElement, PointElement,
  BarController, BarElement,
  LinearScale, CategoryScale,
  Tooltip, Legend, Title
} from 'chart.js'
import HeaderBar from '../components/HeaderBar.vue'

// Register only what we use
Chart.register(
  LineController, LineElement, PointElement,
  BarController, BarElement,
  LinearScale, CategoryScale,
  Tooltip, Legend, Title
)

// JSON (make sure both files exist at these paths)
import vehicleGrowth from '../assets/data/vehicle_growth.json'
import cbdPopulation from '../assets/data/cbd_population.json'

export default {
  name: 'InsightsView',
  components: { HeaderBar },
  data() {
    return {
      charts: [],
      vehicleKey: 0,
      popKey: 0
    }
  },
  methods: {
    safeCtx(refName) {
      const el = this.$refs[refName]
      if (!el || typeof el.getContext !== 'function') return null
      const ctx = el.getContext('2d')
      return ctx || null
    },
    destroyCharts() {
      this.charts.forEach(c => {
        try { c && c.destroy && c.destroy() } catch (_) {
          // ignore chart destroy errors
        }
      })
      this.charts = []
    },
    drawCharts(vLabels, vValues, pLabels, pValues) {
      // Always clean first
      this.destroyCharts()

      // Re-key canvases to force remount (fresh <canvas>)
      this.vehicleKey++
      this.popKey++

      this.$nextTick(() => {
        const vCtx = this.safeCtx('vehicleChart')
        const pCtx = this.safeCtx('popChart')
        if (!vCtx || !pCtx) {
          // If you navigate away quickly, refs may be gone—just skip gracefully
          return
        }

        const vVals = vValues.map(Number).filter(Number.isFinite)
        const pVals = pValues.map(Number).filter(Number.isFinite)

        // Vehicles (no fill; avoids filler path entirely)
        const vChart = new Chart(vCtx, {
          type: 'line',
          data: {
            labels: vLabels,
            datasets: [{
              label: 'Vehicles',
              data: vVals,
              borderColor: '#16a34a',
              backgroundColor: 'rgba(22,163,74,0.15)',
              fill: false,
              tension: 0.3,
              pointRadius: 3,
              pointHoverRadius: 5
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,               // also helps avoid late draws after route change
            plugins: { legend: { position: 'top' } },
            scales: {
              x: { grid: { display: false } },
              y: { ticks: { callback: v => v.toLocaleString() } }
            }
          }
        })

        const pChart = new Chart(pCtx, {
          type: 'bar',
          data: {
            labels: pLabels,
            datasets: [{
              label: 'Population',
              data: pVals,
              backgroundColor: 'rgba(37,99,235,0.6)',
              borderColor: '#2563eb',
              borderWidth: 1,
              borderRadius: 6
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: { legend: { position: 'top' } },
            scales: {
              x: { grid: { display: false } },
              y: { ticks: { callback: v => v.toLocaleString() } }
            }
          }
        })

        this.charts = [vChart, pChart]
      })
    }
  },
  mounted() {
    const vLabels = vehicleGrowth.series.map(r => r.year)
    const vValues = vehicleGrowth.series.map(r => r.registrations)
    const pLabels = cbdPopulation.series.map(r => r.year)
    const pValues = cbdPopulation.series.map(r => r.population)
    this.drawCharts(vLabels, vValues, pLabels, pValues)
  },
  beforeUnmount() {
    this.destroyCharts()
  },
  // destroy charts as soon as you navigate away
  beforeRouteLeave(to, from, next) {
    this.destroyCharts()
    next()
  }
}
</script>

<style scoped>
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 16px;
}
h1 { font-size: 28px; font-weight: 800; margin-bottom: 16px; }
.card-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
.card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
.card-header { padding: 10px 14px; border-bottom: 1px solid #e5e7eb; background: #fafafa; }
.small-text { font-size: 13px; color: #555; }
.card-body { padding: 14px; }
.split-grid { display: grid; grid-template-columns: 1.4fr 1fr; gap: 16px; align-items: start; }
.chart-wrap { position: relative; width: 100%; height: 260px; }
.insight-list h2 { font-size: 18px; font-weight: 800; margin: 0 0 10px; }
.insight-list ul { padding-left: 18px; margin: 0; }
.insight-list li { margin: 8px 0; line-height: 1.45; color: #374151; }
@media (max-width: 900px) { .split-grid { grid-template-columns: 1fr; } .chart-wrap { height: 240px; } }
@media (max-width: 640px) { .container { padding: 24px 12px; } h1 { font-size: 22px; } }

.bottom-button {
  margin-top: 24px;
  text-align: center;
}

.btn-link {
  display: inline-block;
  background: #2563eb;
  color: #fff;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.btn-link:hover {
  background: #1d4ed8;
}

</style>
