import os
import csv
import json
import subprocess

# Load CSV data
def load_csv_data():
    sambas_dict = {}
    colocacoes_dict = {}
    
    if os.path.exists("data/sambas_enredo_historico.csv"):
        with open("data/sambas_enredo_historico.csv", mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row["escola_slug"]
                if slug not in sambas_dict:
                    sambas_dict[slug] = []
                sambas_dict[slug].append({
                    "ano": int(row["ano"]),
                    "titulo": row["titulo_samba"],
                    "compositores": row["compositores"],
                    "interpretacao": row["interpretacao"]
                })
                
    if os.path.exists("data/colocacoes_historico.csv"):
        with open("data/colocacoes_historico.csv", mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row["escola_slug"]
                if slug not in colocacoes_dict:
                    colocacoes_dict[slug] = []
                colocacoes_dict[slug].append({
                    "ano": int(row["ano"]),
                    "grupo": row["grupo"],
                    "posicao": int(row["posicao"]),
                    "pontos": float(row["pontos"]) if row["pontos"] else 0.0,
                    "resultado": row["resultado"]
                })
                
    return sambas_dict, colocacoes_dict

# Master List of 39 Samba Schools
from populate_100percent_schools import escolas_completas

def update_all_schools():
    sambas_dict, colocacoes_dict = load_csv_data()
    
    for e in escolas_completas:
        slug = e["slug"]
        
        # Merge CSV sambas if available
        if slug in sambas_dict:
            existing_years = {s["ano"] for s in e.get("sambas_enredo", [])}
            for csv_samba in sambas_dict[slug]:
                if csv_samba["ano"] not in existing_years:
                    e.setdefault("sambas_enredo", []).append(csv_samba)
            e["sambas_enredo"].sort(key=lambda x: x["ano"], reverse=True)
            
        # Merge CSV colocacoes if available
        if slug in colocacoes_dict:
            existing_col_years = {c["ano"] for c in e.get("colocacoes", [])}
            for csv_col in colocacoes_dict[slug]:
                if csv_col["ano"] not in existing_col_years:
                    e.setdefault("colocacoes", []).append(csv_col)
            e["colocacoes"].sort(key=lambda x: x["ano"], reverse=True)

        # Set URLs
        e["logo_url"] = f"assets/logos/{slug}.png"
        e["logo_png_url"] = f"assets/logos/{slug}.png"
        e["logo_svg_url"] = f"assets/logos/{slug}.svg"

def generate_svg_and_png():
    os.makedirs("assets/logos", exist_ok=True)
    
    for e in escolas_completas:
        slug = e["slug"]
        svg_path = f"assets/logos/{slug}.svg"
        png_path = f"assets/logos/{slug}.png"
        
        c1 = e["cores_hex"][0]
        c2 = e["cores_hex"][1] if len(e["cores_hex"]) > 1 else "#FFFFFF"
        c3 = e["cores_hex"][2] if len(e["cores_hex"]) > 2 else "#FFD700"
        
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bgGrad_{slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}" />
      <stop offset="100%" stop-color="{c2}" />
    </linearGradient>
    <filter id="shadow_{slug}" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>
  <circle cx="250" cy="250" r="230" fill="url(#bgGrad_{slug})" stroke="{c3}" stroke-width="12" filter="url(#shadow_{slug})" />
  <circle cx="250" cy="250" r="195" fill="none" stroke="{c3}" stroke-width="4" stroke-dasharray="8 6"/>
  <path d="M 180 170 L 210 220 L 250 160 L 290 220 L 320 170 L 330 250 L 170 250 Z" fill="{c3}" />
  <circle cx="180" cy="165" r="8" fill="#FFF"/>
  <circle cx="250" cy="155" r="10" fill="#FFF"/>
  <circle cx="320" cy="165" r="8" fill="#FFF"/>
  <text x="250" y="310" font-family="sans-serif" font-weight="900" font-size="22" fill="#FFFFFF" text-anchor="middle">{e['nome'].upper()}</text>
  <text x="250" y="345" font-family="sans-serif" font-weight="700" font-size="18" fill="{c3}" text-anchor="middle">{e['cidade'].upper()}</text>
  <text x="250" y="380" font-family="sans-serif" font-weight="600" font-size="14" fill="#E0E0E0" text-anchor="middle">FUNDADA EM {e['fundacao'][:4]}</text>
</svg>'''
        
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        # Convert SVG to PNG using sips
        subprocess.run(["sips", "-s", "format", "png", svg_path, "--out", png_path], capture_output=True)
        
        print(f"Generated PNG & SVG logos for {slug}")

def write_json_files():
    update_all_schools()
    os.makedirs("api/v1/escolas", exist_ok=True)
    os.makedirs("api/v1/carnavais", exist_ok=True)
    
    # /api/v1/escolas.json
    with open("api/v1/escolas.json", "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "total": len(escolas_completas),
                "organizacao": "Brasil Com S",
                "licenca": "MIT / Dados Abertos Culturais",
                "versao": "1.0.0"
            },
            "escolas": escolas_completas
        }, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/rj.json
    rj = [e for e in escolas_completas if e["estado"] == "RJ"]
    with open("api/v1/escolas/rj.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(rj), "estado": "RJ"}, "escolas": rj}, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/sp.json
    sp = [e for e in escolas_completas if e["estado"] == "SP"]
    with open("api/v1/escolas/sp.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(sp), "estado": "SP"}, "escolas": sp}, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/especial.json
    esp = [e for e in escolas_completas if e["grupo"] == "Especial"]
    with open("api/v1/escolas/especial.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(esp), "grupo": "Grupo Especial"}, "escolas": esp}, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/acesso.json
    acesso = [e for e in escolas_completas if "Acesso" in e["grupo"]]
    with open("api/v1/escolas/acesso.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(acesso), "grupo": "Grupo de Acesso"}, "escolas": acesso}, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/:slug.json
    for e in escolas_completas:
        with open(f"api/v1/escolas/{e['slug']}.json", "w", encoding="utf-8") as f:
            json.dump({"status": "success", "data": e}, f, ensure_ascii=False, indent=2)
            
    print(f"WRITTEN {len(escolas_completas)} SCHOOLS JSON DATA!")

if __name__ == "__main__":
    generate_svg_and_png()
    write_json_files()
