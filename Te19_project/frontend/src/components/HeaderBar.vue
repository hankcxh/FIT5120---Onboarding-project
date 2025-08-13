<template>
  <header class="header-bar">
    <nav class="nav">
      <!-- Brand -->
      <router-link to="/" class="brand">
        <img src="@/assets/logo.png" alt="Logo" class="logo-img" />
        <span class="brand-text">Melbourne Traffic</span>
      </router-link>

      <!-- Nav links -->
      <div class="nav-links">
        <router-link to="/" exact-active-class="active">Home</router-link>
        <router-link to="/insights" active-class="active">Data Insights</router-link>
        <router-link to="/parking" active-class="active">Parking Information</router-link>
      </div>
    </nav>
  </header>
</template>

<script>
export default { name: 'HeaderBar' }
</script>

<style scoped>
.header-bar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: #fff;
  border-bottom: 1px solid #eee;
}

.nav {
  max-width: 1100px;
  margin: 0 auto;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-img {
  width: 36px;
  height: 36px;
  object-fit: contain;
}

.brand-text {
  font-weight: 800;
  letter-spacing: .3px;
}

.nav-links {
  display: flex;
  gap: 18px;
}

.nav-links a {
  text-decoration: none;
  color: #555;
  font-size: 14px;
}

.nav-links a:hover { color: #000; }
.active {
  color: #000;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 4px;
}

/* Responsive */
@media (max-width: 640px) {
  .nav { flex-direction: column; gap: 8px; align-items: flex-start; }
  .nav-links { flex-wrap: wrap; gap: 10px; margin-top: 8px; }
  .brand-text { font-size: 16px; }
  .logo-img { width: 28px; height: 28px; }
}
</style>
