<template>
  <div class="pdf-watermark">
    <div class="section-header">
      <h3>Marca d'Água</h3>
      <p>Adicione texto de marca d'água ao seu PDF</p>
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
          <label class="control-label">Texto da Marca d'Água</label>
          <input
            v-model="watermarkText"
            type="text"
            placeholder="Ex: CONFIDENCIAL"
            class="text-input"
            maxlength="50"
          />
          <p v-if="watermarkText" class="char-count">{{ watermarkText.length }}/50</p>
        </div>

        <div class="control-group">
          <label class="control-label">Cor</label>
          <div class="color-options">
            <button
              v-for="color in colors"
              :key="color.value"
              @click="selectedColor = color.value"
              :class="['color-btn', { active: selectedColor === color.value }]"
              :style="{ backgroundColor: color.hex }"
              :title="color.label"
            />
          </div>
        </div>

        <div class="control-group">
          <label class="control-label">Opacidade</label>
          <input
            v-model.number="opacity"
            type="range"
            min="0.1"
            max="1"
            step="0.05"
            class="range-input"
          />
          <span class="range-value">{{ Math.round(opacity * 100) }}%</span>
        </div>

        <div class="control-group">
          <label class="control-label">Tamanho da Fonte</label>
          <input
            v-model.number="fontSize"
            type="range"
            min="24"
            max="120"
            step="4"
            class="range-input"
          />
          <span class="range-value">{{ fontSize }}px</span>
        </div>

        <div class="control-group">
          <label class="control-label">Ângulo</label>
          <div class="angle-options">
            <button
              v-for="angleOption in angles"
              :key="angleOption"
              @click="angle = angleOption"
              :class="['angle-btn', { active: angle === angleOption }]"
            >
              {{ angleOption }}°
            </button>
          </div>
        </div>

        <button
          @click="handleWatermark"
          :disabled="isProcessing || !watermarkText"
          class="action-button primary"
        >
          <span class="btn-text">{{ isProcessing ? 'Processando...' : 'Adicionar Marca d\'Água' }}</span>
          <svg v-if="!isProcessing" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
        </button>
      </div>

      <!-- Pré-visualização (Direita) -->
      <div class="preview-panel">
        <PDFPreview
          :file="selectedFile"
          :watermark-text="watermarkText"
          :watermark-opacity="opacity"
          :watermark-angle="angle"
          :watermark-font-size="fontSize"
          :watermark-color="selectedColor"
        />
      </div>
    </div>

    <p v-else-if="selectedFile && !watermarkText" class="hint">
      Digite o texto da marca d'água para habilitar
    </p>
  </div>
</template>

<script>
import FileUploader from './FileUploader.vue'
import PDFPreview from './PDFPreview.vue'

export default {
  name: 'PDFWatermark',
  components: { FileUploader, PDFPreview },
  data() {
    return {
      selectedFile: null,
      watermarkText: '',
      selectedColor: 'gray',
      opacity: 0.3,
      fontSize: 48,
      angle: 45,
      isProcessing: false,
      colors: [
        { value: 'gray', hex: '#6b7280', label: 'Cinza' },
        { value: 'red', hex: '#ef4444', label: 'Vermelho' },
        { value: 'blue', hex: '#3b82f6', label: 'Azul' },
        { value: 'green', hex: '#22c55e', label: 'Verde' },
        { value: 'black', hex: '#1f2937', label: 'Preto' }
      ],
      angles: [0, 45, 90, 135, 180]
    }
  },
  methods: {
    handleFileSelected(file) {
      this.selectedFile = file
    },
    async handleWatermark() {
      if (!this.selectedFile) {
        this.$emit('error', 'Selecione um arquivo PDF')
        return
      }

      if (!this.watermarkText) {
        this.$emit('error', 'Digite o texto da marca d\'água')
        return
      }

      this.isProcessing = true
      try {
        const options = {
          watermark_text: this.watermarkText,
          opacity: this.opacity,
          angle: this.angle,
          font_size: this.fontSize,
          color: this.selectedColor
        }
        await this.$emit('watermark', this.selectedFile, options)
      } finally {
        this.isProcessing = false
      }
    }
  }
}
</script>

<style scoped>
.pdf-watermark {
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

.char-count {
  margin: 0;
  font-size: 11px;
  color: #666;
  text-align: right;
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

.color-options {
  display: flex;
  gap: 10px;
}

.color-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 3px solid var(--color-border);
  cursor: pointer;
  transition: all 0.2s ease;
}

.color-btn:hover {
  transform: scale(1.1);
}

.color-btn.active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(255, 159, 28, 0.2);
}

.range-input {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  background: var(--color-border);
  border-radius: 4px;
  outline: none;
}

.range-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: var(--color-primary);
  border-radius: 50%;
  cursor: pointer;
}

.range-value {
  font-size: 13px;
  color: #737373;
  text-align: right;
}

.angle-options {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.angle-btn {
  padding: 10px 18px;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-bg-elevated);
  font-size: 13px;
  font-weight: 600;
  color: #a3a3a3;
  cursor: pointer;
  transition: all 0.2s ease;
}

.angle-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.angle-btn.active {
  border-color: var(--color-primary);
  background-color: var(--color-primary);
  color: #111;
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
  opacity: 0.5;
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

.hint {
  margin: 0;
  padding: 20px;
  color: #f59e0b;
  font-size: 13px;
  text-align: center;
  background: rgba(245, 158, 11, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(245, 158, 11, 0.2);
}
</style>