import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith('el-')
        }
      },
      ssr: {
        noExternal: ['element-plus']  // 如果使用了element-plus
      }
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // 配置 @ 指向 src 目录
    },
  },
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/chat': {
        target: 'https://cloud.fastgpt.cn',
        changeOrigin: true
      }
    },
    static: {
      directory: path.resolve(__dirname, './stock_daily_two_years'),
      publicPath: '/stock_daily_two_years/'
    }
  },
  ssr: {
    format: 'cjs'
  },
  build: {
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return 'vendor';
          }
        }
      }
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: ``
      }
    }
  },
  assetsInclude: ['**/*.csv'],  // 添加这一行
})
