<template>
  <div class="home-page">
    <HeaderBar />
    <section class="hero">
      <h1>Smart commuting, greening Melbourne</h1>
      <p>Get instant parking and commuting information to create a green city</p>
      <router-link to="/insights" class="cta-button">Get started</router-link>
    </section>
  </div>
</template>

<script>
import HeaderBar from '../components/HeaderBar.vue'
export default { name: 'HomeView', components: { HeaderBar } }
</script>

<style scoped>
.home-page {
  background: #f7f7f7;
  min-height: 100vh;
}

.hero {
  max-width: 800px;
  margin: 0 auto;
  padding: 100px 20px;
  text-align: center;
}

.hero h1 {
  font-size: 36px;
  font-weight: 800;
  color: #111;
}

.hero p {
  margin-top: 16px;
  font-size: 18px;
  color: #666;
}

.cta-button {
  display: inline-block;
  margin-top: 40px;
  padding: 14px 40px;
  background: #10b981;
  color: white;
  border-radius: 999px;
  font-size: 18px;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.3s;
}

.cta-button:hover {
  background: #0ea472;
}
</style>
