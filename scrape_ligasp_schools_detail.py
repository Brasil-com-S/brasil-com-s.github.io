import urllib.request
import re

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

def scrape_pages():
    for path in ["desfiles/", "ligasp/"]:
        url = f"https://ligasp.com.br/{path}"
        html = fetch_url(url)
        print(f"=== {url} ({len(html)} bytes) ===")
        # Extract images
        imgs = re.findall(r'src=["\'](https?://ligasp\.com\.br/wp-content/uploads/[^"\']+)["\']', html)
        for img in imgs:
            if any(term in img.lower() for term in ["logo", "brasao", "escola", "escudo", "escudo-", "logo-"]):
                print("  🖼️ Logo/Escudo encontrado:", img)

if __name__ == "__main__":
    scrape_pages()
