<template>
  <div class="pdf-split">
    <div class="section-header">
      <h3>Dividir PDF</h3>
      <p>Divida seu PDF em múltiplos arquivos</p>
    </div>

    <FileUploader
      accept=".pdf"
      @file-selected="handleFileSelected"
      @error="$emit('error', $event)"
    />

    <div v-if="selectedFile" class="tool-layout">
      <!-- Painel de Controles (Esquerda) -->
      <div class="controls-panel">
        <div class="control-group">
          <label class="control-label">Modo de Divisão</label>

          <label class="radio-option">
            <input type="radio" v-model="splitMode" value="all" name="split-mode" />
            <span class="radio-custom"></span>
            <span class="radio-label">Separar cada página em um arquivo</span>
          </label>

          <label class="radio-option">
            <input type="radio" v-model="splitMode" value="range" name="split-mode" />
            <span class="radio-custom"></span>
            <span class="radio-label">Selecionar intervalos de páginas</span>
          </label>

          <div v-if="splitMode === 'range'" class="ranges-input">
            <p class="input-hint">Exemplo: 1-3, 5-7, 10-12</p>
            <input
              v-model="pageRanges"
              type="text"
              placeholder="1-3,5-7,10-12"
              class="text-input"
            />
          </div>

          <label class="radio-option">
            <input type="radio" v-model="splitMode" value="every_n" name="split-mode" />
            <span class="radio-custom"></span>
            <span class="radio-label">A cada N páginas</span>
          </label>

          <div v-if="splitMode === 'every_n'" class="n-input">
            <input
              v-model.number="pagesPerFile"
              type="number"
              min="1"
              max="100"
              class="text-input small"
              placeholder="5"
            />
            <span>páginas por arquivo</span>
          </div>
        </div>

        <button
          @click="handleSplit"
          :disabled="isProcessing"
          class="action-button primary"
        >
          <span class="btn-text">{{ isProcessing ? 'Processando...' : 'Dividir PDF' }}</span>
          <svg v-if="!isProcessing" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
          </svg>
        </button>
      </div>

      <!-- Pré-visualização (Direita) -->
      <div class="preview-panel">
        <PDFPreview
          :file="selectedFile"
          :selected-pages="getPreviewPages"
        />
      </div>
    </div>
  </div>
</template>

<script>
import FileUploader from './FileUploader.vue'
import PDFPreview from './PDFPreview.vue'

export default {
  name: 'PDFSplit',
  components: { FileUploader, PDFPreview },
  data() {
    return {
      selectedFile: null,
      splitMode: 'all',
      pageRanges: '',
      pagesPerFile: 5,
      isProcessing: false
    }
  },
  computed: {
    getPreviewPages() {
      if (!this.pageRanges) return []
      return this.pageRanges.split(',').map(s => s.trim()).filter(Boolean)
    }
  },
  methods: {
    handleFileSelected(file) {
      this.selectedFile = file
    },
    async handleSplit() {
      if (!this.selectedFile) {
        this.$emit('error', 'Selecione um arquivo PDF')
        return
      }

      if (this.splitMode === 'range' && !this.pageRanges) {
        this.$emit('error', 'Informe os intervalos de páginas')
        return
      }

      if (this.splitMode === 'every_n' && (!this.pagesPerFile || this.pagesPerFile < 1)) {
        this.$emit('error', 'Informe o número de páginas por arquivo')
        return
      }

      this.isProcessing = true
      try {
        const options = {
          splitMode: this.splitMode,
          pageRanges: this.splitMode === 'range' ? this.pageRanges :
                     this.splitMode === 'every_n' ? this.pagesPerFile.toString() : null
        }
        await this.$emit('split', this.selectedFile, options)
      } finally {
        this.isProcessing = false
      }
    }
  }
}
</script>

<style scoped>
.pdf-split {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-header h3 {
  margin: 0;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.section-header p {
  margin: 4px 0 0;
  color: #a3a3a3;
  font-size: 14px;
}

.tool-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

@media (min-width: 960px) {
  .tool-layout {
    grid-template-columns: 360px 1fr;
    align-items: start;
  }
}

.controls-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background-color: var(--color-surface);
  border-radius: 12px;
  border: 1px solid var(--color-border);
  position: sticky;
  top: 88px;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.control-label {
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  font-size: 14px;
  color: #a3a3a3;
  padding: 10px;
  border-radius: 8px;
  transition: all 0.2s;
}

.radio-option:hover {
  background: rgba(255, 159, 28, 0.05);
  color: #fff;
}

.radio-custom {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-radius: 50%;
  position: relative;
  transition: all 0.2s;
  flex-shrink: 0;
}

.radio-option input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.radio-option input:checked + .radio-custom {
  border-color: var(--color-primary);
}

.radio-option input:checked + .radio-custom::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary);
}

.radio-label {
  font-weight: 500;
}

.ranges-input, .n-input {
  margin-left: 32px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.n-input {
  flex-direction: row;
  align-items: center;
  margin-top: 8px;
}

.input-hint {
  margin: 0;
  font-size: 12px;
  color: #737373;
}

.text-input {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  font-size: 14px;
  background-color: var(--color-bg);
  color: var(--color-text);
  transition: border-color 0.2s ease;
}

.text-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.text-input.small {
  width: 80px;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  padding: 14px 24px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.action-button.primary {
  background: linear-gradient(135deg, #FF9F1C, #FFB84D);
  color: #111;
  box-shadow: 0 4px 16px rgba(255, 159, 28, 0.3);
}

.action-button.primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #FFB84D, #FFD180);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(255, 159, 28, 0.4);
}

.action-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.preview-panel {
  min-height: 300px;
}

@media (min-width: 960px) {
  .preview-panel {
    position: sticky;
    top: 88px;
  }
}
</style>