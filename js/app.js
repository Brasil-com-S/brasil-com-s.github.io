// Brasil Com S - Samba Schools Catalog with Caching & Pagination
document.addEventListener('DOMContentLoaded', async () => {
  const schoolsGrid = document.getElementById('schoolsGrid');
  const searchInput = document.getElementById('searchInput');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const modalOverlay = document.getElementById('modalOverlay');
  const modalBody = document.getElementById('modalBody');
  const modalClose = document.getElementById('modalClose');

  const CACHE_KEY = 'brasil_com_s_escolas_v1';
  const CACHE_TTL = 3600 * 1000; // 1 hour cache

  let allEscolas = [];
  let filteredEscolas = [];
  let currentFilter = 'all';
  
  // Pagination State
  const ITEMS_PER_PAGE = 8;
  let currentPage = 1;

  // Load Schools with Caching (localStorage)
  async function loadSchoolsData() {
    const cachedData = localStorage.getItem(CACHE_KEY);
    const cachedTime = localStorage.getItem(CACHE_KEY + '_time');

    if (cachedData && cachedTime && (Date.now() - parseInt(cachedTime, 10)) < CACHE_TTL) {
      console.log('⚡ Cargando escolas de samba do CACHE local');
      allEscolas = JSON.parse(cachedData);
      initApp();
      return;
    }

    try {
      console.log('🌐 Requisitando escolas de samba via API...');
      const res = await fetch('api/v1/escolas.json');
      const data = await res.json();
      allEscolas = data.escolas;
      
      // Save to localStorage cache
      localStorage.setItem(CACHE_KEY, JSON.stringify(allEscolas));
      localStorage.setItem(CACHE_KEY + '_time', Date.now().toString());

      initApp();
    } catch (err) {
      if (schoolsGrid) {
        schoolsGrid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: #ef4444;">Erro ao carregar catálogo de escolas de samba.</p>`;
      }
    }
  }

  function initApp() {
    updateStats(allEscolas);
    applyFilters();
  }

  function updateStats(escolas) {
    const statTotal = document.getElementById('statTotal');
    const statSambas = document.getElementById('statSambas');
    const statTitulos = document.getElementById('statTitulos');
    
    if (statTotal) statTotal.textContent = escolas.length;
    
    if (statSambas) {
      const totalSambas = escolas.reduce((acc, curr) => acc + (curr.sambas_enredo ? curr.sambas_enredo.length : 0), 0);
      statSambas.textContent = totalSambas + '+';
    }

    if (statTitulos) {
      const totalTitulos = escolas.reduce((acc, curr) => acc + (curr.titulos || 0), 0);
      statTitulos.textContent = totalTitulos + '+';
    }
  }

  function renderPaginatedSchools(reset = false) {
    if (!schoolsGrid) return;
    
    if (reset) {
      schoolsGrid.innerHTML = '';
      currentPage = 1;
    }

    if (filteredEscolas.length === 0) {
      schoolsGrid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: #94A3B8; padding: 3rem;">Nenhuma escola encontrada para a busca.</p>`;
      removeLoadMoreButton();
      return;
    }

    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const batch = filteredEscolas.slice(startIndex, endIndex);

    batch.forEach(school => {
      const card = document.createElement('div');
      card.className = 'school-card';
      
      const colors = school.cores_hex.map(hex => `<span class="color-dot" style="background-color: ${hex};"></span>`).join('');
      const badgeClass = school.grupo.toLowerCase().includes('especial') ? 'especial' : 'acesso';
      
      // Use PNG logo artwork for high quality raster display
      const logoPng = school.logo_png_url || school.logo_url;

      card.innerHTML = `
        <img src="${logoPng}" alt="Arte Brasão ${school.nome}" class="school-logo" loading="lazy" />
        <span class="badge ${badgeClass}" style="margin-bottom: 0.8rem;">${school.grupo}</span>
        <h3 class="school-name">${school.nome}</h3>
        <p class="school-meta">${school.cidade} - ${school.estado} &bull; Fundada em ${school.fundacao.substring(0, 4)}</p>
        <div class="colors-bar">${colors}</div>
        <button class="btn-details" data-slug="${school.slug}">Ver Histórico Completo (${school.sambas_enredo ? school.sambas_enredo.length : 0} Sambas)</button>
      `;

      card.querySelector('.btn-details').addEventListener('click', () => {
        openSchoolModal(school);
      });

      schoolsGrid.appendChild(card);
    });

    updateLoadMoreButton();
  }

  function updateLoadMoreButton() {
    removeLoadMoreButton();
    
    const remaining = filteredEscolas.length - (currentPage * ITEMS_PER_PAGE);
    if (remaining > 0) {
      const loadMoreContainer = document.createElement('div');
      loadMoreContainer.id = 'loadMoreContainer';
      loadMoreContainer.style.cssText = 'grid-column: 1/-1; text-align: center; margin-top: 2rem;';
      
      const btn = document.createElement('button');
      btn.className = 'btn-secondary';
      btn.innerHTML = `Carregar Mais Escolas (${remaining} restantes)`;
      btn.style.cssText = 'padding: 0.8rem 2rem; border-color: #FFCC00; color: #FFCC00; cursor: pointer;';
      
      btn.addEventListener('click', () => {
        currentPage++;
        renderPaginatedSchools(false);
      });

      loadMoreContainer.appendChild(btn);
      schoolsGrid.appendChild(loadMoreContainer);
    }
  }

  function removeLoadMoreButton() {
    const existing = document.getElementById('loadMoreContainer');
    if (existing) existing.remove();
  }

  // Filter Buttons Logic
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.filter;
      applyFilters();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      applyFilters();
    });
  }

  function applyFilters() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
    filteredEscolas = allEscolas.filter(school => {
      const matchesSearch = school.nome.toLowerCase().includes(query) || 
                            school.bairro.toLowerCase().includes(query) || 
                            school.cidade.toLowerCase().includes(query);

      if (currentFilter === 'all') return matchesSearch;
      if (currentFilter === 'rj') return matchesSearch && school.estado === 'RJ';
      if (currentFilter === 'sp') return matchesSearch && school.estado === 'SP';
      if (currentFilter === 'especial') return matchesSearch && school.grupo === 'Especial';
      if (currentFilter === 'acesso') return matchesSearch && school.grupo.includes('Acesso');
      return matchesSearch;
    });

    renderPaginatedSchools(true);
  }

  // Modal Dialog Logic
  function openSchoolModal(school) {
    if (!modalOverlay || !modalBody) return;

    const logoEscola = school.logo_original_url || school.logo_url;

    const sambasHtml = school.sambas_enredo ? school.sambas_enredo.map(s => `
      <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 0.6rem;">
        <strong style="color: #FFCC00;">Ano ${s.ano}:</strong> "${s.titulo}"
        <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 0.2rem;">Compositores: ${s.compositores} &bull; Intérprete: ${s.interpretacao || 'N/I'}</div>
      </div>
    `).join('') : '<p>Sem registros de sambas-enredo.</p>';

    const colocacoesHtml = school.colocacoes ? school.colocacoes.map(c => `
      <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
        <td style="padding: 0.6rem; color: #FFCC00; font-weight: 700;">${c.ano}</td>
        <td style="padding: 0.6rem;">${c.grupo}</td>
        <td style="padding: 0.6rem; font-weight: 700;">${c.resultado || c.posicao + 'º Lugar'}</td>
        <td style="padding: 0.6rem; color: #94A3B8;">${c.pontos != null ? c.pontos + ' pts' : '—'}</td>
      </tr>
    `).join('') : '<tr><td colspan="4">Sem registros.</td></tr>';

    const fundadoresHtml = school.fundadores && school.fundadores.length ? school.fundadores.join(', ') : 'Não documentados nas fontes oficiais';

    modalBody.innerHTML = `
      <div style="display: flex; align-items: center; gap: 1.5rem; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 1.5rem; flex-wrap: wrap;">
        <img id="modalSchoolLogoImg" src="${logoEscola}" alt="Brasão ${school.nome}" style="width: 110px; height: 110px; border-radius: 50%; border: 3px solid #FFCC00; object-fit: cover; background: #000;" />
        <div style="flex: 1; min-width: 250px;">
          <h2 style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; color: #F1F5F9; line-height: 1.1;">${school.nome_completo}</h2>
          <p style="color: #94A3B8; font-size: 0.95rem; margin-top: 0.4rem;">
            Fundada em <strong>${new Date(school.fundacao).toLocaleDateString('pt-BR')}</strong> &bull; ${school.bairro}, ${school.cidade} - ${school.estado}
          </p>
          <p style="color: #CBD5E1; font-size: 0.85rem; margin-top: 0.3rem;">
            <strong>Fundadores:</strong> ${fundadoresHtml}
          </p>
          <div style="display: flex; gap: 0.6rem; margin-top: 0.8rem; flex-wrap: wrap;">
            <span class="badge ${school.grupo.toLowerCase().includes('especial') ? 'especial' : 'acesso'}">${school.grupo}</span>
            <span class="badge" style="background: rgba(0, 168, 89, 0.2); color: #00A859; border-color: #00A859;">${school.titulos} Títulos Conquistados</span>
          </div>
        </div>
      </div>

      <div style="margin-bottom: 2rem;">
        <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.3rem; margin-bottom: 1rem; color: #FFCC00;">🎵 Histórico de Sambas-Enredo (${school.sambas_enredo ? school.sambas_enredo.length : 0})</h3>
        <div style="max-height: 300px; overflow-y: auto; padding-right: 0.5rem;">
          ${sambasHtml}
        </div>
      </div>

      <div>
        <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.3rem; margin-bottom: 1rem; color: #FFCC00;">🏆 Histórico de Colocações no Carnaval</h3>
        <div style="max-height: 250px; overflow-y: auto;">
          <table style="width: 100%; text-align: left; border-collapse: collapse; font-size: 0.9rem;">
            <thead>
              <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: #94A3B8;">
                <th style="padding: 0.6rem;">Ano</th>
                <th style="padding: 0.6rem;">Grupo</th>
                <th style="padding: 0.6rem;">Resultado</th>
                <th style="padding: 0.6rem;">Pontos</th>
              </tr>
            </thead>
            <tbody>
              ${colocacoesHtml}
            </tbody>
          </table>
        </div>
      </div>
    `;

    modalOverlay.classList.add('active');
  }

  if (modalClose && modalOverlay) {
    modalClose.addEventListener('click', () => {
      modalOverlay.classList.remove('active');
    });

    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
      }
    });
  }

  // Start app
  loadSchoolsData();
});
