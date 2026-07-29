import os
import csv
import json

# Single Source of Truth Builder Script
# Reads the CSVs in data/ (fonte da verdade, dados raspados de fontes
# oficiais — ver README) e compila todos os endpoints /api/v1/.

ESCOLAS_CSV = "data/escolas_de_samba.csv"
COLOCACOES_CSV = "data/colocacoes_historico.csv"
SAMBAS_CSV = "data/sambas_enredo_historico.csv"
ENREDOS_2027_CSV = "data/sambas_e_colocacoes.csv"

def parse_list(val, sep=";"):
    if not val:
        return []
    return [x.strip() for x in val.split(sep) if x.strip()]

def parse_int_list(val, sep=";"):
    if not val:
        return []
    res = []
    for x in val.split(sep):
        x = x.strip()
        if x.isdigit():
            res.append(int(x))
    return res

def build_api():
    print("🔄 Compilando a API a partir dos arquivos CSV (Fonte da Verdade)...")

    if not os.path.exists(ESCOLAS_CSV):
        print(f"❌ Arquivo {ESCOLAS_CSV} não encontrado.")
        return

    # ---- Sambas-enredo históricos (Wikipedia: páginas de resultados) ----
    sambas_by_slug = {}
    enredo_by_key = {}
    if os.path.exists(SAMBAS_CSV):
        with open(SAMBAS_CSV, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not row.get("titulo_samba"):
                    continue
                slug, ano = row["escola_slug"], int(row["ano"])
                sambas_by_slug.setdefault(slug, []).append({
                    "ano": ano,
                    "titulo": row["titulo_samba"],
                    "compositores": row["compositores"],
                    "interpretacao": row["interpretacao"],
                })
                enredo_by_key[(slug, ano)] = row["titulo_samba"]

    # ---- Enredos 2027 anunciados (LigaSP) ----
    if os.path.exists(ENREDOS_2027_CSV):
        with open(ENREDOS_2027_CSV, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("tipo_registro") == "enredo" and row.get("titulo_samba"):
                    slug, ano = row["escola_slug"], int(row["ano"])
                    if (slug, ano) not in enredo_by_key:
                        sambas_by_slug.setdefault(slug, []).append({
                            "ano": ano,
                            "titulo": row["titulo_samba"],
                            "compositores": row["compositores"],
                            "interpretacao": row["interpretacao"],
                        })
                        enredo_by_key[(slug, ano)] = row["titulo_samba"]

    # ---- Colocações históricas (Wikipedia: páginas de resultados) ----
    colocacoes_by_slug = {}
    colocacoes_by_ano = {}
    if os.path.exists(COLOCACOES_CSV):
        with open(COLOCACOES_CSV, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not row.get("posicao"):
                    continue
                slug, ano = row["escola_slug"], int(row["ano"])
                entry = {
                    "ano": ano,
                    "grupo": row["grupo"],
                    "posicao": int(row["posicao"]),
                    "pontos": float(row["pontos"]) if row.get("pontos") else None,
                    "resultado": row.get("resultado") or f"{row['posicao']}º Lugar",
                }
                colocacoes_by_slug.setdefault(slug, []).append(entry)
                colocacoes_by_ano.setdefault(ano, []).append({
                    "estado": row["estado"],
                    "grupo": row["grupo"],
                    "posicao": int(row["posicao"]),
                    "escola_slug": slug,
                    "escola_nome": row["escola_nome"],
                    "pontos": float(row["pontos"]) if row.get("pontos") else None,
                    "enredo": enredo_by_key.get((slug, ano), ""),
                })

    # ---- Escolas (master) ----
    escolas = []
    with open(ESCOLAS_CSV, mode="r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            slug = row["slug"]
            logo = row.get("logo_original_url") or f"assets/logos/original/{slug}.png"
            escolas.append({
                "id": row["id"],
                "slug": slug,
                "nome": row["nome"],
                "nome_completo": row["nome_completo"],
                "fundacao": row["fundacao"],
                "fundadores": parse_list(row["fundadores"]),
                "estado": row["estado"],
                "cidade": row["cidade"],
                "bairro": row["bairro"],
                "grupo": row["grupo"],
                "cores": parse_list(row["cores"]),
                "cores_hex": parse_list(row["cores_hex"]),
                "simbolo": row["simbolo"],
                "titulos": int(row["titulos"]) if row["titulos"] else 0,
                "anos_titulos": parse_int_list(row["anos_titulos"]),
                "logo_url": logo,
                "logo_original_url": logo,
                "sambas_enredo": sorted(sambas_by_slug.get(slug, []),
                                        key=lambda x: x["ano"], reverse=True),
                "colocacoes": sorted(colocacoes_by_slug.get(slug, []),
                                     key=lambda x: x["ano"], reverse=True),
            })

    os.makedirs("api/v1/escolas", exist_ok=True)
    os.makedirs("api/v1/carnavais", exist_ok=True)

    meta = {
        "total": len(escolas),
        "organizacao": "Brasil Com S",
        "fonte_da_verdade": "data/*.csv (raspados da Wikipedia, LigaSP e fontes oficiais)",
        "licenca": "MIT / Dados Abertos Culturais",
        "versao": "2.0.0",
    }

    with open("api/v1/escolas.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": meta, "escolas": escolas}, f, ensure_ascii=False, indent=2)

    rj = [e for e in escolas if e["estado"] == "RJ"]
    with open("api/v1/escolas/rj.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(rj), "estado": "RJ"}, "escolas": rj}, f, ensure_ascii=False, indent=2)

    sp = [e for e in escolas if e["estado"] == "SP"]
    with open("api/v1/escolas/sp.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(sp), "estado": "SP"}, "escolas": sp}, f, ensure_ascii=False, indent=2)

    esp = [e for e in escolas if e["grupo"] == "Especial"]
    with open("api/v1/escolas/especial.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(esp), "grupo": "Grupo Especial"}, "escolas": esp}, f, ensure_ascii=False, indent=2)

    acesso = [e for e in escolas if "Acesso" in e["grupo"]]
    with open("api/v1/escolas/acesso.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(acesso), "grupo": "Grupo de Acesso"}, "escolas": acesso}, f, ensure_ascii=False, indent=2)

    for e in escolas:
        with open(f"api/v1/escolas/{e['slug']}.json", "w", encoding="utf-8") as f:
            json.dump({"status": "success", "data": e}, f, ensure_ascii=False, indent=2)

    # ---- Carnavais por ano (dinâmico, a partir das colocações) ----
    for ano, linhas in colocacoes_by_ano.items():
        grupos = {}
        for l in sorted(linhas, key=lambda x: (x["estado"], x["grupo"], x["posicao"])):
            grupos.setdefault(f"{l['estado']} - {l['grupo']}", []).append({
                "posicao": l["posicao"],
                "escola_slug": l["escola_slug"],
                "escola_nome": l["escola_nome"],
                "pontos": l["pontos"],
                "enredo": l["enredo"],
            })
        campeas = {}
        for chave, classificacao in grupos.items():
            if chave.endswith("Grupo Especial"):
                estado = chave.split(" - ")[0]
                primeiro = classificacao[0]
                campeas[estado] = {"escola_slug": primeiro["escola_slug"],
                                   "escola_nome": primeiro["escola_nome"],
                                   "pontos": primeiro["pontos"]}
        with open(f"api/v1/carnavais/{ano}.json", "w", encoding="utf-8") as f:
            json.dump({
                "ano": ano,
                "campeas_grupo_especial": campeas,
                "grupos": grupos,
                "nota": "Classificação das escolas presentes na base Brasil Com S.",
            }, f, ensure_ascii=False, indent=2)

    anos = sorted(colocacoes_by_ano.keys(), reverse=True)
    with open("api/v1/carnavais.json", "w", encoding="utf-8") as f:
        json.dump({"anos_disponiveis": anos}, f, ensure_ascii=False, indent=2)

    print(f"✅ SUCESSO! API compilada: {len(escolas)} escolas, "
          f"{sum(len(v) for v in colocacoes_by_slug.values())} colocações, "
          f"{sum(len(v) for v in sambas_by_slug.values())} sambas-enredo, "
          f"{len(anos)} anos de carnavais.")

if __name__ == "__main__":
    build_api()
