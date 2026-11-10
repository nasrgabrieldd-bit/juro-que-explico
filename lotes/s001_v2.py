"""Reescreve o JQE-S001 (juro simples × composto) no formato de cenas tipadas, para o motor genérico e a marca atual."""
import json

MARCA = json.load(open("/home/claude/juro-que-explico/marca/marca.json"))
P = "/home/claude/juro-que-explico/episodios/JQE-S001/roteiro.json"
AVISO = "Conteúdo educativo, não é recomendação financeira.\nNarração gerada por inteligência artificial."


def cena(id_, tipo, tts, leg, dados=None):
    c = {"id": id_, "tipo": tipo, "tts": tts, "leg": leg}
    if dados is not None:
        c["dados"] = dados
    return c


pts_s = [[m, round(1000 * (1 + 0.02 * m), 2)] for m in range(0, 37, 2)]
pts_c = [[m, round(1000 * 1.02 ** m, 2)] for m in range(0, 37, 2)]

r = {
    "id": "JQE-S001", "titulo": "Juro simples × juro composto: a mesma dívida, dois resultados", "formato": "vertical 9:16",
    "pilar": "Dinheiro no cotidiano", "tipo": "evergreen / explicador",
    "risco": "baixo — exemplo matemático ilustrativo, sem dado de mercado, sem recomendação",
    "nota_tela": "Exemplo ilustrativo · sem IOF, tarifas ou multas",
    "parametros": {"principal": 1000, "taxa_mensal": 0.02, "meses": 36, "anos_longo": 5},
    "numeros_livres": [], "numeros_fonte": [],
    "calculos": {
        "juro_mes": "1000 * 0.02", "juros_simples_36": "1000 * 0.02 * 36", "simples_36": "1000 * (1 + 0.02 * 36)",
        "composto_36": "1000 * 1.02 ** 36", "fator": "1 + 0.02", "ultimo_juros": "1000 * 1.02 ** 35 * 0.02",
        "diferenca_36": "composto_36 - simples_36",
        "simples_60": "1000 * (1 + 0.02 * 60)", "composto_60": "1000 * 1.02 ** 60", "diferenca_60": "composto_60 - simples_60",
    },
    "fontes": ["Cálculo próprio (juro simples M = C(1 + i·n) e composto M = C(1 + i)^n)"],
    "capa": {"linha1": "R$ 1.000 a 2% ao mês", "linha2": "viram quanto?", "destaque": "Simples × composto"},
    "cenas": [
        cena("hook", "numero_grande",
             "Você pega mil reais emprestados, a dois por cento ao mês. Três anos depois, quanto você deve?",
             "Você pega R$ 1.000 emprestados, a 2% ao mês. Três anos depois, quanto você deve?",
             {"valor": "R$ 1.000", "linhas": ["a 2% ao mês", "viram quanto em 3 anos?"]}),
        cena("pergunta", "versus", "A resposta depende de um detalhe: o juro é simples ou composto?",
             "A resposta depende de um detalhe: o juro é simples ou composto?",
             {"a": "simples", "b": "composto", "rotulo_a": "juro sobre o valor inicial", "rotulo_b": "juro sobre juro",
              "centro": "?"}),
        cena("simples1", "formula",
             "No juro simples, os dois por cento incidem sempre sobre os mil reais iniciais. São vinte reais todo mês.",
             "No juro simples, os 2% incidem sempre sobre os R$ 1.000 iniciais. São R$ 20 todo mês.",
             {"titulo": "Juro simples", "linha1": "2% de R$ 1.000", "resultado": "R$ 20/mês", "nota": "sempre sobre o valor inicial"}),
        cena("simples2", "formula",
             "Em trinta e seis meses, são setecentos e vinte reais de juros. A dívida chega a mil setecentos e vinte.",
             "Em 36 meses, são R$ 720 de juros. A dívida chega a R$ 1.720.",
             {"titulo": "Em 36 meses", "linha1": "R$ 20 × 36 = R$ 720", "resultado": "R$ 1.720", "nota": "dívida com juro simples"}),
        cena("composto1", "titulo",
             "No juro composto, o juro de cada mês entra na conta do mês seguinte. É juro sobre juro.",
             "No juro composto, o juro de cada mês entra na conta do mês seguinte. É juro sobre juro.",
             {"titulo": ["Juro composto", "juro sobre juro"], "subtitulo": "o juro de cada mês entra na conta do seguinte"}),
        cena("composto2", "barras",
             "No primeiro mês, são vinte reais de juros. No último, já são quarenta.",
             "No primeiro mês, são R$ 20 de juros. No último, já são R$ 40.",
             {"titulo": ["Juros do mês", "no juro composto"],
              "itens": [{"rotulo": "mês 1", "valor": 20, "texto": "R$ 20"},
                        {"rotulo": "mês 36", "valor": 40, "texto": "R$ 40", "destaque": True}],
              "nota": "o juro cresce porque a base cresce"}),
        cena("composto3", "linhas",
             "Resultado: dois mil e trinta e nove reais. A dívida dobrou.",
             "Resultado: R$ 2.039. A dívida dobrou.",
             {"titulo": "Dívida de R$ 1.000 a 2% ao mês", "x_rotulo": "meses", "x_ticks": [0, 12, 24, 36],
              "ymax": 2200, "ymin": 1000, "y_passo": 250,
              "series": [{"nome": "juro composto", "destaque": True, "velocidade": 0.6, "inicio": 0.2,
                          "rotulo_final": "R$ 2.039,89", "pontos": pts_c},
                         {"nome": "juro simples", "velocidade": 0.6, "inicio": 0.2,
                          "rotulo_final": "R$ 1.720", "pontos": pts_s}]}),
        cena("diferenca", "versus",
             "São quase trezentos e vinte reais a mais, só pela forma de calcular. E essa diferença cresce quanto maior o prazo.",
             "São quase R$ 320 a mais, só pela forma de calcular. E essa diferença cresce quanto maior o prazo.",
             {"a": "R$ 1.720", "b": "R$ 2.039,89", "rotulo_a": "simples", "rotulo_b": "composto", "centro": "+R$ 320"}),
        cena("prazo5", "barras",
             "E se o prazo fosse de cinco anos? No juro simples, dois mil e duzentos reais. No composto, três mil duzentos e oitenta e um. Mais de mil reais de diferença.",
             "E se o prazo fosse de 5 anos? No juro simples, R$ 2.200. No composto, R$ 3.281. Mais de R$ 1.000 de diferença.",
             {"titulo": ["E em 5 anos?"],
              "itens": [{"rotulo": "simples", "valor": 2200, "texto": "R$ 2.200"},
                        {"rotulo": "composto", "valor": 3281.03, "texto": "R$ 3.281", "destaque": True}],
              "nota": "mais de R$ 1.000 de diferença"}),
        cena("dica", "lista", "Antes de parcelar ou atrasar uma conta, olhe sempre a taxa ao mês e o prazo.",
             "Antes de parcelar ou atrasar uma conta, olhe sempre a taxa ao mês e o prazo.",
             {"titulo": ["Antes de parcelar"], "itens": ["olhe a taxa ao mês", "olhe o prazo", "pergunte se é composto"]}),
        cena("comenta", "cta", "Qual dívida você quer que eu explique no próximo vídeo? Escreve aqui nos comentários.",
             "Qual dívida você quer que eu explique no próximo vídeo? Escreve aqui nos comentários.",
             {"linhas": ["Qual dívida você quer", "que eu explique?"], "botao": "Comenta aqui embaixo"}),
        cena("assinatura", "assinatura", MARCA["assinatura_tts"], MARCA["assinatura_tts"]),
    ],
    "posts": {
        "youtube": {"titulo": "R$ 1.000 a 2% ao mês: juro simples ou composto?",
                    "texto": "Mesma dívida, mesma taxa: quase R$ 320 de diferença em 3 anos, e mais de R$ 1.000 em 5. Tudo depende de como o juro é calculado.\n\n"
                             "Juro simples: M = C × (1 + i × n) → R$ 1.720 em 36 meses\nJuro composto: M = C × (1 + i)^n → R$ 2.039,89 em 36 meses\n"
                             "Em 5 anos: R$ 2.200 × R$ 3.281\n\nExemplo ilustrativo com R$ 1.000 a 2% ao mês, sem IOF, tarifas ou multas. " + AVISO +
                             "\n\nQual dívida você quer que eu explique no próximo vídeo? Comenta aqui.\n\n#educacaofinanceira #juros #financaspessoais #shorts"},
        "instagram": {"texto": "Mesma dívida, mesma taxa: quase R$ 320 de diferença.\n\nR$ 1.000 a 2% ao mês, por 36 meses:\n• juro simples → R$ 1.720\n• juro composto → R$ 2.039,89\n\nEm 5 anos, a diferença passa de R$ 1.000.\n\nAntes de parcelar ou atrasar uma conta, olhe a taxa ao mês e o prazo.\n\nQual dívida você quer que eu explique no próximo vídeo? Comenta aqui 👇\n\nExemplo ilustrativo, sem IOF, tarifas ou multas. Narração gerada por IA.\n\n#educacaofinanceira #juros #jurocomposto #financaspessoais #dinheiro"},
        "tiktok": {"texto": "R$ 1.000 a 2% ao mês vira quanto em 3 anos? Juro simples × composto, na conta. Exemplo ilustrativo, narração por IA. #educacaofinanceira #juros #financaspessoais #dinheiro"},
    },
}
json.dump(r, open(P, "w"), ensure_ascii=False, indent=1)
print("ok", r["id"])
