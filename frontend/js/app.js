const API = 'http://localhost:5000/api';

/* ══════════════════════════════════════════
   NAVEGAÇÃO
══════════════════════════════════════════ */
function goTo(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const target = document.getElementById('page-' + pageId);
  if (target) target.classList.add('active');
}

/* ══════════════════════════════════════════
   TOAST
══════════════════════════════════════════ */
function showToast(msg, type = 'ok') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = type === 'ok' ? 'show-ok' : 'show-err';
  setTimeout(() => t.className = '', 3000);
}

/* ══════════════════════════════════════════
   UTILITÁRIOS
══════════════════════════════════════════ */
function setLoading(btnId, loading, originalHTML) {
  const btn = document.getElementById(btnId);
  if (!btn) return;
  btn.disabled = loading;
  btn.innerHTML = loading ? '<span class="spinner"></span>' : originalHTML;
}

function setStatus(elId, msg, type = '') {
  const el = document.getElementById(elId);
  if (!el) return;
  el.textContent = msg;
  el.className = 'status-msg ' + type;
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result.split(',')[1]);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function addPreview(containerId, file, fileList) {
  const container = document.getElementById(containerId);
  const wrap = document.createElement('div');
  wrap.className = 'preview-thumb';
  const img = document.createElement('img');
  img.src = URL.createObjectURL(file);
  const btn = document.createElement('button');
  btn.textContent = '✕';
  btn.onclick = () => {
    fileList.splice(fileList.indexOf(file), 1);
    wrap.remove();
  };
  wrap.appendChild(img);
  wrap.appendChild(btn);
  container.appendChild(wrap);
}

/* ══════════════════════════════════════════
   BUSCA — Frame 2 → Frame 4
══════════════════════════════════════════ */
const searchFiles = [];

document.getElementById('search-file').addEventListener('change', function () {
  Array.from(this.files).forEach(f => {
    searchFiles.push(f);
    addPreview('search-previews', f, searchFiles);
  });
  this.value = '';
});

async function handleSearch() {
  const description = document.getElementById('search-desc').value.trim();

  if (!description && searchFiles.length === 0) {
    showToast('Insira uma descrição ou imagem.', 'err');
    return;
  }

  setLoading('search-btn', true, '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg> Enviar');
  setStatus('search-status', 'Gerando assinatura visual do pet...');

  try {
    const body = { description };

    if (searchFiles.length > 0) {
      body.image = await fileToBase64(searchFiles[0]);
    }

    setStatus('search-status', 'Procurando correspondências...');

    const res = await fetch(`${API}/pets/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.error || 'Erro na busca.');

    renderMatches(data.matches || []);
    goTo('matches');
    setStatus('search-status', '');

  } catch (err) {
    setStatus('search-status', err.message, 'error');
  } finally {
    setLoading('search-btn', false, '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg> Enviar');
  }
}

/* ══════════════════════════════════════════
   RESULTADOS — Frame 4
══════════════════════════════════════════ */
let currentMatches = [];

function renderMatches(matches) {
  currentMatches = matches;
  const container = document.getElementById('matches-container');
  container.innerHTML = '';

  if (matches.length === 0) {
    container.innerHTML = `
      <div class="no-results">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <p><strong>Nenhum pet encontrado.</strong></p>
        <p>Tente uma foto diferente ou descrição mais detalhada.</p>
      </div>`;
    return;
  }

  matches.forEach((pet, i) => {
    const card = document.createElement('div');
    card.className = 'match-card';
    card.onclick = () => renderDetail(i);
    card.innerHTML = `
      <div class="match-card-wrap">
        <img src="${pet.imageUrl || 'https://placehold.co/200x170/e8e0d8/7a6e65?text=Pet'}" alt="${pet.name || 'Pet'}"/>
        <span class="match-pct">${Math.round((pet.similarity || 0) * 100)}%</span>
      </div>
      <div class="match-card-body">
        <div class="match-card-loc">${pet.lastLocation || 'Localização não informada'}</div>
        ${pet.breed ? `<div class="match-card-breed">${pet.breed}</div>` : ''}
      </div>`;
    container.appendChild(card);
  });
}

/* ══════════════════════════════════════════
   DETALHE — Frame 6
══════════════════════════════════════════ */
function renderDetail(index) {
  const pet = currentMatches[index];
  if (!pet) return;

  const waNumber = (pet.contactInfo || '').replace(/\D/g, '');
  const pct = Math.round((pet.similarity || 0) * 100);

  const tags = [pet.breed, pet.color, pet.species]
    .filter(Boolean)
    .map(t => `<span class="detail-tag">${t}</span>`)
    .join('');

  document.getElementById('detail-card').innerHTML = `
    <div class="detail-header">
      <div class="detail-avatar">🐾</div>
      <div>
        <div class="detail-user">${pet.contactInfo || '@usuario'}</div>
        <div class="detail-loc">📍 ${pet.lastLocation || ''}</div>
      </div>
      <div class="detail-pct">${pct}% match</div>
    </div>
    <div class="detail-img">
      <img src="${pet.imageUrl || 'https://placehold.co/400x260/e8e0d8/7a6e65?text=Pet'}" alt="${pet.name || 'Pet'}"/>
    </div>
    <div class="detail-body">
      <p class="detail-desc">*${pet.description || 'Descrição do animal'}*</p>
      ${tags ? `<div class="detail-tags">${tags}</div>` : ''}
      <a href="${waNumber ? `https://wa.me/${waNumber}` : '#'}" target="_blank" rel="noopener noreferrer">
        <button class="btn-contact">
          💬 Entrar em contato
        </button>
      </a>
    </div>`;

  goTo('detail');
}

/* ══════════════════════════════════════════
   CADASTRAR PET — Frame 7
══════════════════════════════════════════ */
const petFiles = [];

document.getElementById('pet-file').addEventListener('change', async function () {
  const files = Array.from(this.files);
  files.forEach(f => {
    petFiles.push(f);
    addPreview('pet-previews', f, petFiles);
  });
  this.value = '';

  // Auto-análise IA na primeira imagem
  if (files[0] && petFiles.length === 1) {
    setStatus('pet-status', 'IA analisando imagem...');
    try {
      const b64 = await fileToBase64(files[0]);
      const res = await fetch(`${API}/pets/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: b64 }),
      });
      const data = await res.json();
      if (data.species)  document.getElementById('pet-animal').value = data.species;
      if (data.breed || data.primaryColor || data.distinguishingMarks) {
        document.getElementById('pet-desc').value =
          [data.breed, data.primaryColor, data.distinguishingMarks].filter(Boolean).join(', ');
      }
      setStatus('pet-status', 'IA preencheu os campos! Verifique antes de enviar.', 'success');
    } catch {
      setStatus('pet-status', 'Preencha os campos manualmente.');
    }
  }
});

