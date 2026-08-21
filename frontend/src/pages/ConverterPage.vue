<template>
  <div class="w-full bg-brand min-h-screen flex flex-col antialiased">
    <!-- Main Content -->
    <main class="flex-grow max-w-[1180px] w-full mx-auto px-4 md:px-8 pt-[116px] pb-20 flex flex-col gap-10">
      <!-- Hero Section -->
      <section class="text-center flex flex-col items-center gap-4 max-w-3xl mx-auto">
        <span class="uppercase tracking-[0.22em] text-xs font-bold text-orange">Conversor de arquivos online</span>
        <h1 class="text-4xl md:text-6xl font-extrabold text-white tracking-tight leading-tight">
          Converta qualquer arquivo em <span class="text-orange">segundos.</span>
        </h1>
        <p class="text-lg md:text-xl text-muted max-w-xl">
          PDF, imagens, Word, Excel, PowerPoint, CSV e muito mais. Arraste, escolha o formato e converta instantaneamente.
        </p>
      </section>

      <!-- Advertisement Banner -->
      <AdBanner :show-ads="true" placement="headerBanner" />

      <!-- Tab Selector -->
      <div class="flex justify-center">
        <div class="inline-flex bg-[#151515] border border-brand rounded-lg p-1 gap-1 shadow-lg">
          <button
            @click="activeTab = 'convert'"
            :class="[
              'px-6 py-3 rounded-md font-bold text-sm transition-all',
              activeTab === 'convert'
                ? 'bg-orange text-black shadow-[0_0_0_1px_rgba(255,159,28,0.3)]'
                : 'text-muted hover:text-white hover:bg-surface-hover'
            ]"
          >
            Conversão
          </button>
          <button
            @click="activeTab = 'pdf-tools'"
            :class="[
              'px-6 py-3 rounded-md font-bold text-sm transition-all',
              activeTab === 'pdf-tools'
                ? 'bg-orange text-black shadow-[0_0_0_1px_rgba(255,159,28,0.3)]'
                : 'text-muted hover:text-white hover:bg-surface-hover'
            ]"
          >
            Ferramentas PDF
          </button>
        </div>
      </div>

      <!-- Conversion Interface (Tab: Conversão) -->
      <section v-if="activeTab === 'convert'" class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <!-- Main Tool Area -->
        <div class="lg:col-span-2 bg-elevated rounded-xl border border-brand p-6 flex flex-col gap-6 shadow-[0_12px_32px_rgba(0,0,0,0.34)]">

          <!-- Upload Drop Zone -->
          <div
            class="border-2 border-dashed border-brand hover:border-orange hover:bg-surface transition-all duration-200 rounded-lg p-16 flex flex-col items-center justify-center text-center cursor-pointer group relative"
            @click="$refs.fileInput.click()"
            @drop="handleDrop"
            @dragover.prevent
            @dragenter.prevent
          >
            <svg class="w-12 h-12 text-orange mb-3 group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.172 2.828a1 1 0 011.656 0l4 4a1 1 0 11-1.414 1.414L11 6.414V15a1 1 0 11-2 0V6.414L6.586 8.828a1 1 0 111.414-1.414l4-4z" />
            </svg>
            <h3 class="text-lg font-semibold text-white mb-1">Arraste e solte seu arquivo aqui</h3>
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
            <h4 class="text-lg font-semibold text-white">Formato de Saída</h4>
            <div class="grid grid-cols-3 sm:grid-cols-6 gap-2">
              <button
                v-for="format in availableFormats"
                :key="format"
                @click="toggleFormat(format)"
                :class="[
                  'py-2 px-3 rounded-lg border-2 font-medium text-sm transition-all',
                  selectedFormats.includes(format)
                    ? 'border-orange bg-orange text-black shadow-[0_0_0_1px_rgba(255,159,28,0.3)]'
                    : 'border-brand bg-surface text-white hover:border-orange hover:bg-surface-hover'
                ]"
              >
                {{ format }}
              </button>
            </div>
          </div>

          <!-- Action Button -->
          <button
            @click="handleConvert"
            :disabled="!selectedFile || selectedFormats.length === 0 || isConverting"
            :class="[
              'w-full py-3 px-6 rounded-md font-bold text-black transition-all flex items-center justify-center gap-2',
              isConverting || !selectedFile || selectedFormats.length === 0
                ? 'bg-dim text-muted cursor-not-allowed'
                : 'bg-orange hover-bg-orange active:scale-95 shadow-[0_4px_16px_rgba(255,159,28,0.25)]'
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

                <h3 class="text-xl font-bold text-white">Pronto!</h3>
                <p class="text-center text-muted">Seu arquivo foi convertido com sucesso.</p>

                <div class="w-full flex flex-col gap-3 pt-4">
                  <button
                    @click="resetForm"
                    class="w-full py-3 px-6 bg-orange hover-bg-orange text-black font-bold rounded-md transition-all active:scale-95"
                  >
                    Converter Outro
                  </button>
                  <button
                    @click="handleCloseSuccess"
                    class="w-full py-3 px-6 bg-surface hover:bg-surface-hover text-white font-semibold rounded-lg transition-all active:scale-95 border border-brand"
                  >
                    Fechar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Status Panel (Sidebar) -->
        <aside class="lg:col-span-1 bg-elevated rounded-xl border border-brand p-6 flex flex-col gap-6 h-full shadow-[0_12px_32px_rgba(0,0,0,0.34)]">
          <div class="border-b border-brand pb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-white">Informações</h2>
            <svg class="w-5 h-5 text-dim" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>

          <ul class="flex flex-col gap-4 text-sm text-muted">
            <li><strong class="text-white">Tamanho máximo:</strong> 50 MB</li>
            <li><strong class="text-white">Entrada:</strong> PDF, PNG, JPG, WEBP, GIF, BMP, DOCX, XLSX, PPTX, TXT, CSV</li>
            <li><strong class="text-white">Saída:</strong> depende do tipo enviado</li>
            <li><strong class="text-white">Segurança:</strong> Arquivos deletados após 1 hora</li>
            <li><strong class="text-white">Múltiplos formatos:</strong> Receba um ZIP</li>
          </ul>
        </aside>
      </section>

      <!-- PDF Tools Interface (Tab: Ferramentas PDF) -->
      <section v-if="activeTab === 'pdf-tools'" class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <!-- Main Tool Area -->
        <div class="lg:col-span-2 bg-elevated rounded-xl border border-brand p-6 flex flex-col gap-6 shadow-[0_12px_32px_rgba(0,0,0,0.34)]">

          <!-- Tool Selector -->
          <div class="flex flex-col gap-2">
            <h4 class="text-lg font-semibold text-white">Selecione uma ferramenta</h4>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
              <button
                v-for="tool in pdfTools"
                :key="tool.id"
                @click="activeTool = tool.id"
                :class="[
                  'py-3 px-3 rounded-lg border-2 font-medium text-sm transition-all flex flex-col items-center gap-1',
                  activeTool === tool.id
                    ? 'border-orange bg-orange text-black shadow-[0_0_0_1px_rgba(255,159,28,0.3)]'
                    : 'border-brand bg-surface text-white hover:border-orange hover:bg-surface-hover'
                ]"
              >
                <span class="text-2xl">{{ tool.emoji }}</span>
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

                <h3 class="text-xl font-bold text-white">Pronto!</h3>
                <p class="text-center text-muted">Operação concluída com sucesso.</p>

                <div class="w-full flex flex-col gap-3 pt-4">
                  <button
                    @click="resetToolForm"
                    class="w-full py-3 px-6 bg-orange hover-bg-orange text-black font-bold rounded-md transition-all active:scale-95"
                  >
                    Nova Operação
                  </button>
                  <button
                    @click="handleCloseToolSuccess"
                    class="w-full py-3 px-6 bg-surface hover:bg-surface-hover text-white font-semibold rounded-lg transition-all active:scale-95 border border-brand"
                  >
                    Fechar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Status Panel (Sidebar) -->
        <aside class="lg:col-span-1 bg-elevated rounded-xl border border-brand p-6 flex flex-col gap-6 h-full shadow-[0_12px_32px_rgba(0,0,0,0.34)]">
          <div class="border-b border-brand pb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-white">Ferramentas</h2>
            <svg class="w-5 h-5 text-dim" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
            </svg>
          </div>

          <ul class="flex flex-col gap-4 text-sm text-muted">
            <li><strong class="text-white">Unir PDFs:</strong> Combine múltiplos arquivos</li>
            <li><strong class="text-white">Dividir:</strong> Separe páginas em arquivos</li>
            <li><strong class="text-white">Rotacionar:</strong> Gire páginas 90°/180°/270°</li>
            <li><strong class="text-white">Marca d'água:</strong> Texto personalizado</li>
            <li><strong class="text-white">Proteger:</strong> Senha e permissões</li>
          </ul>
        </aside>
      </section>

      <!-- Bottom Advertisement Banner -->
      <AdBanner :show-ads="true" placement="footerBanner" />
    </main>
  </div>
