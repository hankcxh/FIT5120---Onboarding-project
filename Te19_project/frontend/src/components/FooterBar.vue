<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <!-- Column 1: Brand -->
        <div class="footer-col brand-col">
          <div class="brand">
            <img src="@/assets/logo.png" alt="Logo" class="logo-img" />
            <span class="brand-text">Melbourne Traffic</span>
          </div>
          <p class="tagline">
            Smarter commuting and sustainable transport for Melbourne.
          </p>
        </div>

        <!-- Column 2: Quick Links -->
        <div class="footer-col">
          <h4>Quick Links</h4>
          <nav class="links">
            <router-link to="/">Home</router-link>
            <router-link to="/insights">Data Insights</router-link>
            <router-link to="/parking">Parking Info</router-link>
          </nav>
        </div>

        <!-- Column 3: Contact -->
        <div class="footer-col">
          <h4>Contact</h4>
          <ul class="contact-list">
            <li>Email: <a href="mailto:support@meltraffic.com">support@meltraffic.com</a></li>
            <li>Phone: +61 3 1234 5678</li>
            <li>Melbourne, VIC</li>
          </ul>
        </div>

        <!-- Column 4: Social -->
        <div class="footer-col">
          <h4>Follow Us</h4>
            <li>FaceBook</li>
            <li>Instgram</li>

          </div>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="footer-bottom">
        <span>© {{ new Date().getFullYear() }} Melbourne Traffic. All rights reserved.</span>
      </div>
  </footer>
</template>

<script>
export default { name: 'FooterBar' }
</script>

<style scoped>
.footer {
  background: #0f172a;
  color: #e2e8f0;
  margin-top: 40px;
  padding: 40px 0 20px;
  font-size: 14px;
}
.container {
  max-width: none;
  margin: 0 auto;
  padding: 0 16px;
}
.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 24px;
}
.footer-col h4 {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #fff;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.logo-img {
  width: 36px;
  height: 36px;
  object-fit: contain;
}
.brand-text {
  font-size: 18px;
  font-weight: 700;
}
.tagline {
  margin-top: 8px;
  color: #94a3b8;
  line-height: 1.4;
}
.links {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.links a {
  color: #94a3b8;
  text-decoration: none;
}
.links a:hover {
  color: #fff;
}
.contact-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.contact-list li {
  margin-bottom: 6px;
  color: #94a3b8;
}
.contact-list a {
  color: #94a3b8;
  text-decoration: none;
}
.contact-list a:hover {
  color: #fff;
}
.social-icons {
  display: flex;
  gap: 10px;
}
.social-icons a {
  font-size: 20px;
  text-decoration: none;
  color: #94a3b8;
}
.social-icons a:hover {
  color: #fff;
}
.footer-bottom {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid rgba(255,255,255,0.1);
  text-align: center;
  font-size: 13px;
  color: #94a3b8;
}
</style>
