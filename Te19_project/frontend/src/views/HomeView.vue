<template>
  <div class="home-page">
    <HeaderBar />
    <section class="hero">
      <div class="overlay">
        <h1>Smart commuting, greening Melbourne</h1>
        <p>Get instant parking and commuting information to create a green city</p>
        <router-link to="/insights" class="cta-button">Get started</router-link>
      </div>
    </section>
  </div>
</template>

<script>
import HeaderBar from '../components/HeaderBar.vue'
export default { name: 'HomeView', components: { HeaderBar } }
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.hero {
  flex: 1;
  background: url('@/assets/road.jpg') center/cover no-repeat; 
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.overlay {
  background: rgba(0, 0, 0, 0.4); 
  padding: 40px;
  border-radius: 12px;
  text-align: center;
  max-width: 700px;
}

.overlay h1 {
  font-size: 36px;
  font-weight: 800;
  color: #fff;
  margin-bottom: 16px;
}

.overlay p {
  font-size: 18px;
  color: #e2e8f0;
  margin-bottom: 24px;
}

.cta-button {
  display: inline-block;
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

@media (max-width: 640px) {
  .overlay h1 { font-size: 24px; }
  .overlay p { font-size: 16px; }
  .cta-button { font-size: 16px; padding: 12px 28px; }
}
</style>
