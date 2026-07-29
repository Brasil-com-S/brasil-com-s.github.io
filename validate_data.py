#!/usr/bin/env python3
"""
validate_data.py

Checagens de integridade da base (data/*.csv) e da API compilada (api/v1).
Roda depois de build_api_from_csv.py. Sai com código 1 se algo falhar.
"""

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
API = ROOT / "api" / "v1"

erros, avisos = [], []


def check(cond, msg):
    if not cond:
        erros.append(msg)


def main():
    escolas = list(csv.DictReader((DATA / "escolas_de_samba.csv").open(encoding="utf-8")))
    colocacoes = list(csv.DictReader((DATA / "colocacoes_historico.csv").open(encoding="utf-8")))
    sambas = list(csv.DictReader((DATA / "sambas_enredo_historico.csv").open(encoding="utf-8")))
    by_slug = {e["slug"]: e for e in escolas}

    # ---- escolas ----
    check(len(escolas) == 39, f"esperadas 39 escolas, há {len(escolas)}")
    check(len(by_slug) == len(escolas), "slugs duplicados")
    for e in escolas:
        for campo in ("nome", "nome_completo", "fundacao", "cores", "bairro",
                      "grupo", "cidade", "estado"):
            check(bool(e[campo].strip()), f"{e['slug']}: campo vazio: {campo}")
        check(re.match(r"^\d{4}(-\d{2}-\d{2})?$", e["fundacao"]) is not None,
              f"{e['slug']}: fundacao fora do padrão ISO: {e['fundacao']}")
        titulos = int(e["titulos"])
        anos = [int(a) for a in e["anos_titulos"].split(";") if a.strip()]
        check(titulos == len(anos) or titulos == len(anos) + 1,
              f"{e['slug']}: titulos={titulos} mas {len(anos)} anos")
        check(len(e["cores"].split(";")) == len(e["cores_hex"].split(";"))
              or not e["cores_hex"].strip(),
              f"{e['slug']}: cores e cores_hex em quantidades diferentes")
        logo = ROOT / e["logo_original_url"]
        check(logo.exists(), f"{e['slug']}: logo ausente em disco: {logo}")

    # ---- colocações ----
    com_colocacao = set()
    for r in colocacoes:
        check(r["escola_slug"] in by_slug, f"colocação de escola desconhecida: {r['escola_slug']}")
        pos = int(r["posicao"])
        check(pos > 0, f"{r['escola_slug']} {r['ano']}: posicao inválida")
        if r["pontos"]:
            check(re.match(r"^\d+(\.\d+)?$", r["pontos"]) is not None,
                  f"{r['escola_slug']} {r['ano']}: pontos inválidos: {r['pontos']}")
            check(float(r["pontos"]) != 10.0 or int(r["ano"]) < 1940,
                  f"{r['escola_slug']} {r['ano']}: pontos suspeitos de placeholder (10.0)")
        com_colocacao.add(r["escola_slug"])
    for slug in by_slug:
        check(slug in com_colocacao, f"{slug}: nenhuma colocação registrada")

    # ---- sambas ----
    for r in sambas:
        check(bool(r["titulo_samba"].strip()),
              f"{r['escola_slug']} {r['ano']}: titulo_samba vazio")

    # ---- spot-checks de fatos conhecidos (fontes oficiais) ----
    m = by_slug["mangueira"]
    check(int(m["titulos"]) == 20, "Mangueira deveria ter 20 títulos")
    check("1932" in m["anos_titulos"] and "2019" in m["anos_titulos"],
          "anos de título da Mangueira incorretos")
    check(m["fundacao"] == "1928-04-28", "fundação da Mangueira incorreta")
    check(int(by_slug["portela"]["titulos"]) == 22, "Portela deveria ter 22 títulos")
    check(int(by_slug["vai-vai"]["titulos"]) == 15, "Vai-Vai deveria ter 15 títulos")

    vir2024 = [r for r in colocacoes if r["escola_slug"] == "viradouro" and r["ano"] == "2024"]
    check(vir2024 and vir2024[0]["posicao"] == "1" and vir2024[0]["pontos"] == "270",
          "Viradouro 2024: campeã com 270 pontos")
    moc2017 = [r for r in colocacoes if r["escola_slug"] == "mocidade-independente" and r["ano"] == "2017"]
    check(moc2017 and moc2017[0]["posicao"] == "1",
          "Mocidade 2017: co-campeã (título dividido com a Portela)")

    # ---- API compilada ----
    api_escolas = json.load((API / "escolas.json").open(encoding="utf-8"))
    check(len(api_escolas["escolas"]) == 39, "api/v1/escolas.json: total != 39")
    for e in api_escolas["escolas"]:
        if not e["colocacoes"]:
            avisos.append(f"API {e['slug']}: colocacoes vazias")
        check((API / "escolas" / f"{e['slug']}.json").exists(),
              f"API: endpoint individual ausente: {e['slug']}.json")
    carn_index = json.load((API / "carnavais.json").open(encoding="utf-8"))
    for ano in carn_index["anos_disponiveis"]:
        check((API / "carnavais" / f"{ano}.json").exists(),
              f"API: carnavais/{ano}.json anunciado mas ausente")

    # ---- relatório ----
    for a in avisos:
        print("AVISO:", a)
    if erros:
        print(f"\n❌ {len(erros)} erro(s):")
        for e in erros:
            print("  -", e)
        sys.exit(1)
    print(f"✅ Validação OK: {len(escolas)} escolas, {len(colocacoes)} colocações, "
          f"{len(sambas)} sambas, {len(carn_index['anos_disponiveis'])} anos de carnaval.")


if __name__ == "__main__":
    main()
