<template>
  <div v-if="pdfUrl" class="pdf-preview">
    <div class="preview-header">
      <h4>Pré-visualização</h4>
      <div class="preview-controls">
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="preview-btn"
          :class="{ disabled: currentPage === 1 }"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <span class="page-indicator">{{ currentPage }} / {{ pageCount }}</span>
        <button
          @click="nextPage"
          :disabled="currentPage === pageCount"
          class="preview-btn"
          :class="{ disabled: currentPage === pageCount }"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
        <input
          type="range"
          :min="1"
          :max="pageCount"
          v-model.number="currentPage"
          class="page-slider"
        />
      </div>
    </div>
    <div class="preview-canvas-container" @wheel.prevent="handleWheel">
      <canvas ref="canvas" class="preview-canvas"></canvas>
    </div>
    <div class="preview-thumbnails" v-if="pageCount > 1">
      <button
        v-for="page in pageCount"
        :key="page"
        @click="currentPage = page"
        :class="['thumb', { active: currentPage === page }]"
      >
        <canvas class="thumb-canvas" :data-page="page"></canvas>
        <span class="thumb-num">{{ page }}</span>
      </button>
    </div>
  </div>
  <div v-else class="pdf-preview empty">
    <div class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
      </svg>
      <p>Nenhum PDF carregado</p>
      <span>Selecione um arquivo para ver a prévia</span>
    </div>
  </div>
</template>

<script>
import { nextTick } from 'vue'
import * as pdfjsLib from 'pdfjs-dist'
import 'pdfjs-dist/build/pdf.worker.min.mjs'

export default {
  name: 'PDFPreview',
  props: {
    file: {
      type: File,
      default: null
    },
    rotation: {
      type: Number,
      default: 0
    },
    selectedPages: {
      type: Array,
      default: () => []
    },
    // Watermark props for preview
    watermarkText: {
      type: String,
      default: ''
    },
    watermarkOpacity: {
      type: Number,
      default: 0.3
    },
    watermarkAngle: {
      type: Number,
      default: 45
    },
    watermarkFontSize: {
      type: Number,
      default: 48
    },
    watermarkColor: {
      type: String,
      default: 'gray'
    }
  },
  data() {
    return {
      pdfDoc: null,
      pageCount: 0,
      currentPage: 1,
      pdfUrl: null,
      scale: 1.2,
      isLoading: false
    }
  },
  watch: {
    file: {
      immediate: true,
      async handler(newFile) {
        if (newFile) {
          await this.loadPDF(newFile)
        } else {
          this.clear()
        }
      }
    },
    async rotation() {
      await this.renderPage()
      await this.renderThumbnails()
    },
    watermarkText() {
      this.renderPage()
      this.renderThumbnails()
    },
    watermarkOpacity() {
      this.renderPage()
      this.renderThumbnails()
    },
    watermarkAngle() {
      this.renderPage()
      this.renderThumbnails()
    },
    watermarkFontSize() {
      this.renderPage()
      this.renderThumbnails()
    },
    watermarkColor() {
      this.renderPage()
      this.renderThumbnails()
    }
  },
  methods: {
    async loadPDF(file) {
      this.isLoading = true
      try {
        this.pdfUrl = URL.createObjectURL(file)
        const arrayBuffer = await file.arrayBuffer()
        this.pdfDoc = await pdfjsLib.getDocument({ data: arrayBuffer }).promise
        this.pageCount = this.pdfDoc.numPages
        this.currentPage = 1
        await nextTick()
        await this.renderPage()
        this.renderThumbnails()
      } catch (err) {
        console.error('Erro ao carregar PDF:', err)
        this.$emit('error', 'Erro ao carregar prévia do PDF')
      } finally {
        this.isLoading = false
      }
    },
    async renderPage() {
      if (!this.pdfDoc) return
      try {
        await nextTick()
        const page = await this.pdfDoc.getPage(this.currentPage)
        const canvas = this.$refs.canvas
        if (!canvas) return
        const viewport = page.getViewport({ scale: this.scale, rotation: this.rotation })

        canvas.width = viewport.width
        canvas.height = viewport.height

        const context = canvas.getContext('2d')
        // Clear canvas with white background for better PDF visibility
        context.fillStyle = '#ffffff'
        context.fillRect(0, 0, canvas.width, canvas.height)

        await page.render({ canvasContext: context, viewport }).promise

        // Render watermark on top if text is provided
        if (this.watermarkText && this.watermarkText.trim()) {
          this.renderWatermark(context, viewport)
        }
      } catch (err) {
        console.error('Erro ao renderizar página:', err)
      }
    },
    renderWatermark(context, viewport) {
      // Save current context state
      context.save()

      // Get center of the page
      const centerX = viewport.width / 2
      const centerY = viewport.height / 2

      // Translate to center
      context.translate(centerX, centerY)

      // Rotate
      const angleRad = (this.watermarkAngle * Math.PI) / 180
      context.rotate(angleRad)

      // Set font
      const fontSize = Math.min(this.watermarkFontSize, Math.min(viewport.width, viewport.height) * 0.1)
      context.font = `bold ${fontSize}px Arial, sans-serif`
      context.textAlign = 'center'
      context.textBaseline = 'middle'

      // Set color and opacity
      const colorMap = {
        'gray': [107, 114, 128],
        'red': [239, 68, 68],
        'blue': [59, 130, 246],
        'green': [34, 197, 94],
        'black': [31, 41, 55]
      }
      const [r, g, b] = colorMap[this.watermarkColor] || colorMap.gray
      context.fillStyle = `rgba(${r}, ${g}, ${b}, ${this.watermarkOpacity})`

      // Draw watermark text
      context.fillText(this.watermarkText, 0, 0)

      // Restore context
      context.restore()
    },
    async renderThumbnails() {
      if (!this.pdfDoc || this.pageCount <= 1) return

      await nextTick()
      for (let i = 1; i <= this.pageCount; i++) {
        const page = await this.pdfDoc.getPage(i)
        const viewport = page.getViewport({ scale: 0.3, rotation: this.rotation })
        const canvas = this.$el.querySelector(`.thumb-canvas[data-page="${i}"]`)
        if (canvas) {
          canvas.width = viewport.width
          canvas.height = viewport.height
          const context = canvas.getContext('2d')
          // Clear canvas with white background for better PDF visibility
          context.fillStyle = '#ffffff'
          context.fillRect(0, 0, canvas.width, canvas.height)
          await page.render({ canvasContext: context, viewport }).promise

          // Render watermark on thumbnails too
          if (this.watermarkText && this.watermarkText.trim()) {
            this.renderWatermark(context, viewport)
          }
        }
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    nextPage() {
      if (this.currentPage < this.pageCount) {
        this.currentPage++
      }
    },
    handleWheel(e) {
      if (e.deltaY > 0) this.nextPage()
      else if (e.deltaY < 0) this.prevPage()
    },
    clear() {
      if (this.pdfUrl) {
        URL.revokeObjectURL(this.pdfUrl)
        this.pdfUrl = null
      }
      this.pdfDoc = null
      this.pageCount = 0
      this.currentPage = 1
    }
  },
  beforeUnmount() {
    this.clear()
  }
}
</script>

<style scoped>
.pdf-preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
}

.pdf-preview.empty {
  min-height: 200px;
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
  background: rgba(255, 159, 28, 0.05);
}

.preview-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
}

