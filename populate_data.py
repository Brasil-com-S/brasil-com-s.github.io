import os
import json
import glob
import shutil

# Master list of Samba Schools (RJ & SP - Especial e Acesso)
escolas = [
    {
        "id": "mangueira",
        "slug": "mangueira",
        "nome": "Estação Primeira de Mangueira",
        "nome_completo": "Grêmio Recreativo Escola de Samba Estação Primeira de Mangueira",
        "fundacao": "1928-04-28",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Mangueira",
        "grupo": "Especial",
        "cores": ["Verde", "Rosa"],
        "cores_hex": ["#008000", "#FF69B4"],
        "simbolo": "Surdo e Coroa Imperial",
        "titulos": 20,
        "anos_titulos": [1932, 1933, 1934, 1940, 1949, 1950, 1954, 1960, 1961, 1967, 1968, 1973, 1984, 1986, 1987, 1998, 2002, 2016, 2019],
        "logo_url": "assets/logos/mangueira.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "A Black Apenas: A Música Que Move a Alma", "compositores": "Lequinho, Junior Fionda, Gabriel Machado", "interpretacao": "Marquinho Art'Samba"},
            {"ano": 2019, "titulo": "História pra Ninar Gente Grande", "compositores": "Deivid Domênico, Tomaz Miranda, Mama, Luiz Carlos Máximo", "interpretacao": "Marquinho Art'Samba"},
            {"ano": 2016, "titulo": "Maria Bethânia: A Menina dos Olhos de Oyá", "compositores": "Alemão do Cavaco, Almyr Senna, Cadu, Lacyr D'Mangueira", "interpretacao": "Cinnara Leal, Marquinho Art'Samba"},
            {"ano": 2002, "titulo": "Brazil com 'Z' é pra Gringo de Fechar os Olhos. Brasil com 'S' é pra Você Viu!", "compositores": "Amendoim, Lequinho", "interpretacao": "Jamelão"},
            {"ano": 1984, "titulo": "Yes, Nós Temos Braguinha", "compositores": "Hélio Turco, Jurandir, Comprido, Artheme, Jodo", "interpretacao": "Jamelão"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 7, "pontos": 268.8},
            {"ano": 2023, "grupo": "Especial", "posicao": 5, "pontos": 269.1},
            {"ano": 2020, "grupo": "Especial", "posicao": 6, "pontos": 268.9},
            {"ano": 2019, "grupo": "Especial", "posicao": 1, "pontos": 270.0},
            {"ano": 2016, "grupo": "Especial", "posicao": 1, "pontos": 269.8}
        ]
    },
    {
        "id": "portela",
        "slug": "portela",
        "nome": "Portela",
        "nome_completo": "Grêmio Recreativo Escola de Samba Portela",
        "fundacao": "1923-04-11",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Madureira",
        "grupo": "Especial",
        "cores": ["Azul", "Branco"],
        "cores_hex": ["#0047AB", "#FFFFFF"],
        "simbolo": "Águia Majestosa",
        "titulos": 22,
        "anos_titulos": [1935, 1939, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1951, 1953, 1957, 1958, 1959, 1960, 1962, 1964, 1966, 1970, 1980, 1984, 2017],
        "logo_url": "assets/logos/portela.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Um Defeito de Cor", "compositores": "Rafael Gigante, Vinicius Ferreira, Wanderley Monteiro", "interpretacao": "Gilsinho"},
            {"ano": 2017, "titulo": "Quem Nunca Sentiu o Corpo Arrepiar ao Ver Esse Rio Passar?", "compositores": "Samir Trindade, Elson Ramires, Neyzinho do Cavaco", "interpretacao": "Gilsinho"},
            {"ano": 1980, "titulo": "Hoje Tem Marmelada", "compositores": "David Corrêa, Jorge Macedo", "interpretacao": "Silvinho da Portela"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 5, "pontos": 269.1},
            {"ano": 2023, "grupo": "Especial", "posicao": 10, "pontos": 267.7},
            {"ano": 2017, "grupo": "Especial", "posicao": 1, "pontos": 269.9}
        ]
    },
    {
        "id": "beija-flor",
        "slug": "beija-flor",
        "nome": "Beija-Flor de Nilópolis",
        "nome_completo": "Grêmio Recreativo Escola de Samba Beija-Flor de Nilópolis",
        "fundacao": "1948-12-25",
        "estado": "RJ",
        "cidade": "Nilópolis",
        "bairro": "Centro",
        "grupo": "Especial",
        "cores": ["Azul", "Branco"],
        "cores_hex": ["#002366", "#FFFFFF"],
        "simbolo": "Beija-Flor",
        "titulos": 14,
        "anos_titulos": [1976, 1977, 1978, 1983, 1998, 2003, 2004, 2005, 2007, 2008, 2011, 2015, 2018],
        "logo_url": "assets/logos/beija-flor.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Um Delírio de Carnaval na Maceió de Rás Gonguila", "compositores": "Kirizinho, Lucas Guedes, Marquinhos da Hora", "interpretacao": "Nego"},
            {"ano": 2018, "titulo": "Monstro É Aquele Que Não Sabe Amar. Os Filhos Abandonados da Pátria Que Os Pariu", "compositores": "Di Menor FM, Kirizinho, Diego Oliveira", "interpretacao": "Nego, Samir Trindade"},
            {"ano": 1989, "titulo": "Ratos e Urubus, Comprem Meu Vazio", "compositores": "Glyvis, Betinho, Zé Maria", "interpretacao": "Nego"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 8, "pontos": 268.5},
            {"ano": 2018, "grupo": "Especial", "posicao": 1, "pontos": 269.6}
        ]
    },
    {
        "id": "salgueiro",
        "slug": "salgueiro",
        "nome": "Acadêmicos do Salgueiro",
        "nome_completo": "Grêmio Recreativo Escola de Samba Acadêmicos do Salgueiro",
        "fundacao": "1953-03-05",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Andaraí",
        "grupo": "Especial",
        "cores": ["Vermelho", "Branco"],
        "cores_hex": ["#D32F2F", "#FFFFFF"],
        "simbolo": "Tambor e Tocha",
        "titulos": 9,
        "anos_titulos": [1960, 1963, 1965, 1969, 1971, 1974, 1975, 1993, 2009],
        "logo_url": "assets/logos/salgueiro.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Hutukara", "compositores": "Pedrinho da Rocha, Marcelo Adnet, Guilherme Sá", "interpretacao": "Emerson Dias"},
            {"ano": 2009, "titulo": "Tambor", "compositores": "Moisés Santiago, Paulo Shell, Leandro Thompson", "interpretacao": "Quinho"},
            {"ano": 1993, "titulo": "Peguei Um Ita no Norte", "compositores": "Demá Chagas, Arizão, Celso Trindade, Bala", "interpretacao": "Quinho"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 4, "pontos": 269.2},
            {"ano": 2009, "grupo": "Especial", "posicao": 1, "pontos": 270.0}
        ]
    },
    {
        "id": "viradouro",
        "slug": "viradouro",
        "nome": "Unidos do Viradouro",
        "nome_completo": "Grêmio Recreativo Escola de Samba Unidos do Viradouro",
        "fundacao": "1946-06-24",
        "estado": "RJ",
        "cidade": "Niterói",
        "bairro": "Barreto",
        "grupo": "Especial",
        "cores": ["Vermelho", "Branco"],
        "cores_hex": ["#C62828", "#FFFFFF"],
        "simbolo": "Coroa e Aperto de Mãos",
        "titulos": 3,
        "anos_titulos": [1997, 2020, 2024],
        "logo_url": "assets/logos/viradouro.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Arroboboi Dangbé", "compositores": "Claudio Mattos, Julio Alves, Thiago Meiners, Manolo", "interpretacao": "Zé Paulo Sierra"},
            {"ano": 2020, "titulo": "Viradouro de Alma Lavada", "compositores": "Claudio Mattos, Yuri Silva, Robinho, Flavinho Avellar", "interpretacao": "Zé Paulo Sierra"},
            {"ano": 1997, "titulo": "Trevas! Luz! A Explosão do Universo", "compositores": "Dominguinhos do Estácio, Dom Panides, Geraldo", "interpretacao": "Dominguinhos do Estácio"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 1, "pontos": 270.0},
            {"ano": 2023, "grupo": "Especial", "posicao": 2, "pontos": 269.7},
            {"ano": 2020, "grupo": "Especial", "posicao": 1, "pontos": 269.6}
        ]
    },
    {
        "id": "imperatriz",
        "slug": "imperatriz",
        "nome": "Imperatriz Leopoldinense",
        "nome_completo": "Grêmio Recreativo Escola de Samba Imperatriz Leopoldinense",
        "fundacao": "1959-03-06",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Ramos",
        "grupo": "Especial",
        "cores": ["Verde", "Branco", "Ouro"],
        "cores_hex": ["#2E7D32", "#FFFFFF", "#FFD700"],
        "simbolo": "Coroa da Imperatriz",
        "titulos": 9,
        "anos_titulos": [1980, 1981, 1989, 1994, 1995, 1999, 2000, 2001, 2023],
        "logo_url": "assets/logos/imperatriz.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Com a Sorte Virada pra Lua Segundo o Testamento da Cigana Esmeralda", "compositores": "Meumel, Gabriel Coelho, Luiz Brinco", "interpretacao": "Pitty de Menezes"},
            {"ano": 2023, "titulo": "O Aperreio do Cabra Que o Excomungado Tratou com Má-Criação e o Santíssimo Com Benevolência", "compositores": "Meumel, Gabriel Coelho, Luiz Brinco", "interpretacao": "Pitty de Menezes"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 2, "pontos": 269.8},
            {"ano": 2023, "grupo": "Especial", "posicao": 1, "pontos": 269.8}
        ]
    },
    {
        "id": "grande-rio",
        "slug": "grande-rio",
        "nome": "Acadêmicos do Grande Rio",
        "nome_completo": "Grêmio Recreativo Escola de Samba Acadêmicos do Grande Rio",
        "fundacao": "1988-09-22",
        "estado": "RJ",
        "cidade": "Duque de Caxias",
        "bairro": "25 de Agosto",
        "grupo": "Especial",
        "cores": ["Verde", "Vermelho", "Branco"],
        "cores_hex": ["#388E3C", "#D32F2F", "#FFFFFF"],
        "simbolo": "Coroa e Brasão de Caxias",
        "titulos": 1,
        "anos_titulos": [2022],
        "logo_url": "assets/logos/grande-rio.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Nos Nosso Tambores, A Voz de Tupinambá", "compositores": "Derico, Igor Leal, Robson Moratelli", "interpretacao": "Evandro Malandro"},
            {"ano": 2022, "titulo": "Fala, Majeté! Sete Chaves de Exu", "compositores": "Gustavo Clarão, Arlindinho Cruz, Jr. Fragga, Claudio Mattos", "interpretacao": "Evandro Malandro"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 3, "pontos": 269.3},
            {"ano": 2022, "grupo": "Especial", "posicao": 1, "pontos": 269.9}
        ]
    },
    {
        "id": "vila-isabel",
        "slug": "vila-isabel",
        "nome": "Unidos de Vila Isabel",
        "nome_completo": "Grêmio Recreativo Escola de Samba Unidos de Vila Isabel",
        "fundacao": "1946-04-04",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Vila Isabel",
        "grupo": "Especial",
        "cores": ["Azul", "Branco"],
        "cores_hex": ["#0288D1", "#FFFFFF"],
        "simbolo": "Partitura Musical e Noel Rosa",
        "titulos": 3,
        "anos_titulos": [1988, 2006, 2013],
        "logo_url": "assets/logos/vila-isabel.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Gbala - Viagem ao Temple da Criação", "compositores": "Martinho da Vila", "interpretacao": "Tingua"},
            {"ano": 2013, "titulo": "A Vila Canta o Brasil Celeiro do Mundo - Água no Feijão Que Chegou Mais Um", "compositores": "Martinho da Vila, Arlindo Cruz, André Diniz", "interpretacao": "Tingua"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 6, "pontos": 268.9},
            {"ano": 2013, "grupo": "Especial", "posicao": 1, "pontos": 299.7}
        ]
    },
    {
        "id": "vai-vai",
        "slug": "vai-vai",
        "nome": "Vai-Vai",
        "nome_completo": "Grêmio Recreativo Cultural Social Escola de Samba Vai-Vai",
        "fundacao": "1930-01-01",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Bela Vista (Bixiga)",
        "grupo": "Especial",
        "cores": ["Preto", "Branco"],
        "cores_hex": ["#000000", "#FFFFFF"],
        "simbolo": "Harpa e Coroa",
        "titulos": 15,
        "anos_titulos": [1978, 1981, 1982, 1986, 1987, 1988, 1993, 1996, 1998, 1999, 2000, 2008, 2011, 2015],
        "logo_url": "assets/logos/vai-vai.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Capítulo 4, Versículo 3 – Da Seita ao Princípio", "compositores": "Dinei, Darlan Alves, Rodrigo Atômico", "interpretacao": "Luiz Felipe"},
            {"ano": 2015, "titulo": "Simplesmente Elis - A Fábula de Uma Voz Que Voou", "compositores": "Zeca do Cavaco, Zé Carlinhos, Ronaldinho", "interpretacao": "Wander Pires"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 8, "pontos": 269.4},
            {"ano": 2015, "grupo": "Especial", "posicao": 1, "pontos": 269.9}
        ]
    },
    {
        "id": "mocidade-alegre",
        "slug": "mocidade-alegre",
        "nome": "Mocidade Alegre",
        "nome_completo": "Grêmio Recreativo Cultural Escola de Samba Mocidade Alegre",
        "fundacao": "1967-09-24",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Limão",
        "grupo": "Especial",
        "cores": ["Vermelho", "Verde", "Branco"],
        "cores_hex": ["#D32F2F", "#388E3C", "#FFFFFF"],
        "simbolo": "Tambor e Par de Dançarinos",
        "titulos": 12,
        "anos_titulos": [1971, 1972, 1973, 1980, 2004, 2007, 2009, 2012, 2013, 2014, 2023, 2024],
        "logo_url": "assets/logos/mocidade-alegre.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Brasiléia Desvairada: A Busca de Mário de Andrade pelo País", "compositores": "Biro Biro, Turko, Rafa Do Cavaco", "interpretacao": "Igor Sorriso"},
            {"ano": 2023, "titulo": "Yasuke", "compositores": "Márcio André, Aquiles da Vila, Fabiano Sorriso", "interpretacao": "Igor Sorriso"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 1, "pontos": 270.0},
            {"ano": 2023, "grupo": "Especial", "posicao": 1, "pontos": 270.0}
        ]
    },
    {
        "id": "gavioes-da-fiel",
        "slug": "gavioes-da-fiel",
        "nome": "Gaviões da Fiel",
        "nome_completo": "Grêmio Gaviões da Fiel Torcida",
        "fundacao": "1969-07-01",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Bom Retiro",
        "grupo": "Especial",
        "cores": ["Preto", "Branco"],
        "cores_hex": ["#000000", "#FFFFFF"],
        "simbolo": "Gavião em Voo",
        "titulos": 4,
        "anos_titulos": [1995, 1999, 2002, 2003],
        "logo_url": "assets/logos/gavioes-da-fiel.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Vou Te Levar Pro Infinito", "compositores": "Araken, Luciano Costa, Renato do Pandeiro", "interpretacao": "Ernesto Teixeira"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 4, "pontos": 269.6}
        ]
    },
    {
        "id": "dragoes-da-real",
        "slug": "dragoes-da-real",
        "nome": "Dragões da Real",
        "nome_completo": "Grêmio Recreativo Cultural Escola de Samba Dragões da Real",
        "fundacao": "2000-03-17",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Vila Anastácio",
        "grupo": "Especial",
        "cores": ["Vermelho", "Branco", "Preto"],
        "cores_hex": ["#D32F2F", "#FFFFFF", "#000000"],
        "simbolo": "Dragão Alado",
        "titulos": 0,
        "anos_titulos": [],
        "logo_url": "assets/logos/dragoes-da-real.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Africa - Uma Constelação de Reis e Rainhas", "compositores": "Igor Pires, Robson Valente", "interpretacao": "Rene Sobral"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 2, "pontos": 269.9}
        ]
    },
    {
        "id": "imperio-serrano",
        "slug": "imperio-serrano",
        "nome": "Império Serrano",
        "nome_completo": "Grêmio Recreativo Escola de Samba Império Serrano",
        "fundacao": "1947-03-23",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Madureira",
        "grupo": "Acesso",
        "cores": ["Verde", "Branco"],
        "cores_hex": ["#2E7D32", "#FFFFFF"],
        "simbolo": "Coroa Imperial",
        "titulos": 9,
        "anos_titulos": [1948, 1949, 1950, 1951, 1956, 1960, 1972, 1982],
        "logo_url": "assets/logos/imperio-serrano.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Ilú-Ọba Ọ̀yọ́: A Gira dos Orixás", "compositores": "Aluizio Machado, Henrique Hoffmann", "interpretacao": "Nêgo"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 2, "pontos": 269.8}
        ]
    },
    {
        "id": "uniao-da-ilha",
        "slug": "uniao-da-ilha",
        "nome": "União da Ilha do Governador",
        "nome_completo": "Grêmio Recreativo Escola de Samba União da Ilha do Governador",
        "fundacao": "1953-03-07",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Cacuia",
        "grupo": "Acesso",
        "cores": ["Azul", "Vermelho", "Branco"],
        "cores_hex": ["#1976D2", "#D32F2F", "#FFFFFF"],
        "simbolo": "Sol e Mar",
        "titulos": 0,
        "anos_titulos": [],
        "logo_url": "assets/logos/uniao-da-ilha.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Doum e Amelinha: Crianças de Axé", "compositores": "André de Raça, Bruno Revelação", "interpretacao": "Nêgo"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 4, "pontos": 269.4}
        ]
    },
    {
        "id": "nene-de-vila-matilde",
        "slug": "nene-de-vila-matilde",
        "nome": "Nenê de Vila Matilde",
        "nome_completo": "Grêmio Recreativo Cultural Escola de Samba Nenê de Vila Matilde",
        "fundacao": "1949-05-03",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Vila Matilde",
        "grupo": "Acesso",
        "cores": ["Azul", "Branco"],
        "cores_hex": ["#1565C0", "#FFFFFF"],
        "simbolo": "Águia e Árvore",
        "titulos": 11,
        "anos_titulos": [1956, 1958, 1959, 1960, 1963, 1965, 1968, 1969, 1970, 1985, 2001],
        "logo_url": "assets/logos/nene-de-vila-matilde.jpg",
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Circo Macabro: O Show Não Pode Parar", "compositores": "Kadu, Nilson, Portuga", "interpretacao": "Agnaldo Amaral"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Acesso 1", "posicao": 3, "pontos": 269.1}
        ]
    }
]

