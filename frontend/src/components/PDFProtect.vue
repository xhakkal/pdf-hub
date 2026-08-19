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

    <div v-if="selectedFile" class="protect-options">
      <div class="field">
        <label class="field-label">Senha para abrir *</label>
        <input
          v-model="userPassword"
          type="password"
          placeholder="Digite a senha"
          class="text-input"
        />
      </div>

      <div class="field">
        <label class="field-label">Senha do proprietário (opcional)</label>
        <input
          v-model="ownerPassword"
          type="password"
          placeholder="Senha administrativa"
          class="text-input"
        />
        <p class="input-hint">Controla quem pode alterar as permissões</p>
      </div>

      <div class="field">
        <label class="field-label">Permissões</label>
        <div class="permissions-grid">
          <label class="permission-item">
            <input type="checkbox" v-model="permissions.print" />
            <span>Imprimir</span>
          </label>
          <label class="permission-item">
            <input type="checkbox" v-model="permissions.copy" />
            <span>Copiar texto</span>
          </label>
          <label class="permission-item">
            <input type="checkbox" v-model="permissions.modify" />
            <span>Modificar</span>
          </label>
          <label class="permission-item">
            <input type="checkbox" v-model="permissions.annotate" />
            <span>Anotar</span>
          </label>
        </div>
      </div>
    </div>

    <button
      v-if="selectedFile && userPassword"
      @click="handleProtect"
      :disabled="isProcessing"
      class="action-button primary"
    >
      <svg v-if="!isProcessing" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
      <span>{{ isProcessing ? 'Processando...' : 'Proteger PDF' }}</span>
    </button>

    <p v-if="selectedFile && !userPassword" class="hint">
      Digite uma senha para proteger o arquivo
    </p>
  </div>
</template>

<script>
import FileUploader from './FileUploader.vue'

export default {
  name: 'PDFProtect',
  components: { FileUploader },
  data() {
    return {
      selectedFile: null,
      userPassword: '',
      ownerPassword: '',
      permissions: {
        print: true,
        copy: true,
        modify: true,
        annotate: true
      },
      isProcessing: false
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

.protect-options {
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

.input-hint {
  margin: 0;
  font-size: 12px;
  color: #737373;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.permission-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #a3a3a3;
  cursor: pointer;
}

.permission-item input {
  width: 16px;
  height: 16px;
  accent-color: var(--color-primary);
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
