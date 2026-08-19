<template>
  <div class="pdf-tool">
    <div class="section-header">
      <h3>Unir PDFs</h3>
      <p>Selecione 2 ou mais PDFs para unir em um único arquivo</p>
    </div>

    <FileUploader
      multiple
      accept=".pdf"
      :max-files="20"
      @files-selected="handleFilesSelected"
      @error="$emit('error', $event)"
    />

    <button
      v-if="selectedFiles.length >= 2"
      @click="handleMerge"
      :disabled="isProcessing"
      class="action-button primary"
    >
      <svg v-if="!isProcessing" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
      <span>{{ isProcessing ? 'Processando...' : `Unir ${selectedFiles.length} PDFs` }}</span>
    </button>

    <p v-if="selectedFiles.length > 0 && selectedFiles.length < 2" class="hint">
      Selecione pelo menos 2 arquivos PDF
    </p>
  </div>
</template>

<script>
import FileUploader from './FileUploader.vue'

export default {
  name: 'PDFMerge',
  components: { FileUploader },
  data() {
    return {
      selectedFiles: [],
      isProcessing: false
    }
  },
  methods: {
    handleFilesSelected(files) {
      this.selectedFiles = files
    },
    async handleMerge() {
      if (this.selectedFiles.length < 2) {
        this.$emit('error', 'Selecione pelo menos 2 arquivos PDF')
        return
      }

      this.isProcessing = true
      try {
        await this.$emit('merge', this.selectedFiles)
      } finally {
        this.isProcessing = false
      }
    }
  }
}
</script>

<style scoped>
.pdf-tool {
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

.hint {
  margin: 0;
  color: #f59e0b;
  font-size: 13px;
  text-align: center;
}
</style>
