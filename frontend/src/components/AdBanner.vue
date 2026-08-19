<template>
  <div v-if="showAds" class="w-full p-2 my-4 rounded-lg border border-orange-500/30 flex items-center justify-center">
    <!-- Ad Container - Smaller Size -->
    <div class="w-full max-w-[320px] md:max-w-[336px]">
      <div class="bg-orange-500/10 p-2 rounded text-center border border-orange-500/20">
        <!-- Google AdSense Ad - Mobile optimized -->
        <ins class="adsbygoogle"
             style="display:inline-block;width:320px;height:50px;max-width:100%"
             data-ad-client="ca-pub-xxxxxxxxxxxxxxxx"
             data-ad-slot="1234567890"></ins>
      </div>
    </div>
  </div>
  <!-- Fallback placeholder for development -->
  <div v-else-if="isDevelopment && showAds" class="w-full bg-gradient-to-r from-orange-900/50 to-orange-500/30 p-2 my-4 rounded-lg border border-orange-500/30 text-center max-w-[336px] mx-auto">
    <p class="text-xs text-orange-300 font-medium">📢 Anúncio</p>
  </div>
</template>

<script>
export default {
  name: 'AdBanner',
  props: {
    showAds: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      isDevelopment: process.env.NODE_ENV === 'development'
    }
  },
  mounted() {
    // Carregar anúncios do Google AdSense
    if (window.adsbygoogle && this.showAds) {
      try {
        (adsbygoogle = window.adsbygoogle || []).push({})
      } catch (e) {
        console.log('AdSense ainda não carregado')
      }
    }
  }
}
</script>

<style scoped>
ins.adsbygoogle {
  display: inline-block;
}
</style>
