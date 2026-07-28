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
        return ""

def search_school_pages():
    schools = [
        "mocidade-alegre", "mancha-verde", "gavioes-da-fiel", "vai-vai",
        "dragoes-da-real", "imperio-de-casa-verde", "academicos-do-tatuape",
        "rosas-de-ouro", "aguia-de-ouro", "barroca-zona-sul", "tom-maior",
        "camisa-verde-e-branco", "academicos-do-tucuruvi", "estrela-do-terceiro-milenio",
        "nene-de-vila-matilde", "colorado-do-bras", "perola-negra", "unidos-do-peruche", "x-9-paulistana"
    ]

    enredos_2027 = {}

    for school in schools:
        # Try candidate URLs on ligasp.com.br
        urls = [
            f"https://ligasp.com.br/{school}-carnaval-2027/",
            f"https://ligasp.com.br/{school}/",
            f"https://ligasp.com.br/?s={school}+2027"
        ]
        
        for url in urls:
            html = fetch_url(url)
            if html and ("2027" in html or "Enredo" in html or "Ficha Técnica" in html):
                title_match = re.search(r'<title>(.*?)</title>', html)
                title = title_match.group(1) if title_match else ""
                
                meta_desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
                desc = meta_desc.group(1) if meta_desc else ""
                
                # Check for enredo title pattern
                enredo_match = re.search(r'Enredo\s*(?:2027)?\s*[:·-]?\s*([^<"\n\.\!]+)', html, re.IGNORECASE)
                enredo_title = enredo_match.group(1).strip() if enredo_match else ""
                
                if enredo_title or desc:
                    enredos_2027[school] = {
                        "url": url,
                        "titulo_pagina": title,
                        "enredo_2027": enredo_title or desc,
                        "descricao": desc
                    }
                    print(f"✅ [{school}] Encontrado! Enredo 2027: {enredo_title or desc[:100]}")
                    break

    print(f"\n🎉 Total de escolas com dados de 2027 extraídos da Liga-SP: {len(enredos_2027)}")
    
    with open("data/enredos_2027_oficiais.json", "w", encoding="utf-8") as f:
        json.dump(enredos_2027, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    search_school_pages()
