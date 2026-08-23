<template>
  <div class="turnstile-container" ref="turnstileContainer"></div>
</template>

<script>
export default {
  name: 'Turnstile',
  props: {
    siteKey: {
      type: String,
      required: true
    },
    theme: {
      type: String,
      default: 'light'
    },
    size: {
      type: String,
      default: 'normal'
    }
  },
  data() {
    return {
      widgetId: null,
      isLoaded: false,
      token: null
    }
  },
  mounted() {
    this.loadTurnstile()
  },
  beforeUnmount() {
    if (this.widgetId !== null && window.turnstile) {
      window.turnstile.remove(this.widgetId)
    }
  },
  methods: {
    loadTurnstile() {
      // Check if turnstile is already loaded
      if (window.turnstile) {
        this.renderWidget()
        return
      }

      // Load the script
      const script = document.createElement('script')
      script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js'
      script.async = true
      script.defer = true
      script.onload = () => {
        this.renderWidget()
      }
      script.onerror = () => {
        this.$emit('error', 'Falha ao carregar Turnstile')
      }
      document.head.appendChild(script)
    },
    renderWidget() {
      if (!this.$refs.turnstileContainer || this.widgetId !== null) return

      this.widgetId = window.turnstile.render(this.$refs.turnstileContainer, {
        sitekey: this.siteKey,
        theme: this.theme,
        size: this.size,
        callback: (token) => {
          this.token = token
          this.$emit('verify', token)
        },
        'expired-callback': () => {
          this.token = null
          this.$emit('expired')
        },
        'error-callback': () => {
          this.token = null
          this.$emit('error', 'Erro no Turnstile')
        }
      })
      this.isLoaded = true
    },
    reset() {
      if (this.widgetId !== null && window.turnstile) {
        window.turnstile.reset(this.widgetId)
        this.token = null
      }
    },
    getToken() {
      return this.token
    }
  }
}
</script>

<style scoped>
.turnstile-container {
  display: inline-block;
}
</style>