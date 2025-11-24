import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    cors: true,
    proxy: {
      '/cooking/ver3': {
        // target: 'http://localhost:8000',
        // 力合网
        // target: 'http://192.168.1.7:8000',
        target: 'http://192.168.0.100:8000',
        changeOrigin: true,
      }
    }
  }
})