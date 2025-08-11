<template>
  <header class="header-bar">
    <nav class="nav">
      <!-- Logo + brand -->
      <div class="brand">
        <img src="@/assets/logo.png" alt="Logo" class="logo-img" />
        <span class="brand-text">Melbourne Traffic</span>
      </div>

      <!-- nav links -->
      <div class="nav-links">
        <router-link to="/" exact-active-class="active">Home</router-link>
        <router-link to="/insights" active-class="active">Data Insights</router-link>
        <router-link to="/parking" active-class="active">Real-time parking information</router-link>
      </div>
    </nav>
  </header>
</template>

<script>
export default { name: 'HeaderBar' }
</script>

<style scoped>
.header-bar {
  background: white;
  border-bottom: 1px solid #e5e5e5;
}
.nav {
  max-width: 1100px;
  margin: 0 auto;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 8px; /* space between logo and text */
}
.logo-img {
  height: 28px; /* adjust logo size here */
  width: auto;
}
.brand-text {
  font-weight: bold;
  color: #111;
}
.nav-links a {
  margin-left: 24px;
  text-decoration: none;
  color: #555;
  font-size: 14px;
}
.nav-links a:hover {
  color: #000;
}
.active {
  color: #000;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 4px;
}
</style>
