<template>
  <footer class="w-full border-t mt-auto border-neutral-800 bg-[#090909]">
    <div class="max-w-[1180px] mx-auto px-4 py-10 flex flex-col md:flex-row justify-between items-center gap-6">
      <!-- Brand & Copyright -->
      <div class="flex flex-col gap-2 items-center md:items-start">
        <span class="text-lg font-black text-white tracking-tight">PDF<span class="ml-1 px-1.5 py-0.5 rounded-sm bg-orange text-black">hub</span></span>
        <p class="text-sm text-neutral-500">© 2026 PDFhub. Processamento seguro de arquivos. Limite de 50MB por conversão.</p>
        <button class="credit" type="button" @click="revealCreator">por xhakkal <span v-if="showCreator">· eliel</span></button>
      </div>

      <!-- Links -->
      <nav class="flex flex-wrap justify-center gap-6">
        <button
          @click="$emit('navigate', 'termos')"
          class="text-sm text-neutral-500 hover:text-[#ffb13d] hover:underline transition-all focus:ring-2 focus:ring-orange-500 outline-none cursor-pointer bg-transparent border-none"
        >
          Termos de Uso
        </button>
        <button
          @click="$emit('navigate', 'privacidade')"
          class="text-sm text-neutral-500 hover:text-[#ffb13d] hover:underline transition-all focus:ring-2 focus:ring-orange-500 outline-none cursor-pointer bg-transparent border-none"
        >
          Privacidade
        </button>
        <button
          @click="$emit('navigate', 'seguranca')"
          class="text-sm text-neutral-500 hover:text-[#ffb13d] hover:underline transition-all focus:ring-2 focus:ring-orange-500 outline-none cursor-pointer bg-transparent border-none"
        >
          Segurança
        </button>
      </nav>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return { showCreator: false, revealTimer: null }
  },
  beforeUnmount() {
    clearTimeout(this.revealTimer)
  },
  methods: {
    revealCreator() {
      this.showCreator = true
      clearTimeout(this.revealTimer)
      this.revealTimer = setTimeout(() => { this.showCreator = false }, 2800)
    }
  }
}
</script>

<style scoped>
.credit {
  width: fit-content;
  padding: 0;
  border: 0;
  background: transparent;
  color: #5f5f5f;
  font-size: 0.72rem;
  cursor: pointer;
  transition: color 160ms ease;
}

.credit:hover, .credit:focus-visible { color: #aaa; }
.credit span { color: var(--color-primary); }
</style>
