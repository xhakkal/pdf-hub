<template>
  <div class="pdf-protect">
    <div class="section-header">
      <h3>Proteger com Senha</h3>
      <p>Adicione proteção por senha ao seu PDF</p>
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
          <label class="control-label">Senha para Abrir *</label>
          <div class="password-wrapper">
            <input
              v-model="userPassword"
              :type="showUserPassword ? 'text' : 'password'"
              placeholder="Digite a senha (mín. 4 caracteres)"
              class="text-input"
            />
            <button
              type="button"
              @click="showUserPassword = !showUserPassword"
              class="password-toggle"
              :aria-label="showUserPassword ? 'Ocultar senha' : 'Mostrar senha'"
            >
              <svg v-if="showUserPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
          <p v-if="userPassword" class="password-strength" :class="passwordStrengthClass">
            {{ passwordStrengthText }}
          </p>
        </div>

        <div class="control-group">
          <label class="control-label">Senha do Proprietário (opcional)</label>
          <div class="password-wrapper">
            <input
              v-model="ownerPassword"
              :type="showOwnerPassword ? 'text' : 'password'"
              placeholder="Senha administrativa (padrão: igual à senha de abertura)"
              class="text-input"
            />
            <button
              type="button"
              @click="showOwnerPassword = !showOwnerPassword"
              class="password-toggle"
              :aria-label="showOwnerPassword ? 'Ocultar senha' : 'Mostrar senha'"
            >
              <svg v-if="showOwnerPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
        </div>

        <div class="control-group">
          <label class="control-label">Permissões</label>
          <p class="control-hint">O que usuários sem a senha de proprietário podem fazer</p>
          <div class="permissions-grid">
            <label class="permission-item">
              <input type="checkbox" v-model="permissions.print" />
              <span class="permission-custom"></span>
              <span>Imprimir</span>
            </label>
            <label class="permission-item">
              <input type="checkbox" v-model="permissions.copy" />
              <span class="permission-custom"></span>
              <span>Copiar texto</span>
            </label>
            <label class="permission-item">
              <input type="checkbox" v-model="permissions.modify" />
              <span class="permission-custom"></span>
              <span>Modificar</span>
            </label>
            <label class="permission-item">
              <input type="checkbox" v-model="permissions.annotate" />
              <span class="permission-custom"></span>
              <span>Anotar</span>
            </label>
          </div>
        </div>

        <button
          @click="handleProtect"
          :disabled="isProcessing || !userPassword || userPassword.length < 4"
          class="action-button primary"
        >
          <span class="btn-text">{{ isProcessing ? 'Processando...' : 'Proteger PDF' }}</span>
          <svg v-if="!isProcessing" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </button>
      </div>

      <!-- Pré-visualização (Direita) -->
      <div class="preview-panel">
        <PDFPreview
          :file="selectedFile"
        />
      </div>
    </div>

    <p v-else-if="selectedFile && !userPassword" class="hint">
      Digite uma senha para proteger o arquivo
    </p>
  </div>
</template>

<script>
import FileUploader from './FileUploader.vue'
import PDFPreview from './PDFPreview.vue'

export default {
  name: 'PDFProtect',
  components: { FileUploader, PDFPreview },
  data() {
    return {
      selectedFile: null,
      userPassword: '',
      ownerPassword: '',
      showUserPassword: false,
      showOwnerPassword: false,
      permissions: {
        print: true,
        copy: true,
        modify: true,
        annotate: true
      },
      isProcessing: false
    }
  },
  computed: {
    passwordStrength() {
      const pwd = this.userPassword
      if (!pwd) return 0
      let score = 0
      if (pwd.length >= 8) score++
      if (/[A-Z]/.test(pwd)) score++
      if (/[a-z]/.test(pwd)) score++
      if (/[0-9]/.test(pwd)) score++
      if (/[^A-Za-z0-9]/.test(pwd)) score++
      return Math.min(score, 4)
    },
    passwordStrengthClass() {
      const levels = ['strength-weak', 'strength-weak', 'strength-fair', 'strength-good', 'strength-strong']
      return levels[this.passwordStrength]
    },
    passwordStrengthText() {
      const texts = ['', 'Muito fraca', 'Fraca', 'Boa', 'Forte', 'Muito forte']
      return texts[this.passwordStrength]
    }
  },
  methods: {
    handleFileSelected(file) {
      this.selectedFile = file
    },
    async handleProtect() {
      if (!this.selectedFile) {
        this.$emit('error', 'Selecione um arquivo PDF')
        return
      }

      if (!this.userPassword) {
        this.$emit('error', 'Digite uma senha')
        return
      }

      if (this.userPassword.length < 4) {
        this.$emit('error', 'A senha deve ter pelo menos 4 caracteres')
        return
      }

      this.isProcessing = true
      try {
        const options = {
          user_password: this.userPassword,
          owner_password: this.ownerPassword || undefined,
          permissions: this.permissions
        }
        await this.$emit('protect', this.selectedFile, options)
      } finally {
        this.isProcessing = false
      }
    }
  }
}
</script>

<style scoped>
.pdf-protect {
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

.control-hint {
  margin: 0;
  font-size: 12px;
  color: #737373;
}

.password-wrapper {
  position: relative;
}

.password-wrapper .text-input {
  padding-right: 48px;
}

.password-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #737373;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
}

.password-toggle:hover {
  color: #fff;
  background: rgba(255, 159, 28, 0.1);
}

.password-toggle svg {
  width: 20px;
  height: 20px;
}

.password-strength {
  margin: 0;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.password-strength.strength-weak { color: #EF4444; }
.password-strength.strength-fair { color: #F59E0B; }
.password-strength.strength-good { color: #3B82F6; }
.password-strength.strength-strong { color: #22C55E; }

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

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.permission-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #a3a3a3;
  cursor: pointer;
  padding: 8px 10px;
  border-radius: 8px;
  transition: all 0.2s;
}

.permission-item:hover {
  background: rgba(255, 159, 28, 0.05);
  color: #fff;
}

.permission-custom {
  width: 18px;
  height: 18px;
  border: 2px solid var(--color-border);
  border-radius: 4px;
  position: relative;
  transition: all 0.2s;
  flex-shrink: 0;
}

.permission-item input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.permission-item input:checked + .permission-custom {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.permission-item input:checked + .permission-custom::after {
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