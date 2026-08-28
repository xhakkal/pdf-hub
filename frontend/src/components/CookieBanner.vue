<template>
  <div
    v-if="showBanner"
    class="fixed bottom-4 right-4 z-40 w-[min(380px,calc(100vw-2rem))] bg-elevated border border-brand rounded-xl shadow-2xl"
  >
    <div class="p-4 flex flex-col gap-3">
      <!-- Texto -->
      <div>
        <p class="text-sm text-muted leading-relaxed">
          Usamos cookies para melhorar sua experiência. Consulte nossa
          <button
            @click="$emit('navigate', 'privacidade')"
            class="text-red hover:text-red underline cursor-pointer"
          >
            política de privacidade
          </button>
        </p>
      </div>

      <!-- Botões -->
      <div class="flex justify-end gap-2">
        <button
          @click="rejectCookies"
          class="px-3 py-2 rounded-md border border-brand text-muted hover:bg-surface-hover transition-all text-sm font-medium"
        >
          Rejeitar
        </button>
        <button
          @click="acceptCookies"
          class="px-3 py-2 rounded-md bg-red hover-bg-red text-white transition-all text-sm font-medium"
        >
          Aceitar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CookieBanner',
  data() {
    return {
      showBanner: false
    }
  },
  mounted() {
    // Verificar se já aceitou cookies
    const cookieConsent = localStorage.getItem('cookieConsent')
    if (!cookieConsent) {
      this.showBanner = true
    }
  },
  methods: {
    acceptCookies() {
      localStorage.setItem('cookieConsent', 'accepted')
      this.showBanner = false
      // Aqui você pode inicializar Google Analytics ou outros serviços
    },
    rejectCookies() {
      localStorage.setItem('cookieConsent', 'rejected')
      this.showBanner = false
    }
  }
}
</script>

<style scoped>
</style>
