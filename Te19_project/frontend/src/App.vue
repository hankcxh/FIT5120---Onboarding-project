<template>
  <div id="app">
    <router-view />
    <FooterBar />
  </div>
</template>

<script>
import FooterBar from '@/components/FooterBar.vue'

export default {
  name: 'App',
  components: { FooterBar }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  background-color: #ffffff; 
}

* {
  box-sizing: border-box;
}
</style>
