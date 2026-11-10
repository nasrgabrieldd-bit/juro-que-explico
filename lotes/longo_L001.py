"""Gera o vídeo longo JQE-L001 (YouTube, 16:9) e os cortes JQE-L001-P1..P3 (9:16, TikTok/Instagram).
Tema: juros compostos na prática — ponto de virada, por que começar cedo, quanto investir para viver de dividendos.
Uso: python3 lotes/longo_L001.py"""
import json
import os

REPO = "/home/claude/juro-que-explico/episodios"
AVISO = "Conteúdo educativo, não é recomendação financeira.\nNarração gerada por inteligência artificial."
I, A = 0.008, 500


def fv(a, i, n):
    return a * ((1 + i) ** n - 1) / i


def cena(id_, tipo, tts, leg, dados=None):
    c = {"id": id_, "tipo": tipo, "tts": tts, "leg": leg}
    if dados is not None:
        c["dados"] = dados
    return c


MARCA = json.load(open("/home/claude/juro-que-explico/marca/marca.json"))
ASS = cena("assinatura", "assinatura", MARCA["assinatura_tts"], MARCA["assinatura_tts"])

parametros = {"aporte": 500, "taxa_mes": 0.008, "anos": 30, "anos_seguintes": 20, "dy": 0.08, "dy_baixo": 0.06,
              "dy_alto": 0.10, "renda_mes": 1000, "dividendo_acao": 3, "preco_baixo": 40, "preco_alto": 60,
              "mes_juros_passam_aportes": 159}
calculos = {
    "taxa_ano": "(1.008 ** 12 - 1) * 100",
    "juros_mes1": "500 * 0.008",
    "saldo_virada": "500 / 0.008",
    "mes_virada": "log(2) / log(1.008)",
    "juros_120": "0.008 * 500 * (1.008 ** 120 - 1) / 0.008",
    "fv_159": "500 * (1.008 ** 159 - 1) / 0.008", "aportado_159": "500 * 159",
    "juros_159": "fv_159 - aportado_159",
    "fv_158": "500 * (1.008 ** 158 - 1) / 0.008", "juros_158": "fv_158 - 500 * 158",
    "anos_159": "floor(159 / 12)",
    "fv30": "500 * (1.008 ** 360 - 1) / 0.008", "fv30_mi": "fv30 / 1000000",
    "aportado30_mil": "500 * 360 / 1000", "juros30_mil": "(fv30 - 180000) / 1000",
    "prim10_mil": "500 * (1.008 ** 360 - 1.008 ** 240) / 0.008 / 1000",
    "ult20_mil": "500 * (1.008 ** 240 - 1) / 0.008 / 1000",
    "aporte10_mil": "500 * 120 / 1000", "aporte20_mil": "500 * 240 / 1000",
    "aporte_ano": "500 * 12",
    "ano1_mil": "500 * (1.008 ** 360 - 1.008 ** 348) / 0.008 / 1000",
    "ano10_mil": "500 * (1.008 ** 252 - 1.008 ** 240) / 0.008 / 1000",
    "ano20_mil": "500 * (1.008 ** 132 - 1.008 ** 120) / 0.008 / 1000",
    "ano30": "500 * (1.008 ** 12 - 1) / 0.008",
    "renda_ano": "1000 * 12",
    "capital_8_mil": "12000 / 0.08 / 1000", "capital_6_mil": "12000 / 0.06 / 1000", "capital_10_mil": "12000 / 0.10 / 1000",
    "tempo_8": "log(1 + 150000 * 0.008 / 500) / log(1.008)", "tempo_8_anos": "tempo_8 / 12",
    "teto": "3 / 0.06", "dy_40": "3 / 40 * 100", "dy_60": "3 / 60 * 100",
}
numeros_fonte = [
    {"descricao": "Décio Bazin publicou 'Faça Fortuna com Ações Antes que seja Tarde' em 1992", "valor": 1992,
     "url": "https://investidor10.com.br/conteudo/estrategia-de-decio-bazin/", "data_referencia": "2026-08-05"},
    {"descricao": "Critério de Bazin: dividend yield mínimo de 6% ao ano; preço-teto = proventos ÷ 0,06", "valor": 6,
     "url": "https://www.infomoney.com.br/?p=1982816", "data_referencia": "2023"},
]
fontes = ["Cálculo próprio: VF = A × ((1 + i)^n − 1) / i; ponto de virada n = ln 2 / ln(1 + i); capital = renda anual ÷ DY",
          "Método Bazin: InfoMoney e Investidor10 (links em numeros_fonte)"]
