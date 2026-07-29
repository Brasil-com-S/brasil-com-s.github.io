#!/usr/bin/env python3
"""
scrape_wikipedia_resultados.py

Raspa as páginas oficiais de resultados da Wikipédia em português:
  - "Resultados do Carnaval do Rio de Janeiro em {ano}" (1932+)
  - "Resultados do Carnaval de São Paulo em {ano}" (1969+)

e reescreve, com dados reais:
  - data/colocacoes_historico.csv
  - data/sambas_enredo_historico.csv

Convenções:
  - HTML cacheado em data/cache/wikipedia/ (re-run não re-busca).
  - Nomes de escolas que não casam com as 39 da base vão para
    data/cache/unmatched_names.log (revisão manual).
  - pontos ausentes na fonte ficam vazios — nunca placeholder.
"""

import csv
import json
import re
import time
import unicodedata
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
DATA = ROOT / "data"
CACHE = DATA / "cache" / "wikipedia"
CACHE.mkdir(parents=True, exist_ok=True)

ESCOLAS_CSV = DATA / "escolas_de_samba.csv"
OUT_COLOCACOES = DATA / "colocacoes_historico.csv"
OUT_SAMBAS = DATA / "sambas_enredo_historico.csv"
UNMATCHED_LOG = DATA / "cache" / "unmatched_names.log"

UA = {"User-Agent": "brasil-com-s-api data bot (https://github.com/Brasil-com-S/brasil-com-s.github.io)"}

RJ_FIRST_YEAR, SP_FIRST_YEAR, LAST_YEAR = 1932, 1969, 2026

# ---------------------------------------------------------------------------
# Escolas e aliases
# ---------------------------------------------------------------------------

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\(.*?\)", " ", s)          # remove parênteses
    s = re.sub(r"\[.*?\]", " ", s)          # remove refs [1]
    s = s.lower().replace("*", " ").replace("†", " ")
    s = re.sub(r"[-–—]", " ", s)            # hífens separam palavras
    return re.sub(r"\s+", " ", s).strip()


def load_escolas():
    with ESCOLAS_CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


# Aliases históricos (normalizados) -> slug. Nomes canônicos são adicionados
# automaticamente a partir do CSV.
EXTRA_ALIASES = {
    "vai como pode": "portela",
    "conjunto carnavalesco osvaldo cruz": "portela",
    "conjunto osvaldo cruz": "portela",
    "quem nos faz e o capricho": "portela",
    "estacao primeira": "mangueira",
    "beija flor": "beija-flor",
    "imperatriz": "imperatriz",
    "grande rio": "grande-rio",
    "vila isabel": "vila-isabel",
    "mocidade": "mocidade-independente",          # RJ; SP usa "mocidade alegre"
    "mocidade independente": "mocidade-independente",
    "tuiuti": "paraiso-do-tuiuti",
    "uniao da ilha": "uniao-da-ilha",
    "inocentes": "inocentes-de-belford-roxo",
    "vigario geral": "academicos-de-vigario-geral",
    "uniao de marica": "uniao-de-marica",
    "estacio de sa": "estacio-de-sa",
    "barroca": "barroca-zona-sul",
    "vai vai": "vai-vai",
    "gavioes da fiel": "gavioes-da-fiel",
    "dragoes da real": "dragoes-da-real",
    "imperio de casa verde": "imperio-de-casa-verde",
    "academicos do tatuape": "academicos-do-tatuape",
    "mancha verde": "mancha-verde",
    "aguia de ouro": "aguia-de-ouro",
    "academicos do tucuruvi": "academicos-do-tucuruvi",
    "rosas de ouro": "rosas-de-ouro",
    "camisa verde e branco": "camisa-verde-e-branco",
    "tom maior": "tom-maior",
    "estrela do terceiro milenio": "estrela-do-terceiro-milenio",
    "nene de vila matilde": "nene-de-vila-matilde",
    "colorado do bras": "colorado-do-bras",
    "perola negra": "perola-negra",
    "unidos do peruche": "unidos-do-peruche",
    "x 9 paulistana": "x-9-paulistana",
    "x9 paulistana": "x-9-paulistana",
}