def ensure_logos_and_svgs():
    os.makedirs("assets/logos", exist_ok=True)
    brain_dir = "/Users/outis/.gemini/antigravity/brain/27bc9467-7325-4fdf-827a-d8f3e6e619d9"
    
    mapping = {
        "mangueira": "logo_mangueira_*.jpg",
        "portela": "logo_portela_*.jpg",
        "beija-flor": "logo_beija_flor_*.jpg",
        "vai-vai": "logo_vai_vai_*.jpg",
        "salgueiro": "logo_salgueiro_*.jpg",
        "mocidade-alegre": "logo_mocidade_alegre_*.jpg"
    }
    
    for slug, pattern in mapping.items():
        matches = glob.glob(os.path.join(brain_dir, pattern))
        if matches:
            dest = f"assets/logos/{slug}.jpg"
            shutil.copyfile(matches[0], dest)
            print(f"Copied {matches[0]} to {dest}")
            
    for e in escolas:
        slug = e["slug"]
        jpg_path = f"assets/logos/{slug}.jpg"
        svg_path = f"assets/logos/{slug}.svg"
        
        if not os.path.exists(jpg_path) and not os.path.exists(svg_path):
            c1 = e["cores_hex"][0]
            c2 = e["cores_hex"][1] if len(e["cores_hex"]) > 1 else "#FFFFFF"
            c3 = e["cores_hex"][2] if len(e["cores_hex"]) > 2 else "#FFD700"
            
            svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
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
  <text x="250" y="310" font-family="sans-serif" font-weight="900" font-size="24" fill="#FFFFFF" text-anchor="middle">{e['nome'].upper()}</text>
  <text x="250" y="345" font-family="sans-serif" font-weight="700" font-size="18" fill="{c3}" text-anchor="middle">{e['cidade'].upper()}</text>
  <text x="250" y="380" font-family="sans-serif" font-weight="600" font-size="14" fill="#E0E0E0" text-anchor="middle">FUNDADA EM {e['fundacao'][:4]}</text>