NOTA = "Exemplo ilustrativo · taxa hipotética, sem impostos nem inflação"

# ---------------- cenas ----------------
pts_juros = [[m, round(I * fv(A, I, m), 2)] for m in range(0, 121, 4)]
pts_aporte = [[m, 500] for m in range(0, 121, 4)]

C = {}
C["i1"] = cena("i1", "numero_grande",
               "Quinhentos reais por mês, durante trinta anos, podem passar de um milhão de reais. E o surpreendente é de onde ele vem.",
               "R$ 500 por mês, durante 30 anos, podem passar de R$ 1 milhão. E o surpreendente é de onde ele vem.",
               {"valor": "R$ 1,04 milhão", "linhas": ["com R$ 500 por mês", "durante 30 anos"]})
C["i2"] = cena("i2", "lista",
               "Este vídeo tem três partes. Primeiro, o ponto de virada, quando os juros começam a trabalhar mais que você. Depois, por que os primeiros aportes valem tanto. E no fim, quanto dinheiro você precisa para receber mil reais por mês em dividendos. O exemplo é sempre o mesmo: quinhentos reais por mês, rendendo zero vírgula oito por cento ao mês, cerca de dez por cento ao ano.",
               "Três partes: o ponto de virada dos juros, por que os primeiros aportes valem tanto, e quanto investir para receber R$ 1.000 por mês em dividendos. Exemplo: R$ 500 por mês a 0,8% ao mês, cerca de 10% ao ano.",
               {"titulo": ["Três partes"], "itens": ["o ponto de virada", "por que começar cedo", "viver de dividendos"]})

# bloco 1 — ponto de virada
C["b1_hook"] = cena("b1_hook", "numero_grande",
                    "Tem um mês em que os juros rendem mais que o seu aporte. É o ponto de virada. E dá para calcular quando ele chega.",
                    "Tem um mês em que os juros rendem mais que o seu aporte. É o ponto de virada. E dá para calcular.",
                    {"valor": "Mês 87", "linhas": ["os juros do mês", "passam o seu aporte"]})
C["b1_mes1"] = cena("b1_mes1", "formula",
                    "No primeiro mês, você coloca quinhentos reais e eles rendem zero vírgula oito por cento. São quatro reais de juros. Quase nada. Quem está fazendo o trabalho é você.",
                    "No primeiro mês, R$ 500 rendem 0,8%: R$ 4 de juros. Quase nada. Quem faz o trabalho é você.",
                    {"titulo": "No primeiro mês", "linha1": "R$ 500 × 0,8%", "resultado": "= R$ 4", "nota": "de juros no mês"})
C["b1_conta"] = cena("b1_conta", "formula",
                     "Os juros do mês chegam a quinhentos reais quando o saldo bate sessenta e dois mil e quinhentos reais. Porque zero vírgula oito por cento de sessenta e dois mil e quinhentos dá exatamente quinhentos.",
                     "Os juros do mês chegam a R$ 500 quando o saldo bate R$ 62.500. Porque 0,8% de R$ 62.500 dá exatamente R$ 500.",
                     {"titulo": "Juros do mês = R$ 500?", "linha1": "R$ 500 ÷ 0,8%", "resultado": "R$ 62.500", "nota": "saldo necessário"})
