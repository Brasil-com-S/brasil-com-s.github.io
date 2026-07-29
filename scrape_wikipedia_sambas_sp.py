#!/usr/bin/env python3
"""
scrape_wikipedia_sambas_sp.py

Extrai compositores dos sambas-enredo das escolas de SP a partir das tabelas
de "segmentos históricos" dos artigos das escolas na Wikipédia (linhas
"ANO | Colocação | Grupo | Enredo <small>Compositores: ...</small>").

Faz merge em data/sambas_enredo_historico.csv: preenche `compositores`
vazios e cria linhas de anos cobertos pelo artigo que faltem no CSV
(a escola precisa ter colocação registrada naquele ano — a colocação é a
prova de que ela desfilou).

Intérprete NÃO é extraído dessas tabelas: a última coluna é ambígua
(carnavalesco em várias escolas). Intérpretes de SP ficam vazios, exceto
onde documentados pontualmente (ver MANUAL_ENREDOS em
scrape_wikipedia_resultados.py e os enredos 2027 da LigaSP).

Rode DEPOIS de scrape_wikipedia_resultados.py e scrape_galeria_sambas.py.
"""

import csv
import re
import time
from pathlib import Path

import requests

ROOT = Path(__file__).parent
DATA = ROOT / "data"
CACHE = DATA / "cache" / "wikipedia" / "escolas_wiki"
CACHE.mkdir(parents=True, exist_ok=True)

SAMBAS_CSV = DATA / "sambas_enredo_historico.csv"
COLOCACOES_CSV = DATA / "colocacoes_historico.csv"

UA = {"User-Agent": "brasil-com-s-api data bot (https://github.com/Brasil-com-S/brasil-com-s.github.io)"}

SP_ARTICLES = {
    "vai-vai": "Vai-Vai",
    "mocidade-alegre": "Mocidade Alegre",
    "gavioes-da-fiel": "Gaviões da Fiel",
    "dragoes-da-real": "Dragões da Real (escola de samba)",
    "imperio-de-casa-verde": "Império de Casa Verde",
    "academicos-do-tatuape": "Acadêmicos do Tatuapé",
    "mancha-verde": "Mancha Verde",
    "barroca-zona-sul": "Barroca Zona Sul",
    "aguia-de-ouro": "Águia de Ouro",
    "academicos-do-tucuruvi": "Acadêmicos do Tucuruvi",
    "rosas-de-ouro": "Rosas de Ouro",
    "camisa-verde-e-branco": "Camisa Verde e Branco",
    "tom-maior": "Tom Maior",
    "estrela-do-terceiro-milenio": "Estrela do Terceiro Milênio",
    "nene-de-vila-matilde": "Nenê de Vila Matilde",
    "colorado-do-bras": "Colorado do Brás",
    "perola-negra": "Pérola Negra (escola de samba)",
    "unidos-do-peruche": "Unidos do Peruche",
    "x-9-paulistana": "X-9 Paulistana",
}


def fetch_full_wikitext(title: str) -> str:
    safe = re.sub(r"[^\w]+", "_", title)
    path = CACHE / f"{safe}.full.wiki"
    if path.exists():
        return path.read_text(encoding="utf-8")
    time.sleep(1.0)
    r = requests.get(
        "https://pt.wikipedia.org/w/api.php",
        params={"action": "parse", "page": title, "prop": "wikitext",
                "format": "json", "redirects": 1},
        headers=UA, timeout=30,
    )
    j = r.json()
    wt = j["parse"]["wikitext"]["*"] if "parse" in j else ""
    path.write_text(wt, encoding="utf-8")
    return wt


def clean(s: str) -> str:
    s = re.sub(r"\[\[([^]|]*)\|([^]]*)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^]]*)\]\]", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", s).strip(" ;,.")


def parse_segmentos(wt: str):
    """Extrai {ano: (enredo, compositores)} das linhas com 'Compositores:'."""
    out = {}
    for row in re.split(r"\n\|-", wt):
        if "ompositores" not in row:
            continue
        # remove wikilinks ANTES de tudo: o '|' interno do link quebraria
        # tanto o split da célula quanto o limite da regex de compositores
        row = re.sub(r"\[\[([^]|]*)\|([^]]*)\]\]", r"\2", row)
        row = re.sub(r"\[\[([^]]*)\]\]", r"\1", row)
        # junta <small> adjacentes (há nomes quebrados ao meio no wikitext,
        # ex.: "Na</small><small>io Denay")
        row = re.sub(r"</small>\s*<small[^>]*>", "", row)
        ym = re.search(r"!+\s*'*(\d{4})'*\s*\n", row)
        if not ym:
            continue
        ano = int(ym.group(1))
        m = re.search(r"!(.*?)[Cc]ompositores:\s*(.*?)(?:\||</small>|\n!|\Z)",
                      row, flags=re.S)
        if not m:
            continue
        # a célula do enredo é a última antes de "Compositores:"
        enredo = clean(re.split(r"[|!]", m.group(1))[-1])
        comp = clean(m.group(2))
        if enredo and len(enredo) >= 4:
            out[ano] = (enredo, comp)
    return out


def main():
    sambas = list(csv.DictReader(SAMBAS_CSV.open(encoding="utf-8")))
    colocacoes = list(csv.DictReader(COLOCACOES_CSV.open(encoding="utf-8")))
    escola_nome = {r["escola_slug"]: r["escola_nome"] for r in colocacoes}
    grupo_by_key = {(r["escola_slug"], r["ano"]): r["grupo"] for r in colocacoes}
    desfilou = set(grupo_by_key)
    by_key = {(r["escola_slug"], r["ano"]): r for r in sambas}

    stats = {"comp": 0, "novos": 0}
    for slug, title in SP_ARTICLES.items():
        wt = fetch_full_wikitext(title)
        if not wt:
            print(f"{slug}: artigo indisponível ({title})")
            continue
        seg = parse_segmentos(wt)
        for ano, (enredo, comp) in seg.items():
            key = (slug, str(ano))
            if key not in desfilou:
                continue  # sem colocação registrada -> não entra na base
            row = by_key.get(key)
            if row is None:
                row = {"escola_slug": slug,
                       "escola_nome": escola_nome.get(slug, slug),
                       "ano": str(ano), "estado": "SP",
                       "grupo": grupo_by_key.get(key, ""),
                       "titulo_samba": enredo,
                       "compositores": comp, "interpretacao": ""}
                sambas.append(row)
                by_key[key] = row
                stats["novos"] += 1
            else:
                if not row["titulo_samba"] and enredo:
                    row["titulo_samba"] = enredo
                if not row["compositores"] and comp:
                    row["compositores"] = comp
                    stats["comp"] += 1
        print(f"{slug}: {len(seg)} anos com compositores no artigo")

    sambas.sort(key=lambda r: (r["escola_slug"], int(r["ano"])))
    with SAMBAS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["escola_slug", "escola_nome", "ano",
                                          "estado", "grupo", "titulo_samba",
                                          "compositores", "interpretacao"])
        w.writeheader()
        w.writerows(sambas)

    sp = [r for r in sambas if r["estado"] == "SP"]
    print("\n== Resumo ==")
    print(f"linhas SP: {len(sp)} | com compositores: "
          f"{sum(1 for r in sp if r['compositores'])}")
    print(f"compositores preenchidos: {stats['comp']} | novos anos: {stats['novos']}")


if __name__ == "__main__":
    main()
