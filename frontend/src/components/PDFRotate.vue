<template>
  <div class="pdf-rotate">
    <div class="section-header">
      <h3>Rotacionar PDF</h3>
      <p>Gire as páginas do seu PDF</p>
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
          <label class="control-label">Ângulo de Rotação</label>
          <div class="rotation-buttons">
            <button
              v-for="angle in [90, 180, 270]"
              :key="angle"
              @click="rotation = angle"
              :class="['rotation-btn', { active: rotation === angle }]"
            >
              <svg class="rotate-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" :d="getRotateIconPath(angle)" />
              </svg>
              {{ angle }}°
            </button>
          </div>
        </div>

        <div class="control-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="specificPages" />
            <span class="checkbox-custom"></span>
            <span>Rotacionar apenas páginas específicas</span>
          </label>
          <div v-if="specificPages" class="pages-field">
            <input
              v-model="pageNumbers"
              type="text"
              placeholder="Ex: 1, 3, 5-7 (deixe vazio para todas)"
              class="text-input"
            />
            <p class="input-hint">Use números separados por vírgula ou intervalos: 1, 3, 5-7</p>
          </div>
        </div>

        <button
          @click="handleRotate"
          :disabled="isProcessing"
          class="action-button primary"
        >
          <span class="btn-text">{{ isProcessing ? 'Processando...' : `Rotacionar ${rotation}°` }}</span>
          <svg v-if="!isProcessing" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>

      <!-- Pré-visualização (Direita) -->
      <div class="preview-panel">
        <PDFPreview
          :file="selectedFile"
          :rotation="previewRotation"
          :selected-pages="parsedPageNumbers"
        />
      </div>
    </div>
  </div>
</template>

<script>
import FileUploader from './FileUploader.vue'
import PDFPreview from './PDFPreview.vue'

export default {
  name: 'PDFRotate',
  components: { FileUploader, PDFPreview },
  data() {
    return {
      selectedFile: null,
      rotation: 90,
      specificPages: false,
      pageNumbers: '',
      isProcessing: false
    }
  },
  computed: {
    previewRotation() {
      return this.rotation
    },
    parsedPageNumbers() {
      if (!this.specificPages || !this.pageNumbers.trim()) return []
      return this.pageNumbers.split(',').map(s => s.trim()).filter(Boolean)
    }
  },
  methods: {
    getRotateIconPath(angle) {
      const paths = {
        90: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
        180: 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4',
        270: 'M20 12V7.582A8.001 8.001 0 0119.418 15M20 12h-5m0 0l4 4m-4-4l-4 4M12 5v14'
      }
      return paths[angle] || paths[90]
    },
    handleFileSelected(file) {
      this.selectedFile = file
    },
    async handleRotate() {
      if (!this.selectedFile) {
        this.$emit('error', 'Selecione um arquivo PDF')
        return
      }

      this.isProcessing = true
      try {
        const options = {
          rotation: this.rotation,
          pageNumbers: this.specificPages ? this.pageNumbers : null
        }
        await this.$emit('rotate', this.selectedFile, options)
      } finally {
        this.isProcessing = false
      }
    }
  }
}
</script>

<style scoped>
.pdf-rotate {
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
  gap: 10px;
}

.control-label {
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.rotation-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.rotation-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 14px 10px;
  border: 2px solid var(--color-border);
  border-radius: 10px;
  background-color: var(--color-bg-elevated);
  font-size: 13px;
  font-weight: 600;
  color: #a3a3a3;
  cursor: pointer;
  transition: all 0.2s ease;
}

.rotation-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: rgba(255, 159, 28, 0.1);
}

.rotation-btn.active {
  border-color: var(--color-primary);
  background-color: var(--color-primary);
  color: #111;
}

.rotate-icon {
  width: 22px;
  height: 22px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #a3a3a3;
  cursor: pointer;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border: 2px solid var(--color-border);
  border-radius: 4px;
  background: var(--color-bg);
  position: relative;
  transition: all 0.2s;
  flex-shrink: 0;
}

.checkbox-label input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.checkbox-label input:checked + .checkbox-custom {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.checkbox-label input:checked + .checkbox-custom::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid #111;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.pages-field {
  margin-left: 28px;
  display: flex;
  flex-direction: column;
  gap: 6px;
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

.input-hint {
  margin: 0;
  font-size: 12px;
  color: #737373;
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