C["b1_grafico"] = cena("b1_grafico", "linhas",
                       "No gráfico, a linha verde são os juros de cada mês, e a cinza é o seu aporte. Elas se cruzam no mês oitenta e sete, depois de sete anos e três meses. A partir daí, os juros sozinhos colocam mais dinheiro na conta do que você.",
                       "A linha verde são os juros de cada mês; a cinza, o seu aporte. Elas se cruzam no mês 87, depois de 7 anos e 3 meses. Daí em diante, os juros colocam mais dinheiro que você.",
                       {"titulo": "Juros do mês × seu aporte", "x_rotulo": "meses", "x_ticks": [0, 24, 48, 72, 96, 120],
                        "ymax": 900, "ymin": 0, "y_passo": 200,
                        "series": [{"nome": "juros do mês", "destaque": True, "velocidade": 0.6, "inicio": 0.3,
                                    "rotulo_final": "R$ 801", "pontos": pts_juros},
                                   {"nome": "seu aporte", "velocidade": 0.6, "inicio": 0.3,
                                    "rotulo_final": "R$ 500", "pontos": pts_aporte}]})
C["b1_qualquer"] = cena("b1_qualquer", "titulo",
                        "E tem um detalhe curioso: com essa taxa, a virada chega no mês oitenta e sete para qualquer valor de aporte. Cem reais, quinhentos ou mil. Quem muda a data é a taxa, não o tamanho do aporte.",
                        "Detalhe curioso: com essa taxa, a virada chega no mês 87 para qualquer valor de aporte. Quem muda a data é a taxa, não o tamanho do aporte.",
                        {"titulo": ["Vale para", "qualquer aporte"], "subtitulo": "a 0,8% ao mês, a virada é no mês 87"})
C["b1_cruza"] = cena("b1_cruza", "versus",
                     "Tem um segundo marco. No mês cento e cinquenta e nove, com treze anos e três meses, os juros acumulados passam o total que você aportou. Dali em diante, mais da metade do seu patrimônio veio dos juros.",
                     "Segundo marco: no mês 159, com 13 anos e 3 meses, os juros acumulados passam o total aportado. Dali em diante, mais da metade do patrimônio veio dos juros.",
                     {"a": "R$ 79.500", "b": "R$ 79.873", "rotulo_a": "você aportou", "rotulo_b": "juros acumulados",
                      "centro": "mês 159"})

# bloco 2 — por que começar cedo
C["b2_hook"] = cena("b2_hook", "numero_grande",
                    "Seus primeiros dez anos investindo valem mais que os vinte anos seguintes. Parece estranho, mas a conta mostra.",
                    "Seus primeiros 10 anos investindo valem mais que os 20 anos seguintes. Parece estranho, mas a conta mostra.",
                    {"valor": "10 > 20", "linhas": ["os 10 primeiros anos", "valem mais que os 20 seguintes"]})
C["b2_total"] = cena("b2_total", "formula",
                     "Em trinta anos, com quinhentos reais por mês a zero vírgula oito por cento, você aporta cento e oitenta mil reais e termina com cerca de um vírgula zero quatro milhão. Oitocentos e cinquenta e oito mil vieram dos juros.",
                     "Em 30 anos, com R$ 500 por mês a 0,8%, você aporta R$ 180 mil e termina com cerca de R$ 1,04 milhão. R$ 858 mil vieram dos juros.",
                     {"titulo": "Em 30 anos", "linha1": "R$ 180 mil aportados", "resultado": "R$ 1,04 milhão",
                      "nota": "R$ 858 mil vieram dos juros"})
C["b2_divide"] = cena("b2_divide", "barras",
                      "Agora separe esse resultado. Os aportes dos primeiros dez anos, sessenta mil reais, viram seiscentos e setenta e sete mil. Os aportes dos vinte anos seguintes, o dobro, cento e vinte mil, viram só trezentos e sessenta mil.",
                      "Separando: os aportes dos primeiros 10 anos, R$ 60 mil, viram R$ 677 mil. Os dos 20 anos seguintes, R$ 120 mil, viram só R$ 360 mil.",
                      {"titulo": ["De onde vem", "o R$ 1,04 milhão"],
                       "itens": [{"rotulo": "anos 1 a 10", "valor": 677641, "texto": "R$ 677 mil", "destaque": True},
                                 {"rotulo": "anos 11 a 30", "valor": 360566, "texto": "R$ 360 mil"}],
                       "nota": "aportes: R$ 60 mil × R$ 120 mil"})
