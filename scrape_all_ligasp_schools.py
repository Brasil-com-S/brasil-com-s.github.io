import urllib.request
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

def fetch_url(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return ""

def discover_schools():
    html = fetch_url("https://ligasp.com.br/")
    print(f"Main page length: {len(html)}")
    
    # Extract links containing school names or wp-content images
    img_urls = re.findall(r'https?://ligasp\.com\.br/wp-content/uploads/[^"\'>\s]+\.(?:png|jpg|jpeg)', html)
    print(f"Encontradas {len(img_urls)} imagens no site oficial!")
    for img in img_urls[:10]:
        print("  - Imagem LigaSP:", img)

    # Search for links
    links = re.findall(r'href=["\'](https?://ligasp\.com\.br/[^"\']+)["\']', html)
    unique_links = sorted(list(set(links)))
    print(f"Encontrados {len(unique_links)} links únicos no site da Liga-SP:")
    for link in unique_links[:20]:
        print("  - Link:", link)

if __name__ == "__main__":
    discover_schools()
