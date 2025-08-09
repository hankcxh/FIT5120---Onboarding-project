<template>
  <div class="min-h-screen bg-white">
    <HeaderBar />

    <main class="mx-auto max-w-6xl px-4 py-12">

      <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight text-gray-900 mb-6">
        Real-time parking information
      </h1>


      <p class="text-lg text-gray-600 max-w-3xl mb-10">
        View live parking availability and guidance for Melbourne CBD.
        We use real-time sensors and traffic data to help drivers find
        the nearest parking spots quickly, reducing congestion and emissions.
      </p>


      <div class="rounded-xl border bg-gray-50 p-8 text-gray-500 text-center min-h-[200px] flex items-center justify-center">
        Parking map and live availability will be displayed here.
      </div>
    </main>
  </div>
</template>

<script>
import HeaderBar from '../components/HeaderBar.vue'
export default { name: 'ParkingView', components: { HeaderBar } }
</script>
