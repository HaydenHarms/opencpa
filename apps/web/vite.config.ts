import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // In dev, /api/* goes to the local Worker (wrangler dev on :8787).
    proxy: { '/api': { target: 'http://localhost:8787', rewrite: (p) => p.replace(/^\/api/, '') } },
  },
});