C["b2_ano"] = cena("b2_ano", "barras",
                   "Olhe ano a ano. Os seis mil reais aportados no primeiro ano viram cem mil. Os do décimo ano, quarenta e dois mil. Os do vigésimo, dezesseis mil. E os do último ano, pouco mais de seis mil. O mesmo dinheiro, com menos tempo para render.",
                   "Ano a ano: os R$ 6.000 do 1º ano viram R$ 100 mil. Os do 10º, R$ 42 mil. Os do 20º, R$ 16 mil. Os do último, R$ 6.271. Mesmo dinheiro, menos tempo.",
                   {"titulo": ["R$ 6.000 aportados", "em cada ano viram"],
                    "itens": [{"rotulo": "ano 1", "valor": 100372, "texto": "R$ 100 mil", "destaque": True},
                              {"rotulo": "ano 10", "valor": 42450, "texto": "R$ 42 mil"},
                              {"rotulo": "ano 20", "valor": 16316, "texto": "R$ 16 mil"},
                              {"rotulo": "ano 30", "valor": 6271, "texto": "R$ 6.271"}],
                    "nota": "valor de cada ano no fim do ano 30"})
C["b2_licao"] = cena("b2_licao", "lista",
                     "Por isso o começo importa tanto. Os primeiros aportes parecem pequenos e lentos, mas são eles que ficam mais tempo rendendo. São a base da bola de neve.",
                     "Por isso o começo importa tanto. Os primeiros aportes parecem pequenos, mas são os que ficam mais tempo rendendo.",
                     {"titulo": ["Por que começar cedo"], "itens": ["o tempo multiplica", "o começo é a base", "atrasar custa caro"]})

# bloco 3 — dividendos e Bazin
C["b3_hook"] = cena("b3_hook", "numero_grande",
                    "Quanto dinheiro você precisa para receber mil reais por mês em dividendos? Depende de um número só.",
                    "Quanto você precisa para receber R$ 1.000 por mês em dividendos? Depende de um número só.",
                    {"valor": "R$ 1.000/mês", "linhas": ["em dividendos:", "quanto precisa investir?"]})
C["b3_dy"] = cena("b3_dy", "formula",
                  "Esse número é o dividend yield: quanto um investimento pagou em dividendos no ano, dividido pelo valor investido. Um yield de oito por cento significa oito reais por ano para cada cem reais investidos.",
                  "Dividend yield: dividendos do ano divididos pelo valor investido. Yield de 8% = R$ 8 por ano para cada R$ 100 investidos.",
                  {"titulo": "Dividend yield (DY)", "linha1": "dividendos no ano ÷ valor investido", "resultado": "8% ao ano",
                   "nota": "R$ 8 por ano a cada R$ 100"})
C["b3_conta"] = cena("b3_conta", "formula",
                     "Mil reais por mês são doze mil por ano. Dividindo doze mil por oito por cento, você chega a cento e cinquenta mil reais investidos.",
                     "R$ 1.000 por mês são R$ 12.000 por ano. Dividindo por 8%, você chega a R$ 150 mil investidos.",
                     {"titulo": "Para R$ 1.000 por mês", "linha1": "R$ 12.000 ÷ 8%", "resultado": "= R$ 150 mil",
                      "nota": "capital = renda anual ÷ DY"})
