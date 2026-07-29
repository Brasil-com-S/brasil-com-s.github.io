#!/usr/bin/env python3
"""
scrape_wikipedia_escolas.py

Reescreve data/escolas_de_samba.csv com dados extraídos dos artigos das
escolas na Wikipédia em português (fonte oficial de referência):

  - infobox {{Info/Carnaval}}: fundação, cores (+hex), símbolo, bairro
  - lead do artigo: nome completo (negrito), fundadores ("fundada ... por ...")
  - títulos/anos_titulos: de data/cache/titulos_derivados.json
    (gerado por scrape_wikipedia_resultados.py a partir das listas de campeãs)

Wikitext cacheado em data/cache/wikipedia/escolas_wiki/.
Campos que a extração automática não resolve ficam vazios (nunca inventados)
e são listados no resumo final para revisão manual.
"""

import csv
import json
import re
import time
import unicodedata
from pathlib import Path

import requests

ROOT = Path(__file__).parent
DATA = ROOT / "data"
CACHE = DATA / "cache" / "wikipedia" / "escolas_wiki"
CACHE.mkdir(parents=True, exist_ok=True)

ESCOLAS_CSV = DATA / "escolas_de_samba.csv"
TITULOS_JSON = DATA / "cache" / "titulos_derivados.json"
OUT_CSV = ESCOLAS_CSV  # reescreve in-place

UA = {"User-Agent": "brasil-com-s-api data bot (https://github.com/Brasil-com-S/brasil-com-s.github.io)"}

# Títulos de artigo que divergem do nome oficial no CSV.
ARTICLE_TITLES = {
    "mangueira": "Estação Primeira de Mangueira",
    "portela": "Portela (escola de samba)",
    "beija-flor": "Beija-Flor (escola de samba)",
    "viradouro": "Unidos do Viradouro",
    "imperatriz": "Imperatriz Leopoldinense",
    "grande-rio": "Acadêmicos do Grande Rio",
    "vila-isabel": "Unidos de Vila Isabel",
    "mocidade-independente": "Mocidade Independente de Padre Miguel",
    "paraiso-do-tuiuti": "Paraíso do Tuiuti",
    "unidos-de-padre-miguel": "Unidos de Padre Miguel",
    "estacio-de-sa": "Estácio de Sá (escola de samba)",
    "imperio-serrano": "Império Serrano",
    "uniao-da-ilha": "União da Ilha do Governador",
    "sao-clemente": "São Clemente (escola de samba)",
    "inocentes-de-belford-roxo": "Inocentes de Belford Roxo",
    "academicos-de-niteroi": "Acadêmicos de Niterói",
    "unidos-de-bangu": "Unidos de Bangu",
    "uniao-de-marica": "União de Maricá",
    "academicos-de-vigario-geral": "Acadêmicos de Vigário Geral",
    "vai-vai": "Vai-Vai",
    "mocidade-alegre": "Mocidade Alegre",
    "gavioes-da-fiel": "Gaviões da Fiel",
    "dragoes-da-real": "Dragões da Real (escola de samba)",
    "imperio-de-casa-verde": "Império de Casa Verde",
    "academicos-do-tatuape": "Acadêmicos do Tatuapé",
    "mancha-verde": "Mancha Verde",
    "barroca-zona-sul": "Barroca Zona Sul",
    "aguia-de-ouro": "Águia de Ouro",
    "academicos-do-tucuruvi": "Acadêmicos do Tucuruvi",
    "rosas-de-ouro": "Rosas de Ouro",
    "camisa-verde-e-branco": "Camisa Verde e Branco",
    "tom-maior": "Tom Maior",
    "estrela-do-terceiro-milenio": "Estrela do Terceiro Milênio",
    "nene-de-vila-matilde": "Nenê de Vila Matilde",
    "colorado-do-bras": "Colorado do Brás",
    "perola-negra": "Pérola Negra (escola de samba)",
    "unidos-do-peruche": "Unidos do Peruche",
    "x-9-paulistana": "X-9 Paulistana",
}