def build_alias_map(escolas):
    amap = {}
    for e in escolas:
        amap[norm(e["nome"])] = e["slug"]
        amap[norm(e["slug"].replace("-", " "))] = e["slug"]
    for alias, slug in EXTRA_ALIASES.items():
        amap[norm(alias)] = slug
    return amap


# ---------------------------------------------------------------------------
# Fetch com cache
# ---------------------------------------------------------------------------

def fetch_html(title: str) -> str | None:
    safe = re.sub(r"[^\w]+", "_", title)
    path = CACHE / f"{safe}.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    time.sleep(1.0)
    r = requests.get(
        "https://pt.wikipedia.org/w/api.php",
        params={"action": "parse", "page": title, "prop": "text",
                "format": "json", "redirects": 1},
        headers=UA, timeout=30,
    )
    j = r.json()
    if "error" in j:
        return None
    html = j["parse"]["text"]["*"]
    path.write_text(html, encoding="utf-8")
    return html


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

IGNORE_HEADINGS = {
    "classificacao", "notas", "quesitos e julgadores", "julgadores",
    "premiacoes", "desfile das campeas", "ver tambem", "referencias",
    "notas e referencias", "ligacoes externas", "bibliografia", "galeria",
    "ordem dos desfiles", "enredo", "samba enredo",
}

CAMPEAS_PAGES = {
    "RJ": "Lista de campeãs do carnaval do Rio de Janeiro",
    "SP": "Lista de campeãs do carnaval de São Paulo",
}


def clean_cell(cell) -> str:
    txt = cell.get_text(" ", strip=True)
    txt = re.sub(r"\[\d+\]|\[[a-z]\]", "", txt)
    return re.sub(r"\s+", " ", txt).strip()


def parse_year_page(html: str, estado: str, alias_map, escolas_by_slug, unmatched):
    """Extrai linhas de classificação de uma página de resultados."""
    soup = BeautifulSoup(html, "lxml")
    rows_out = []
    current_group = None

    for el in soup.find_all(["h2", "h3", "h4", "table"]):
        if el.name in ("h2", "h3", "h4"):
            htxt = norm(el.get_text(" ", strip=True))
            if htxt and htxt not in IGNORE_HEADINGS:
                current_group = el.get_text(" ", strip=True)
                current_group = re.sub(r"\[.*?\]", "", current_group).strip()
            continue

        # table
        rows = el.find_all("tr")
        if not rows:
            continue
        header = [clean_cell(c).lower() for c in rows[0].find_all(["th", "td"])]
        joined = " ".join(header)
        if not re.search(r"\bcol\.?\b|\bpos\.?\b", joined) or "escola" not in joined:
            continue

        def col(*names):
            for n in names:
                for i, h in enumerate(header):
                    if h.startswith(n):
                        return i
            return None

        i_pos = col("col", "pos")
        i_esc = col("escola")
        i_enr = col("enredo", "samba-enredo", "samba")
        i_pts = col("pontos", "total")
        if i_pos is None or i_esc is None:
            continue

        for tr in rows[1:]:
            cells = tr.find_all(["td", "th"])
            if len(cells) <= max(i_pos, i_esc):
                continue
            pos_txt = clean_cell(cells[i_pos])
            m = re.match(r"^(\d+)", pos_txt)
            if not m:
                continue
            pos = int(m.group(1))
            nome_raw = clean_cell(cells[i_esc])
            slug = alias_map.get(norm(nome_raw))
            if not slug:
                unmatched.add(f"{estado}|{current_group}|{nome_raw}")
                continue
            esc = escolas_by_slug[slug]
            enredo = clean_cell(cells[i_enr]) if i_enr is not None and i_enr < len(cells) else ""
            enredo = re.sub(r"\(reedi[çc][ãa]o.*?\)", "", enredo, flags=re.I).strip()
            pts = ""
            if i_pts is not None and i_pts < len(cells):
                pts_raw = clean_cell(cells[i_pts])
                pts_raw = pts_raw.replace(".", "").replace(",", ".") if re.match(r"^\d{1,3}(\.\d{3})*(,\d+)?$", pts_raw) else pts_raw.replace(",", ".")
                if re.match(r"^\d+(\.\d+)?$", pts_raw):
                    pts = pts_raw
            grupo = current_group or "Grupo Principal"
            rows_out.append({
                "escola_slug": slug,
                "escola_nome": esc["nome"],
                "estado": estado,
                "grupo": grupo,
                "posicao": pos,
                "pontos": pts,
                "enredo": enredo,
            })
    return rows_out