C["b3_barras"] = cena("b3_barras", "barras",
                      "Com yield de seis por cento, precisaria de duzentos mil. Com dez por cento, cento e vinte mil. Mas atenção: dividendos variam de um ano para o outro e não têm garantia. E yield alto demais às vezes é sinal de problema, não de oportunidade.",
                      "Com yield de 6%, R$ 200 mil. Com 10%, R$ 120 mil. Atenção: dividendos variam e não têm garantia. Yield alto demais pode ser sinal de problema.",
                      {"titulo": ["Capital para", "R$ 1.000 por mês"],
                       "itens": [{"rotulo": "DY 6%", "valor": 200000, "texto": "R$ 200 mil"},
                                 {"rotulo": "DY 8%", "valor": 150000, "texto": "R$ 150 mil", "destaque": True},
                                 {"rotulo": "DY 10%", "valor": 120000, "texto": "R$ 120 mil"}],
                       "nota": "dividendos variam e não têm garantia"})
C["b3_tempo"] = cena("b3_tempo", "formula",
                     "E quanto tempo leva para juntar cento e cinquenta mil? Com quinhentos reais por mês, rendendo zero vírgula oito por cento, cerca de cento e cinquenta e quatro meses. Quase treze anos.",
                     "Quanto tempo para juntar R$ 150 mil? Com R$ 500 por mês a 0,8%, cerca de 154 meses. Quase 13 anos.",
                     {"titulo": "Quanto tempo até lá", "linha1": "R$ 500 por mês a 0,8%", "resultado": "≈ 12,8 anos",
                      "nota": "154 meses até R$ 150 mil"})
C["b3_bazin"] = cena("b3_bazin", "formula",
                     "Essa mesma conta está por trás de um método famoso no Brasil. Décio Bazin, no livro Faça Fortuna com Ações, de mil novecentos e noventa e dois, defendia comprar uma ação só se ela pagasse pelo menos seis por cento ao ano em dividendos. O preço máximo, o preço-teto, é o dividendo dividido por seis por cento.",
                     "Essa conta está por trás do método Bazin. No livro Faça Fortuna com Ações, de 1992, Décio Bazin defendia só comprar com pelo menos 6% ao ano em dividendos. Preço-teto = dividendo ÷ 6%.",
                     {"titulo": "O método Bazin", "linha1": "dividendo anual ÷ 6%", "resultado": "= preço-teto",
                      "nota": "Décio Bazin, 1992"})
C["b3_bazin_ex"] = cena("b3_bazin_ex", "versus",
                        "Exemplo com uma empresa fictícia que paga três reais por ação no ano. O preço-teto é cinquenta reais. A quarenta reais, o yield seria sete e meio por cento. A sessenta, só cinco por cento, abaixo do critério. É um filtro de preço, não uma promessa de retorno.",
                        "Empresa fictícia que paga R$ 3 por ação no ano: preço-teto de R$ 50. A R$ 40, yield de 7,5%. A R$ 60, só 5%. É um filtro de preço, não uma promessa de retorno.",
                        {"a": "R$ 40", "b": "R$ 60", "rotulo_a": "DY 7,5% · abaixo do teto", "rotulo_b": "DY 5% · acima do teto",
                         "centro": "teto R$ 50"})

# encerramento do longo
C["o_resumo"] = cena("o_resumo", "lista",
                     "Resumindo. Com zero vírgula oito por cento ao mês, os juros passam o seu aporte no mês oitenta e sete. Os primeiros dez anos valem mais que os vinte seguintes. E, com yield de oito por cento, cento e cinquenta mil reais pagariam cerca de mil reais por mês.",
                     "Resumo: a 0,8% ao mês, os juros passam o aporte no mês 87. Os primeiros 10 anos valem mais que os 20 seguintes. Com yield de 8%, R$ 150 mil pagariam cerca de R$ 1.000 por mês.",
                     {"titulo": ["Resumo"], "itens": ["virada no mês 87", "o começo vale mais", "R$ 150 mil → R$ 1.000/mês"]})
C["o_cta"] = cena("o_cta", "cta",
                  "Se essa conta te ajudou, se inscreve no canal. E comenta qual conta você quer ver no próximo vídeo.",
                  "Se essa conta te ajudou, se inscreve no canal. E comenta qual conta você quer ver no próximo vídeo.",
                  {"linhas": ["Qual conta você quer", "ver no próximo vídeo?"], "botao": "Inscreva-se e comente"})

