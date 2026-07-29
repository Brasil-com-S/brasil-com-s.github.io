#!/usr/bin/env python3
"""
scrape_logos.py

Baixa os escudos/bandeiras oficiais das escolas:

  - RJ (+ Águia de Ouro, que a LigaSP não expôs): imagem do infobox do
    artigo da Wikipédia (wikitext já cacheado por scrape_wikipedia_escolas.py),
    baixada do Wikimedia Commons via Special:FilePath.
  - SP: mantém os PNGs oficiais já baixados da LigaSP
    (download_all_official_ligasp_logos.py); não sobrescreve.

Saída: assets/logos/original/{slug}.png (convertido com `sips` quando o
arquivo original não é PNG).

Nota de licenciamento: as imagens do Commons têm licença livre indicada na
respectiva página de descrição; os escudos são propriedade das agremiações.
"""

import csv
import re
import subprocess
import time
from pathlib import Path

import requests

ROOT = Path(__file__).parent
DATA = ROOT / "data"
WIKI_CACHE = DATA / "cache" / "wikipedia" / "escolas_wiki"
OUT_DIR = ROOT / "assets" / "logos" / "original"
OUT_DIR.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "brasil-com-s-api data bot (https://github.com/Brasil-com-S/brasil-com-s.github.io)"}

# Escolas cujo logo oficial já veio da LigaSP (não sobrescrever).
KEEP_LIGASP = True


def infobox_image(wt: str) -> str | None:
    """Nome do ficheiro de imagem do infobox (imagem, senão imagem2)."""
    for field in ("imagem", "imagem2"):
        m = re.search(rf"\|\s*{field}\s*=\s*(.*)", wt)
        if not m:
            continue
        val = m.group(1).strip()
        fm = re.search(r"(?:Ficheiro|File|Imagem|Image):([^]|]+)", val, flags=re.I)
        if fm:
            return fm.group(1).strip()
        bare = re.match(r"([^]|<>{]+\.(?:jpe?g|png|gif|svg|webp))", val, flags=re.I)
        if bare:
            return bare.group(1).strip()
    return None


def resolve_urls(filenames: list[str]) -> dict[str, str]:
    """Resolve nomes de ficheiros para URLs reais via API da ptwiki
    (funciona tanto para arquivos locais quanto do Commons)."""
    out = {}
    titles = "|".join(f"Ficheiro:{f}" for f in filenames)
    r = requests.get(
        "https://pt.wikipedia.org/w/api.php",
        params={"action": "query", "prop": "imageinfo", "iiprop": "url",
                "format": "json", "titles": titles, "redirects": 1},
        headers=UA, timeout=30,
    )
    for page in r.json()["query"]["pages"].values():
        if "imageinfo" in page:
            nome = re.sub(r"^(Ficheiro|File)\s*:", "", page["title"])
            out[nome] = page["imageinfo"][0]["url"]
    return out


def download(url: str) -> bytes | None:
    r = requests.get(url, headers=UA, timeout=60)
    if r.status_code != 200 or len(r.content) < 500:
        return None
    return r.content


def main():
    from scrape_wikipedia_escolas import ARTICLE_TITLES
    escolas = list(csv.DictReader((DATA / "escolas_de_samba.csv").open(encoding="utf-8")))

    # 1ª passada: descobre o ficheiro de cada escola
    alvo = {}   # slug -> (filename, dest)
    falhas, mantidos = [], []
    for e in escolas:
        slug, estado = e["slug"], e["estado"]
        dest = OUT_DIR / f"{slug}.png"
        if KEEP_LIGASP and estado == "SP" and dest.exists():
            mantidos.append(slug)
            continue
        title = ARTICLE_TITLES.get(slug, e["nome"])
        safe = re.sub(r"[^\w]+", "_", title)
        wt_path = WIKI_CACHE / f"{safe}.wiki"
        fname = infobox_image(wt_path.read_text(encoding="utf-8")) if wt_path.exists() else None
        if not fname:
            falhas.append(f"{slug}: infobox sem imagem")
            continue
        alvo[slug] = (fname, dest)

    # resolve URLs em lote e baixa
    urls = resolve_urls([f for f, _ in alvo.values()])
    ok = []
    for slug, (fname, dest) in alvo.items():
        url = urls.get(fname)
        if not url:
            falhas.append(f"{slug}: URL não resolvida ({fname})")
            continue
        time.sleep(1.0)
        blob = download(url)
        if blob is None:
            falhas.append(f"{slug}: download falhou ({fname})")
            continue
        tmp = OUT_DIR / f".{slug}.tmp"
        tmp.write_bytes(blob)
        subprocess.run(["sips", "-s", "format", "png", str(tmp),
                        "--out", str(dest)], capture_output=True)
        tmp.unlink(missing_ok=True)
        if dest.exists():
            ok.append(f"{slug} <- {fname}")
        else:
            falhas.append(f"{slug}: conversão sips falhou ({fname})")

    print(f"baixados: {len(ok)}")
    for o in ok:
        print("  ", o)
    print(f"mantidos (LigaSP): {len(mantidos)}")
    print(f"falhas: {len(falhas)}")
    for f in falhas:
        print("  ", f)


if __name__ == "__main__":
    main()
