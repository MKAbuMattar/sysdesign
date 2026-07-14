import { defineConfig } from 'astro/config';

// Static landing page for the sysdesign plugin. No integrations — plain HTML/CSS.
// Served at the root of a custom domain, so base stays "/".
export default defineConfig({
  site: 'https://sysdesign.mkabumattar.com',
});
