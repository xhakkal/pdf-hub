<template>
  <div class="uploader" @drop="handleDrop" @dragover.prevent @dragenter.prevent>
    <div class="upload-area" :class="{ 'drag-over': isDragging }">
      <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
      <h3>{{ multiple ? 'Arraste seus PDFs aqui' : 'Arraste seu PDF aqui' }}</h3>
      <p>ou</p>
      <label class="file-input-label">
        <input
          ref="fileInput"
          type="file"
          :accept="accept"
          :multiple="multiple"
          @change="handleFileSelect"
          class="file-input"
        />
        <span class="browse-button">{{ multiple ? 'Escolher arquivos' : 'Escolher arquivo' }}</span>
      </label>

      <!-- Lista de arquivos selecionados -->
      <div v-if="selectedFiles.length > 0" class="files-list">
        <div class="file-item" v-for="(file, index) in selectedFiles" :key="index">
          <svg class="file-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zm0 16H6V4h7v7h7v7z"/>
          </svg>
          <span class="file-name">{{ file.name }}</span>
          <span class="file-size">{{ formatFileSize(file.size) }}</span>
          <button type="button" class="remove-file" @click.stop="removeFile(index)" title="Remover">×</button>
        </div>
      </div>

      <p class="file-count" v-if="selectedFiles.length > 0">
        {{ selectedFiles.length }} arquivo{{ selectedFiles.length > 1 ? 's' : '' }} selecionado{{ selectedFiles.length > 1 ? 's' : '' }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileUploader',
  props: {
    multiple: {
      type: Boolean,
      default: false
    },
    accept: {
      type: String,
      default: '.pdf'
    },
    maxFiles: {
      type: Number,
      default: 10
    }
  },
  data() {
    return {
      isDragging: false,
      selectedFiles: []
    }
  },
  methods: {
    handleDrop(e) {
      e.preventDefault()
      e.stopPropagation()
      this.isDragging = false

      const files = Array.from(e.dataTransfer.files)
      this.processFiles(files)
    },
    handleFileSelect() {
      const files = Array.from(this.$refs.fileInput.files)
      this.processFiles(files)
      // Limpar input para permitir selecionar o mesmo arquivo novamente
      this.$refs.fileInput.value = ''
    },
    processFiles(files) {
      const validFiles = files.filter(file => {
        const isValid = this.validateFile(file)
        if (!isValid) {
          this.$emit('error', `Arquivo inválido: ${file.name}`)
        }
        return isValid
      })

      if (this.multiple) {
        // Adicionar arquivos válidos à lista
        for (const file of validFiles) {
          if (this.selectedFiles.length < this.maxFiles) {
            // Verificar duplicatas
            if (!this.selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
              this.selectedFiles.push(file)
            }
          }
        }
        this.$emit('files-selected', this.selectedFiles)
      } else {
        // Modo single - substituir
        if (validFiles.length > 0) {
          this.selectedFiles = [validFiles[0]]
          this.$emit('file-selected', validFiles[0])
        }
      }
    },
    validateFile(file) {
      // Verificar tipo MIME ou extensão
      const allowedTypes = this.accept.split(',').map(t => t.trim())
      const fileExt = '.' + file.name.split('.').pop().toLowerCase()

      // Verificar extensão primeiro (mais confiável)
      const extMatch = allowedTypes.some(t => t.startsWith('.') && t === fileExt)
      if (extMatch) return true

      // Verificar MIME type
      const mimeMatch = allowedTypes.some(t => {
        if (t.startsWith('.')) return false
        // Para wildcards como "image/*"
        if (t.endsWith('/*')) {
          return file.type.startsWith(t.slice(0, -1))
        }
        return file.type === t
      })

      return mimeMatch
    },
    removeFile(index) {
      this.selectedFiles.splice(index, 1)
      if (this.multiple) {
        this.$emit('files-selected', this.selectedFiles)
      } else if (this.selectedFiles.length > 0) {
        this.$emit('file-selected', this.selectedFiles[0])
      } else {
        this.$emit('file-selected', null)
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
    }
  }
}
</script>

<style scoped>
.uploader {
  width: 100%;
}

.upload-area {
  border: 2px dashed var(--color-border);
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: var(--color-surface);
}

.upload-area:hover {
  border-color: var(--color-primary);
  background-color: var(--color-surface-hover);
}

.upload-area.drag-over {
  border-color: var(--color-primary);
  background-color: rgba(249, 115, 22, 0.1);
  transform: scale(1.02);
}

.upload-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  color: var(--color-primary);
}

.upload-area h3 {
  margin: 0 0 8px;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.upload-area p {
  margin: 8px 0;
  color: #a3a3a3;
  font-size: 14px;
}

.file-input {
  display: none;
}

.file-input-label {
  display: inline-block;
}

.browse-button {
  display: inline-block;
  padding: 10px 24px;
  margin-top: 8px;
  background-color: var(--color-primary);
  color: white;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.browse-button:hover {
  background-color: var(--color-primary-hover);
}

.files-list {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: left;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background-color: var(--color-bg-elevated);
  border: 1px solid var(--color-primary);
  border-radius: 8px;
  font-size: 14px;
}

.file-icon {
  width: 24px;
  height: 24px;
  color: var(--color-primary);
  flex-shrink: 0;
}

.file-name {
  flex: 1;
  color: white;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  color: #737373;
  font-size: 12px;
  flex-shrink: 0;
}

.remove-file {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: none;
  background-color: var(--color-error);
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background-color 0.2s ease;
  line-height: 1;
}

.remove-file:hover {
  background-color: #dc2626;
}

.file-count {
  margin-top: 12px;
  margin-bottom: 0;
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 500;
}
</style>
