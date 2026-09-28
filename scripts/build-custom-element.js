// Regenerates src/public/custom-elements/unisas-app.js from wix-embed.html.
// Run after editing wix-embed.html, before `wix dev` / `wix preview` / `wix publish`.
const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');
const srcHtmlPath = path.join(repoRoot, 'wix-embed.html');
const outPath = path.join(repoRoot, 'src', 'public', 'custom-elements', 'unisas-app.js');

const html = fs.readFileSync(srcHtmlPath, 'utf8');

const out = `// Auto-generated from wix-embed.html by scripts/build-custom-element.js — do not hand-edit.
const APP_HTML = ${JSON.stringify(html)};

class UnisasApp extends HTMLElement {
  connectedCallback() {
    this.style.cssText = 'display:block;width:100%;height:100%;';

    const iframe = document.createElement('iframe');
    iframe.style.cssText = 'width:100%;height:100%;border:0;';
    iframe.setAttribute('title', 'Unisas OS');
    iframe.srcdoc = APP_HTML;

    this.attachShadow({ mode: 'open' }).appendChild(iframe);
  }
}

customElements.define('unisas-app', UnisasApp);
`;

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, out, 'utf8');
console.log('Wrote', outPath, `(${out.length} bytes)`);
