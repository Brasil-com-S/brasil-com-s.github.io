// Brasil Com S - API Explorer & Playground
document.addEventListener('DOMContentLoaded', () => {
  const endpointSelect = document.getElementById('endpointSelect');
  const btnSend = document.getElementById('btnSend');
  const codeOutput = document.getElementById('codeOutput');
  const btnCopy = document.getElementById('btnCopy');
  const visualPreview = document.getElementById('visualPreview');

  async function fetchEndpoint(endpoint) {
    codeOutput.textContent = '// Carregando resposta da API...';
    try {
      const response = await fetch(endpoint);
      const data = await response.json();
      
      // Syntax highlight / Pretty format JSON
      codeOutput.textContent = JSON.stringify(data, null, 2);
      
      // Update Visual Preview Card
      updateVisualPreview(data, endpoint);
    } catch (err) {
      codeOutput.textContent = `// Erro ao carregar endpoint: ${err.message}`;
      visualPreview.innerHTML = `<p style="color: #ef4444;">Falha na requisição ao endpoint</p>`;
    }
  }

  function updateVisualPreview(data, endpoint) {
    if (data.data) {
      // Single school object
      const e = data.data;
      visualPreview.innerHTML = `
        <img src="${e.logo_url}" alt="${e.nome}" class="preview-logo" />
        <h3 class="preview-title">${e.nome}</h3>
        <div class="preview-meta">
          <span class="badge ${e.grupo.toLowerCase().includes('especial') ? 'especial' : 'acesso'}">${e.grupo}</span>
          <span class="badge">${e.estado} - ${e.cidade}</span>
        </div>
        <p style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 0.8rem;">
          <strong>Fundação:</strong> ${new Date(e.fundacao).toLocaleDateString('pt-BR')} &bull; 
          <strong>Títulos:</strong> ${e.titulos}
        </p>
        <p style="font-size: 0.85rem; color: #CBD5E1;">
          <em>"${e.sambas_enredo && e.sambas_enredo[0] ? e.sambas_enredo[0].titulo : 'Samba enredo em destaque'}"</em>
        </p>
      `;
    } else if (data.escolas) {
      // List of schools
      const total = data.metadata ? data.metadata.total : data.escolas.length;
      const firstThreeLogos = data.escolas.slice(0, 4).map(e => 
        `<img src="${e.logo_url}" style="width: 50px; height: 50px; border-radius: 50%; border: 2px solid #FFCC00; object-fit: cover;" />`
      ).join('');

      visualPreview.innerHTML = `
        <div style="display: flex; gap: 0.5rem; margin-bottom: 1.2rem;">
          ${firstThreeLogos}
        </div>
        <h3 class="preview-title">${total} Escolas Encontradas</h3>
        <p style="color: #94A3B8; font-size: 0.95rem; margin-top: 0.4rem;">
          Coleção completa de brasões, histórico e sambas-enredo retornado em JSON.
        </p>
      `;
    } else if (data.anos_disponiveis) {
      visualPreview.innerHTML = `
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎭</div>
        <h3 class="preview-title">Histórico de Carnavais</h3>
        <p style="color: #94A3B8; font-size: 0.95rem;">Anos disponíveis: ${data.anos_disponiveis.join(', ')}</p>
      `;
    }
  }

  if (endpointSelect && btnSend) {
    btnSend.addEventListener('click', () => {
      fetchEndpoint(endpointSelect.value);
    });

    endpointSelect.addEventListener('change', () => {
      fetchEndpoint(endpointSelect.value);
    });

    // Initial fetch
    fetchEndpoint(endpointSelect.value);
  }

  if (btnCopy && codeOutput) {
    btnCopy.addEventListener('click', () => {
      navigator.clipboard.writeText(codeOutput.textContent);
      const originalText = btnCopy.textContent;
      btnCopy.textContent = 'Copiat!';
      setTimeout(() => { btnCopy.textContent = originalText; }, 2000);
    });
  }
});