.preview-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.preview-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-bg);
  color: #a3a3a3;
  cursor: pointer;
  transition: all 0.2s;
}

.preview-btn:hover:not(.disabled) {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: rgba(255, 159, 28, 0.1);
}

.preview-btn.disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.preview-btn svg {
  width: 18px;
  height: 18px;
}

.page-indicator {
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  min-width: 60px;
  text-align: center;
}

.page-slider {
  width: 120px;
  accent-color: var(--color-primary);
}

.preview-canvas-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  max-height: 500px;
  padding: 20px;
  background: #f5f5f5;
  overflow: auto;
}

.preview-canvas {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border-radius: 4px;
  max-width: 100%;
  height: auto;
  background: #ffffff;
}

.preview-thumbnails {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid var(--color-border);
  overflow-x: auto;
  background: var(--color-bg);
}

.thumb {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 4px;
  border: 2px solid transparent;
  border-radius: 6px;
  background: var(--color-surface);
  cursor: pointer;
  transition: all 0.2s;
  min-width: 60px;
}

.thumb:hover {
  border-color: var(--color-primary);
}

.thumb.active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(255, 159, 28, 0.2);
}

.thumb-canvas {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border-radius: 2px;
}

.thumb-num {
  font-size: 10px;
  font-weight: 600;
  color: #a3a3a3;
}

.thumb.active .thumb-num {
  color: var(--color-primary);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #666;
  text-align: center;
  min-height: 200px;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  color: #333;
  margin-bottom: 12px;
}

.empty-state p {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 500;
  color: #888;
}

.empty-state span {
  font-size: 12px;
  color: #555;
}
</style>