CTA_P = {
    1: cena("p_cta", "cta", "Na parte dois, a conta que mostra por que os primeiros anos valem mais que todos os outros. Segue o perfil para não perder.",
            "Na parte 2: por que os primeiros anos valem mais que todos os outros. Segue o perfil para não perder.",
            {"linhas": ["Parte 2: por que", "começar cedo vale tanto"], "botao": "Segue para ver a parte 2"}),
    2: cena("p_cta", "cta", "Na parte três, quanto dinheiro você precisa para receber mil reais por mês em dividendos. Segue o perfil.",
            "Na parte 3: quanto você precisa para receber R$ 1.000 por mês em dividendos. Segue o perfil.",
            {"linhas": ["Parte 3: quanto investir", "para viver de dividendos"], "botao": "Segue para ver a parte 3"}),
    3: cena("p_cta", "cta", "E você, quanto gostaria de receber por mês em dividendos? Comenta aqui que eu faço a conta.",
            "Quanto você gostaria de receber por mês em dividendos? Comenta aqui que eu faço a conta.",
            {"linhas": ["Quanto você quer", "receber por mês?"], "botao": "Comenta aqui embaixo"}),
}

BLOCOS = {1: ["b1_hook", "b1_mes1", "b1_conta", "b1_grafico", "b1_qualquer", "b1_cruza"],
          2: ["b2_hook", "b2_total", "b2_divide", "b2_ano", "b2_licao"],
          3: ["b3_hook", "b3_dy", "b3_conta", "b3_barras", "b3_tempo", "b3_bazin", "b3_bazin_ex"]}


def base(id_, titulo, formato, cenas, capa, posts):
    return {"id": id_, "titulo": titulo, "formato": formato, "pilar": "Investimentos", "tipo": "evergreen / explicador",
            "risco": "baixo — taxa ilustrativa, sem ativos citados; Bazin com fonte", "nota_tela": NOTA,
            "parametros": parametros, "calculos": calculos, "numeros_livres": [100], "numeros_fonte": numeros_fonte,
            "fontes": fontes, "capa": capa, "cenas": cenas, "posts": posts}


TIT_LONGO = "Juros compostos na prática: quando o dinheiro trabalha sozinho"
longo = base("JQE-L001", TIT_LONGO, "horizontal 16:9",
             [C["i1"], C["i2"]] + [C[k] for k in BLOCOS[1] + BLOCOS[2] + BLOCOS[3]] + [C["o_resumo"], C["o_cta"], ASS],
             {"linha1": "Quando o dinheiro", "linha2": "trabalha sozinho?", "destaque": "Mês 87"},
             {"youtube": {"titulo": TIT_LONGO,
                          "texto": "R$ 500 por mês, durante 30 anos, a 0,8% ao mês (cerca de 10% ao ano), podem passar de R$ 1 milhão. Neste vídeo, a conta completa:\n\n"
                                   "1. O ponto de virada: no mês 87, os juros do mês passam o seu aporte. No mês 159, os juros acumulados passam o total aportado.\n"
                                   "2. Por que começar cedo: os aportes dos primeiros 10 anos (R$ 60 mil) viram R$ 677 mil; os dos 20 anos seguintes (R$ 120 mil) viram R$ 360 mil.\n"
                                   "3. Viver de dividendos: para R$ 1.000 por mês com dividend yield de 8%, cerca de R$ 150 mil. E o método Bazin: preço-teto = dividendo ÷ 6%.\n\n"
                                   "Taxa hipotética, sem impostos nem inflação. Dividendos variam e não têm garantia. " + AVISO +
                                   "\n\nFontes do método Bazin: InfoMoney e Investidor10.\n\n#educacaofinanceira #jurocomposto #dividendos #investimentos"}})

partes = []
TITULOS_P = {1: "O ponto de virada dos juros compostos", 2: "Por que os primeiros 10 anos valem mais",
             3: "Quanto investir para receber R$ 1.000 por mês em dividendos"}
