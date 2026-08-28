<template>
  <div class="w-full bg-brand min-h-screen flex flex-col antialiased">
    <!-- Main Content -->
    <main class="flex-grow max-w-[1180px] w-full mx-auto px-4 md:px-8 pt-[116px] pb-20 flex flex-col gap-10">
      <!-- Hero Section -->
      <section class="hero-copy text-center flex flex-col items-center gap-4 max-w-3xl mx-auto">
        <span class="hero-kicker uppercase tracking-[0.22em] text-xs font-bold text-red">Conversor de arquivos online</span>
        <h1 class="hero-title text-4xl md:text-6xl font-extrabold text-brand tracking-tight leading-tight">
          Converta qualquer arquivo em <span class="hero-accent text-red">segundos.</span>
        </h1>
        <p class="hero-description text-lg md:text-xl text-muted max-w-xl">
          PDF, imagens, Word, Excel, PowerPoint, CSV e muito mais. Arraste, escolha o formato e converta instantaneamente.
        </p>
      </section>

      <!-- Tab Selector -->
      <div class="flex justify-center">
        <div class="inline-flex bg-surface border border-brand rounded-lg p-1 gap-1 shadow-lg">
          <button
            @click="activeTab = 'convert'"
            :class="[
              'px-6 py-3 rounded-md font-bold text-sm transition-all',
              activeTab === 'convert'
                ? 'bg-red text-white shadow-red-glow'
                : 'text-muted hover:text-brand hover:bg-surface-hover'
            ]"
          >
            Conversão
          </button>
          <button
            @click="activeTab = 'pdf-tools'"
            :class="[
              'px-6 py-3 rounded-md font-bold text-sm transition-all',
              activeTab === 'pdf-tools'
                ? 'bg-red text-white shadow-red-glow'
                : 'text-muted hover:text-brand hover:bg-surface-hover'
            ]"
          >
            Ferramentas PDF
          </button>
        </div>
      </div>

      <!-- Conversion Interface (Tab: Conversão) -->
      <section v-if="activeTab === 'convert'" class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <!-- Main Tool Area -->
        <div class="lg:col-span-2 bg-elevated rounded-xl border border-brand p-6 flex flex-col gap-6 shadow-[0_12px_32px_rgba(0,0,0,0.1)]">

          <!-- Upload Drop Zone -->
          <div
            class="border-2 border-dashed border-brand hover:border-red hover:bg-surface transition-all duration-200 rounded-lg p-16 flex flex-col items-center justify-center text-center cursor-pointer group relative"
            @click="$refs.fileInput.click()"
            @drop="handleDrop"
            @dragover.prevent
            @dragenter.prevent
          >
            <svg class="w-12 h-12 text-red mb-3 group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.172 2.828a1 1 0 011.656 0l4 4a1 1 0 11-1.414 1.414L11 6.414V15a1 1 0 11-2 0V6.414L6.586 8.828a1 1 0 111.414-1.414l4-4z" />
            </svg>
            <h3 class="text-lg font-semibold text-brand mb-1">Arraste e solte seu arquivo aqui</h3>
            <p class="text-sm text-muted">ou clique para procurar no seu computador</p>
            <p class="text-xs text-dim mt-1">PDF · PNG · JPG · WEBP · DOCX · XLSX · PPTX · TXT · CSV</p>
            <input
              ref="fileInput"
              type="file"
              accept=".pdf,.png,.jpg,.jpeg,.webp,.gif,.bmp,.docx,.xlsx,.pptx,.txt,.csv"
              @change="handleFileSelect"
              class="hidden"
            />
            <p v-if="selectedFile" class="mt-4 text-sm text-success flex items-center gap-2">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              {{ selectedFile.name }}
            </p>
          </div>

          <!-- Format Selection -->
          <div class="flex flex-col gap-3">
            <h4 class="text-lg font-semibold text-brand">Formato de Saída</h4>
            <div class="grid grid-cols-3 sm:grid-cols-6 gap-2">
              <button
                v-for="format in availableFormats"
                :key="format"
                @click="toggleFormat(format)"
                :class="[
                  'py-2 px-3 rounded-lg border-2 font-medium text-sm transition-all',
                  selectedFormats.includes(format)
                    ? 'border-red bg-red text-white shadow-red-glow'
                    : 'border-brand bg-surface text-brand hover:border-red hover:bg-surface-hover'
                ]"
              >
                {{ format }}
              </button>
            </div>
          </div>

          <!-- Turnstile Captcha -->
          <div v-if="selectedFile && selectedFormats.length > 0" class="flex justify-center">
            <Turnstile
              ref="turnstile"
              :site-key="turnstileSiteKey"
              theme="light"
              @verify="onTurnstileVerify"
              @expired="onTurnstileExpired"
              @error="onTurnstileError"
            />
          </div>

          <!-- Action Button -->
          <button
            @click="handleConvert"
            :disabled="!selectedFile || selectedFormats.length === 0 || isConverting || !turnstileToken"
            :class="[
              'w-full py-3 px-6 rounded-md font-bold text-white transition-all flex items-center justify-center gap-2',
              isConverting || !selectedFile || selectedFormats.length === 0 || !turnstileToken
                ? 'bg-dim text-muted cursor-not-allowed'
                : 'bg-red hover-bg-red active:scale-95 shadow-red-glow'
            ]"
          >
            <svg v-if="!isConverting" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>{{ isConverting ? 'Convertendo...' : 'Converter Agora' }}</span>
          </button>

          <!-- Status Messages -->
          <ConversionStatus
            :status="conversionStatus"
            :error-message="errorMessage"
            :progress="conversionProgress"
            :estimated-time="estimatedTime"
            @close="resetForm"
          />

          <!-- Success Dialog -->
          <div
            v-if="conversionStatus === 'success'"
            class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            @click="resetForm"
          >
            <div
              class="bg-elevated rounded-2xl p-8 max-w-sm w-full shadow-2xl border border-brand"
              @click.stop
            >
              <div class="flex flex-col items-center gap-4">
                <div class="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center border border-green-500/30">
                  <svg class="w-8 h-8 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>

                <h3 class="text-xl font-bold text-brand">Pronto!</h3>
                <p class="text-center text-muted">Seu arquivo foi convertido com sucesso.</p>

                <div class="w-full flex flex-col gap-3 pt-4">
                  <button
                    @click="resetForm"
                    class="w-full py-3 px-6 bg-red hover-bg-red text-white font-bold rounded-md transition-all active:scale-95"
                  >
                    Converter Outro
                  </button>
                  <button
                    @click="handleCloseSuccess"
                    class="w-full py-3 px-6 bg-surface hover:bg-surface-hover text-brand font-semibold rounded-lg transition-all active:scale-95 border border-brand"
                  >
                    Fechar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Status Panel (Sidebar) -->
        <aside class="lg:col-span-1 bg-elevated rounded-xl border border-brand p-6 flex flex-col gap-6 h-full shadow-[0_12px_32px_rgba(0,0,0,0.1)]">
          <div class="border-b border-brand pb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-brand">Informações</h2>
            <svg class="w-5 h-5 text-dim" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>

          <ul class="flex flex-col gap-4 text-sm text-muted">
            <li><strong class="text-brand">Tamanho máximo:</strong> 50 MB</li>
            <li><strong class="text-brand">Entrada:</strong> PDF, PNG, JPG, WEBP, GIF, BMP, DOCX, XLSX, PPTX, TXT, CSV</li>
            <li><strong class="text-brand">Saída:</strong> depende do tipo enviado</li>
            <li><strong class="text-brand">Segurança:</strong> Arquivos deletados após 1 hora</li>
            <li><strong class="text-brand">Múltiplos formatos:</strong> Receba um ZIP</li>
          </ul>
        </aside>
      </section>

      <!-- PDF Tools Interface (Tab: Ferramentas PDF) -->
      <section v-if="activeTab === 'pdf-tools'" class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <!-- Main Tool Area -->
        <div class="lg:col-span-2 bg-elevated rounded-xl border border-brand p-6 flex flex-col gap-6 shadow-[0_12px_32px_rgba(0,0,0,0.1)]">

          <!-- Tool Selector -->
          <div class="flex flex-col gap-2">
            <h4 class="text-lg font-semibold text-brand">Selecione uma ferramenta</h4>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
              <button
                v-for="tool in pdfTools"
                :key="tool.id"
                @click="activeTool = tool.id"
                :class="[
                  'py-3 px-3 rounded-lg border-2 font-medium text-sm transition-all flex flex-col items-center gap-1',
                  activeTool === tool.id
                    ? 'border-red bg-red text-white shadow-red-glow'
                    : 'border-brand bg-surface text-brand hover:border-red hover:bg-surface-hover'
                ]"
              >
                <svg v-if="tool.id === 'merge'" class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M7 3h7l4 4v14H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Z" />
                  <path stroke-linecap="round" d="M14 3v5h5M8 13h6m-6 4h6" />
                </svg>
                <svg v-else-if="tool.id === 'split'" class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                  <circle cx="6" cy="6" r="2.5" />
                  <circle cx="6" cy="18" r="2.5" />
                  <path stroke-linecap="round" d="m8.2 7.4 9.8 9.2M8.2 16.6 12 13m0 0 6-6" />
                </svg>
                <svg v-else-if="tool.id === 'rotate'" class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 7v5h5M20 17v-5h-5" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6.3 12A6 6 0 0 1 17 7.2L20 10M18 12a6 6 0 0 1-10.7 4.8L4 14" />
                </svg>
                <svg v-else-if="tool.id === 'watermark'" class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 3.5S6.5 9.2 6.5 13.5a5.5 5.5 0 0 0 11 0C17.5 9.2 12 3.5 12 3.5Z" />
                  <path stroke-linecap="round" d="M9.5 16a3 3 0 0 0 4.5.5" />
                </svg>
                <svg v-else class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 3 5 6v5c0 4.4 2.8 8.4 7 10 4.2-1.6 7-5.6 7-10V6l-7-3Z" />
                  <rect width="5" height="4.5" x="9.5" y="10" rx="1" />
                  <path stroke-linecap="round" d="M11 10V8.8a1 1 0 0 1 2 0V10" />
                </svg>
                <span>{{ tool.name }}</span>
              </button>
            </div>
          </div>

          <!-- Tool Components -->
          <div class="tool-container">
            <PDFMerge
              v-if="activeTool === 'merge'"
              @merge="handleMerge"
              @error="$emit('error', $event)"
            />
            <PDFSplit
              v-else-if="activeTool === 'split'"
              @split="handleSplit"
              @error="$emit('error', $event)"
            />
            <PDFRotate
              v-else-if="activeTool === 'rotate'"
              @rotate="handleRotate"
              @error="$emit('error', $event)"
            />
            <PDFWatermark
              v-else-if="activeTool === 'watermark'"
              @watermark="handleWatermark"
              @error="$emit('error', $event)"
            />
            <PDFProtect
              v-else-if="activeTool === 'protect'"
              @protect="handleProtect"
              @error="$emit('error', $event)"
            />
          </div>

          <!-- Status Messages -->
          <ConversionStatus
            :status="toolStatus"
            :error-message="toolErrorMessage"
            :progress="toolProgress"
            :estimated-time="toolEstimatedTime"
            @close="resetToolForm"
          />

          <!-- Success Dialog -->
          <div
            v-if="toolStatus === 'success'"
            class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
            @click="resetToolForm"
          >
            <div
              class="bg-elevated rounded-2xl p-8 max-w-sm w-full shadow-2xl border border-brand"
              @click.stop
            >
              <div class="flex flex-col items-center gap-4">
                <div class="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center border border-green-500/30">
                  <svg class="w-8 h-8 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>

                <h3 class="text-xl font-bold text-brand">Pronto!</h3>
                <p class="text-center text-muted">Operação concluída com sucesso.</p>

                <div class="w-full flex flex-col gap-3 pt-4">
                  <button
                    @click="resetToolForm"
                    class="w-full py-3 px-6 bg-red hover-bg-red text-white font-bold rounded-md transition-all active:scale-95"
                  >
                    Nova Operação
                  </button>
                  <button
                    @click="handleCloseToolSuccess"
                    class="w-full py-3 px-6 bg-surface hover:bg-surface-hover text-brand font-semibold rounded-lg transition-all active:scale-95 border border-brand"
                  >
                    Fechar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Status Panel (Sidebar) -->
        <aside class="lg:col-span-1 bg-elevated rounded-xl border border-brand p-6 flex flex-col gap-6 h-full shadow-[0_12px_32px_rgba(0,0,0,0.1)]">
          <div class="border-b border-brand pb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-brand">Ferramentas</h2>
            <svg class="w-5 h-5 text-dim" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>

          <ul class="flex flex-col gap-4 text-sm text-muted">
            <li><strong class="text-brand">Unir PDFs:</strong> Combine múltiplos arquivos</li>
            <li><strong class="text-brand">Dividir:</strong> Separe páginas em arquivos</li>
            <li><strong class="text-brand">Rotacionar:</strong> Gire páginas 90°/180°/270°</li>
            <li><strong class="text-brand">Marca d'água:</strong> Texto personalizado</li>
            <li><strong class="text-brand">Proteger:</strong> Senha e permissões</li>
          </ul>
        </aside>
      </section>

    </main>
  </div>