</template>

<script>
import ConversionStatus from '../components/ConversionStatus.vue'
import AdBanner from '../components/AdBanner.vue'
import conversionService from '../services/conversionService.js'

// Lazy-load PDF tools to reduce initial bundle size
const PDFMerge = () => import('../components/PDFMerge.vue')
const PDFSplit = () => import('../components/PDFSplit.vue')
const PDFRotate = () => import('../components/PDFRotate.vue')
const PDFWatermark = () => import('../components/PDFWatermark.vue')
const PDFProtect = () => import('../components/PDFProtect.vue')

export default {
  name: 'ConverterPage',
  components: {
    ConversionStatus,
    AdBanner,
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
        { id: 'merge', name: 'Unir PDFs', emoji: '📄' },
        { id: 'split', name: 'Dividir', emoji: '✂️' },
        { id: 'rotate', name: 'Rotacionar', emoji: '🔄' },
        { id: 'watermark', name: 'Marca d\'Água', emoji: '💧' },
        { id: 'protect', name: 'Proteger', emoji: '🔒' }
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
      progressInterval: null
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
    async handleConvert() {
      if (!this.selectedFile || this.selectedFormats.length === 0) {
        this.errorMessage = 'Selecione um arquivo e pelo menos um formato'
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
        this.selectedFormats
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
.background {
  background-color: #faf9ff;
}
</style>
