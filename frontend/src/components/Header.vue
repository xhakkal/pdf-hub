<template>
  <header class="fixed top-0 w-full z-50 border-b border-neutral-800 shadow-lg bg-black/95 backdrop-blur-md">
    <div class="max-w-[1120px] mx-auto px-4 md:px-8 h-16 flex justify-between items-center">
      <!-- Brand -->
      <div
        @click="$emit('navigate', 'conversor')"
        class="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity"
      >
        <img src="/logo.svg" alt="PDFhub" class="h-10 w-auto" />
        <span class="text-xl font-bold text-white tracking-tight hidden sm:block">PDFhub</span>
      </div>

      <!-- Navigation -->
      <nav class="hidden md:flex items-center gap-2">
        <button
          @click="$emit('navigate', 'conversor')"
          :class="[
            'px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 active:scale-95',
            activePage === 'conversor'
              ? 'bg-orange-600 text-white shadow-[0_0_0_1px_rgba(251,146,60,0.5)]'
              : 'text-neutral-400 hover:text-white hover:bg-neutral-800'
          ]"
        >
          Conversor
        </button>
        <button
          @click="$emit('navigate', 'faq')"
          :class="[
            'px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 active:scale-95',
            activePage === 'faq'
              ? 'bg-orange-600 text-white shadow-[0_0_0_1px_rgba(251,146,60,0.5)]'
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
</style>
