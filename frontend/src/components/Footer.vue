<template>
  <footer class="w-full border-t mt-auto border-neutral-800 bg-[#090909]">
    <div class="max-w-[1180px] mx-auto px-4 py-10 flex flex-col md:flex-row justify-between items-center gap-6">
      <!-- Brand & Copyright -->
      <div class="flex flex-col gap-2 items-center md:items-start">
        <span class="text-lg font-black text-white font-['Inter'] tracking-tight">PDF<span class="ml-1 px-1.5 py-0.5 rounded-sm bg-orange text-black">hub</span></span>
        <p class="font-['Inter'] text-sm text-neutral-500">© 2026 PDFhub. Processamento seguro de arquivos. Limite de 50MB por conversão.</p>
        <p class="font-['Inter'] text-xs text-neutral-600">prod by eliel</p>
      </div>

      <!-- Links -->
      <nav class="flex flex-wrap justify-center gap-6">
        <button
          @click="$emit('navigate', 'termos')"
          class="font-['Inter'] text-sm text-neutral-500 hover:text-[#ffb13d] hover:underline transition-all focus:ring-2 focus:ring-orange-500 outline-none cursor-pointer bg-transparent border-none"
        >
          Termos de Uso
        </button>
        <button
          @click="$emit('navigate', 'privacidade')"
          class="font-['Inter'] text-sm text-neutral-500 hover:text-[#ffb13d] hover:underline transition-all focus:ring-2 focus:ring-orange-500 outline-none cursor-pointer bg-transparent border-none"
        >
          Privacidade
        </button>
        <button
          @click="$emit('navigate', 'seguranca')"
          class="font-['Inter'] text-sm text-neutral-500 hover:text-[#ffb13d] hover:underline transition-all focus:ring-2 focus:ring-orange-500 outline-none cursor-pointer bg-transparent border-none"
        >
          Segurança
        </button>
      </nav>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>
