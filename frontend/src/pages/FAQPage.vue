<template>
  <div class="w-full bg-brand min-h-screen flex flex-col antialiased">
    <!-- Main Content -->
    <main class="flex-grow max-w-[1120px] w-full mx-auto px-4 md:px-8 pt-[120px] pb-20 flex flex-col gap-12">
      <!-- Hero Section -->
      <section class="text-center max-w-3xl mx-auto flex flex-col gap-3">
        <h1 class="text-5xl font-bold text-white">Central de Ajuda</h1>
        <p class="text-lg text-muted">
          Tudo o que você precisa saber para converter seus documentos com segurança, rapidez e eficiência.
        </p>
      </section>

      <!-- Step-by-Step Section -->
      <section class="flex flex-col gap-6">
        <h2 class="text-4xl font-bold text-white text-center">Como Converter</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Step 1 -->
          <div class="bg-elevated border border-brand rounded-xl p-6 flex flex-col items-center text-center gap-4 shadow-[0_12px_32px_rgba(0,0,0,0.34)] hover:shadow-orange-glow transition-shadow">
            <div class="bg-primary/20 text-primary w-16 h-16 rounded-full flex items-center justify-center mb-2">
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 17a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2zm0-5a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2zM3 5a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V5z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white">1. Envie o Arquivo</h3>
            <p class="text-muted">
              Arraste e solte seu documento na área de conversão ou clique para selecionar do seu dispositivo.
            </p>
          </div>

          <!-- Step 2 -->
          <div class="bg-elevated border border-brand rounded-xl p-6 flex flex-col items-center text-center gap-4 shadow-[0_12px_32px_rgba(0,0,0,0.34)] hover:shadow-orange-glow transition-shadow">
            <div class="bg-primary/20 text-primary w-16 h-16 rounded-full flex items-center justify-center mb-2">
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white">2. Configure</h3>
            <p class="text-muted">
              Escolha o formato de saída desejado. Nosso motor inteligente ajustará as configurações automaticamente.
            </p>
          </div>

          <!-- Step 3 -->
          <div class="bg-elevated border border-brand rounded-xl p-6 flex flex-col items-center text-center gap-4 shadow-[0_12px_32px_rgba(0,0,0,0.34)] hover:shadow-orange-glow transition-shadow">
            <div class="bg-primary/20 text-primary w-16 h-16 rounded-full flex items-center justify-center mb-2">
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1v-2zm0-5a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V5z" clip-rule="evenodd" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white">3. Baixe</h3>
            <p class="text-muted">
              Em segundos seu arquivo estará pronto. Clique em baixar e salve o novo documento com qualidade perfeita.
            </p>
          </div>
        </div>
      </section>

      <!-- Formats & Security -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Formats -->
        <section class="bg-elevated border border-brand rounded-xl p-8 flex flex-col gap-6 shadow-[0_12px_32px_rgba(0,0,0,0.34)]">
          <div class="flex items-center gap-3">
            <svg class="w-6 h-6 text-primary" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" />
            </svg>
            <h2 class="text-xl font-semibold text-white">Formatos Suportados</h2>
          </div>
          <p class="text-muted">
            Nossa ferramenta suporta uma ampla gama de extensões para conversão mantendo a integridade visual e textual.
          </p>
          <div class="flex flex-wrap gap-2 mt-auto pt-4">
            <span class="bg-surface text-white font-medium px-3 py-1 rounded-full border border-brand">PDF</span>
            <span class="bg-surface text-white font-medium px-3 py-1 rounded-full border border-brand">DOCX</span>
            <span class="bg-surface text-white font-medium px-3 py-1 rounded-full border border-brand">XLSX</span>
            <span class="bg-surface text-white font-medium px-3 py-1 rounded-full border border-brand">PPTX</span>
            <span class="bg-surface text-white font-medium px-3 py-1 rounded-full border border-brand">JPG</span>
            <span class="bg-surface text-white font-medium px-3 py-1 rounded-full border border-brand">PNG</span>
            <span class="bg-surface text-white font-medium px-3 py-1 rounded-full border border-brand">TXT</span>
            <span class="bg-surface text-white font-medium px-3 py-1 rounded-full border border-brand">CSV</span>
            <span class="bg-surface text-white font-medium px-3 py-1 rounded-full border border-brand">WEBP</span>
          </div>
        </section>

        <!-- Security -->
        <section class="bg-elevated border border-brand rounded-xl p-8 flex flex-col gap-6 shadow-[0_12px_32px_rgba(0,0,0,0.34)]">
          <div class="flex items-center gap-3">
            <svg class="w-6 h-6 text-success" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
            </svg>
            <h2 class="text-xl font-semibold text-white">Segurança</h2>
          </div>
          <p class="text-muted">
            Seus documentos são processados com criptografia de ponta a ponta e deletados automaticamente após 1 hora.
          </p>
          <ul class="flex flex-col gap-3 text-sm text-muted mt-auto pt-4">
            <li class="flex items-center gap-2">
              <span class="text-success">✓</span>
              Limite de 50MB por arquivo
            </li>
            <li class="flex items-center gap-2">
              <span class="text-success">✓</span>
              Arquivos deletados após 1 hora
            </li>
            <li class="flex items-center gap-2">
              <span class="text-success">✓</span>
              Processamento sem histórico público
            </li>
            <li class="flex items-center gap-2">
              <span class="text-success">✓</span>
              Sem anúncios ou rastreamento
            </li>
          </ul>
        </section>
      </div>

      <!-- FAQ Items -->
      <section class="flex flex-col gap-6">
        <h2 class="text-4xl font-bold text-white text-center">Perguntas Frequentes</h2>
        <div class="space-y-4">
          <div
            v-for="(faq, index) in faqs"
            :key="index"
            class="bg-elevated border border-brand rounded-xl overflow-hidden"
          >
            <button
              @click="toggleFaq(index)"
              class="w-full px-6 py-4 flex items-center justify-between hover:bg-surface-hover transition-colors"
            >
              <h3 class="text-lg font-semibold text-white text-left">{{ faq.question }}</h3>
              <svg
                :class="['w-5 h-5 text-dim transition-transform', expandedFaq === index && 'rotate-180']"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </button>
            <div v-if="expandedFaq === index" class="px-6 py-4 border-t border-brand bg-surface">
              <p class="text-muted">{{ faq.answer }}</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'FAQPage',
  data() {
    return {
      expandedFaq: null,
      faqs: [
        {
          question: 'Qual é o tamanho máximo de arquivo que posso converter?',
          answer: 'O tamanho máximo é de 50MB por arquivo. Se seu PDF for maior, você pode dividi-lo em partes menores antes de enviar.'
        },
        {
          question: 'Meus arquivos são seguros?',
          answer: 'Sim! Todos os arquivos são processados com segurança e deletados automaticamente após 1 hora. Nós não armazenamos nenhum histórico de suas conversões.'
        },
        {
          question: 'Posso converter múltiplos PDFs de uma vez?',
          answer: 'Atualmente, você pode converter um arquivo por vez. Porém, você pode selecionar múltiplos formatos de saída para receber todos em um arquivo ZIP.'
        },
        {
          question: 'Quanto tempo leva para converter um arquivo?',
          answer: 'A maioria das conversões é concluída em segundos, dependendo do tamanho e complexidade do arquivo. Arquivos muito grandes podem levar um pouco mais.'
        },
        {
          question: 'Preciso criar uma conta para usar?',
          answer: 'Não! Você pode usar nossa ferramenta gratuitamente sem criar qualquer conta ou fazer login.'
        },
        {
          question: 'Quais formatos de saída estão disponíveis?',
          answer: 'Oferecemos conversão para: DOCX (Word), XLSX (Excel), PPTX (PowerPoint), PNG (Imagem), JPG (Imagem) e TXT (Texto).'
        }
      ]
    }
  },
  methods: {
    toggleFaq(index) {
      this.expandedFaq = this.expandedFaq === index ? null : index
    }
  }
}
</script>

<style scoped>
.background {
  background-color: var(--color-bg);
}
</style>