CAPAS_P = {1: {"linha1": "Quando os juros", "linha2": "passam o seu aporte?", "destaque": "Parte 1"},
           2: {"linha1": "10 primeiros anos", "linha2": "valem mais que 20", "destaque": "Parte 2"},
           3: {"linha1": "R$ 1.000 por mês", "linha2": "em dividendos", "destaque": "Parte 3"}}
POSTS_P = {
    1: {"instagram": "Tem um mês em que os juros rendem mais que o seu aporte. (Parte 1/3)\n\nR$ 500 por mês a 0,8% ao mês:\n• mês 1 → R$ 4 de juros\n• mês 87 → os juros do mês passam os R$ 500\n• mês 159 → os juros acumulados passam tudo o que você aportou\n\nE a virada no mês 87 vale para qualquer valor de aporte.\n\nParte 2 amanhã: por que os primeiros 10 anos valem mais. 👇\n\nTaxa hipotética, sem impostos. Narração gerada por IA.\n\n#educacaofinanceira #jurocomposto #investimentos #financaspessoais #dinheiro",
        "tiktok": "Tem um mês em que os juros rendem mais que o seu aporte: no exemplo, o mês 87. Parte 1 de 3. Taxa hipotética, narração por IA. #educacaofinanceira #jurocomposto #investimentos #dinheiro"},
    2: {"instagram": "Seus primeiros 10 anos investindo valem mais que os 20 seguintes. (Parte 2/3)\n\nR$ 500 por mês a 0,8% ao mês, por 30 anos:\n• aportes dos anos 1 a 10 (R$ 60 mil) → R$ 677 mil\n• aportes dos anos 11 a 30 (R$ 120 mil) → R$ 360 mil\n\nOs primeiros aportes são os que ficam mais tempo rendendo.\n\nParte 3 amanhã: quanto investir para viver de dividendos. 👇\n\nTaxa hipotética, sem impostos. Narração gerada por IA.\n\n#educacaofinanceira #jurocomposto #investimentos #financaspessoais #dinheiro",
        "tiktok": "Seus primeiros 10 anos investindo valem mais que os 20 seguintes. A conta está aqui. Parte 2 de 3. Taxa hipotética, narração por IA. #educacaofinanceira #jurocomposto #investimentos"},
    3: {"instagram": "Quanto investir para receber R$ 1.000 por mês em dividendos? (Parte 3/3)\n\nCapital = renda anual ÷ dividend yield\n• DY 6% → R$ 200 mil\n• DY 8% → R$ 150 mil\n• DY 10% → R$ 120 mil\n\nE o método Bazin: preço-teto = dividendo ÷ 6%.\nDividendos variam e não têm garantia.\n\nQuanto você quer receber por mês? Comenta que eu faço a conta 👇\n\nExemplo ilustrativo. Narração gerada por IA.\n\n#educacaofinanceira #dividendos #investimentos #rendapassiva #dinheiro",
        "tiktok": "Quanto investir para receber R$ 1.000 por mês em dividendos? Com DY de 8%, R$ 150 mil. E o método Bazin explicado. Parte 3 de 3. Narração por IA. #educacaofinanceira #dividendos #investimentos"},
}
for k in (1, 2, 3):
    pid = f"JQE-L001-P{k}"
    r = base(pid, TITULOS_P[k], "vertical 9:16", [C[c] for c in BLOCOS[k]] + [CTA_P[k], ASS], CAPAS_P[k],
             {"instagram": {"texto": POSTS_P[k]["instagram"]}, "tiktok": {"texto": POSTS_P[k]["tiktok"]}})
    r["parte_de"] = "JQE-L001"
    partes.append(r)

for r in [longo] + partes:
    os.makedirs(f"{REPO}/{r['id']}", exist_ok=True)
    json.dump(r, open(f"{REPO}/{r['id']}/roteiro.json", "w"), ensure_ascii=False, indent=1)
    print("ok", r["id"], sum(len(c["tts"].split()) for c in r["cenas"]), "palavras")
