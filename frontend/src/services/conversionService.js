import axios from 'axios'

// Em desenvolvimento usa localhost; em produção usa a variável de ambiente
const API_URL = import.meta.env.VITE_API_URL || 'https://pdf-house.onrender.com/api'

export default {
  async convertFile(file, formats) {
    const formData = new FormData()
    formData.append('file', file)

    formats.forEach(format => {
      formData.append('formats', format)
    })

    try {
      const response = await axios.post(`${API_URL}/convert`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob'
      })
      return { success: true, data: response.data }
    } catch (error) {
      let errorMsg = error.message || 'Erro desconhecido'
      if (error.response?.data instanceof Blob) {
        try {
          const text = await error.response.data.text()
          const json = JSON.parse(text)
          errorMsg = json.error || errorMsg
        } catch {
          errorMsg = `Erro ${error.response.status}`
        }
      } else if (error.response?.data?.error) {
        errorMsg = error.response.data.error
      }
      return { success: false, error: errorMsg }
    }
  },

  // Mantido para retrocompatibilidade
  async convertPDF(file, formats) {
    return this.convertFile(file, formats)
  },

  async healthCheck() {
    try {
      const response = await axios.get(`${API_URL}/health`)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.message }
    }
  },

  // ───────────────── OPERAÇÕES DE PDF ─────────────────

  async mergePdfs(files) {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    try {
      const response = await axios.post(`${API_URL}/merge`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob'
      })
      return { success: true, data: response.data }
    } catch (error) {
      return this._handleError(error)
    }
  },

  async splitPdf(file, options) {
    const formData = new FormData()
    formData.append('file', file)
    if (options.splitMode) formData.append('split_mode', options.splitMode)
    if (options.pageRanges) formData.append('page_ranges', options.pageRanges)

    try {
      const response = await axios.post(`${API_URL}/split`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob'
      })
      return { success: true, data: response.data }
    } catch (error) {
      return this._handleError(error)
    }
  },

  async rotatePdf(file, options) {
    const formData = new FormData()
    formData.append('file', file)
    if (options.rotation) formData.append('rotation', options.rotation.toString())
    if (options.pageNumbers) formData.append('page_numbers', options.pageNumbers)

    try {
      const response = await axios.post(`${API_URL}/rotate`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob'
      })
      return { success: true, data: response.data }
    } catch (error) {
      return this._handleError(error)
    }
  },

  async watermarkPdf(file, options) {
    const formData = new FormData()
    formData.append('file', file)
    Object.entries(options).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        formData.append(key, value.toString())
      }
    })

    try {
      const response = await axios.post(`${API_URL}/watermark`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob'
      })
      return { success: true, data: response.data }
    } catch (error) {
      return this._handleError(error)
    }
  },

  async protectPdf(file, options) {
    const formData = new FormData()
    formData.append('file', file)
    Object.entries(options).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        formData.append(key, typeof value === 'object' ? JSON.stringify(value) : value.toString())
      }
    })

    try {
      const response = await axios.post(`${API_URL}/protect`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob'
      })
      return { success: true, data: response.data }
    } catch (error) {
      return this._handleError(error)
    }
  },

  // Helper para tratamento de erros
  async _handleError(error) {
    let errorMsg = error.message || 'Erro desconhecido'
    if (error.response?.data instanceof Blob) {
      try {
        const text = await error.response.data.text()
        const json = JSON.parse(text)
        errorMsg = json.error || errorMsg
      } catch {
        errorMsg = `Erro ${error.response.status}`
      }
    } else if (error.response?.data?.error) {
      errorMsg = error.response.data.error
    }
    return { success: false, error: errorMsg }
  }
}
