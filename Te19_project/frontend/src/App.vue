<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    // Just log the environment for debugging
    console.log('=== APP MOUNTED ===')
    console.log('Environment:', process.env.NODE_ENV)
    console.log('API URL:', process.env.VUE_APP_API_URL)
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>