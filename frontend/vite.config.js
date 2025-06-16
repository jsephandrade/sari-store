import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // whenever you request /api/*, Vite will forward to your Django backend
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // no need to rewrite in this simple case
      },
    },
  },
})