async function handleRegisterPet() {
  const animal  = document.getElementById('pet-animal').value.trim();
  const regiao  = document.getElementById('pet-regiao').value.trim();
  const descricao = document.getElementById('pet-desc').value.trim();

  if (!animal || !regiao) {
    showToast('Animal e região são obrigatórios.', 'err');
    return;
  }

  setLoading('pet-btn', true, '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg> Enviar');
  setStatus('pet-status', 'Cadastrando animal...');

  try {
    const formData = new FormData();
    formData.append('animal', animal);
    formData.append('regiao', regiao);
    formData.append('descricao', descricao);
    if (petFiles.length > 0) formData.append('image', petFiles[0]);

    const res = await fetch(`${API}/pets/register`, {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erro ao cadastrar.');

    setStatus('pet-status', 'Animal cadastrado com sucesso! ✓', 'success');
    showToast('Animal cadastrado com sucesso! 🐾');

    // Reset
    setTimeout(() => {
      document.getElementById('pet-animal').value = '';
      document.getElementById('pet-regiao').value = '';
      document.getElementById('pet-desc').value = '';
      document.getElementById('pet-previews').innerHTML = '';
      petFiles.length = 0;
      setStatus('pet-status', '');
      goTo('home');
    }, 1800);

  } catch (err) {
    setStatus('pet-status', err.message, 'error');
  } finally {
    setLoading('pet-btn', false, '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg> Enviar');
  }
}

/* ══════════════════════════════════════════
   CADASTRO DE USUÁRIO — Frame 8 / 9
══════════════════════════════════════════ */
async function handleRegisterUser(e) {
  e.preventDefault();

  const senha   = document.getElementById('reg-senha').value;
  const confirm = document.getElementById('reg-confirm').value;

  if (senha !== confirm) {
    setStatus('reg-status', 'As senhas não coincidem.', 'error');
    return;
  }

  setLoading('reg-btn', true, 'Registrar');
  setStatus('reg-status', 'Criando conta...');

  try {
    const res = await fetch(`${API}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nome:            document.getElementById('reg-nome').value,
        sobrenome:       document.getElementById('reg-sobrenome').value,
        dataNascimento:  document.getElementById('reg-data').value,
        telefone:        document.getElementById('reg-tel').value,
        email:           document.getElementById('reg-email').value,
        senha,
      }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erro ao cadastrar.');

    setStatus('reg-status', 'Conta criada! Verifique seu e-mail. ✓', 'success');
    showToast('Conta criada com sucesso! 🎉');
    setTimeout(() => goTo('home'), 2000);

  } catch (err) {
    setStatus('reg-status', err.message, 'error');
  } finally {
    setLoading('reg-btn', false, 'Registrar');
  }
}

/* ══════════════════════════════════════════
   LOGIN
══════════════════════════════════════════ */
async function handleLogin(e) {
  e.preventDefault();
  setLoading('login-btn', true, 'Entrar');
  setStatus('login-status', 'Autenticando...');

  try {
    const res = await fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: document.getElementById('login-email').value,
        senha: document.getElementById('login-senha').value,
      }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Email ou senha incorretos.');

    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
    }

    setStatus('login-status', 'Login realizado! ✓', 'success');
    showToast('Bem-vindo de volta! 🐾');
    setTimeout(() => goTo('home'), 1500);

  } catch (err) {
    setStatus('login-status', err.message, 'error');
  } finally {
    setLoading('login-btn', false, 'Entrar');
  }
}

/* ══════════════════════════════════════════
   TOOLTIP — Frame 9
══════════════════════════════════════════ */
function toggleTooltip() {
  const t = document.getElementById('tooltip');
  t.classList.toggle('open');
}

document.addEventListener('click', (e) => {
  const tooltip = document.getElementById('tooltip');
  if (!e.target.closest('.label-with-tip')) {
    tooltip.classList.remove('open');
  }
});
