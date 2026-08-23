<template>
  <header class="fixed top-0 w-full z-50 border-b border-brand shadow-lg bg-white/95 backdrop-blur-md">
    <div class="max-w-[1180px] mx-auto px-4 md:px-8 h-[68px] flex justify-between items-center">
      <!-- Brand -->
      <div
        @click="$emit('navigate', 'conversor')"
        class="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity"
      >
        <LogoIcon size="lg" aria-label="PDFhub - Voltar ao início" />
      </div>

      <!-- Navigation -->
      <nav class="hidden md:flex items-center gap-2">
        <button
          @click="$emit('navigate', 'conversor')"
          :class="[
            'px-4 py-2 rounded-md font-semibold text-sm transition-all duration-200 active:scale-95',
            activePage === 'conversor'
              ? 'bg-red text-white shadow-red-glow'
              : 'text-muted hover:text-red hover:bg-surface-hover'
          ]"
        >
          Conversor
        </button>
        <button
          @click="$emit('navigate', 'faq')"
          :class="[
            'px-4 py-2 rounded-md font-semibold text-sm transition-all duration-200 active:scale-95',
            activePage === 'faq'
              ? 'bg-red text-white shadow-red-glow'
              : 'text-muted hover:text-red hover:bg-surface-hover'
          ]"
        >
          FAQ
        </button>
      </nav>
    </div>
  </header>
</template>

<script>
import LogoIcon from './LogoIcon.vue'

export default {
  name: 'Header',
  components: { LogoIcon },
  props: {
    activePage: {
      type: String,
      default: 'conversor'
    }
  },
  emits: ['navigate']
}
</script>

<style scoped>
button {
  outline: none;
}
</style>
