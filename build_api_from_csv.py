import os
import csv
import json
import subprocess

# Single Source of Truth Builder Script
# Reads data/escolas_de_samba.csv & data/sambas_e_colocacoes.csv and compiles all /api/v1/ endpoints

ESCOLAS_CSV = "data/escolas_de_samba.csv"
SAMBAS_CSV = "data/sambas_e_colocacoes.csv"

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

    # Load Sambas & Colocações CSV
    sambas_by_slug = {}
    colocacoes_by_slug = {}
    
    if os.path.exists(SAMBAS_CSV):
        with open(SAMBAS_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row["escola_slug"]
                if row.get("titulo_samba"):
                    sambas_by_slug.setdefault(slug, []).append({
                        "ano": int(row["ano"]),
                        "titulo": row["titulo_samba"],
                        "compositores": row["compositores"],
                        "interpretacao": row["interpretacao"]
                    })
                if row.get("posicao"):
                    colocacoes_by_slug.setdefault(slug, []).append({
                        "ano": int(row["ano"]),
                        "grupo": row["grupo_carnaval"],
                        "posicao": int(row["posicao"]),
                        "pontos": float(row["pontos"]) if row.get("pontos") else 0.0,
                        "resultado": row.get("resultado_oficial", f"{row['posicao']}º Lugar")
                    })

    # Read Master Escolas CSV
    escolas = []
    with open(ESCOLAS_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row["slug"]
            
            # Combine CSV arrays
            school_obj = {
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
                "logo_url": f"assets/logos/{slug}.png",
                "logo_png_url": f"assets/logos/{slug}.png",
                "logo_svg_url": f"assets/logos/{slug}.svg",
                "sambas_enredo": sorted(sambas_by_slug.get(slug, []), key=lambda x: x["ano"], reverse=True),
                "colocacoes": sorted(colocacoes_by_slug.get(slug, []), key=lambda x: x["ano"], reverse=True)
            }
            escolas.append(school_obj)

    os.makedirs("api/v1/escolas", exist_ok=True)
    os.makedirs("api/v1/carnavais", exist_ok=True)
    
    # Write /api/v1/escolas.json
    with open("api/v1/escolas.json", "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "total": len(escolas),
                "organizacao": "Brasil Com S",
                "fonte_da_verdade": "data/escolas_de_samba.csv",
                "licenca": "MIT / Dados Abertos Culturais",
                "versao": "1.0.0"
            },
            "escolas": escolas
        }, f, ensure_ascii=False, indent=2)

    # Write state and group filters
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

    # Write individual /api/v1/escolas/:slug.json
    for e in escolas:
        with open(f"api/v1/escolas/{e['slug']}.json", "w", encoding="utf-8") as f:
            json.dump({"status": "success", "data": e}, f, ensure_ascii=False, indent=2)

    # Write carnavais index
    with open("api/v1/carnavais.json", "w", encoding="utf-8") as f:
        json.dump({"anos_disponiveis": [2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015]}, f, ensure_ascii=False, indent=2)

    print(f"✅ SUCESSO! API estática compilada perfeitamente para {len(escolas)} escolas de samba a partir dos CSVs!")

if __name__ == "__main__":
    build_api()
