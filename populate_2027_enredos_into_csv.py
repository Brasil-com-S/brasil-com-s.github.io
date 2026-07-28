import csv
import json
import os
import subprocess

SAMBAS_CSV = "data/sambas_e_colocacoes.csv"

# 2027 Official Enredos from Liga-SP
enredos_2027_map = {
    "mocidade-alegre": {
        "titulo": "Sete Anos de Mar, Sete Léguas de Encanto: A Nau que Venceu o Diabo sob a Benção do Sagrado Manto",
        "compositores": "Comissão de Carnaval / Caio Araújo (Carnavalesco)",
        "interpretacao": "Igor Sorriso",
        "grupo": "Grupo Especial"
    },
    "mancha-verde": {
        "titulo": "Ruth Rocha: a Palavra que Ensina a Criança a Voar",
        "compositores": "André Machado (Carnavalesco)",
        "interpretacao": "Fredy Vianna",
        "grupo": "Grupo Especial"
    },
    "dragoes-da-real": {
        "titulo": "Sob as Bênçãos de Xangô, a Coroação do Príncipe Reinaldo",
        "compositores": "Jorge Marcos Freitas (Carnavalesco)",
        "interpretacao": "Renê Sobral",
        "grupo": "Grupo Especial"
    },
    "imperio-de-casa-verde": {
        "titulo": "Sob o Céu do Interior Brilha o Sonho Caipira: Jaguariúna, a Capital Country do Brasil",
        "compositores": "Fabio Ricardo Rangel da Costa (Carnavalesco)",
        "interpretacao": "Tinga",
        "grupo": "Grupo Especial"
    },
    "academicos-do-tatuape": {
        "titulo": "Congo Kinshasa: O Coração da África, a Herança Viva de um Povo que Resiste ao Tempo",
        "compositores": "Wagner Santos (Carnavalesco)",
        "interpretacao": "Cordan",
        "grupo": "Grupo Especial"
    },
    "rosas-de-ouro": {
        "titulo": "Mar de Rosas",
        "compositores": "Bruno de Oliveira e Yago Duarte (Carnavalescos)",
        "interpretacao": "Royce do Cavaco",
        "grupo": "Grupo Especial"
    },
    "aguia-de-ouro": {
        "titulo": "Águia na Encantaria de Fés, Folguedos e Milagres que Deságuam no Sertão",
        "compositores": "Leandro Barboza (Carnavalesco)",
        "interpretacao": "Douglani",
        "grupo": "Grupo Especial"
    },
    "barroca-zona-sul": {
        "titulo": "Elekô Obá Xirê — A Força da Mulher que Não se Curva",
        "compositores": "Pedro Alexandre Alves de Lacerda / Magoo (Carnavalesco)",
        "interpretacao": "Pixulé",
        "grupo": "Grupo Especial"
    },
    "tom-maior": {
        "titulo": "Eu Sou o Pão da Vida",
        "compositores": "Flávio Campello (Carnavalesco)",
        "interpretacao": "Gilsinho",
        "grupo": "Acesso 1"
    },
    "academicos-do-tucuruvi": {
        "titulo": "Ogbódirin, Ògbóni",
        "compositores": "Nícolas Gonçalves (Carnavalesco)",
        "interpretacao": "Hudson Luiz",
        "grupo": "Grupo Especial"
    },
    "estrela-do-terceiro-milenio": {
        "titulo": "Incrível, Fantástico, Extraordinário",
        "compositores": "Murilo Lobo (Carnavalesco)",
        "interpretacao": "Grazzi Brasil",
        "grupo": "Grupo Especial"
    },
    "nene-de-vila-matilde": {
        "titulo": "Mulheres de Palmares — A Liberdade tem Rosto de Mulher",
        "compositores": "Chico Ângelo (Carnavalesco)",
        "interpretacao": "Agnaldo Amaral",
        "grupo": "Acesso 1"
    },
    "colorado-do-bras": {
        "titulo": "Ojuara — O Homem que Desafiou o Diabo",
        "compositores": "David Eslavick (Carnavalesco)",
        "interpretacao": "Léo Reis",
        "grupo": "Grupo Especial"
    },
    "perola-negra": {
        "titulo": "Sem Vacilar, Sem me Exibir: Sou Jovelina, a Pérola Negra",
        "compositores": "André Machado (Carnavalesco)",
        "interpretacao": "Daniel Collete",
        "grupo": "Acesso 1"
    },
    "unidos-do-peruche": {
        "titulo": "Filhos de Mãe Preta",
        "compositores": "Mauro Pegoraro / Xuxa (Carnavalesco)",
        "interpretacao": "Toninho Penteado",
        "grupo": "Acesso 2"
    },
    "x-9-paulistana": {
        "titulo": "Se o Rio Muda de Curso Poderá Mudar o Curso da História",
        "compositores": "Amauri Santos (Carnavalesco)",
        "interpretacao": "Darlan Alves",
        "grupo": "Acesso 1"
    }
}

def update_csv():
    # Read existing entries from SAMBAS_CSV
    existing_entries = []
    if os.path.exists(SAMBAS_CSV):
        with open(SAMBAS_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing_entries = list(reader)

    # Filter out existing 2027 entries to avoid duplicates
    filtered_entries = [e for e in existing_entries if int(e["ano"]) != 2027]

    # Append new 2027 enredos from Liga-SP
    for slug, data in enredos_2027_map.items():
        filtered_entries.append({
            "escola_slug": slug,
            "ano": 2027,
            "tipo_registro": "enredo",
            "titulo_samba": data["titulo"],
            "compositores": data["compositores"],
            "interpretacao": data["interpretacao"],
            "grupo_carnaval": data["grupo"],
            "posicao": "",
            "pontos": "",
            "resultado_oficial": "Enredo Anunciado Carnaval 2027"
        })

    # Write back to SAMBAS_CSV
    fieldnames = ["escola_slug", "ano", "tipo_registro", "titulo_samba", "compositores", "interpretacao", "grupo_carnaval", "posicao", "pontos", "resultado_oficial"]
    with open(SAMBAS_CSV, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_entries)

    print(f"✅ Sucesso! {len(enredos_2027_map)} enredos oficiais do Carnaval 2027 adicionados ao {SAMBAS_CSV}!")

if __name__ == "__main__":
    update_csv()