# Fundadores conforme os artigos da Wikipédia (lead ou seção "Fundação").
# Escolas sem nomes de fundadores documentados no artigo ficam com o campo
# vazio — nunca inventado. Entradas no estilo "Fusão..."/"Dissidência..."
# descrevem a origem quando o artigo não lista pessoas.
MANUAL_FUNDADORES = {
    "mangueira": "Cartola; Carlos Cachaça; Zé Espinguela; Saturnino Gonçalves; Euclides Roberto dos Santos (Seu Euclides); Marcelino José Claudino (Maçu da Mangueira); Pedro Caim (Paquetá); Abelardo da Bolinha",
    "portela": "Galdino Marcelino dos Santos; Antônio Rufino dos Reis; Antônio da Silva Caetano; Paulo Benjamim de Oliveira (Paulo da Portela)",
    "beija-flor": "Milton de Oliveira (Negão da Cuíca); Edson Vieira Rodrigues (Edinho do Ferro Velho); Valentim Lemos; Helles Ferreira da Silva; Hamilton Floriano; José Fernandes da Silva; Mário Silva; Walter da Silva; Dona Eulália",
    "salgueiro": "Fusão das escolas Depois Eu Digo e Azul e Branco (Morro do Salgueiro)",
    "imperatriz": "Amaury Jório; sambistas da Zona da Leopoldina e remanescentes da Recreio de Ramos",
    "grande-rio": "Fusão das agremiações GRES Grande Rio e Acadêmicos de Duque de Caxias",
    "vila-isabel": "Antônio Fernandes da Silveira (Seu China); Aílton Cléber da Silva; Antonio Rodrigues (Tuninho Carpinteiro); Ari Barbosa; Cesso da Silva; Joaquim José Rodrigues (Quinzinho); Osmar Mariano; Paulo Gomes de Aquino (Paulo Brazão); Servan Heitor de Carvalho",
    "mocidade-independente": "Sílvio Trindade; Renato da Silva; Djalma Rosa; Olímpio Bonifácio (Bronquinha); Ary de Lima; Jorge Avelino da Silva; Orozimbo de Oliveira (Seu Orozimbo); Garibaldi F. Lima; Felipe de Souza (Pavão); José Pereira da Silva (Mestre André); Alfredo Briggs",
    "estacio-de-sa": "Originária da Unidos de São Carlos (Morro de São Carlos)",
    "imperio-serrano": "Dissidência da escola de samba Prazer da Serrinha",
    "uniao-da-ilha": "Maurício Gazelle; Quincas; Orphylo",
    "sao-clemente": "Ivo da Rocha Gomes; João Marinho; Aílton Teixeira",
    "vai-vai": "Grupo de sambistas do Bixiga",
    "imperio-de-casa-verde": "Dissidentes do Unidos do Peruche",
    "barroca-zona-sul": "Sebastião Eduardo do Amaral (Pé Rachado); sambistas da Vila Mariana",
    "academicos-do-tucuruvi": "Grupo de moradores do bairro do Tucuruvi",
    "rosas-de-ouro": "José Luciano Tomás da Silva; Jorge Augusto de Andrade; João Roque (Cajé); José Benedito da Silva (Zelão); Hernane Basílio; Ronaldo Gomes; Eduardo Basílio",
    "nene-de-vila-matilde": "Alberto Alves da Silva",
}

COLUMNS = ["id", "slug", "nome", "nome_completo", "fundacao", "fundadores",
           "estado", "cidade", "bairro", "grupo", "cores", "cores_hex",
           "simbolo", "titulos", "anos_titulos", "logo_original_url"]


# ---------------------------------------------------------------------------
# Fetch com cache
# ---------------------------------------------------------------------------

def fetch_wikitext(title: str) -> str | None:
    safe = re.sub(r"[^\w]+", "_", title)
    path = CACHE / f"{safe}.wiki"
    if path.exists():
        txt = path.read_text(encoding="utf-8")
        return txt or None
    time.sleep(1.0)
    r = requests.get(
        "https://pt.wikipedia.org/w/api.php",
        params={"action": "query", "prop": "revisions", "rvprop": "content",
                "rvsection": 0, "format": "json", "titles": title,
                "redirects": 1},
        headers=UA, timeout=30,
    )
    pages = r.json()["query"]["pages"]
    page = next(iter(pages.values()))
    wt = ""
    if "missing" not in page and "revisions" in page:
        wt = page["revisions"][0]["*"]
    path.write_text(wt, encoding="utf-8")
    return wt or None