</template>

<script>
import { defineAsyncComponent } from 'vue'
import ConversionStatus from '../components/ConversionStatus.vue'
import Turnstile from '../components/Turnstile.vue'
import conversionService from '../services/conversionService.js'

// Lazy-load PDF tools to reduce initial bundle size
const PDFMerge = defineAsyncComponent(() => import('../components/PDFMerge.vue'))
const PDFSplit = defineAsyncComponent(() => import('../components/PDFSplit.vue'))
const PDFRotate = defineAsyncComponent(() => import('../components/PDFRotate.vue'))
const PDFWatermark = defineAsyncComponent(() => import('../components/PDFWatermark.vue'))
const PDFProtect = defineAsyncComponent(() => import('../components/PDFProtect.vue'))

export default {
  name: 'ConverterPage',
  components: {
    ConversionStatus,
    Turnstile,
    PDFMerge,
    PDFSplit,
    PDFRotate,
    PDFWatermark,
    PDFProtect
  },
  data() {
    return {
      // Tab system
      activeTab: 'convert',
      // PDF tools
      activeTool: 'merge',
      toolStatus: 'idle',
      toolErrorMessage: '',
      toolProgress: 0,
      toolEstimatedTime: null,
      toolProgressInterval: null,
      pdfTools: [
        { id: 'merge', name: 'Unir PDFs' },
        { id: 'split', name: 'Dividir' },
        { id: 'rotate', name: 'Rotacionar' },
        { id: 'watermark', name: 'Marca d\'Água' },
        { id: 'protect', name: 'Proteger' }
      ],
      // Conversion
      selectedFile: null,
      selectedFormats: [],
      availableFormats: [],
      conversionStatus: 'idle',
      isConverting: false,
      errorMessage: '',
      conversionProgress: 0,
      estimatedTime: null,
      progressInterval: null,
      // Turnstile
      turnstileSiteKey: import.meta.env.VITE_TURNSTILE_SITE_KEY || '0x4AAAAAAAExampleKey',
      turnstileToken: null
    }
  },
  methods: {
    SUPPORTED_CONVERSIONS() {
      return {
        pdf:  ['PNG', 'JPG', 'TXT', 'DOCX', 'XLSX', 'COMPRESS'],
        png:  ['PDF', 'JPG', 'WEBP'],
        jpg:  ['PDF', 'PNG', 'WEBP'],
        jpeg: ['PDF', 'PNG', 'WEBP'],
        webp: ['PDF', 'PNG', 'JPG'],
        gif:  ['PDF', 'PNG', 'JPG'],
        bmp:  ['PDF', 'PNG', 'JPG'],
        docx: ['PDF', 'TXT'],
        xlsx: ['PDF', 'CSV', 'TXT'],
        pptx: ['PDF', 'TXT'],
        txt:  ['PDF', 'DOCX'],
        csv:  ['XLSX', 'TXT'],
      }
    },
    getFileExtension(filename) {
      return filename.split('.').pop().toLowerCase()
    },
    setFileAndFormats(file) {
      this.selectedFile = file
      this.errorMessage = ''
      const ext = this.getFileExtension(file.name)
      this.availableFormats = this.SUPPORTED_CONVERSIONS()[ext] || []
      this.selectedFormats = this.availableFormats.length ? [this.availableFormats[0]] : []
      if (!this.availableFormats.length) {
        this.errorMessage = `Tipo de arquivo não suportado: .${ext}`
        this.conversionStatus = 'error'
        this.selectedFile = null
      }
    },
    handleDrop(e) {
      e.preventDefault()
      const files = e.dataTransfer.files
      if (files.length > 0) {
        this.setFileAndFormats(files[0])
      }
    },
    handleFileSelect() {
      const file = this.$refs.fileInput.files[0]
      if (file) {
        this.setFileAndFormats(file)
      }
    },
    toggleFormat(format) {
      const index = this.selectedFormats.indexOf(format)
      if (index > -1) {
        this.selectedFormats.splice(index, 1)
      } else {
        this.selectedFormats.push(format)
      }
    },
    // Turnstile methods
    onTurnstileVerify(token) {
      this.turnstileToken = token
    },
    onTurnstileExpired() {
      this.turnstileToken = null
    },
    onTurnstileError() {
      this.turnstileToken = null
      this.errorMessage = 'Erro na verificação do captcha. Tente novamente.'
      this.conversionStatus = 'error'
    },
    async handleConvert() {
      if (!this.selectedFile || this.selectedFormats.length === 0) {
        this.errorMessage = 'Selecione um arquivo e pelo menos um formato'
        this.conversionStatus = 'error'
        return
      }

      if (!this.turnstileToken) {
        this.errorMessage = 'Complete a verificação do captcha'
        this.conversionStatus = 'error'
        return
      }

      this.isConverting = true
      this.conversionStatus = 'loading'
      this.errorMessage = ''
      this.conversionProgress = 0
      this.estimatedTime = 30

      this.progressInterval = setInterval(() => {
        if (this.conversionProgress < 90) {
          this.conversionProgress += Math.random() * 20
          if (this.conversionProgress > 90) this.conversionProgress = 90
          this.estimatedTime = Math.max(1, this.estimatedTime - 1)
        }
      }, 500)

      const result = await conversionService.convertFile(
        this.selectedFile,
        this.selectedFormats,
        this.turnstileToken
      )

      this.isConverting = false
      clearInterval(this.progressInterval)
      this.conversionProgress = 100
      this.estimatedTime = null

      if (result.success) {
        this.conversionStatus = 'success'

        const url = window.URL.createObjectURL(result.data)
        const link = document.createElement('a')
        link.href = url

        const baseName = this.selectedFile.name.replace(/\.[^.]+$/, '')
        let downloadName
        if (this.selectedFormats.length === 1) {
          const fmt = this.selectedFormats[0].toLowerCase()
          const ext = fmt === 'compress' ? 'pdf' : fmt
          const suffix = fmt === 'compress' ? '_compressed' : '_converted'
          downloadName = `${baseName}${suffix}.${ext}`
        } else {
          downloadName = `${baseName}_converted.zip`
        }
        link.download = downloadName

        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
      } else {
        this.conversionStatus = 'error'
        this.errorMessage = result.error || 'Erro desconhecido na conversão'
      }
    },
    resetForm() {
      this.selectedFile = null
      this.selectedFormats = []
      this.conversionStatus = 'idle'
      this.errorMessage = ''
      this.conversionProgress = 0
      this.estimatedTime = null
      this.turnstileToken = null
      if (this.$refs.turnstile) {
        this.$refs.turnstile.reset()
      }
      if (this.progressInterval) clearInterval(this.progressInterval)
    },
    handleCloseSuccess() {
      this.conversionStatus = 'idle'
    },

    // ───────────────── PDF Tools ─────────────────
    _startToolProgress() {
      this.toolStatus = 'loading'
      this.toolErrorMessage = ''
      this.toolProgress = 0
      this.toolEstimatedTime = 30
      this.toolProgressInterval = setInterval(() => {
        if (this.toolProgress < 90) {
          this.toolProgress += Math.random() * 15
          if (this.toolProgress > 90) this.toolProgress = 90
          this.toolEstimatedTime = Math.max(1, this.toolEstimatedTime - 1)
        }
      }, 500)
    },
    _finishToolProgress(result) {
      clearInterval(this.toolProgressInterval)
      this.toolProgress = 100
      this.toolEstimatedTime = null

      if (result.success) {
        this.toolStatus = 'success'
        const url = window.URL.createObjectURL(result.data)
        const link = document.createElement('a')
        link.href = url
        link.download = result.filename || 'resultado.pdf'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
      } else {
        this.toolStatus = 'error'
        this.toolErrorMessage = result.error || 'Erro desconhecido'
      }
    },
    async handleMerge(files) {
      this._startToolProgress()
      const result = await conversionService.mergePdfs(files)
      this._finishToolProgress({ ...result, filename: 'merged.pdf' })
    },
    async handleSplit(file, options) {
      this._startToolProgress()
      const result = await conversionService.splitPdf(file, options)
      this._finishToolProgress({ ...result, filename: 'split.pdf' })
    },
    async handleRotate(file, options) {
      this._startToolProgress()
      const result = await conversionService.rotatePdf(file, options)
      this._finishToolProgress({ ...result, filename: 'rotated.pdf' })
    },
    async handleWatermark(file, options) {
      this._startToolProgress()
      const result = await conversionService.watermarkPdf(file, options)
      this._finishToolProgress({ ...result, filename: 'watermarked.pdf' })
    },
    async handleProtect(file, options) {
      this._startToolProgress()
      const result = await conversionService.protectPdf(file, options)
      this._finishToolProgress({ ...result, filename: 'protected.pdf' })
    },
    resetToolForm() {
      this.toolStatus = 'idle'
      this.toolErrorMessage = ''
      this.toolProgress = 0
      this.toolEstimatedTime = null
      if (this.toolProgressInterval) clearInterval(this.toolProgressInterval)
    },
    handleCloseToolSuccess() {
      this.toolStatus = 'idle'
    }
  }
}
</script>

<style scoped>
.hero-copy > * {
  opacity: 0;
  animation: hero-rise 700ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.hero-kicker { animation-delay: 80ms; }
.hero-title { animation-delay: 180ms; }
.hero-description { animation-delay: 300ms; }

.hero-accent {
  display: inline-block;
  animation: accent-breathe 2.8s ease-in-out 900ms infinite;
}

@keyframes hero-rise {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes accent-breathe {
  0%, 100% { text-shadow: 0 0 0 var(--color-primary-glow); }
  50% { text-shadow: 0 0 18px var(--color-primary-glow); }
}

@media (prefers-reduced-motion: reduce) {
  .hero-copy > *, .hero-accent {
    animation: none;
    opacity: 1;
  }
}

.background {
  background-color: #faf9ff;
}
</style>