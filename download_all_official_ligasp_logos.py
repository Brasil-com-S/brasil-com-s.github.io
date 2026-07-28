import urllib.request
import re
import os

os.makedirs("assets/logos/original", exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_url(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return ""

def download_image(img_url, dest_path):
    req = urllib.request.Request(img_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as f:
            f.write(resp.read())
        print(f"✅ Baixado com sucesso: {dest_path} <- {img_url}")
    except Exception as e:
        print(f"❌ Erro ao baixar {img_url}: {e}")

def main():
    pages = ["https://ligasp.com.br/desfiles/", "https://ligasp.com.br/ligasp/", "https://ligasp.com.br/"]
    all_imgs = set()
    
    for page in pages:
        html = fetch_url(page)
        imgs = re.findall(r'src=["\'](https?://ligasp\.com\.br/wp-content/uploads/[^"\']+)["\']', html)
        for img in imgs:
            all_imgs.add(img)

    print(f"Encontradas {len(all_imgs)} URLs de imagem no site da Liga-SP!")
    
    # Mapping patterns to school slugs
    slug_patterns = {
        "mocidade-alegre": ["mocidade-alegre", "mocidade_alegre"],
        "barroca-zona-sul": ["barroca"],
        "tom-maior": ["tom-maior", "tom_maior"],
        "mancha-verde": ["mancha-verde", "mancha_verde"],
        "vai-vai": ["vai-vai", "vaivai"],
        "gavioes-da-fiel": ["gavioes", "gaviões"],
        "dragoes-da-real": ["dragoes", "dragões"],
        "imperio-de-casa-verde": ["imperio-de-casa-verde", "casa-verde"],
        "academicos-do-tatuape": ["tatuape", "tatuapé"],
        "rosas-de-ouro": ["rosas-de-ouro", "rosas_de_ouro"],
        "camisa-verde-e-branco": ["camisa-verde", "camisa_verde"],
        "aguia-de-ouro": ["aguia-de-ouro", "águia-de-ouro"],
        "academicos-do-tucuruvi": ["tucuruvi"],
        "estrela-do-terceiro-milenio": ["terceiro-milenio", "estrela-do-terceiro"],
        "nene-de-vila-matilde": ["nene-de-vila-matilde", "nenê"],
        "colorado-do-bras": ["colorado"],
        "perola-negra": ["perola-negra", "pérola"],
        "unidos-do-peruche": ["peruche"],
        "x-9-paulistana": ["x-9", "x9"]
    }

    downloaded_count = 0
    for img_url in all_imgs:
        img_lower = img_url.lower()
        for slug, patterns in slug_patterns.items():
            if any(p in img_lower for p in patterns):
                dest_path = f"assets/logos/original/{slug}.png"
                download_image(img_url, dest_path)
                downloaded_count += 1
                break

    print(f"🎉 Finalizado! {downloaded_count} logotipos oficiais baixados do site da Liga-SP para assets/logos/original/")

if __name__ == "__main__":
    main()
