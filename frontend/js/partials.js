/* Shared UI fragments (navbar, footer, icons) and mock API */

const SVG = {
  logo: `<svg viewBox="0 0 64 64" width="44" height="44" fill="none" stroke="#0b3b24" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="26" cy="26" r="17" fill="#ffffff"/>
    <line x1="38" y1="38" x2="54" y2="54"/>
    <g fill="#4cbb17" stroke="none">
      <circle cx="20" cy="20" r="2.3"/><circle cx="26" cy="17" r="2.3"/>
      <circle cx="32" cy="20" r="2.3"/><circle cx="17" cy="27" r="2.3"/>
      <ellipse cx="26" cy="31" rx="6.5" ry="5"/>
    </g>
  </svg>`,
  camera: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>`,
  image: `<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-5-5L5 21"/><path d="M19 3v4M17 5h4"/></svg>`,
  back: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>`,
  paw: `<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><circle cx="6" cy="9" r="1.8"/><circle cx="10" cy="6" r="1.8"/><circle cx="14" cy="6" r="1.8"/><circle cx="18" cy="9" r="1.8"/><path d="M12 11c-3 0-5 2.4-5 4.6 0 1.7 1.5 2.4 5 2.4s5-.7 5-2.4c0-2.2-2-4.6-5-4.6z"/></svg>`,
  search: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>`,
  fb: `<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H8v-3h2.4V9.5c0-2.4 1.4-3.7 3.6-3.7 1 0 2.1.2 2.1.2v2.3h-1.2c-1.2 0-1.5.7-1.5 1.5V12h2.6l-.4 3h-2.2v7A10 10 0 0 0 22 12z"/></svg>`,
  ig: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>`,
};

function renderNavbar(active = "home") {
  const links = [
    { id: "home", label: "Início", href: "home.html" },
    { id: "about", label: "Sobre", href: "#" },
    { id: "stories", label: "Histórias de Sucesso", href: "#" },
  ];
  return `
    <nav class="navbar">
      <a class="brand" href="home.html">
        <span class="brand-logo">${SVG.logo}</span>
        <span class="brand-text">Achou meu pet AI?</span>
      </a>
      <ul class="nav-links" id="navLinks">
        ${links.map(l => `<li><a href="${l.href}" ${l.id === active ? 'style="color:var(--color-primary-2)"' : ''}>${l.label}</a></li>`).join("")}
      </ul>
      <div class="nav-cta">
        <button class="btn btn-primary" onclick="alert('Login será conectado ao backend.')">Login</button>
        <button class="hamburger" id="hamburger" aria-label="Menu"><span></span></button>
      </div>
    </nav>
  `;
}

function renderFooter() {
  return "";
}

function mountChrome(active) {
  const navMount = document.getElementById("nav-mount");
  const footMount = document.getElementById("foot-mount");
  if (navMount) navMount.innerHTML = renderNavbar(active);
  if (footMount) footMount.innerHTML = renderFooter();
  const h = document.getElementById("hamburger");
  if (h) h.addEventListener("click", () => document.getElementById("navLinks").classList.toggle("open"));
}

/* ===========================================================
   MOCK API — substitua estas funções por chamadas fetch reais
   =========================================================== */
const API = {
  uploadImage(file) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          raca: "Golden Retriever",
          porte: "Médio",
          cor: "Dourado",
          cidade: "Recife - PE",
          data: new Date().toISOString().slice(0, 10),
        });
      }, 1200);
    });
  },
  submitPet(payload) {
    return new Promise((resolve) => setTimeout(() => resolve({ ok: true, id: "pet_" + Date.now() }), 1500));
  },
  listPets() {
    return new Promise((resolve) => setTimeout(() => resolve([
      { id: "1", match: 92, city: "Recife - PE", time: "5m atrás", photo: "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=600&q=80" },
      { id: "2", match: 90, city: "Recife - PE", time: "2d atrás", photo: "https://images.unsplash.com/photo-1552053831-71594a27632d?w=600&q=80" },
      { id: "3", match: 87, city: "Recife - PE", time: "5d atrás", photo: "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600&q=80" },
      { id: "4", match: 81, city: "Olinda - PE", time: "1sem atrás", photo: "https://images.unsplash.com/photo-1561037404-61cd46aa615b?w=600&q=80" },
      { id: "5", match: 74, city: "Jaboatão - PE", time: "2sem atrás", photo: "https://images.unsplash.com/photo-1568572933382-74d440642117?w=600&q=80" },
      { id: "6", match: 70, city: "Recife - PE", time: "3sem atrás", photo: "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=600&q=80" },
    ]), 600));
  },
  getPet(id) {
    return new Promise((resolve) => setTimeout(() => resolve({
      id, user: "@Camila_Mendes",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&q=80",
      data: "24/03/26 (hoje)",
      local: "Parque da Jaqueira, Recife PE (em frente a igreja branca)",
      horario: "16:12",
      descricao: 'Golden encontrado no Parque da Jaqueira. Muito dócil e bem treinado, responde a comandos como: "Senta", "Me dá a patinha".',
      fotos: [
        "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=800&q=80",
        "https://images.unsplash.com/photo-1552053831-71594a27632d?w=800&q=80",
      ],
    }), 400));
  },
};

window.SVG = SVG;
window.API = API;
window.mountChrome = mountChrome;
