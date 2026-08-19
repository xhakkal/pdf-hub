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

    <div v-if="selectedFile" class="split-options">
      <label class="radio-option">
        <input type="radio" v-model="splitMode" value="all" name="split-mode" />
        <span class="radio-label">Separar cada página em um arquivo</span>
      </label>

      <label class="radio-option">
        <input type="radio" v-model="splitMode" value="range" name="split-mode" />
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
      v-if="selectedFile"
      @click="handleSplit"
      :disabled="isProcessing"
      class="action-button primary"
    >
      <svg v-if="!isProcessing" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
      </svg>
      <span>{{ isProcessing ? 'Processando...' : 'Dividir PDF' }}</span>
    </button>
  </div>
</template>

<script>
import FileUploader from './FileUploader.vue'

export default {
  name: 'PDFSplit',
  components: { FileUploader },
  data() {
    return {
      selectedFile: null,
      splitMode: 'all',
      pageRanges: '',
      pagesPerFile: 5,
      isProcessing: false
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

.split-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background-color: var(--color-surface);
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 14px;
  color: #a3a3a3;
}

.radio-option input {
  width: 18px;
  height: 18px;
  accent-color: var(--color-primary);
}

.radio-label {
  font-weight: 500;
}

.ranges-input, .n-input {
  margin-left: 28px;
}

.input-hint {
  margin: 0 0 8px;
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
  margin-right: 8px;
}

.n-input {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #a3a3a3;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 14px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.action-button.primary {
  background-color: #f97316;
  color: white;
  box-shadow: 0 4px 16px rgba(249, 115, 22, 0.3);
}

.action-button.primary:hover:not(:disabled) {
  background-color: #fb923c;
}

.action-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-icon {
  width: 20px;
  height: 20px;
}
</style>
