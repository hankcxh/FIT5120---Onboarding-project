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
              <canvas ref="vehicleChart" aria-label="Vehicles over time" role="img"></canvas>
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
              <canvas ref="popChart" aria-label="CBD population over time" role="img"></canvas>
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
  Tooltip, Legend, Filler, Title
} from 'chart.js'
import HeaderBar from '../components/HeaderBar.vue'

// Register required bits (v3/v4)
Chart.register(
  LineController, LineElement, PointElement,
  BarController, BarElement,
  LinearScale, CategoryScale,
  Tooltip, Legend, Filler, Title
)

// Use RELATIVE imports (Vue CLI)
import vehicleGrowth from '../assets/vehicle_growth.json'
import cbdPopulation from '../assets/cbd_population.json'

export default {
  name: 'InsightsView',
  components: { HeaderBar },
  data() {
    return { charts: [] }
  },
  methods: {
    drawCharts(vLabels, vValues, pLabels, pValues) {
      // cleanup
      this.charts.forEach(c => c?.destroy?.())
      this.charts = []

      const vVals = vValues.map(Number).filter(Number.isFinite)
      const pVals = pValues.map(Number).filter(Number.isFinite)

      // Vehicles line + soft green fill
      const vCtx = this.$refs.vehicleChart.getContext('2d')
      const vGrad = vCtx.createLinearGradient(0, 0, 0, 260)
      vGrad.addColorStop(0, 'rgba(22,163,74,0.25)')  // green-600 @ 25%
      vGrad.addColorStop(1, 'rgba(22,163,74,0.04)')

      const vChart = new Chart(vCtx, {
        type: 'line',
        data: {
          labels: vLabels,
          datasets: [{
            label: 'Vehicles',
            data: vVals,
            borderColor: '#16a34a',
            backgroundColor: vGrad,
            fill: true,
            tension: 0.3,
            pointRadius: 3,
            pointHoverRadius: 5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'top' } },
          scales: {
            x: { grid: { display: false } },
            y: { ticks: { callback: v => v.toLocaleString() } }
          }
        }
      })

      // Population bars in blue
      const pCtx = this.$refs.popChart.getContext('2d')
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
          plugins: { legend: { position: 'top' } },
          scales: {
            x: { grid: { display: false } },
            y: { ticks: { callback: v => v.toLocaleString() } }
          }
        }
      })

      this.charts = [vChart, pChart]
    }
  },
  mounted() {
    const vLabels = vehicleGrowth.series.map(r => r.year)
    const vValues = vehicleGrowth.series.map(r => r.registrations)
    const pLabels = cbdPopulation.series.map(r => r.year)
    const pValues = cbdPopulation.series.map(r => r.population)
    this.$nextTick(() => this.drawCharts(vLabels, vValues, pLabels, pValues))
  },
  beforeUnmount() {
    this.charts.forEach(c => c?.destroy?.())
  }
}
</script>

<style scoped>
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 16px;
}

h1 {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 16px;
}

.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

.card-header {
  padding: 10px 14px;
  border-bottom: 1px solid #e5e7eb;
  background: #fafafa;
}

.small-text { font-size: 13px; color: #555; }

.card-body { padding: 14px; }

/* chart + text side-by-side (stack on mobile) */
.split-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 16px;
  align-items: start;
}

.chart-wrap {
  position: relative;
  width: 100%;
  height: 260px;
}

.insight-list h2 {
  font-size: 18px;
  font-weight: 800;
  margin: 0 0 10px;
}

.insight-list ul {
  padding-left: 18px;
  margin: 0;
}

.insight-list li {
  margin: 8px 0;
  line-height: 1.45;
  color: #374151;
}

@media (max-width: 900px) {
  .split-grid { grid-template-columns: 1fr; }
  .chart-wrap { height: 240px; }
}

@media (max-width: 640px) {
  .container { padding: 24px 12px; }
  h1 { font-size: 22px; }
}
</style>