</svg>'''
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            e["logo_url"] = f"assets/logos/{slug}.svg"
            print(f"Generated SVG logo for {slug}")
        elif os.path.exists(jpg_path):
            e["logo_url"] = f"assets/logos/{slug}.jpg"
        elif os.path.exists(svg_path):
            e["logo_url"] = f"assets/logos/{slug}.svg"

def write_json_files():
    os.makedirs("api/v1/escolas", exist_ok=True)
    os.makedirs("api/v1/carnavais", exist_ok=True)
    
    all_escolas_payload = {
        "metadata": {
            "total": len(escolas),
            "organizacao": "Brasil Com S",
            "licenca": "MIT / Dados Abertos Culturais",
            "versao": "1.0.0"
        },
        "escolas": escolas
    }
    with open("api/v1/escolas.json", "w", encoding="utf-8") as f:
        json.dump(all_escolas_payload, f, ensure_ascii=False, indent=2)
        
    rj_escolas = [e for e in escolas if e["estado"] == "RJ"]
    with open("api/v1/escolas/rj.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(rj_escolas), "estado": "RJ"}, "escolas": rj_escolas}, f, ensure_ascii=False, indent=2)
        
    sp_escolas = [e for e in escolas if e["estado"] == "SP"]
    with open("api/v1/escolas/sp.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(sp_escolas), "estado": "SP"}, "escolas": sp_escolas}, f, ensure_ascii=False, indent=2)
        
    esp_escolas = [e for e in escolas if e["grupo"] == "Especial"]
    with open("api/v1/escolas/especial.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(esp_escolas), "grupo": "Grupo Especial"}, "escolas": esp_escolas}, f, ensure_ascii=False, indent=2)
        
    acesso_escolas = [e for e in escolas if "Acesso" in e["grupo"]]
    with open("api/v1/escolas/acesso.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(acesso_escolas), "grupo": "Grupo de Acesso"}, "escolas": acesso_escolas}, f, ensure_ascii=False, indent=2)
        
    for e in escolas:
        slug = e["slug"]
        with open(f"api/v1/escolas/{slug}.json", "w", encoding="utf-8") as f:
            json.dump({"status": "success", "data": e}, f, ensure_ascii=False, indent=2)
            
    carnavais_index = {
        "anos_disponiveis": [2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015]
    }
    with open("api/v1/carnavais.json", "w", encoding="utf-8") as f:
        json.dump(carnavais_index, f, ensure_ascii=False, indent=2)
        
    carnaval_2024 = {
        "ano": 2024,
        "campeã_rj": "Unidos do Viradouro",
        "campeã_sp": "Mocidade Alegre",
        "resultados": [
            {"escola": "Unidos do Viradouro", "estado": "RJ", "posicao": 1, "pontos": 270.0},
            {"escola": "Imperatriz Leopoldinense", "estado": "RJ", "posicao": 2, "pontos": 269.8},
            {"escola": "Acadêmicos do Grande Rio", "estado": "RJ", "posicao": 3, "pontos": 269.3},
            {"escola": "Mocidade Alegre", "estado": "SP", "posicao": 1, "pontos": 270.0},
            {"escola": "Dragões da Real", "estado": "SP", "posicao": 2, "pontos": 269.9}
        ]
    }
    with open("api/v1/carnavais/2024.json", "w", encoding="utf-8") as f:
        json.dump(carnaval_2024, f, ensure_ascii=False, indent=2)
        
    print("All JSON endpoint files created successfully!")

if __name__ == "__main__":
    ensure_logos_and_svgs()
    write_json_files()
