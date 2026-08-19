<template>
  <section v-if="showAds" class="ad-banner">
    <span class="ad-label">Publicidade</span>
    <ins
      v-if="slot"
      class="adsbygoogle"
      style="display:block"
      :data-ad-client="clientId"
      :data-ad-slot="slot"
      data-ad-format="auto"
      data-full-width-responsive="true"
    ></ins>
    <a v-else href="#" class="house-ad" @click.prevent="$emit('ad-click')">
      <span class="house-ad-icon">✦</span>
      <span><strong>Ferramentas PDF, sem complicação.</strong><small>Converta, una e proteja arquivos em poucos cliques.</small></span>
      <span class="house-ad-cta">Conhecer</span>
    </a>
  </section>
</template>

<script>
import { ADSENSE_CONFIG } from '../config/monetization.js'

export default {
  name: 'AdBanner',
  emits: ['ad-click'],
  computed: {
    clientId() {
      return ADSENSE_CONFIG.clientId
    },
    slot() {
      return ADSENSE_CONFIG.adSlots[this.placement] || ''
    }
  },
  props: {
    showAds: { type: Boolean, default: true },
    placement: { type: String, default: 'headerBanner' }
  },
  mounted() {
    // Carregar anúncios do Google AdSense
    if (window.adsbygoogle && this.showAds && this.slot) {
      try {
        (adsbygoogle = window.adsbygoogle || []).push({})
      } catch (e) { /* O AdSense pode carregar após o componente. */ }
    }
  }
}
</script>

<style scoped>
.ad-banner {
  width: 100%;
  min-height: 86px;
  margin: 0.25rem 0;
  padding: 0.5rem;
  border: 1px solid rgba(255, 159, 28, 0.2);
  border-radius: 0.5rem;
  background: #111;
  position: relative;
}

.ad-label {
  position: absolute;
  top: 0.3rem;
  left: 0.5rem;
  z-index: 1;
  color: #717171;
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.house-ad {
  min-height: 68px;
  padding: 1.2rem 1rem 0.55rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: #eee;
  text-decoration: none;
}

.house-ad-icon { color: var(--color-primary); font-size: 1.4rem; }
.house-ad strong, .house-ad small { display: block; }
.house-ad strong { font-size: 0.8rem; }
.house-ad small { color: #9b9b9b; font-size: 0.7rem; }
.house-ad-cta { margin-left: auto; color: var(--color-primary); font-size: 0.75rem; font-weight: 800; }

@media (max-width: 480px) {
  .house-ad small { display: none; }
}
</style>
