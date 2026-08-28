<template>
  <footer class="w-full border-t mt-auto border-brand bg-brand">
    <div class="max-w-[1180px] mx-auto px-4 py-10 flex flex-col md:flex-row justify-between items-center gap-6">
      <!-- Brand & Copyright -->
      <div class="flex flex-col gap-2 items-center md:items-start">
        <span class="text-lg font-black text-brand tracking-tight">PDF<span class="ml-1 px-1.5 py-0.5 rounded-sm bg-red text-white">hub</span></span>
        <p class="text-sm text-muted">© 2026 PDFhub. Processamento seguro de arquivos. Limite de 50MB por conversão.</p>
        <div class="flex flex-col gap-1 text-xs text-dim">
          <span>Versão 1.5</span>
          <span class="credit">Prod by E²</span>
        </div>
      </div>

      <!-- Links -->
      <nav class="flex flex-wrap justify-center gap-6">
        <button
          @click="$emit('navigate', 'termos')"
          class="text-sm text-muted hover:text-red hover:underline transition-all focus:ring-2 focus:ring-red-500 outline-none cursor-pointer bg-transparent border-none"
        >
          Termos de Uso
        </button>
        <button
          @click="$emit('navigate', 'privacidade')"
          class="text-sm text-muted hover:text-red hover:underline transition-all focus:ring-2 focus:ring-red-500 outline-none cursor-pointer bg-transparent border-none"
        >
          Privacidade
        </button>
        <button
          @click="$emit('navigate', 'seguranca')"
          class="text-sm text-muted hover:text-red hover:underline transition-all focus:ring-2 focus:ring-red-500 outline-none cursor-pointer bg-transparent border-none"
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
}
</script>

<style scoped>
.credit {
  color: var(--color-text-muted);
  font-size: 0.72rem;
}
</style>