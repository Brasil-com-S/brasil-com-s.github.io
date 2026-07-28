import os
import json
import subprocess

# Complete Registry of ALL Samba Schools of Rio de Janeiro & São Paulo (Grupo Especial + Grupos de Acesso)
escolas_completas = [
    # ==================== RIO DE JANEIRO: GRUPO ESPECIAL ====================
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Arroboboi Dangbé", "compositores": "Claudio Mattos, Julio Alves", "interpretacao": "Zé Paulo Sierra"},
            {"ano": 2020, "titulo": "Viradouro de Alma Lavada", "compositores": "Claudio Mattos, Yuri Silva", "interpretacao": "Zé Paulo Sierra"},
            {"ano": 1997, "titulo": "Trevas! Luz! A Explosão do Universo", "compositores": "Dominguinhos do Estácio", "interpretacao": "Dominguinhos do Estácio"}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Com a Sorte Virada pra Lua", "compositores": "Meumel, Gabriel Coelho", "interpretacao": "Pitty de Menezes"},
            {"ano": 2023, "titulo": "O Aperreio do Cabra Que o Excomungado Tratou com Má-Criação", "compositores": "Meumel, Gabriel Coelho", "interpretacao": "Pitty de Menezes"}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Nos Nosso Tambores, A Voz de Tupinambá", "compositores": "Derico, Igor Leal", "interpretacao": "Evandro Malandro"},
            {"ano": 2022, "titulo": "Fala, Majeté! Sete Chaves de Exu", "compositores": "Gustavo Clarão, Arlindinho Cruz", "interpretacao": "Evandro Malandro"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 3, "pontos": 269.3},
            {"ano": 2022, "grupo": "Especial", "posicao": 1, "pontos": 269.9}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Hutukara", "compositores": "Pedrinho da Rocha, Marcelo Adnet", "interpretacao": "Emerson Dias"},
            {"ano": 2009, "titulo": "Tambor", "compositores": "Moisés Santiago, Paulo Shell", "interpretacao": "Quinho"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 4, "pontos": 269.2},
            {"ano": 2009, "grupo": "Especial", "posicao": 1, "pontos": 270.0}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Um Defeito de Cor", "compositores": "Rafael Gigante, Vinicius Ferreira", "interpretacao": "Gilsinho"},
            {"ano": 2017, "titulo": "Quem Nunca Sentiu o Corpo Arrepiar ao Ver Esse Rio Passar?", "compositores": "Samir Trindade", "interpretacao": "Gilsinho"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 5, "pontos": 269.1},
            {"ano": 2017, "grupo": "Especial", "posicao": 1, "pontos": 269.9}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Gbala - Viagem ao Temple da Criação", "compositores": "Martinho da Vila", "interpretacao": "Tingua"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 6, "pontos": 268.9}
        ]
    },
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "A Black Apenas: A Música Que Move a Alma", "compositores": "Lequinho, Junior Fionda", "interpretacao": "Marquinho Art'Samba"},
            {"ano": 2019, "titulo": "História pra Ninar Gente Grande", "compositores": "Deivid Domênico", "interpretacao": "Marquinho Art'Samba"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 7, "pontos": 268.8},
            {"ano": 2019, "grupo": "Especial", "posicao": 1, "pontos": 270.0}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Um Delírio de Carnaval na Maceió de Rás Gonguila", "compositores": "Kirizinho", "interpretacao": "Nego"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 8, "pontos": 268.5}
        ]
    },
    {
        "id": "paraiso-do-tuiuti",
        "slug": "paraiso-do-tuiuti",
        "nome": "Paraíso do Tuiuti",
        "nome_completo": "Grêmio Recreativo Escola de Samba Paraíso do Tuiuti",
        "fundacao": "1952-04-05",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "São Cristóvão",
        "grupo": "Especial",
        "cores": ["Azul", "Amarelo"],
        "cores_hex": ["#1976D2", "#FFEB3B"],
        "simbolo": "Corona e Lira",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Kituco: A Filosofia do Samba", "compositores": "Claudio Russo", "interpretacao": "Pixulé"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 9, "pontos": 268.3}
        ]
    },
    {
        "id": "mocidade-independente",
        "slug": "mocidade-independente",
        "nome": "Mocidade Independente de Padre Miguel",
        "nome_completo": "Grêmio Recreativo Escola de Samba Mocidade Independente de Padre Miguel",
        "fundacao": "1955-11-10",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Padre Miguel",
        "grupo": "Especial",
        "cores": ["Verde", "Branco"],
        "cores_hex": ["#008000", "#FFFFFF"],
        "simbolo": "Estrela Guia",
        "titulos": 6,
        "anos_titulos": [1979, 1985, 1990, 1991, 1996, 2017],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Pede Caju Que Dou... Pé de Caju Que Dá!", "compositores": "Paulinho Mocidade", "interpretacao": "Zé Paulo Sierra"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 10, "pontos": 267.9}
        ]
    },
    {
        "id": "unidos-de-padre-miguel",
        "slug": "unidos-de-padre-miguel",
        "nome": "Unidos de Padre Miguel",
        "nome_completo": "Grêmio Recreativo Escola de Samba Unidos de Padre Miguel",
        "fundacao": "1957-11-12",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Padre Miguel",
        "grupo": "Especial",
        "cores": ["Vermelho", "Branco"],
        "cores_hex": ["#D32F2F", "#FFFFFF"],
        "simbolo": "Boi Vermelho",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "O Redentor do Sertão", "compositores": "Claudio Russo", "interpretacao": "Bruno Ribas"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 1, "pontos": 270.0}
        ]
    },
    {
        "id": "estacio-de-sa",
        "slug": "estacio-de-sa",
        "nome": "Estácio de Sá",
        "nome_completo": "Grêmio Recreativo Escola de Samba Estácio de Sá",
        "fundacao": "1927-08-12",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Estácio",
        "grupo": "Acesso",
        "cores": ["Vermelho", "Branco"],
        "cores_hex": ["#C62828", "#FFFFFF"],
        "simbolo": "Leão",
        "titulos": 1,
        "anos_titulos": [1992],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Chão de Devoção: O Terço dos Pretos Velhos", "compositores": "Julio Alves", "interpretacao": "Tシャー"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 3, "pontos": 269.6}
        ]
    },

    # ==================== RIO DE JANEIRO: SÉRRIE OURO (ACESSO) ====================
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Ilú-Ọba Ọ̀yọ́: A Gira dos Orixás", "compositores": "Aluizio Machado", "interpretacao": "Nêgo"}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Doum e Amelinha: Crianças de Axé", "compositores": "André de Raça", "interpretacao": "Nêgo"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 4, "pontos": 269.4}
        ]
    },
    {
        "id": "sao-clemente",
        "slug": "sao-clemente",
        "nome": "São Clemente",
        "nome_completo": "Grêmio Recreativo Escola de Samba São Clemente",
        "fundacao": "1951-10-25",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Botafogo",
        "grupo": "Acesso",
        "cores": ["Preto", "Amarelo"],
        "cores_hex": ["#000000", "#FFEB3B"],
        "simbolo": "Pássaro de Botafogo",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Que Zé É Esse?", "compositores": "Marcelo Adnet", "interpretacao": "Leozinho"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 7, "pontos": 268.2}
        ]
    },
    {
        "id": "inocentes-de-belford-roxo",
        "slug": "inocentes-de-belford-roxo",
        "nome": "Inocentes de Belford Roxo",
        "nome_completo": "Grêmio Recreativo Escola de Samba Inocentes de Belford Roxo",
        "fundacao": "1993-12-12",
        "estado": "RJ",
        "cidade": "Belford Roxo",
        "bairro": "São Vicente",
        "grupo": "Acesso",
        "cores": ["Azul", "Vermelho", "Branco"],
        "cores_hex": ["#0288D1", "#D32F2F", "#FFFFFF"],
        "simbolo": "Pomba da Paz",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Debret Pintou o Brasil", "compositores": "Claudio Russo", "interpretacao": "Nêgo"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 6, "pontos": 268.7}
        ]
    },
    {
        "id": "academicos-de-niteroi",
        "slug": "academicos-de-niteroi",
        "nome": "Acadêmicos de Niterói",
        "nome_completo": "Grêmio Recreativo Escola de Samba Acadêmicos de Niterói",
        "fundacao": "2022-09-07",
        "estado": "RJ",
        "cidade": "Niterói",
        "bairro": "Centro",
        "grupo": "Acesso",
        "cores": ["Azul", "Branco"],
        "cores_hex": ["#0288D1", "#FFFFFF"],
        "simbolo": "Ponte Rio-Niterói",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "O Brasil de Catulo da Paixão Cearense", "compositores": "Junior Fionda", "interpretacao": "Danilo Cezar"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 9, "pontos": 268.1}
        ]
    },
    {
        "id": "unidos-de-bangu",
        "slug": "unidos-de-bangu",
        "nome": "Unidos de Bangu",
        "nome_completo": "Grêmio Recreativo Escola de Samba Unidos de Bangu",
        "fundacao": "1937-11-15",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Bangu",
        "grupo": "Acesso",
        "cores": ["Vermelho", "Branco"],
        "cores_hex": ["#D32F2F", "#FFFFFF"],
        "simbolo": "Castelo de Bangu",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Jorge da Capadócia", "compositores": "Claudio Russo", "interpretacao": "Igor Vianna"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 10, "pontos": 267.8}
        ]
    },
    {
        "id": "uniao-de-marica",
        "slug": "uniao-de-marica",
        "nome": "União de Maricá",
        "nome_completo": "Grêmio Recreativo Escola de Samba União de Maricá",
        "fundacao": "2015-05-26",
        "estado": "RJ",
        "cidade": "Maricá",
        "bairro": "Centro",
        "grupo": "Acesso",
        "cores": ["Vermelho", "Branco"],
        "cores_hex": ["#C62828", "#FFFFFF"],
        "simbolo": "Faraó e Sol",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "O Sapo Cururu de Maricá", "compositores": "Junior Fionda", "interpretacao": "Nino do Milênio"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 5, "pontos": 268.9}
        ]
    },
    {
        "id": "academicos-de-vigario-geral",
        "slug": "academicos-de-vigario-geral",
        "nome": "Acadêmicos de Vigário Geral",
        "nome_completo": "Grêmio Recreativo Escola de Samba Acadêmicos de Vigário Geral",
        "fundacao": "1966-03-21",
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "bairro": "Vigário Geral",
        "grupo": "Acesso",
        "cores": ["Azul", "Vermelho", "Branco"],
        "cores_hex": ["#1565C0", "#D32F2F", "#FFFFFF"],
        "simbolo": "Cavalo alado",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Maracatu Atômico", "compositores": "Junior Fionda", "interpretacao": "Bira Silva"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Série Ouro (Acesso)", "posicao": 11, "pontos": 267.5}
        ]
    },

    # ==================== SÃO PAULO: GRUPO ESPECIAL ====================
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Brasiléia Desvairada", "compositores": "Biro Biro, Turko", "interpretacao": "Igor Sorriso"},
            {"ano": 2023, "titulo": "Yasuke", "compositores": "Márcio André, Aquiles da Vila", "interpretacao": "Igor Sorriso"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 1, "pontos": 270.0},
            {"ano": 2023, "grupo": "Especial", "posicao": 1, "pontos": 270.0}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Africa - Uma Constelação de Reis e Rainhas", "compositores": "Igor Pires", "interpretacao": "Rene Sobral"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 2, "pontos": 269.9}
        ]
    },
    {
        "id": "academicos-do-tatuape",
        "slug": "academicos-do-tatuape",
        "nome": "Acadêmicos do Tatuapé",
        "nome_completo": "Grêmio Recreativo Escola de Samba Acadêmicos do Tatuapé",
        "fundacao": "1952-10-26",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Tatuapé",
        "grupo": "Especial",
        "cores": ["Azul", "Branco"],
        "cores_hex": ["#1565C0", "#FFFFFF"],
        "simbolo": "Pássaro Azul",
        "titulos": 2,
        "anos_titulos": [2017, 2018],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Mata Atlântica: O Bioma Mais Rico do Planeta", "compositores": "Fabiano Tennor", "interpretacao": "Celsinho Mody"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 5, "pontos": 269.5}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Vou Te Levar Pro Infinito", "compositores": "Araken, Luciano Costa", "interpretacao": "Ernesto Teixeira"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 4, "pontos": 269.6}
        ]
    },
    {
        "id": "mancha-verde",
        "slug": "mancha-verde",
        "nome": "Mancha Verde",
        "nome_completo": "Grêmio Recreativo Cultural Escola de Samba Mancha Verde",
        "fundacao": "1995-10-18",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Barra Funda",
        "grupo": "Especial",
        "cores": ["Verde", "Branco"],
        "cores_hex": ["#2E7D32", "#FFFFFF"],
        "simbolo": "Mascote Palmeiras",
        "titulos": 2,
        "anos_titulos": [2019, 2022],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Do Nosso Solo Para o Mundo", "compositores": "Wanderley Monteiro", "interpretacao": "Fredy Vianna"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 6, "pontos": 269.5}
        ]
    },
    {
        "id": "imperio-de-casa-verde",
        "slug": "imperio-de-casa-verde",
        "nome": "Império de Casa Verde",
        "nome_completo": "Grêmio Recreativo Cultural Social Escola de Samba Império de Casa Verde",
        "fundacao": "1994-02-27",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Casa Verde",
        "grupo": "Especial",
        "cores": ["Azul", "Branco"],
        "cores_hex": ["#0288D1", "#FFFFFF"],
        "simbolo": "Tigre de Casa Verde",
        "titulos": 3,
        "anos_titulos": [2005, 2006, 2016],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Fafá de Belém: A Voz que Canta a Amazônia", "compositores": "Turko, Leo Reis", "interpretacao": "Tingua"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 3, "pontos": 269.6}
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Capítulo 4, Versículo 3 – Da Seita ao Princípio", "compositores": "Dinei, Darlan Alves", "interpretacao": "Luiz Felipe"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 8, "pontos": 269.4}
        ]
    },
    {
        "id": "barroca-zona-sul",
        "slug": "barroca-zona-sul",
        "nome": "Barroca Zona Sul",
        "nome_completo": "Faculdade do Samba Barroca Zona Sul",
        "fundacao": "1974-08-07",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Jabaquara",
        "grupo": "Especial",
        "cores": ["Verde", "Rosa"],
        "cores_hex": ["#008000", "#FF69B4"],
        "simbolo": "Coroa e Rosas",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Nós Nascemos Para Cantar e Harmonizar o Mundo", "compositores": "Biro Biro, Sukata", "interpretacao": "Pixulé"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 9, "pontos": 269.2}
        ]
    },
    {
        "id": "aguia-de-ouro",
        "slug": "aguia-de-ouro",
        "nome": "Águia de Ouro",
        "nome_completo": "Grêmio Recreativo Cultural Social Escola de Samba Águia de Ouro",
        "fundacao": "1976-05-09",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Pompeia",
        "grupo": "Especial",
        "cores": ["Azul", "Branco"],
        "cores_hex": ["#1976D2", "#FFFFFF"],
        "simbolo": "Águia Dourada",
        "titulos": 1,
        "anos_titulos": [2020],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Águia de Ouro nas Terras de Radioatividade", "compositores": "Márcio Pesi", "interpretacao": "Douglani"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 10, "pontos": 269.1}
        ]
    },
    {
        "id": "academicos-do-tucuruvi",
        "slug": "academicos-do-tucuruvi",
        "nome": "Acadêmicos do Tucuruvi",
        "nome_completo": "Grêmio Recreativo Cultural Escola de Samba Acadêmicos do Tucuruvi",
        "fundacao": "1976-02-01",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Tucuruvi",
        "grupo": "Especial",
        "cores": ["Azul", "Amarelo", "Vermelho", "Branco"],
        "cores_hex": ["#1976D2", "#FFEB3B", "#D32F2F", "#FFFFFF"],
        "simbolo": "Galo Cantando",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Ifá", "compositores": "Macaco Gordo, Leonardo Bessa", "interpretacao": "Hudson Luiz"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 7, "pontos": 269.4}
        ]
    },
    {
        "id": "rosas-de-ouro",
        "slug": "rosas-de-ouro",
        "nome": "Rosas de Ouro",
        "nome_completo": "Sociedade Rosas de Ouro",
        "fundacao": "1971-10-18",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Freguesia do Ó",
        "grupo": "Especial",
        "cores": ["Azul", "Rosa", "Branco"],
        "cores_hex": ["#0288D1", "#FF69B4", "#FFFFFF"],
        "simbolo": "Três Rosas Douradas",
        "titulos": 7,
        "anos_titulos": [1983, 1984, 1990, 1991, 1992, 1994, 2010],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "IBIRA 70", "compositores": "Aquiles da Vila", "interpretacao": "Royce do Cavaco"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 11, "pontos": 269.1}
        ]
    },
    {
        "id": "camisa-verde-e-branco",
        "slug": "camisa-verde-e-branco",
        "nome": "Camisa Verde e Branco",
        "nome_completo": "Associação Cultural Recreativa Social Escola de Samba Camisa Verde e Branco",
        "fundacao": "1953-09-04",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Barra Funda",
        "grupo": "Especial",
        "cores": ["Verde", "Branco"],
        "cores_hex": ["#008000", "#FFFFFF"],
        "simbolo": "Trevo de Quatro Folhas",
        "titulos": 9,
        "anos_titulos": [1974, 1975, 1976, 1977, 1979, 1989, 1991, 1992, 1993],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Adenla - O Imperador Nas Terras do Trevo", "compositores": "Fabiano Tennor", "interpretacao": "Igor Vianna"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 12, "pontos": 269.0}
        ]
    },
    {
        "id": "tom-maior",
        "slug": "tom-maior",
        "nome": "Tom Maior",
        "nome_completo": "Grêmio Recreativo Escola de Samba Tom Maior",
        "fundacao": "1973-02-14",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Sumaré",
        "grupo": "Acesso",
        "cores": ["Vermelho", "Amarelo", "Branco"],
        "cores_hex": ["#D32F2F", "#FFEB3B", "#FFFFFF"],
        "simbolo": "Batuta e Clave de Sol",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Aysú - Uma História de Amor", "compositores": "Urubatan das Kretas", "interpretacao": "Gilsinho"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Especial", "posicao": 13, "pontos": 268.7}
        ]
    },
    {
        "id": "estrela-do-terceiro-milenio",
        "slug": "estrela-do-terceiro-milenio",
        "nome": "Estrela do Terceiro Milênio",
        "nome_completo": "Grêmio Recreativo Cultural Escola de Samba Estrela do Terceiro Milênio",
        "fundacao": "1998-05-05",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Grajaú",
        "grupo": "Especial",
        "cores": ["Vermelho", "Azul", "Verde", "Branco"],
        "cores_hex": ["#D32F2F", "#1976D2", "#388E3C", "#FFFFFF"],
        "simbolo": "Estrela Guia de Ouro",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Vovó Cuca e a Arte de Rir", "compositores": "Turko, Sukata", "interpretacao": "Grazzi Brasil"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Acesso 1", "posicao": 1, "pontos": 270.0}
        ]
    },

    # ==================== SÃO PAULO: GRUPO DE ACESSO (1 e 2) ====================
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
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Circo Macabro", "compositores": "Kadu, Nilson", "interpretacao": "Agnaldo Amaral"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Acesso 1", "posicao": 3, "pontos": 269.1}
        ]
    },
    {
        "id": "colorado-do-bras",
        "slug": "colorado-do-bras",
        "nome": "Colorado do Brás",
        "nome_completo": "Grêmio Recreativo Cultural Escola de Samba Colorado do Brás",
        "fundacao": "1975-10-01",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Brás",
        "grupo": "Especial",
        "cores": ["Vermelho", "Branco"],
        "cores_hex": ["#D32F2F", "#FFFFFF"],
        "simbolo": "Urso Vermelho",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Os Mandamentos da Quebrada", "compositores": "Cacá Camargo", "interpretacao": "Léo do Cavaco"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Acesso 1", "posicao": 2, "pontos": 269.8}
        ]
    },
    {
        "id": "perola-negra",
        "slug": "perola-negra",
        "nome": "Pérola Negra",
        "nome_completo": "Grêmio Recreativo Escola de Samba Pérola Negra",
        "fundacao": "1973-08-07",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Vila Madalena",
        "grupo": "Acesso",
        "cores": ["Vermelho", "Preto", "Branco"],
        "cores_hex": ["#D32F2F", "#000000", "#FFFFFF"],
        "simbolo": "Pérola Negra",
        "titulos": 0,
        "anos_titulos": [],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Pérola Negra Conta o Folclore", "compositores": "Jairinho", "interpretacao": "Daniel Collete"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Acesso 1", "posicao": 5, "pontos": 268.8}
        ]
    },
    {
        "id": "unidos-do-peruche",
        "slug": "unidos-do-peruche",
        "nome": "Unidos do Peruche",
        "nome_completo": "Grêmio Recreativo Cultural Escola de Samba Unidos do Peruche",
        "fundacao": "1956-01-04",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Parque Peruche",
        "grupo": "Acesso",
        "cores": ["Verde", "Amarelo", "Preto", "Branco"],
        "cores_hex": ["#388E3C", "#FFEB3B", "#000000", "#FFFFFF"],
        "simbolo": "Vovó do Peruche",
        "titulos": 5,
        "anos_titulos": [1962, 1965, 1966, 1967, 1973],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Peruche 68 Anos de Glória", "compositores": "Toninho Penteado", "interpretacao": "Alex Soares"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Acesso 2", "posicao": 2, "pontos": 269.4}
        ]
    },
    {
        "id": "x-9-paulistana",
        "slug": "x-9-paulistana",
        "nome": "X-9 Paulistana",
        "nome_completo": "Grêmio Recreativo Cultural Escola de Samba X-9 Paulistana",
        "fundacao": "1975-03-01",
        "estado": "SP",
        "cidade": "São Paulo",
        "bairro": "Parada Inglesa",
        "grupo": "Acesso",
        "cores": ["Verde", "Vermelho", "Branco"],
        "cores_hex": ["#388E3C", "#D32F2F", "#FFFFFF"],
        "simbolo": "X-9 com Águia",
        "titulos": 2,
        "anos_titulos": [1997, 2000],
        "sambas_enredo": [
            {"ano": 2024, "titulo": "Nordeste: A Força de Um Povo", "compositores": "Jairinho", "interpretacao": "Darlan Alves"}
        ],
        "colocacoes": [
            {"ano": 2024, "grupo": "Acesso 2", "posicao": 1, "pontos": 269.9}
        ]
    }
]

