// Configure Vite to run the Svelte frontend locally. /////////////
import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()], ////////// Enable Svelte support in Vite.
  server: { port: 5173 }, //////////// Local development server port.
  test: {
    environment: 'jsdom', ///////// Browser-like environment for frontend tests.
    include: ['src/**/*.test.js'], /////// Find test files in src.
  },
  // Use browser conditions when running Vitest.////////////
  resolve: process.env.VITEST ? { conditions: ['browser'] } : undefined,
});