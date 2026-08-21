import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    chunkSizeWarningLimit: 1000, // Increase limit since pdf-tools loads lazily
    rollupOptions: {
      output: {
        manualChunks: {
          'pdf-tools': [
            './src/components/PDFMerge.vue',
            './src/components/PDFSplit.vue',
            './src/components/PDFRotate.vue',
            './src/components/PDFWatermark.vue',
            './src/components/PDFProtect.vue',
            './src/components/PDFPreview.vue'
          ],
          'pdfjs': ['pdfjs-dist'],
          'vendor': ['axios', 'vue']
        }
      }
    }
  }
})