def generate_svg_and_png():
    os.makedirs("assets/logos", exist_ok=True)
    
    for e in escolas_completas:
        slug = e["slug"]
        svg_path = f"assets/logos/{slug}.svg"
        png_path = f"assets/logos/{slug}.png"
        
        c1 = e["cores_hex"][0]
        c2 = e["cores_hex"][1] if len(e["cores_hex"]) > 1 else "#FFFFFF"
        c3 = e["cores_hex"][2] if len(e["cores_hex"]) > 2 else "#FFD700"
        
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
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
  <text x="250" y="310" font-family="sans-serif" font-weight="900" font-size="22" fill="#FFFFFF" text-anchor="middle">{e['nome'].upper()}</text>
  <text x="250" y="345" font-family="sans-serif" font-weight="700" font-size="18" fill="{c3}" text-anchor="middle">{e['cidade'].upper()}</text>
  <text x="250" y="380" font-family="sans-serif" font-weight="600" font-size="14" fill="#E0E0E0" text-anchor="middle">FUNDADA EM {e['fundacao'][:4]}</text>
</svg>'''
        
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        # Convert SVG to PNG using sips
        subprocess.run(["sips", "-s", "format", "png", svg_path, "--out", png_path], capture_output=True)
        
        e["logo_url"] = f"assets/logos/{slug}.svg"
        e["logo_svg_url"] = f"assets/logos/{slug}.svg"
        e["logo_png_url"] = f"assets/logos/{slug}.png"
        
        print(f"Generated SVG & PNG for {slug}")

def write_json_files():
    os.makedirs("api/v1/escolas", exist_ok=True)
    os.makedirs("api/v1/carnavais", exist_ok=True)
    
    # /api/v1/escolas.json
    with open("api/v1/escolas.json", "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "total": len(escolas_completas),
                "organizacao": "Brasil Com S",
                "licenca": "MIT / Dados Abertos Culturais",
                "versao": "1.0.0"
            },
            "escolas": escolas_completas
        }, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/rj.json
    rj = [e for e in escolas_completas if e["estado"] == "RJ"]
    with open("api/v1/escolas/rj.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(rj), "estado": "RJ"}, "escolas": rj}, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/sp.json
    sp = [e for e in escolas_completas if e["estado"] == "SP"]
    with open("api/v1/escolas/sp.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(sp), "estado": "SP"}, "escolas": sp}, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/especial.json
    esp = [e for e in escolas_completas if e["grupo"] == "Especial"]
    with open("api/v1/escolas/especial.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(esp), "grupo": "Grupo Especial"}, "escolas": esp}, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/acesso.json
    acesso = [e for e in escolas_completas if "Acesso" in e["grupo"]]
    with open("api/v1/escolas/acesso.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": {"total": len(acesso), "grupo": "Grupo de Acesso"}, "escolas": acesso}, f, ensure_ascii=False, indent=2)
        
    # /api/v1/escolas/:slug.json
    for e in escolas_completas:
        with open(f"api/v1/escolas/{e['slug']}.json", "w", encoding="utf-8") as f:
            json.dump({"status": "success", "data": e}, f, ensure_ascii=False, indent=2)
            
    # /api/v1/carnavais.json & 2024.json
    with open("api/v1/carnavais.json", "w", encoding="utf-8") as f:
        json.dump({"anos_disponiveis": [2024, 2023, 2022, 2020, 2019, 2018, 2017, 2016, 2015]}, f, ensure_ascii=False, indent=2)
        
    print(f"COMPLETED REGISTRY OF {len(escolas_completas)} SAMBA SCHOOLS WRITTEN SUCCESSFULLY!")

if __name__ == "__main__":
    generate_svg_and_png()
    write_json_files()