def fetch_lead(title: str) -> str:
    """Lead do artigo em texto puro (prop=extracts), cacheado em .lead.txt."""
    safe = re.sub(r"[^\w]+", "_", title)
    path = CACHE / f"{safe}.lead.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    time.sleep(1.0)
    r = requests.get(
        "https://pt.wikipedia.org/w/api.php",
        params={"action": "query", "prop": "extracts", "exintro": 1,
                "explaintext": 1, "format": "json", "titles": title,
                "redirects": 1},
        headers=UA, timeout=30,
    )
    pages = r.json()["query"]["pages"]
    page = next(iter(pages.values()))
    lead = page.get("extract", "")
    path.write_text(lead, encoding="utf-8")
    return lead


# ---------------------------------------------------------------------------
# Limpeza de wikitext
# ---------------------------------------------------------------------------

def strip_markup(s: str) -> str:
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<ref[^/]*/>", "", s)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"\[\[([^]|]*)\|([^]]*)\]\]", r"\2", s)   # [[a|b]] -> b
    s = re.sub(r"\[\[([^]]*)\]\]", r"\1", s)             # [[a]] -> a
    s = re.sub(r"\{\{[Cc]or\|(#[0-9A-Fa-f]{3,6})\|([^}]*)\}\}", r"\2", s)
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    s = s.replace("'''", "").replace("''", "")
    s = re.sub(r"<br\s*/?>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def extract_infobox(wt: str) -> dict:
    """Extrai o primeiro template {{Info...}} com balanceamento de chaves
    e devolve dict de parâmetros (split em '|' de nível zero)."""
    m = re.search(r"\{\{\s*(?:[Ii]nfo|[Ff]icha)", wt)
    if not m:
        return {}
    depth, i = 0, m.start()
    start = i
    while i < len(wt):
        if wt.startswith("{{", i):
            depth += 1
            i += 2
            continue
        if wt.startswith("}}", i):
            depth -= 1
            i += 2
            if depth == 0:
                break
            continue
        i += 1
    body = wt[start + 2:i - 2]
    # split em '|' de nível zero
    parts, depth, cur = [], 0, []
    j = 0
    while j < len(body):
        if body.startswith("{{", j) or body.startswith("[[", j):
            depth += 1
            cur.append(body[j:j + 2])
            j += 2
            continue
        if body.startswith("}}", j) or body.startswith("]]", j):
            depth -= 1
            cur.append(body[j:j + 2])
            j += 2
            continue
        if body[j] == "|" and depth == 0:
            parts.append("".join(cur))
            cur = []
            j += 1
            continue
        cur.append(body[j])
        j += 1
    parts.append("".join(cur))
    params = {}
    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            params[k.strip().lower()] = v.strip()
    return params


def parse_fundacao(raw: str) -> str:
    m = re.search(r"\{\{[Dd]tlink\|(\d{1,2})\|(\d{1,2})\|(\d{4})", raw)
    if m:
        d, mo, y = m.groups()
        return f"{y}-{int(mo):02d}-{int(d):02d}"
    m = re.search(r"(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})", strip_markup(raw))
    meses = {"janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4,
             "maio": 5, "junho": 6, "julho": 7, "agosto": 8, "setembro": 9,
             "outubro": 10, "novembro": 11, "dezembro": 12}
    if m and m.group(2).lower() in meses:
        d, mes, y = m.groups()
        return f"{y}-{meses[mes.lower()]:02d}-{int(d):02d}"
    m = re.search(r"(\d{4})", raw)
    return m.group(1) if m else ""


CSS_COLORS = {"black": "#000000", "white": "#FFFFFF", "red": "#FF0000",
              "green": "#008000", "yellow": "#FFFF00", "blue": "#0000FF",
              "gold": "#FFD700", "gray": "#808080", "grey": "#808080",
              "orange": "#FFA500", "pink": "#FFC0CB", "purple": "#800080",
              "brown": "#A52A2A", "silver": "#C0C0C0", "navy": "#000080"}


def parse_cores(raw: str):
    nomes, hexes = [], []
    for cor, nome in re.findall(
            r"\{\{[Cc]or\|(#[0-9A-Fa-f]{3,6}|[A-Za-z]+)\|([^}]*)\}\}", raw):
        nomes.append(strip_markup(nome))
        hexes.append(cor.upper() if cor.startswith("#")
                     else CSS_COLORS.get(cor.lower(), ""))
    if not nomes:
        txt = strip_markup(raw)
        nomes = [n.strip() for n in re.split(r"[,;]| e ", txt) if n.strip()]
    return nomes, hexes


def parse_nome_completo(lead: str) -> str:
    # o lead começa com o nome completo oficial: "Grêmio Recreativo Escola de
    # Samba X (ou simplesmente Y) é uma escola de samba ..."
    m = re.match(r"\s*(.{10,120}?)\s*(?:\(|,\s*(?:ou|mais)|\,?\s+é\s)", lead)
    return m.group(1).strip() if m else ""


def parse_fundadores(lead: str) -> str:
    """Extrai a lista de fundadores da frase de fundação do lead."""
    matches = list(re.finditer(
        r"fundad[ao][^.]{0,200}?\bpor\b([^.]{5,400})\.", lead, flags=re.I))
    if not matches:
        return ""
    lista = matches[-1].group(1)   # a menção principal costuma ser a última
    lista = unicodedata.normalize("NFC", lista)
    lista = re.sub(r"^(sambistas|moradores|compositores|um grupo( de \w+)?|"
                   r"integrantes|amigos|carnavalescos|o(s)? então|"
                   r"figuras como)\s*(como|de)?\s*",
                   "", lista, flags=re.I).strip()
    # corta caudas verbais comuns ("que se reuniram...", "no terreiro...")
    lista = re.split(r",?\s+(?:que|tendo|para|cujo)\b", lista)[0]
    partes = re.split(r",|;|\s+e\s+", lista)
    partes = [p.strip(" .") for p in partes]
    partes = [p for p in partes if 3 <= len(p) <= 60 and not re.search(
        r"\b(escola|samba|bairro|comunidade|fundad|carnaval|ano|dia|data|"
        r"quadra|terreiro|morro|cidade|rua|local)\b",
        p, flags=re.I)]
    return "; ".join(partes)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    with ESCOLAS_CSV.open(encoding="utf-8") as f:
        escolas = list(csv.DictReader(f))
    titulos_data = json.loads(TITULOS_JSON.read_text(encoding="utf-8"))
    t_anos = titulos_data["anos"]
    t_count = titulos_data["titulos_oficiais"]

    pendentes = []
    out_rows = []
    for e in escolas:
        slug = e["slug"]
        title = ARTICLE_TITLES.get(slug, e["nome"])
        wt = fetch_wikitext(title)
        row = {c: "" for c in COLUMNS}
        row.update({
            "id": slug, "slug": slug, "nome": e["nome"],
            "estado": e["estado"], "cidade": e["cidade"], "grupo": e["grupo"],
            "logo_original_url": f"assets/logos/original/{slug}.png",
        })
        anos = t_anos.get(slug, [])
        row["titulos"] = str(t_count.get(slug, len(anos)))
        row["anos_titulos"] = "; ".join(str(a) for a in anos)

        if wt is None:
            pendentes.append(f"{slug}: artigo ausente ({title})")
            out_rows.append(row)
            continue

        ibox = extract_infobox(wt)
        lead = fetch_lead(title)

        row["nome_completo"] = parse_nome_completo(lead)
        row["fundacao"] = parse_fundacao(
            ibox.get("fundação", "") or ibox.get("fundacao", ""))
        nomes, hexes = parse_cores(ibox.get("cores", ""))
        row["cores"] = "; ".join(nomes)
        row["cores_hex"] = "; ".join(hexes)
        row["simbolo"] = strip_markup(ibox.get("símbolo", "")
                                      or ibox.get("simbolo", ""))
        row["bairro"] = strip_markup(ibox.get("bairro", ""))
        row["fundadores"] = MANUAL_FUNDADORES.get(slug) or parse_fundadores(lead)

        for campo in ("nome_completo", "fundacao", "cores", "bairro",
                      "fundadores"):
            if not row[campo]:
                pendentes.append(f"{slug}: campo vazio: {campo}")
        out_rows.append(row)
        print(f"{slug}: fundacao={row['fundacao']} cores={row['cores']} "
              f"titulos={row['titulos']} fundadores={row['fundadores'][:60]}")

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(out_rows)

    print("\n== Pendências para revisão ==")
    for p in pendentes:
        print(" -", p)
    print(f"\n{len(out_rows)} escolas gravadas em {OUT_CSV}")


if __name__ == "__main__":
    main()
