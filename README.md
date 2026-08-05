# 🇧🇷 Brasil Com S - API Cultural & GitHub Pages

Plataforma de consulta aberta e API pública sobre cultura brasileira desenvolvida pela organização **Brasil Com S**.

O projeto serve simultaneamente como **Landing Page Interativa** e como uma **API REST Estática em JSON** hospedada diretamente no GitHub Pages (`https://brasil-com-s.github.io/`).

📖 **Documentação técnica completa** (deploy, pipeline, schemas dos CSVs, endpoints): [DOCUMENTACAO.md](DOCUMENTACAO.md)

---

## ⚙️ Pipeline de Dados (Fontes Oficiais)

A fonte da verdade são os CSVs em `data/`, gerados por scraping de fontes
oficiais — **nenhum dado é escrito à mão**:

- **[Wikipédia em português](https://pt.wikipedia.org)** — fundação, fundadores,
  cores, símbolo, bairro (infobox dos artigos das escolas); colocações, pontos e
  enredos ano a ano (páginas "Resultados do Carnaval do Rio de Janeiro/São Paulo em {ano}",
  RJ 1932+ e SP 1969+); títulos (listas oficiais de campeãs).
- **[LigaSP](https://ligasp.com.br)** — logos oficiais das escolas de São Paulo e
  enredos do Carnaval 2027.
- **[Galeria do Samba](https://galeriadosamba.com.br)** — compositores e
  intérpretes dos sambas-enredo do RJ (páginas por ano de cada escola).
- **[LIESA](https://liesa.org.br)** — referência e validação cruzada (a Galeria
  do Samba não publica imagens de escudos; as bandeiras oficiais do RJ vêm
  dos infoboxes da Wikipédia via Wikimedia).

Como rodar (requer Python 3.11+ e macOS `sips` para conversão de imagens).
A ordem importa: `scrape_wikipedia_resultados.py` reescreve
`sambas_enredo_historico.csv` do zero, então os merges de compositores
(Galeria para o RJ, Wikipédia para SP) rodam sempre depois dele:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scrape_wikipedia_resultados.py   # colocacoes_historico.csv + sambas_enredo_historico.csv
.venv/bin/python scrape_galeria_sambas.py         # + compositores/intérpretes RJ (Galeria do Samba)
.venv/bin/python scrape_wikipedia_sambas_sp.py    # + compositores SP (artigos das escolas)
.venv/bin/python scrape_wikipedia_escolas.py      # escolas_de_samba.csv
.venv/bin/python scrape_logos.py                  # assets/logos/original/*.png
.venv/bin/python build_api_from_csv.py            # compila api/v1/**
.venv/bin/python validate_data.py                 # checagens de integridade
```

Os scrapers cacheiam o HTML em `data/cache/` (re-execuções não refazem
downloads) e gravam nomes não reconhecidos em
`data/cache/unmatched_names.log` para revisão.

**Atribuição:** os escudos/bandeiras são propriedade das respectivas
agremiações, servidos aqui apenas para referência cultural; as imagens do RJ
vêm do Wikimedia Commons sob as licenças das suas páginas de descrição.

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
- `GET /api/v1/carnavais.json` - Índice de anos com históricos gravados (1932 até o carnaval mais recente, exceto 2021, cancelado pela pandemia).
- `GET /api/v1/carnavais/:ano.json` - Classificação por grupo/estado e campeãs do Grupo Especial por ano (ex: `2024.json`).

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
    "fundadores": ["Cartola", "Carlos Cachaça", "Zé Espinguela", "Saturnino Gonçalves", "..."],
    "estado": "RJ",
    "cidade": "Rio de Janeiro",
    "bairro": "Mangueira",
    "grupo": "Especial",
    "cores": ["Verde", "Rosa"],
    "cores_hex": ["#006400", "#FF1493"],
    "simbolo": "Tambor surdo encimado por uma coroa e com ramos de louro em volta",
    "titulos": 20,
    "anos_titulos": [1932, 1933, 1934, 1940, 1949, 1950, 1954, 1960, 1961, 1967, 1968, 1973, 1984, 1986, 1987, 1998, 2002, 2016, 2019],
    "logo_url": "assets/logos/original/mangueira.png",
    "sambas_enredo": [
      {
        "ano": 2024,
        "titulo": "A Negra Voz do Amanhã",
        "compositores": "",
        "interpretacao": ""
      }
    ],
    "colocacoes": [
      {
        "ano": 2024,
        "grupo": "Grupo Especial",
        "posicao": 7,
        "pontos": 268.8,
        "resultado": "7º Lugar"
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
