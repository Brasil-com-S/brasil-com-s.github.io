#!/usr/bin/env python3
"""
scrape_galeria_sambas.py

Complementa data/sambas_enredo_historico.csv com dados da Galeria do Samba
(fonte de referência do carnaval carioca — RJ):

  - compositores e intérprete de cada samba-enredo (seção "SAMBA DE ENREDO"
    das páginas /escolas-de-samba/{escola}/{ano}/)
  - títulos de enredo de anos que a Wikipédia não cobriu (a Galeria tem
    páginas por ano para todos os desfiles da escola, inclusive grupos
    de acesso antigos)

Fluxo: para cada escola do RJ, lê o índice /carnavais/ (anos disponíveis),
baixa cada página de ano (cache em data/cache/galeria/) e faz merge no CSV
sem nunca apagar dados existentes — só preenche vazios e adiciona anos novos.
"""

import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
DATA = ROOT / "data"
CACHE = DATA / "cache" / "galeria"
CACHE.mkdir(parents=True, exist_ok=True)

SAMBAS_CSV = DATA / "sambas_enredo_historico.csv"
COLOCACOES_CSV = DATA / "colocacoes_historico.csv"

UA = {"User-Agent": "brasil-com-s-api data bot (https://github.com/Brasil-com-S/brasil-com-s.github.io)"}
BASE = "https://galeriadosamba.com.br/escolas-de-samba"

# slug nosso -> slug na Galeria do Samba (20 escolas do RJ)
GALERIA_SLUGS = {
    "mangueira": "estacao-primeira-de-mangueira",
    "portela": "portela",
    "beija-flor": "beija-flor-de-nilopolis",
    "salgueiro": "academicos-do-salgueiro",
    "viradouro": "unidos-do-viradouro",
    "imperatriz": "imperatriz-leopoldinense",
    "grande-rio": "academicos-do-grande-rio",
    "vila-isabel": "unidos-de-vila-isabel",
    "mocidade-independente": "mocidade-independente-de-padre-miguel",
    "paraiso-do-tuiuti": "paraiso-do-tuiuti",
    "unidos-de-padre-miguel": "unidos-de-padre-miguel",
    "estacio-de-sa": "estacio-de-sa",
    "imperio-serrano": "imperio-serrano",
    "uniao-da-ilha": "uniao-da-ilha-do-governador",
    "sao-clemente": "sao-clemente",
    "inocentes-de-belford-roxo": "inocentes-de-belford-roxo",
    "academicos-de-niteroi": "academicos-de-niteroi",
    "unidos-de-bangu": "unidos-de-bangu",
    "uniao-de-marica": "uniao-de-marica",
    "academicos-de-vigario-geral": "academicos-de-vigario-geral",
}

LIXO = {"publicidade", "", "compositores", "intérprete", "interprete"}


def fetch(url: str) -> str | None:
    safe = re.sub(r"[^\w]+", "_", url)
    path = CACHE / f"{safe}.html"
    if path.exists():
        txt = path.read_text(encoding="utf-8")
        return txt or None
    time.sleep(1.0)
    r = requests.get(url, headers=UA, timeout=30)
    if r.status_code != 200:
        path.write_text("", encoding="utf-8")
        return None
    # o site não envia charset; sem isto o requests assume ISO-8859-1 (mojibake)
    html = r.content.decode("utf-8", errors="replace")
    path.write_text(html, encoding="utf-8")
    return html


def parse_year_page(html: str):
    """Extrai (enredo, compositores, intérprete) da página de um ano."""
    txt = BeautifulSoup(html, "lxml").get_text("\n", strip=True)

    enredo = ""
    m = re.search(r"\nenredo\n([^\n]{3,200})\n", txt)
    if m:
        enredo = m.group(1).strip()

    comp, interp = "", ""
    i = txt.find("SAMBA DE ENREDO")
    if i != -1:
        seg = txt[i:i + 800]
        m = re.search(r"compositores\n([^\n]+)", seg)
        if m and m.group(1).strip().lower() not in LIXO:
            comp = m.group(1).strip()
        m = re.search(r"int[ée]rprete\n([^\n]+)", seg)
        if m and m.group(1).strip().lower() not in LIXO:
            interp = m.group(1).strip()
    return enredo, comp, interp


def main():
    sambas = list(csv.DictReader(SAMBAS_CSV.open(encoding="utf-8")))
    colocacoes = list(csv.DictReader(COLOCACOES_CSV.open(encoding="utf-8")))
    escola_nome = {r["escola_slug"]: r["escola_nome"] for r in colocacoes}
    grupo_by_key = {(r["escola_slug"], r["ano"]): r["grupo"] for r in colocacoes}
    by_key = {(r["escola_slug"], r["ano"]): r for r in sambas}

    stats = {"comp": 0, "interp": 0, "novos": 0, "sem_pagina": 0}
    for slug, gslug in GALERIA_SLUGS.items():
        index = fetch(f"{BASE}/{gslug}/carnavais/")
        if not index:
            print(f"{slug}: índice indisponível")
            continue
        anos = sorted({int(a) for a in
                       re.findall(rf"{gslug}/(\d{{4}})/", index)})
        for ano in anos:
            key = (slug, str(ano))
            row = by_key.get(key)
            # só busca a página se há algo a ganhar
            if row and row["titulo_samba"] and row["compositores"] and row["interpretacao"]:
                continue
            html = fetch(f"{BASE}/{gslug}/{ano}/")
            if html is None:
                stats["sem_pagina"] += 1
                continue
            enredo, comp, interp = parse_year_page(html)
            if row is None and enredo:
                row = {"escola_slug": slug,
                       "escola_nome": escola_nome.get(slug, slug),
                       "ano": str(ano), "estado": "RJ",
                       "grupo": grupo_by_key.get(key, ""),
                       "titulo_samba": enredo,
                       "compositores": "", "interpretacao": ""}
                sambas.append(row)
                by_key[key] = row
                stats["novos"] += 1
            if row:
                if not row["titulo_samba"] and enredo:
                    row["titulo_samba"] = enredo
                if not row["compositores"] and comp:
                    row["compositores"] = comp
                    stats["comp"] += 1
                if not row["interpretacao"] and interp:
                    row["interpretacao"] = interp
                    stats["interp"] += 1
        print(f"{slug}: {len(anos)} anos na Galeria")

    sambas.sort(key=lambda r: (r["escola_slug"], int(r["ano"])))
    with SAMBAS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["escola_slug", "escola_nome", "ano",
                                          "estado", "grupo", "titulo_samba",
                                          "compositores", "interpretacao"])
        w.writeheader()
        w.writerows(sambas)

    rj = [r for r in sambas if r["estado"] == "RJ"]
    com_comp = sum(1 for r in rj if r["compositores"])
    com_interp = sum(1 for r in rj if r["interpretacao"])
    print("\n== Resumo ==")
    print(f"linhas RJ: {len(rj)} | com compositores: {com_comp} | "
          f"com intérprete: {com_interp}")
    print(f"novos anos adicionados: {stats['novos']} | "
          f"páginas de ano ausentes: {stats['sem_pagina']}")


if __name__ == "__main__":
    main()