def parse_campeas(html: str, estado: str, alias_map, unmatched):
    """Extrai {slug: {anos}} da tabela-resumo '# | Escola | Títulos | Anos'.

    As linhas têm células extras vazias (imagens de brasão), então a
    identificação é por conteúdo: o nome casa com o alias map, os anos são
    todos os \\d{4} da linha. Entre várias tabelas candidatas, vale a que
    tiver mais linhas (histórico completo, não recorte de era).
    """
    soup = BeautifulSoup(html, "lxml")
    candidatas = []
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if len(rows) < 5:
            continue
        header = [norm(c.get_text(" ", strip=True))
                  for c in rows[0].find_all(["th", "td"])]
        if header and header[0] == "#" and any("anos" == h for h in header):
            candidatas.append(table)
    if not candidatas:
        return {}
    table = max(candidatas, key=lambda t: len(t.find_all("tr")))

    titulos = {}
    for tr in table.find_all("tr")[1:]:
        texts = [clean_cell(c) for c in tr.find_all(["td", "th"])]
        slug = next((alias_map[norm(t)] for t in texts if norm(t) in alias_map),
                    None)
        anos = {int(y) for t in texts for y in re.findall(r"\b(19\d{2}|20\d{2})\b", t)}
        if not slug:
            nome = max(texts, key=len) if texts else ""
            if anos:
                unmatched.add(f"{estado}|campeas|{nome}")
            continue
        titulos.setdefault(slug, set()).update(anos)
    # extrai também o número oficial de títulos (célula inteira isolada),
    # pois pode diferir de len(anos) — ex.: Mangueira conta 1984 duas vezes
    # (campeã e supercampeã) => 20 títulos em 19 anos.
    titulos_count = {}
    for tr in table.find_all("tr")[1:]:
        texts = [clean_cell(c) for c in tr.find_all(["td", "th"])]
        slug = next((alias_map[norm(t)] for t in texts if norm(t) in alias_map),
                    None)
        if not slug:
            continue
        ints = [int(t) for t in texts
                if re.fullmatch(r"\d+", t) and not (1900 <= int(t) <= 2099)]
        if ints:
            titulos_count[slug] = ints[-1]
    return titulos, titulos_count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# Enredos/compositores que a página de resultados do ano não traz,
# documentados no artigo da própria escola.
# (slug, ano) -> (enredo, compositores, interpretacao)
MANUAL_ENREDOS = {
    # Fonte: artigo "Barroca Zona Sul", tabela de segmentos históricos
    # (enredo+compositores) e tabela "Intérpretes" (2014: Tito Amorim).
    ("barroca-zona-sul", 2014): (
        "Em um canto de fé e devoção, Barroca celebra as religiões nos seus 40 anos de samba e tradição",
        "Imperial, J. Jorge, Juninho Berim, Rafa Do Cavaco e Thiago de Xangô",
        "Tito Amorim"),
}


