<template>
  <div class="insights-page">
    <HeaderBar />
    <main class="container">
      <h1>Let Data tells Melbourne's traffic situation</h1>

      <div class="card-grid">
        <section class="card">
          <div class="card-header">
            <span class="small-text">Melbourne Car ownership</span>
          </div>
          <div class="card-body">
            <canvas ref="vehicleChart"></canvas>
          </div>
        </section>

        <section class="card">
          <div class="card-header">
            <span class="small-text">Melbourne population growth</span>
          </div>
          <div class="card-body">
            <canvas ref="popChart"></canvas>
          </div>
        </section>
      </div>

      <div class="analysis-grid">
        <div class="analysis-box">
          <p>High Vehicle Count - Victoria has had the second-highest number of passenger
motor vehicles in Australia, and that number always keeps on growing year-on-year.</p>
          <p>Fewer Cars Leaving the Roads - The attrition rate (cars being deregistered) is
decreasing, which means older vehicles are staying in use for longer periods.</p>
          <p>Old and New Cars Together - Combination of old and new cars keep the overall
number of vehicles in the city consistently high.</p>
          <p>Impact on Daily Life - More number of vehicles contribute to heavier traffic and
fewer available parking spots, especially during peak hours.</p>
          <p v-if="metaVehicle">
            Total growth: <strong>{{ (metaVehicle.total_growth*100).toFixed(2) }}%</strong> | Peak year: <strong>{{ metaVehicle.peak_year }}</strong>
          </p>
        </div>
        <div class="analysis-box">
          <p>Population Growth - Victorias population has increased over the past two decades,
adding more than 1.7 million people since 2001, with Greater Melbourne accounting
for most of that growth.</p>
          <p>Melbournes Domination - Around 75% of Victorias population lives in Melbourne,
meaning more people are competing for the same city space and resources.</p>
          <p>CBD Pressure Rising - The concentration of people in and around Melbourne’s
CBD has steadily increased, driving up demand for parking, housing, and transport
during peak periods.</p>
          <p>Shared Challenge - These numbers show that parking difficulty is not bad luck for
the drivers. It’s a shared challenge.</p>
          <p v-if="metaPop">
            Growth rate: <strong>{{ (metaPop.growth_rate*100).toFixed(2) }}%</strong> | Density 2021: <strong>{{ formatNumber(metaPop.population_density_2021) }}</strong> ppl/km²
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import { Chart } from 'chart.js/auto'
import HeaderBar from '../components/HeaderBar.vue'

export default {
  name: 'InsightsView',
  components: { HeaderBar },
  data() {
    return { metaVehicle: null, metaPop: null, charts: [] }
  },
  methods: {
    formatNumber(n) {
      if (!n && n !== 0) return '—'
      return Math.round(n).toLocaleString()
    },
    drawCharts(vLabels, vValues, pLabels, pValues) {
      this.charts.forEach(c => c.destroy())
      this.charts = []

      this.charts.push(new Chart(this.$refs.vehicleChart, {
        type: 'line',
        data: { labels: vLabels, datasets: [{ label: 'Vehicles', data: vValues, borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.2)', tension: 0.3 }] }
      }))

      this.charts.push(new Chart(this.$refs.popChart, {
        type: 'bar',
        data: { labels: pLabels, datasets: [{ label: 'Population', data: pValues, backgroundColor: '#10b981' }] }
      }))
    }
  },
  async mounted() {
    try {
      const v = await axios.get('/api/insights/vehicle-growth')
      this.metaVehicle = v.data.meta
      const vLabels = v.data.series.map(r => r.year)
      const vValues = v.data.series.map(r => r.registrations)

      const p = await axios.get('/api/insights/cbd-population')
      this.metaPop = p.data.meta
      const pLabels = p.data.series.map(r => r.year)
      const pValues = p.data.series.map(r => r.population)

      this.$nextTick(() => this.drawCharts(vLabels, vValues, pLabels, pValues))
    } catch (err) {
      console.error(err)
    }
  },
  beforeUnmount() {
    this.charts.forEach(c => c.destroy())
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
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 40px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

.card {
  border: 1px solid #ddd;
  border-radius: 12px;
  background: white;
  overflow: hidden;
}

.card-header {
  border-bottom: 1px solid #eee;
  padding: 16px;
}

.small-text {
  font-size: 12px;
  color: #666;
}

.big-number {
  font-size: 20px;
  font-weight: bold;
  margin-top: 4px;
}

.card-body {
  padding: 16px;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.analysis-box {
  background: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 16px;
  color: #555;
}
</style>
