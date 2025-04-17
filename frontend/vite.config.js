import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  build: {
    rollupOptions: {
      input: '/src/main.js', // 确保路径正确
    },
  },
  optimizeDeps: {
    include: ['lodash', 'axios'],
  },
});