def main():
    escolas = load_escolas()
    by_slug = {e["slug"]: e for e in escolas}
    alias_map = build_alias_map(escolas)
    unmatched = set()
    all_rows = []          # (ano, row)
    missing_pages = []

    jobs = [("RJ", y, f"Resultados do Carnaval do Rio de Janeiro em {y}")
            for y in range(RJ_FIRST_YEAR, LAST_YEAR + 1)]
    jobs += [("SP", y, f"Resultados do Carnaval de São Paulo em {y}")
             for y in range(SP_FIRST_YEAR, LAST_YEAR + 1)]

    for estado, year, title in jobs:
        html = fetch_html(title)
        if html is None:
            missing_pages.append(title)
            continue
        rows = parse_year_page(html, estado, alias_map, by_slug, unmatched)
        for r in rows:
            r["ano"] = year
        all_rows.extend(rows)
        print(f"{estado} {year}: {len(rows)} linhas")

    # ---- dedup por (slug, ano): mantém a 1ª ocorrência (evento principal) ----
    seen, deduped, dropped = set(), [], []
    for r in all_rows:
        key = (r["escola_slug"], r["ano"])
        if key in seen:
            dropped.append(f"{r['escola_slug']}|{r['ano']}|{r['grupo']}")
            continue
        seen.add(key)
        deduped.append(r)
    all_rows = deduped
    if dropped:
        print(f"duplicatas (slug,ano) descartadas: {len(dropped)}")

    # ---- correções pontuais documentadas ----
    # 2017: LIESA dividiu o título entre Portela e Mocidade após recurso;
    # a tabela de classificação lista a Mocidade sem número de posição,
    # então o parser a ignora. Fonte: página de resultados RJ 2017.
    by_key = {(r["escola_slug"], r["ano"]) for r in all_rows}
    if ("mocidade-independente", 2017) not in by_key:
        all_rows.append({
            "escola_slug": "mocidade-independente",
            "escola_nome": by_slug["mocidade-independente"]["nome"],
            "ano": 2017, "estado": "RJ", "grupo": "Grupo Especial",
            "posicao": 1, "pontos": "269.8",
            "enredo": "As Mil e Uma Noites de Uma Mocidade Pra Lá de Marrakesh",
        })

    # ---- colocacoes_historico.csv ----
    all_rows.sort(key=lambda r: (r["escola_slug"], r["ano"]))
    with OUT_COLOCACOES.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola_slug", "escola_nome", "ano", "estado", "grupo",
                    "posicao", "pontos", "resultado"])
        for r in all_rows:
            resultado = "Campeã" if r["posicao"] == 1 else f"{r['posicao']}º Lugar"
            w.writerow([r["escola_slug"], r["escola_nome"], r["ano"], r["estado"],
                        r["grupo"], r["posicao"], r["pontos"], resultado])

    # ---- enredos manuais documentados ----
    for (slug, ano), (enredo, comp, interp) in MANUAL_ENREDOS.items():
        row = next((r for r in all_rows
                    if r["escola_slug"] == slug and r["ano"] == ano), None)
        if row is not None and not row["enredo"]:
            row["enredo"] = enredo
            row["compositores"] = comp
            row["interpretacao"] = interp

    # ---- sambas_enredo_historico.csv ----
    with OUT_SAMBAS.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola_slug", "escola_nome", "ano", "estado", "grupo",
                    "titulo_samba", "compositores", "interpretacao"])
        for r in all_rows:
            if r["enredo"]:
                w.writerow([r["escola_slug"], r["escola_nome"], r["ano"],
                            r["estado"], r["grupo"], r["enredo"],
                            r.get("compositores", ""), r.get("interpretacao", "")])

    # ---- títulos: listas oficiais de campeãs (tabela-resumo por escola) ----
    titulos, titulos_count = {}, {}
    for estado, page in CAMPEAS_PAGES.items():
        html = fetch_html(page)
        if html is None:
            print(f"AVISO: página de campeãs ausente: {page}")
            continue
        t_anos, t_count = parse_campeas(html, estado, alias_map, unmatched)
        for slug, anos in t_anos.items():
            titulos.setdefault(slug, set()).update(anos)
        titulos_count.update(t_count)
    titulos = {s: sorted(a) for s, a in titulos.items()}
    (DATA / "cache" / "titulos_derivados.json").write_text(
        json.dumps({"anos": titulos, "titulos_oficiais": titulos_count},
                   indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- correções pontuais documentadas ----
    # (aplicadas antes da escrita dos CSVs; ver bloco acima)

    UNMATCHED_LOG.write_text("\n".join(sorted(unmatched)) + "\n", encoding="utf-8")

    print("\n== Resumo ==")
    print(f"linhas de classificação: {len(all_rows)}")
    print(f"escolas com dados: {len({r['escola_slug'] for r in all_rows})}/39")
    print(f"páginas inexistentes: {len(missing_pages)} -> {missing_pages[:10]}")
    print(f"nomes não reconhecidos: {len(unmatched)} (ver {UNMATCHED_LOG})")
    for slug, anos in sorted(titulos.items()):
        print(f"  títulos {slug}: {len(anos)} {sorted(anos)}")


if __name__ == "__main__":
    main()
