# Brasil Com S — Documentação Técnica

Documento central do projeto: o que é, como funciona, como é o deploy, de onde
vêm os dados e como reproduzir tudo localmente.

---

## 1. Visão geral

O **Brasil Com S** é uma API pública e estática sobre as escolas de samba do
Rio de Janeiro e de São Paulo, servida pelo GitHub Pages a partir deste
repositório. Não há servidor, banco de dados nem backend: a "API" é um
conjunto de arquivos JSON gerados por um pipeline de scraping + compilação e
commitados no repo. O GitHub Pages simplesmente os serve como arquivos
estáticos.

**Endereços online**

| Recurso | URL |
|---|---|
| Site (vitrine + API explorer) | https://brasil-com-s.github.io/ |
| Índice de escolas | https://brasil-com-s.github.io/api/v1/escolas.json |
| Índice de carnavais | https://brasil-com-s.github.io/api/v1/carnavais.json |
| Repositório | https://github.com/Brasil-com-S/brasil-com-s.github.io |
| Organização | https://github.com/brasil-com-s |

**Números atuais** (jul/2026): 39 escolas (20 RJ + 19 SP), 1984 colocações
históricas, 2077 sambas-enredo, 93 anos de carnaval (1932–2026, sem 2021),
39 logos oficiais.

---

## 2. Princípio fundamental: o CSV é a fonte da verdade

Todo o conteúdo da API deriva de **3 arquivos CSV** em `data/`. Nenhum dado é
escrito à mão nos JSONs e nenhum script "inventa" conteúdo: o pipeline só
transfere dados de fontes externas oficiais para os CSVs, e dos CSVs para os
JSONs. Se um campo não existe na fonte, ele fica **vazio** — nunca é
preenchido com suposição.

### 2.1 `data/escolas_de_samba.csv` — cadastro das escolas (39 linhas)

```
id, slug, nome, nome_completo, fundacao, fundadores, estado, cidade,
bairro, grupo, cores, cores_hex, simbolo, titulos, anos_titulos,
logo_original_url
```

- Listas são separadas por `; ` (ex.: `fundadores`, `cores`, `anos_titulos`).
- `fundacao` em ISO (`1928-04-28`); pode ser só o ano quando a fonte só tem o ano.
- `logo_original_url` aponta para `assets/logos/original/{slug}.png` (servido
  pelo próprio Pages).

### 2.2 `data/colocacoes_historico.csv` — resultados ano a ano (1984 linhas)

```
escola_slug, escola_nome, ano, estado, grupo, posicao, pontos, resultado
```

- Cobertura: RJ desde 1932, SP desde 1969 (primeiros anos com resultados
  estruturados na Wikipédia).
- `grupo` varia com a época (Grupo Especial, Grupo 1, Série Ouro, Acesso...).
- `resultado` é o rótulo textual ("Campeã", "5º Lugar", "Vice-Campeã"...).
- Empates e títulos divididos são reais e estão preservados (ex.: SP 1990,
  1993, 1999, 2000; Mocidade co-campeã 2017 no RJ).

### 2.3 `data/sambas_enredo_historico.csv` — sambas-enredo (2061 linhas)

```
escola_slug, escola_nome, ano, estado, grupo, titulo_samba, compositores,
interpretacao
```

- Toda colocação registrada tem `titulo_samba` (cobertura 100%).
- `compositores`: 987/1197 no RJ (Galeria do Samba), 428/864 em SP (Wikipédia).
- `interpretacao`: 863 linhas no RJ; em SP fica vazio (as tabelas da Wikipédia
  de SP não separam intérprete de carnavalesco — coluna ambígua).
- Pode conter anos sem colocação correspondente (adicionados pela Galeria do
  Samba); nesse caso `grupo` fica vazio.

---

## 3. Pipeline de dados

Os scrapers rodam em Python 3.11+ dentro de `.venv/` (deps em
`requirements.txt`: `requests`, `beautifulsoup4`, `lxml`). Todos:

- **cacheiam** o HTML/wikitext em `data/cache/` (re-execução não refaz
  download; o cache não é commitado — está no `.gitignore`);
- usam `User-Agent` identificado e **delay de 1s** entre requisições;
- gravam nomes não reconhecidos em `data/cache/unmatched_names.log`.

### 3.1 Ordem obrigatória de execução

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

