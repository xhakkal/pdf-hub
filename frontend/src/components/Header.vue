<template>
  <header class="fixed top-0 w-full z-50 border-b border-neutral-800 shadow-lg bg-[#090909]/95 backdrop-blur-md">
    <div class="max-w-[1180px] mx-auto px-4 md:px-8 h-[68px] flex justify-between items-center">
      <!-- Brand -->
      <div
        @click="$emit('navigate', 'conversor')"
        class="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity"
      >
        <span class="brand-mark" aria-label="PDFhub"><span>PDF</span><strong>hub</strong></span>
      </div>

      <!-- Navigation -->
      <nav class="hidden md:flex items-center gap-2">
        <button
          @click="$emit('navigate', 'conversor')"
          :class="[
            'px-4 py-2 rounded-md font-semibold text-sm transition-all duration-200 active:scale-95',
            activePage === 'conversor'
              ? 'bg-[#ff9f1c] text-black shadow-[0_0_0_1px_rgba(255,159,28,0.5)]'
              : 'text-neutral-400 hover:text-white hover:bg-neutral-800'
          ]"
        >
          Conversor
        </button>
        <button
          @click="$emit('navigate', 'faq')"
          :class="[
            'px-4 py-2 rounded-md font-semibold text-sm transition-all duration-200 active:scale-95',
            activePage === 'faq'
              ? 'bg-[#ff9f1c] text-black shadow-[0_0_0_1px_rgba(255,159,28,0.5)]'
              : 'text-neutral-400 hover:text-white hover:bg-neutral-800'
          ]"
        >
          FAQ
        </button>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
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

.brand-mark {
  display: inline-flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: 900;
  letter-spacing: -0.09em;
  line-height: 1;
}

.brand-mark > span { color: #f5f5f5; }

.brand-mark > strong {
  margin-left: 0.2em;
  padding: 0.19em 0.32em 0.23em;
  border-radius: 0.16em;
  background: var(--color-primary);
  color: #111;
  letter-spacing: -0.08em;
}
</style>
