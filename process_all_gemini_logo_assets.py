import os
import glob
import shutil
import subprocess

brain_dir = "/Users/outis/.gemini/antigravity/brain/27bc9467-7325-4fdf-827a-d8f3e6e619d9"
os.makedirs("assets/logos/gemini", exist_ok=True)
os.makedirs("assets/logos/original", exist_ok=True)

# Map AI generated JPG files in brain directory to slugs
ai_hd_maps = {
    "beija-flor": glob.glob(os.path.join(brain_dir, "logo_beija_flor_hd_*.jpg")),
    "salgueiro": glob.glob(os.path.join(brain_dir, "logo_salgueiro_hd_*.jpg")),
    "viradouro": glob.glob(os.path.join(brain_dir, "logo_viradouro_hd_*.jpg")),
    "grande-rio": glob.glob(os.path.join(brain_dir, "logo_grande_rio_hd_*.jpg")),
    "mangueira": glob.glob(os.path.join(brain_dir, "logo_mangueira_hd_*.jpg")),
    "portela": glob.glob(os.path.join(brain_dir, "logo_portela_hd_*.jpg")),
    "gavioes-da-fiel": glob.glob(os.path.join(brain_dir, "logo_gavioes_hd_*.jpg")),
}

for slug, matches in ai_hd_maps.items():
    if matches:
        src_jpg = matches[0]
        dst_png = f"assets/logos/gemini/{slug}.png"
        subprocess.run(["sips", "-s", "format", "png", src_jpg, "--out", dst_png], capture_output=True)
        print(f"✅ Convertido e copiado logo Gemini HD PNG para: {dst_png}")

# Create vector SVG badges for all schools into assets/logos/gemini/
school_color_maps = {
    "mangueira": ("#008000", "#FF69B4", "MANGUEIRA"),
    "portela": ("#0047AB", "#FFFFFF", "PORTELA"),
    "beija-flor": ("#002366", "#FFFFFF", "BEIJA-FLOR"),
    "salgueiro": ("#D32F2F", "#FFFFFF", "SALGUEIRO"),
    "viradouro": ("#C62828", "#FFFFFF", "VIRADOURO"),
    "imperatriz": ("#2E7D32", "#FFD700", "IMPERATRIZ"),
    "grande-rio": ("#388E3C", "#D32F2F", "GRANDE RIO"),
    "vila-isabel": ("#0288D1", "#FFFFFF", "VILA ISABEL"),
    "mocidade-independente": ("#008000", "#FFFFFF", "MOCIDADE"),
    "vai-vai": ("#000000", "#FFCC00", "VAI-VAI"),
    "mocidade-alegre": ("#D32F2F", "#388E3C", "MOCIDADE ALEGRE"),
    "gavioes-da-fiel": ("#000000", "#FFFFFF", "GAVIÕES DA FIEL"),
    "dragoes-da-real": ("#D32F2F", "#000000", "DRAGÕES DA REAL"),
    "imperio-de-casa-verde": ("#0288D1", "#FFFFFF", "IMPÉRIO CASA VERDE"),
    "academicos-do-tatuape": ("#1565C0", "#FFFFFF", "TATUAPÉ"),
    "mancha-verde": ("#2E7D32", "#FFFFFF", "MANCHA VERDE"),
    "barroca-zona-sul": ("#008000", "#FF69B4", "BARROCA ZONA SUL"),
    "aguia-de-ouro": ("#1976D2", "#FFD700", "ÁGUIA DE OURO"),
    "academicos-do-tucuruvi": ("#1976D2", "#D32F2F", "TUCURUVI"),
    "rosas-de-ouro": ("#0288D1", "#FF69B4", "ROSAS DE OURO"),
    "camisa-verde-e-branco": ("#008000", "#FFFFFF", "CAMISA VERDE"),
    "tom-maior": ("#D32F2F", "#FFEB3B", "TOM MAIOR"),
    "estrela-do-terceiro-milenio": ("#D32F2F", "#1976D2", "TERCEIRO MILÊNIO"),
    "nene-de-vila-matilde": ("#1565C0", "#FFFFFF", "NENÊ DE VILA MATILDE"),
    "colorado-do-bras": ("#D32F2F", "#FFFFFF", "COLORADO DO BRÁS"),
    "perola-negra": ("#D32F2F", "#000000", "PÉROLA NEGRA"),
    "unidos-do-peruche": ("#388E3C", "#FFEB3B", "PERUCHE"),
    "x-9-paulistana": ("#388E3C", "#D32F2F", "X-9 PAULISTANA")
}

for slug, (c1, c2, text) in school_color_maps.items():
    svg_path = f"assets/logos/gemini/{slug}.svg"
    png_fallback = f"assets/logos/gemini/{slug}.png"
    
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </radialGradient>
    <linearGradient id="crestGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD700"/>
      <stop offset="100%" stop-color="#FFA500"/>
    </linearGradient>
  </defs>
  <circle cx="250" cy="250" r="240" fill="url(#bgGrad)" stroke="url(#goldGrad)" stroke-width="8"/>
  <circle cx="250" cy="250" r="215" fill="none" stroke="url(#goldGrad)" stroke-width="2" stroke-dasharray="8 6"/>
  <!-- Shield Crest -->
  <path d="M 250 80 Q 340 80 370 140 Q 370 290 250 400 Q 130 290 130 140 Q 160 80 250 80 Z" fill="url(#crestGrad)" stroke="url(#goldGrad)" stroke-width="6"/>
  <!-- Crown Icon -->
  <path d="M 200 130 L 220 170 L 250 120 L 280 170 L 300 130 L 290 185 L 210 185 Z" fill="url(#goldGrad)"/>
  <circle cx="200" cy="125" r="5" fill="#FFF"/>
  <circle cx="250" cy="115" r="6" fill="#FFF"/>
  <circle cx="300" cy="125" r="5" fill="#FFF"/>
  <!-- Laurel Wreath -->
  <path d="M 110 250 Q 90 180 140 120 M 390 250 Q 410 180 360 120" fill="none" stroke="url(#goldGrad)" stroke-width="5" stroke-linecap="round"/>
  <!-- Ribbon Banner -->
  <path d="M 80 380 Q 250 430 420 380 L 400 420 Q 250 470 100 420 Z" fill="url(#goldGrad)"/>
  <text x="250" y="412" font-family="'Outfit', 'Inter', sans-serif" font-weight="900" font-size="22" fill="#000" text-anchor="middle" letter-spacing="2">{text}</text>
</svg>'''
    with open(svg_path, "w", encoding="utf-8") as sf:
        sf.write(svg_content)
    print(f"✅ Criado vetor SVG Gemini em: {svg_path}")
    
    if not os.path.exists(png_fallback):
        # Convert SVG to PNG using sips or fallback copy
        subprocess.run(["sips", "-s", "format", "png", svg_path, "--out", png_fallback], capture_output=True)
        print(f"✅ Criado fallback Gemini PNG em: {png_fallback}")

print("\n🎉 Todas as imagens de logotipo Gemini PNG e SVG processadas!")
