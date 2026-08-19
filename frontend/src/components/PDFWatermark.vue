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

    <div v-if="selectedFile" class="watermark-options">
      <div class="field">
        <label class="field-label">Texto da marca d'água *</label>
        <input
          v-model="watermarkText"
          type="text"
          placeholder="Ex: CONFIDENCIAL"
          class="text-input"
          maxlength="50"
        />
      </div>

      <div class="field">
        <label class="field-label">Cor</label>
        <div class="color-options">
          <button
            v-for="color in colors"
            :key="color.value"
            @click="color = color.value"
            :class="['color-btn', { active: color === color.value }]"
            :style="{ backgroundColor: color.hex }"
            :title="color.label"
          />
        </div>
      </div>

      <div class="field">
        <label class="field-label">Tamanho da fonte</label>
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

      <div class="field">
        <label class="field-label">Ângulo</label>
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
    </div>

    <button
      v-if="selectedFile && watermarkText"
      @click="handleWatermark"
      :disabled="isProcessing"
      class="action-button primary"
    >
      <svg v-if="!isProcessing" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
      </svg>
      <span>{{ isProcessing ? 'Processando...' : 'Adicionar Marca d\'Água' }}</span>
    </button>

    <p v-if="selectedFile && !watermarkText" class="hint">
      Digite o texto da marca d'água
    </p>
  </div>
</template>

<script>
import FileUploader from './FileUploader.vue'

export default {
  name: 'PDFWatermark',
  components: { FileUploader },
  data() {
    return {
      selectedFile: null,
      watermarkText: '',
      color: 'gray',
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
          opacity: 0.3,
          angle: this.angle,
          font_size: this.fontSize,
          color: this.color
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

.watermark-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px;
  background-color: var(--color-surface);
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label {
  font-size: 14px;
  font-weight: 500;
  color: #a3a3a3;
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
  gap: 8px;
}

.color-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 3px solid var(--color-border);
  cursor: pointer;
  transition: all 0.2s ease;
}

.color-btn:hover {
  transform: scale(1.1);
}

.color-btn.active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px var(--color-primary);
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
  font-size: 14px;
  color: #737373;
  text-align: right;
}

.angle-options {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.angle-btn {
  padding: 8px 16px;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-bg-elevated);
  font-size: 14px;
  font-weight: 500;
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
  color: white;
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
