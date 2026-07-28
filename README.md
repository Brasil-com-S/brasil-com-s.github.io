# 🇧🇷 Brasil Com S - API Cultural & GitHub Pages

Plataforma de consulta aberta e API pública sobre cultura brasileira desenvolvida pela organização **Brasil Com S**.

O projeto serve simultaneamente como **Landing Page Interativa** e como uma **API REST Estática em JSON** hospedada diretamente no GitHub Pages (`https://brasil-com-s.github.io/`).

---

## 🚀 Endpoints Disponíveis (`/api/v1/`)

Todos os recursos são servidos como arquivos JSON estáticos com suporte nativo a CORS e alta velocidade de entrega pelo GitHub Pages:

### 1. Escolas de Samba
- `GET /api/v1/escolas.json` - Lista completa de escolas de samba do Rio de Janeiro e São Paulo (Grupo Especial e Acesso).
- `GET /api/v1/escolas/rj.json` - Apenas escolas de samba do Rio de Janeiro.
- `GET /api/v1/escolas/sp.json` - Apenas escolas de samba de São Paulo.
- `GET /api/v1/escolas/especial.json` - Apenas escolas do Grupo Especial.
- `GET /api/v1/escolas/acesso.json` - Apenas escolas dos Grupos de Acesso (Série Ouro RJ, Acesso 1 & 2 SP).
- `GET /api/v1/escolas/:slug.json` - Detalhes completos da escola (ex: `mangueira.json`, `portela.json`, `beija-flor.json`, `vai-vai.json`, `salgueiro.json`, `mocidade-alegre.json`).

### 2. Carnavais
- `GET /api/v1/carnavais.json` - Índice de anos com históricos gravados.
- `GET /api/v1/carnavais/:ano.json` - Resultados e campeãs por ano (ex: `2024.json`).

---

## 🎨 Campos Retornados nos Detalhes da Escola (`:slug.json`)

```json
{
  "status": "success",
  "data": {
    "id": "mangueira",
    "slug": "mangueira",
    "nome": "Estação Primeira de Mangueira",
    "nome_completo": "Grêmio Recreativo Escola de Samba Estação Primeira de Mangueira",
    "fundacao": "1928-04-28",
    "estado": "RJ",
    "cidade": "Rio de Janeiro",
    "bairro": "Mangueira",
    "grupo": "Especial",
    "cores": ["Verde", "Rosa"],
    "cores_hex": ["#008000", "#FF69B4"],
    "simbolo": "Surdo e Coroa Imperial",
    "titulos": 20,
    "anos_titulos": [1932, 1933, 1934, 1940, 1949, 1950, 1954, 1960, 1961, 1967, 1968, 1973, 1984, 1986, 1987, 1998, 2002, 2016, 2019],
    "logo_url": "assets/logos/mangueira.svg",
    "sambas_enredo": [
      {
        "ano": 2024,
        "titulo": "A Black Apenas: A Música Que Move a Alma",
        "compositores": "Lequinho, Junior Fionda, Gabriel Machado",
        "interpretacao": "Marquinho Art'Samba"
      }
    ],
    "colocacoes": [
      {
        "ano": 2024,
        "grupo": "Especial",
        "posicao": 7,
        "pontos": 268.8
      }
    ]
  }
}
```

---

## ⚙️ Jekyll & Deploy no GitHub Pages

Este repositório está configurado para o **Jekyll** e **GitHub Pages**:
- O arquivo `_config.yml` inclui o diretório `api/` na compilação estática do Jekyll.
- Ao dar `git push` na branch `main` do repositório da organização `brasil-com-s/brasil-com-s.github.io`, o GitHub Pages faz o build e disponibiliza a página e a API instantaneamente no domínio público `https://brasil-com-s.github.io`.

---

## 📄 Licença

Desenvolvido para a comunidade. Dados Culturais Abertos sob a licença [MIT](LICENSE).