.venv/bin/python scrape_wikipedia_resultados.py   # 1. reescreve colocacoes + sambas DO ZERO
.venv/bin/python scrape_galeria_sambas.py         # 2. merge: compositores/intérpretes RJ
.venv/bin/python scrape_wikipedia_sambas_sp.py    # 3. merge: compositores SP
.venv/bin/python scrape_wikipedia_escolas.py      # 4. escolas_de_samba.csv
.venv/bin/python scrape_logos.py                  # 5. assets/logos/original/*.png
.venv/bin/python build_api_from_csv.py            # 6. compila api/v1/**
.venv/bin/python validate_data.py                 # 7. checagens de integridade
```

**A ordem importa**: `scrape_wikipedia_resultados.py` reescreve
`sambas_enredo_historico.csv` do zero a partir das colocações. Os scripts 2 e 3
fazem *merge* (só preenchem campos vazios e adicionam anos novos) — se rodarem
antes do 1, o trabalho é apagado.

### 3.2 O que cada script faz

| Script | Função | Fonte |
|---|---|---|
| `scrape_wikipedia_resultados.py` | Raspa as páginas "Resultados do Carnaval do Rio/São Paulo em {ano}"; gera `colocacoes_historico.csv` e o esqueleto de `sambas_enredo_historico.csv`. Tem correções manuais documentadas no código (`MANUAL_ENREDOS`, ex.: Barroca 2014 com intérprete Tito Amorim; título dividido da Mocidade 2017). | Wikipédia |
| `scrape_galeria_sambas.py` | Para cada uma das 20 escolas do RJ, percorre as páginas por ano (`/escolas-de-samba/{escola}/{ano}/`) e extrai enredo, compositores e intérprete. Adiciona anos que a Wikipédia não cobre. | Galeria do Samba |
| `scrape_wikipedia_sambas_sp.py` | Extrai ano/enredo/compositores das tabelas de "segmentos históricos" dos artigos das 19 escolas de SP. Não extrai intérprete (coluna ambígua). | Wikipédia |
| `scrape_wikipedia_escolas.py` | Infobox + lead dos artigos das 39 escolas: fundação, fundadores, cores, símbolo, bairro. | Wikipédia |
| `scrape_logos.py` | Baixa logos oficiais: 18 de SP via LigaSP, 21 do RJ via Wikimedia Commons (infoboxes). Converte com `sips` (macOS) para PNG em `assets/logos/original/`. | LigaSP / Wikimedia |
| `scrape_2027_enredos_ligasp.py` | Enredos do Carnaval 2027 de SP (16 escolas), incorporados no build. | LigaSP |
| `scrape_all_ligasp_posts.py` | Descoberta de páginas de escolas no site da LigaSP (apoio aos scrapers de SP). | LigaSP |
| `download_all_official_ligasp_logos.py` | Download em lote dos logos da LigaSP (usado por `scrape_logos.py`). | LigaSP |
| `build_api_from_csv.py` | Compilador: lê os 3 CSVs e gera todos os JSONs de `api/v1/`. | — |
| `validate_data.py` | Integridade: contagens, chaves duplicadas, escolas sem dados, consistência títulos/anos. Deve passar 100% antes de commitar. | — |
| `push_to_github.py` | Utilitário antigo de publicação via `gh` (cria repo/org e dá push). Hoje o fluxo é `git` normal. | — |

### 3.3 Pegadinhas conhecidas (já tratadas no código)

- **Galeria do Samba não envia `charset`** no header — decodificar sempre como
  UTF-8 (`r.content.decode("utf-8")`), senão vira mojibake (`DomÃªnico`).
- **Wikitext malformado**: wikilinks `[[alvo|texto]]` quebram splits por `|`;
  há tags `<small>` adjacentes partindo nomes ao meio (`Na</small><small>io
  Denay`). Os parsers removem wikilinks e fundem `<small>`s antes de extrair.
- **Headers de tabela da Wikipédia** variam por ano ("Enredo", "Samba-enredo",
  "Samba") — o parser aceita todos.

---

## 4. A API estática (`api/v1/`)

Gerada por `build_api_from_csv.py`. Todos os endpoints retornam
`{"status": "success", "data": ...}`.

| Endpoint | Conteúdo |
|---|---|
| `GET /api/v1/escolas.json` | As 39 escolas (cadastro completo, sem histórico) |
| `GET /api/v1/escolas/rj.json` / `sp.json` | Filtro por estado |
| `GET /api/v1/escolas/especial.json` / `acesso.json` | Filtro por grupo atual |
| `GET /api/v1/escolas/{slug}.json` | Escola completa: cadastro + `colocacoes[]` + `sambas_enredo[]` |
| `GET /api/v1/carnavais.json` | Índice dos 93 anos com resumo |
| `GET /api/v1/carnavais/{ano}.json` | Resultados daquele ano, agrupados por grupo/divisão |

Exemplo real (`escolas/mangueira.json`, trecho):

```json
{
  "status": "success",
  "data": {
    "slug": "mangueira",
    "nome": "Estação Primeira de Mangueira",
    "fundacao": "1928-04-28",
    "fundadores": ["Cartola", "Carlos Cachaça", "Zé Espinguela", "..."],
    "titulos": 20,
    "sambas_enredo": [
      {
        "ano": 2019,
        "titulo": "História pra Ninar Gente Grande",
        "compositores": "Deivid Domênico, Tomaz Miranda, Mama, ...",
        "interpretacao": "Marquinho Art'Samba"
      }
    ]
  }
}
```

Não há paginação, autenticação, CORS restrito ou rate limit — são arquivos
estáticos públicos, consumíveis de qualquer origem.

---

## 5. Deploy no GitHub Pages

- **Repo**: `Brasil-com-S/brasil-com-s.github.io` (repo de Pages de
  organização — a branch `main` inteira é publicada na raiz do domínio).
- **Fluxo**: `git push origin main` → o GitHub dispara o workflow automático
  `pages build and deployment` (~30–60s) → novo conteúdo no ar.
- **Jekyll**: o Pages processa o repo com Jekyll usando `_config.yml`:
  - `include: [api]` garante que a pasta `api/` entre no build;
  - `defaults` com `layout: null` para `api/**` faz os JSONs saírem crus,
    sem template HTML;
  - plugins `jekyll-seo-tag` e `jekyll-sitemap` para o site.
- Não há GitHub Actions customizado, secrets ou variáveis: o deploy é 100%
  o mecanismo padrão do Pages.
- **Publicar dados novos** = rodar o pipeline (seção 3) → `git add -A` →
  commit → push. A validação (`validate_data.py`) deve passar antes do push.

---

## 6. O site (`index.html` + `js/` + `css/`)

Página única servida na raiz, sem framework nem build — HTML/CSS/JS puros.

- **`js/app.js`** — vitrine das escolas:
  - busca `api/v1/escolas.json` e guarda em `localStorage` (cache com
    timestamp, evita refetch a cada visita);
  - cards com logo, cores, fundação e títulos;
  - paginação client-side com botão "carregar mais";
  - filtros por estado/grupo;
  - modal com detalhes da escola.
- **`js/api-explorer.js`** — explorador interativo da API: escolhe um
  endpoint, faz `fetch` ao vivo e mostra o JSON com preview visual.
- **`index.html`** — landing com exemplos de uso (`fetch` de
  `escolas/rj.json` e `escolas/mangueira.json`) e links para a organização.

---

## 7. Fontes de dados e atribuição

| Fonte | Uso |
|---|---|
| [Wikipédia (pt)](https://pt.wikipedia.org) | Resultados ano a ano (RJ 1932+, SP 1969+), cadastro das escolas (infobox/lead), compositores de SP, títulos de campeãs |
| [Galeria do Samba](https://galeriadosamba.com.br) | Compositores e intérpretes dos sambas do RJ; anos não cobertos pela Wikipédia |
| [LigaSP](https://ligasp.com.br) | Logos oficiais das escolas de SP; enredos do Carnaval 2027 |
| [LIESA](https://liesa.org.br) | Referência/validação cruzada do RJ |
| Wikimedia Commons | Bandeiras/escudos das escolas do RJ (a Galeria do Samba não publica escudos) |

**Atribuição**: os escudos/bandeiras são propriedade das respectivas
agremiações, servidos apenas para referência cultural; as imagens do RJ vêm do
Wikimedia Commons sob as licenças das suas páginas de descrição.

---

## 8. Setup local

```bash
git clone git@github.com:Brasil-com-S/brasil-com-s.github.io.git
cd brasil-com-s.github.io
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

- Conversão de logos usa `sips` (nativo do macOS).
- Para ver o site localmente basta um servidor estático
  (`python3 -m http.server`) — não precisa de Jekyll instalado.
- `data/cache/` (cache de scraping), `.venv/` e `__pycache__/` ficam fora do
  git (`.gitignore`).

## 9. Estrutura de diretórios

```
├── index.html, css/, js/        # site estático
├── api/v1/                      # JSONs gerados (commitados)
│   ├── escolas.json, escolas/{slug,rj,sp,especial,acesso}.json
│   └── carnavais.json, carnavais/{ano}.json
├── assets/logos/original/       # 39 logos oficiais (PNG)
├── data/
│   ├── escolas_de_samba.csv         # fonte da verdade: cadastro
│   ├── colocacoes_historico.csv     # fonte da verdade: resultados
│   ├── sambas_enredo_historico.csv  # fonte da verdade: sambas
│   └── cache/                       # HTML/wikitext cacheado (não commitado)
├── scrape_*.py, build_api_from_csv.py, validate_data.py
├── requirements.txt, _config.yml, .gitignore
└── README.md, DOCUMENTACAO.md
```

## 10. Lacunas conhecidas (por decisão, não por bug)

- **Fundadores**: 20 escolas sem nomes — a Wikipédia não os registra no
  infobox/lead. Campo fica vazio.
- **Intérpretes de SP**: vazios (fonte não separa intérprete de carnavalesco),
  exceto casos documentados manualmente (ex.: Barroca 2014 — Tito Amorim).
- **Compositores faltantes**: ~210 linhas RJ e ~436 SP onde a fonte não
  registra a ficha do samba.
- **Anos ausentes por escola**: anos em que a escola não desfilou
  (rebaixada, suspensa ou ainda não fundada).
