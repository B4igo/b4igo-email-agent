import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { crx } from '@crxjs/vite-plugin'
import manifest from './public/manifest.json'

// https://vite.dev/config/
//
// The app talks to the backend through an absolute URL configured by the
// VITE_BACKEND_URL build-time variable (see src/API/Auth.ts), not through a
// dev-server proxy, so no `server.proxy` block is needed here. Set
// VITE_BACKEND_URL to the backend's /api base (default http://localhost:5000/api).
export default defineConfig({
  plugins: [react(), crx({ manifest })],
})
