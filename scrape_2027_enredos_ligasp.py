import urllib.request
import re
import json

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

def scrape_school_pages():
    # Discover all school 2027 / 2026 links on ligasp.com.br
    main_html = fetch_url("https://ligasp.com.br/")
    desfiles_html = fetch_url("https://ligasp.com.br/desfiles/")
    
    links = re.findall(r'href=["\'](https?://ligasp\.com\.br/[^"\']+carnaval-[0-9]{4}[^"\']*)["\']', main_html + desfiles_html)
    unique_links = sorted(list(set(links)))
    
    print(f"🔍 Encontrados {len(unique_links)} links de escolas/enredos no site oficial da Liga-SP:")
    
    school_enredos_2027 = []
    
    for link in unique_links:
        print(f"\n🌐 Lendo página: {link}")
        html = fetch_url(link)
        
        # Extract title / enredo / carnavalesco / ficha técnica
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1) if title_match else ""
        
        # Extract meta description or text blocks
        meta_desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
        desc = meta_desc.group(1) if meta_desc else ""
        
        print(f"  📌 Título: {title}")
        print(f"  📝 Resumo/Enredo: {desc[:150]}...")
        
        school_enredos_2027.append({
            "url": link,
            "titulo_pagina": title,
            "descricao_oficial": desc
        })

    with open("data/enredos_ligasp_2027.json", "w", encoding="utf-8") as f:
        json.dump(school_enredos_2027, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_school_pages()
