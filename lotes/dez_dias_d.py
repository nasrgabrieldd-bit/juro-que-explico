"""Lote 21–30/11/2026 (parte D): JQE-S048 a S052."""
import sys
sys.path.insert(0, "/home/claude/juro-que-explico/lotes")
from _lib import *
ASS = assinatura()

# ====================================================== S048 — aumento de salário (LOOP)
c = Calc({"guarda": "aumento / 2", "f5": "guarda * (((1 + taxa_mes) ** 60 - 1) / taxa_mes)", "f10": "guarda * (((1 + taxa_mes) ** 120 - 1) / taxa_mes)",
          "f20": "guarda * (((1 + taxa_mes) ** 240 - 1) / taxa_mes)", "coloca10": "guarda * 120"},
         {"aumento": 300, "taxa_mes": 0.008}, livres=[10, 20])
HOOK = {"valor": "+R$ 300", "linhas": ["de aumento: separa", "metade antes de gastar"]}
cenas = [
    cena(c, "hook", "numero_grande", "Ganhou trezentos reais de aumento? Separa metade antes de se acostumar.", HOOK),
    cena(c, "fluxo", "fluxo_setas",
         "Papo reto: o aumento sempre parece pouco, e some. A gente se acostuma rápido com o que é melhor. Primeiro vem um jantar melhor, depois uma assinatura, depois uma parcela nova. No fim do mês, o salário subiu, mas a sobra continua igual.",
         {"caixas": [{"texto": "salário sobe R$ 300", "tom": "neutro"}, {"texto": "o gasto sobe junto", "tom": "cinza"}, {"texto": "sobra igual", "tom": "erro"}],
          "setas": [{"rotulo": "sem perceber", "tom": "neutro"}, {"rotulo": "no fim do mês", "tom": "erro"}]},
         leg="Papo reto: o aumento sempre parece pouco, e some. A gente se acostuma rápido com o que é melhor. Primeiro vem um jantar melhor, depois uma assinatura, depois uma parcela nova. No fim do mês, o salário subiu, mas a sobra continua igual."),
    cena(c, "duo", "duo",
         "Agora olha a Bia e o Léo. Os dois ganharam o mesmo aumento. O Léo gastou tudo. A Bia separou cento e cinquenta reais por mês. Depois de dez anos, o Léo tem zero. A Bia tem [[f10|mil]].",
         {"leo": {"fala": "Gastei tudo", "rotulo": "gastou o aumento", "valor": 6, "texto": "R$ 0"}, "bia": {"fala": "Separei metade", "rotulo": "guardou R$ 150/mês", "valor": 100, "texto": "[[f10|mil]]"}},
         leg="Agora olha a Bia e o Léo. Os dois ganharam o mesmo aumento. O Léo gastou tudo. A Bia separou R$ 150 por mês. Depois de 10 anos, o Léo tem zero. A Bia tem [[f10|mil]]."),
    cena(c, "barras", "barras",
         "E olha que a Bia nem passou aperto: continuou com cento e cinquenta reais a mais por mês. Em cinco anos, [[f5|mil]]. Em dez, [[f10|mil]]. Em vinte, [[f20|mil]].",
         {"titulo": ["R$ 150 por mês,", "só do aumento"], "itens": [{"rotulo": "5 anos", "valor": c.v("f5"), "texto": "[[f5|mil]]"}, {"rotulo": "10 anos", "valor": c.v("f10"), "texto": "[[f10|mil]]"}, {"rotulo": "20 anos", "valor": c.v("f20"), "texto": "[[f20|mil]]", "destaque": True}],
          "nota": "juros hipotéticos de 0,8% ao mês, sem impostos"}),
    cena(c, "moral", "titulo",
         "A ideia é simples: o dinheiro que você nunca viu chegar na conta não faz falta. Separar metade do aumento no mesmo dia, de forma automática, deixa você melhorar de vida e ainda guardar. Você aproveita o aumento e constrói o seu futuro ao mesmo tempo, sem sacrifício enorme.",
         {"titulo": ["Metade pro futuro,", "metade pra viver"], "subtitulo": "o aumento melhora o hoje e o amanhã"}),
    cena(c, "volta", "numero_grande", "Então, no dia em que o seu salário aumentar, lembra:", HOOK),
]
escreve(c, "JQE-S048", "Aumento de salário: separe metade antes de se acostumar", "Comportamento", "história", "personagens + passo a passo (loop)",
        "Exemplo ilustrativo · juros hipotéticos de 0,8% ao mês, sem impostos",
        ["Cálculo próprio: valor futuro de aportes mensais, VF = A × ((1 + i)^n − 1) ÷ i", "Exemplo ilustrativo"],
        {"linha1": "Ganhou aumento?", "linha2": "Separe metade", "destaque": "antes de gastar"},
        ["Ganhou R$ 300 de aumento? Separa metade antes de se acostumar.", "O que fazer com o aumento de salário."], cenas,
        posts(c, "Aumento de salário: separe metade antes de se acostumar", "Ganhou R$ 300 de aumento? Separa metade antes de se acostumar.",
              ["R$ 150 por mês durante 10 anos → [[f10|mil]] (você coloca [[coloca10|mil]])", "5 anos → [[f5|mil]]", "20 anos → [[f20|mil]]", "Metade pro futuro, metade pra viver."],
              "O que você faz quando o salário aumenta?", "Exemplo ilustrativo, juros hipotéticos de 0,8% ao mês, sem impostos.",
              ["educacaofinanceira", "investimentos", "salario", "dinheiro"], "Ganhou aumento? Separa metade antes de se acostumar. A conta com o Léo e a Bia."),
        loop=True)

# ====================================================== S049 — carro de R$ 80 mil
c = Calc({"v5": "preco * (1 - dep) ** 5", "perda": "preco - v5", "inv5": "preco * (1 + taxa_mes) ** 60", "ganho": "inv5 - preco", "dif": "inv5 - v5",
          "preco_mil": "preco / 1000"},
         {"preco": 80000, "dep": 0.1, "taxa_mes": 0.008}, livres=[80])
pc = [[a, round(80000 * 0.9 ** a)] for a in range(0, 6)]
pi = [[a, round(80000 * 1.008 ** (12 * a))] for a in range(0, 6)]
cenas = [
    cena(c, "hook", "numero_grande", "Um carro de oitenta mil reais pode custar mais de oitenta mil em cinco anos.",
         {"valor": "[[dif|mil]]", "linhas": ["de custo escondido", "em 5 anos"]}),
    cena(c, "fluxo", "fluxo_setas",
         "Exemplo hipotético. O carro de oitenta mil perde dez por cento do valor por ano. Em cinco anos, ele vale [[v5|mil]]. Só de valor que sumiu, são [[perda|mil]].",
         {"caixas": [{"texto": "carro: R$ 80 mil", "tom": "neutro"}, {"texto": "−10% ao ano", "tom": "cinza"}, {"texto": "vale [[v5|mil]]", "tom": "erro"}],
          "setas": [{"rotulo": "5 anos", "tom": "neutro"}, {"rotulo": "perda de valor", "tom": "erro"}]},
         leg="Exemplo hipotético. O carro de R$ 80 mil perde 10% do valor por ano. Em 5 anos, ele vale [[v5|mil]]. Só de valor que sumiu, são [[perda|mil]]."),
    cena(c, "linhas", "linhas",
         "Agora o outro lado. Se esses mesmos oitenta mil estivessem investidos, com juros hipotéticos de zero vírgula oito por cento ao mês, viriam [[inv5|mil]] em cinco anos. Uma linha desce, a outra sobe.",
         {"titulo": "R$ 80 mil: carro × investido", "x_rotulo": "anos", "x_ticks": [0, 1, 2, 3, 4, 5], "ymax": 140000, "ymin": 0, "y_passo": 35000, "y_fmt": "brl",
          "series": [{"nome": "valor do carro", "pontos": pc, "velocidade": 0.8, "inicio": 0.2, "rotulo_final": "[[v5|mil]]"},
                     {"nome": "dinheiro investido", "destaque": True, "pontos": pi, "velocidade": 0.8, "inicio": 0.4, "rotulo_final": "[[inv5|mil]]"}]},
         leg="Agora o outro lado. Se esses mesmos R$ 80 mil estivessem investidos, com juros hipotéticos de 0,8% ao mês, viriam [[inv5|mil]] em 5 anos. Uma linha desce, a outra sobe."),
    cena(c, "versus", "versus",
         "Somando o valor que o carro perdeu e o ganho que o dinheiro deixou de ter, a diferença passa de [[dif|mil]]. Esse é o custo de oportunidade.",
         {"a": "[[perda|mil]]", "b": "[[ganho|mil]]", "rotulo_a": "perdeu de valor", "rotulo_b": "deixou de render", "centro": "somados: [[dif|mil]]"}),
    cena(c, "ressalva", "titulo",
         "Isso não quer dizer que carro é erro. Pra muita gente, ele é trabalho, família e tempo. O ponto é decidir sabendo o tamanho da conta, e não só olhando a parcela.",
         {"titulo": ["Decidir sabendo", "o tamanho da conta"], "subtitulo": "carro tem valor de uso, mas também tem custo"}),
    cena(c, "lista", "lista", "Antes de comprar, pergunta: eu preciso mesmo dele agora? A parcela cabe com folga? E existe uma opção mais barata que resolva o mesmo problema?",
         {"titulo": ["Antes de comprar"], "itens": ["preciso dele agora?", "a parcela cabe com folga?", "há opção mais barata?"]}),
    cta(c, "cta", "Você já fez essa conta do seu carro? Conta aqui nos comentários.", ["Você já fez essa", "conta do seu carro?"]),
    ASS,
]
escreve(c, "JQE-S049", "Carro de R$ 80 mil: o custo escondido em 5 anos", "Consumo", "custo escondido", "explicador + setas",
        "Exemplo hipotético · depreciação de 10% ao ano; juros de 0,8% ao mês; sem impostos",
        ["Cálculo próprio: valor após n anos = preço × (1 − depreciação)^n; investido = preço × (1 + i)^n", "Valores e taxas hipotéticos"],
        {"linha1": "Carro de R$ 80 mil", "linha2": "custa mais que isso", "destaque": "em 5 anos"},
        ["Um carro de R$ 80 mil pode custar mais de R$ 80 mil em 5 anos.", "O custo de oportunidade de um carro."], cenas,
        posts(c, "Carro de R$ 80 mil: o custo escondido em 5 anos", "Um carro de R$ 80 mil pode custar mais de R$ 80 mil em 5 anos.",
              ["Valor do carro em 5 anos (−10% ao ano): [[v5|mil]]", "Os mesmos R$ 80 mil investidos: [[inv5|mil]]", "Diferença: mais de [[dif|mil]]", "Carro tem valor de uso: só decida sabendo a conta."],
              "Você já fez essa conta do seu carro?", "Exemplo hipotético; depreciação e rendimento hipotéticos, sem impostos.",
              ["educacaofinanceira", "carro", "investimentos", "dinheiro"], "Um carro de R$ 80 mil pode custar mais de R$ 80 mil em 5 anos. Veja a conta."))

# ====================================================== S050 — regra dos 114 e dos 144
c = Calc({"dobra": "72 / taxa", "triplica": "114 / taxa", "quadruplica": "144 / taxa",
          "exato3": "log(3) / log(1 + taxa / 100)", "v6": "1000 * (1 + taxa / 100) ** 6", "v12": "1000 * (1 + taxa / 100) ** 12"},
         {"taxa": 12}, livres=[72, 114, 144, 1000])
cenas = [
    cena(c, "hook", "numero_grande", "Divida cento e catorze pela taxa e descubra quando seu dinheiro triplica.",
         {"valor": "114 ÷ taxa", "linhas": ["em quantos anos", "o dinheiro triplica"]}),
    cena(c, "formula", "formula",
         "Exemplo com taxa hipotética de doze por cento ao ano. Cento e catorze dividido por doze dá nove vírgula cinco. Em uns nove anos e meio, o dinheiro vira o triplo.",
         {"titulo": "Regra do 114", "linha1": "114 ÷ 12", "resultado": "[[triplica|n]] anos", "nota": "para triplicar, a 12% ao ano"},
         leg="Exemplo com taxa hipotética de 12% ao ano. 114 ÷ 12 = 9,5. Em uns 9 anos e meio, o dinheiro vira o triplo."),
    cena(c, "barras", "barras",
         "A mesma ideia vale para dobrar e quadruplicar. Pra dobrar, divide setenta e dois: dá seis anos. Pra triplicar, cento e catorze: nove e meio. Pra quadruplicar, cento e quarenta e quatro: doze anos.",
         {"titulo": ["Anos para multiplicar", "a 12% ao ano"], "itens": [{"rotulo": "dobrar: 72 ÷ 12", "valor": c.v("dobra"), "texto": "[[dobra|n0]] anos"}, {"rotulo": "triplicar: 114 ÷ 12", "valor": c.v("triplica"), "texto": "[[triplica|n]] anos", "destaque": True},
                                                                    {"rotulo": "quadruplicar: 144 ÷ 12", "valor": c.v("quadruplica"), "texto": "[[quadruplica|n0]] anos"}], "nota": "regras de bolso, valores aproximados"}),
    cena(c, "fluxo", "fluxo_setas",
         "Dá pra ver na prática. Mil reais, a doze por cento ao ano, viram quase dois mil em seis anos e quase quatro mil em doze. É dobrar, e dobrar de novo.",
         {"caixas": [{"texto": "hoje: R$ 1.000", "tom": "neutro"}, {"texto": "6 anos: [[v6|R]]", "tom": "cinza"}, {"texto": "12 anos: [[v12|R]]", "tom": "ok"}],
          "setas": [{"rotulo": "dobra", "tom": "neutro"}, {"rotulo": "dobra de novo", "tom": "neutro"}]},
         leg="Dá pra ver na prática. R$ 1.000, a 12% ao ano, viram [[v6|R]] em 6 anos e [[v12|R]] em 12. É dobrar, e dobrar de novo."),
    cena(c, "versus", "versus",
         "É exato? Não. Com a conta completa, o triplo leva uns nove vírgula sete anos, e a regra deu nove vírgula cinco. Fica bem perto, e isso basta pra ter uma noção de cabeça.",
         {"a": "[[triplica|n]]", "b": "[[exato3|n]]", "rotulo_a": "regra do 114", "rotulo_b": "conta exata", "centro": "bem perto"},
         leg="É exato? Não. Com a conta completa, o triplo leva uns [[exato3|n]] anos, e a regra deu [[triplica|n]]. Fica bem perto, e isso basta pra ter uma noção de cabeça."),
    cena(c, "lista", "lista", "Guarda estes três números: setenta e dois para dobrar, cento e catorze para triplicar e cento e quarenta e quatro para quadruplicar. E lembra: a taxa aqui é só exemplo.",
         {"titulo": ["Três números", "para guardar"], "itens": ["72 para dobrar", "114 para triplicar", "144 para quadruplicar"]},
         leg="Guarda estes três números: 72 para dobrar, 114 para triplicar e 144 para quadruplicar. E lembra: a taxa aqui é só exemplo."),
    cta(c, "cta", "Que taxa você usaria na sua conta de cabeça? Comenta aqui.", ["Qual taxa você", "usaria na conta?"]),
    ASS,
]
escreve(c, "JQE-S050", "Regra do 114 e do 144: quando o dinheiro triplica", "Investimentos", "pergunta com número", "explicador (conta de cabeça)",
        "Regra de bolso · taxa hipotética de 12% ao ano, valores aproximados",
        ["Regras de bolso: tempo ≈ 72 ÷ taxa (dobrar), 114 ÷ taxa (triplicar), 144 ÷ taxa (quadruplicar)", "Conta exata: n = ln(3) ÷ ln(1 + i)"],
        {"linha1": "Quando o dinheiro", "linha2": "triplica?", "destaque": "regra do 114"},
        ["Divida 114 pela taxa e descubra quando seu dinheiro triplica.", "Conta de cabeça: dobrar, triplicar, quadruplicar."], cenas,
        posts(c, "Regra do 114 e do 144: quando o dinheiro triplica", "Divida 114 pela taxa e descubra quando seu dinheiro triplica.",
              ["72 ÷ taxa → dobrar ([[dobra|n0]] anos a 12%)", "114 ÷ taxa → triplicar ([[triplica|n]] anos a 12%)", "144 ÷ taxa → quadruplicar ([[quadruplica|n0]] anos a 12%)", "Regras de bolso, valores aproximados."],
              "Que taxa você usaria na sua conta de cabeça?", "Regra de bolso com taxa hipotética de 12% ao ano. Valores aproximados.",
              ["educacaofinanceira", "investimentos", "jurocomposto", "dinheiro"], "Divida 114 pela taxa e descubra quando seu dinheiro triplica."))

# ====================================================== S051 — qual dívida pagar primeiro (LOOP)
c = Calc({"jA": "valor * tA", "jB": "valor * tB", "ecoA": "extra * tA", "ecoB": "extra * tB", "razao": "ecoA / ecoB", "balB": "ecoB / ecoA * 100"},
         {"valor": 3000, "tA": 0.12, "tB": 0.02, "extra": 500}, livres=[12])
HOOK = {"a": "12% ao mês", "b": "2% ao mês", "rotulo_a": "dívida A", "rotulo_b": "dívida B", "centro": "qual pagar primeiro?"}
cenas = [
    cena(c, "hook", "versus", "Duas dívidas e um dinheiro extra: qual pagar primeiro?", HOOK),
    cena(c, "fluxo", "fluxo_setas",
         "Exemplo hipotético. Você deve três mil reais nas duas dívidas, uma com juros de doze por cento ao mês e outra com dois por cento. De repente, sobram quinhentos reais. Pra onde eles vão?",
         {"caixas": [{"texto": "A: R$ 3.000 a 12%", "tom": "erro"}, {"texto": "B: R$ 3.000 a 2%", "tom": "cinza"}, {"texto": "sobram R$ 500", "tom": "ok"}],
          "setas": [{"rotulo": "juros de [[jA|R]]/mês", "tom": "erro"}, {"rotulo": "juros de [[jB|R]]/mês", "tom": "neutro"}]},
         leg="Exemplo hipotético. Você deve R$ 3.000 em cada uma das duas dívidas, uma com juros de 12% ao mês e outra com 2%. De repente, sobram R$ 500. Pra onde eles vão?"),
    cena(c, "barras", "barras",
         "A conta é direta. Os quinhentos na dívida de doze por cento evitam [[ecoA|R]] de juros por mês. Na de dois por cento, só [[ecoB|R]]. A diferença é de seis vezes.",
         {"titulo": ["Juros evitados", "por mês"], "itens": [{"rotulo": "pagar a de 12%", "valor": c.v("ecoA"), "texto": "[[ecoA|R]]", "destaque": True}, {"rotulo": "pagar a de 2%", "valor": c.v("ecoB"), "texto": "[[ecoB|R]]"}],
          "nota": "juros hipotéticos sobre R$ 500 amortizados"}),
    cena(c, "duo", "duo",
         "Olha o Léo e a Bia. O Léo pagou a dívida mais baixa, porque tinha pressa de ver uma delas acabar. A Bia atacou a de juros mais altos. No fim do mês, a Bia economizou seis vezes mais.",
         {"leo": {"fala": "Paguei a de 2%", "rotulo": "juros evitados", "valor": c.v("balB"), "texto": "[[ecoB|R]]/mês"}, "bia": {"fala": "Paguei a de 12%", "rotulo": "juros evitados", "valor": 100, "texto": "[[ecoA|R]]/mês"}}),
    cena(c, "honesto", "titulo",
         "Sem julgamento: se zerar a menor dívida primeiro te dá ânimo pra continuar, isso também funciona. O mais importante é não parar. Mas, pela matemática, a de juros mais altos custa mais caro.",
         {"titulo": ["Pela conta, a mais", "cara vem primeiro"], "subtitulo": "mas o que importa é não desistir"}),
    cena(c, "lista", "lista", "Um roteiro simples: anote todas as dívidas e as taxas, pague o mínimo de todas e coloque o dinheiro extra na de juros mais altos.",
         {"titulo": ["Roteiro simples"], "itens": ["anote dívidas e taxas", "pague o mínimo de todas", "extra na taxa mais alta"]}),
    cena(c, "volta", "versus", "Então, quando tiver duas dívidas e um dinheiro extra, pergunta:", HOOK),
]
escreve(c, "JQE-S051", "Duas dívidas e um dinheiro extra: qual pagar primeiro?", "Dívidas", "escolha", "versus + personagens (loop)",
        "Exemplo hipotético · taxas inventadas; as taxas reais variam",
        ["Cálculo próprio: juros evitados por mês = valor amortizado × taxa mensal", "Exemplo hipotético"],
        {"linha1": "Duas dívidas,", "linha2": "um dinheiro extra", "destaque": "qual pagar primeiro?"},
        ["Duas dívidas e um dinheiro extra: qual pagar primeiro?", "Qual dívida pagar primeiro?"], cenas,
        posts(c, "Duas dívidas e um dinheiro extra: qual pagar primeiro?", "Duas dívidas e um dinheiro extra: qual pagar primeiro?",
              ["R$ 500 na dívida de 12% ao mês → [[ecoA|R]] de juros evitados por mês", "R$ 500 na dívida de 2% ao mês → [[ecoB|R]] por mês", "Pela matemática, a de juros mais altos vem primeiro", "Se zerar a menor te motiva, isso também funciona: o importante é não parar"],
              "Qual dívida você pagaria primeiro?", "Exemplo hipotético, taxas inventadas. Não é recomendação.",
              ["educacaofinanceira", "dividas", "juros", "dinheiro"], "Duas dívidas e um dinheiro extra: qual pagar primeiro? A conta com o Léo e a Bia."),
        loop=True)

# ====================================================== S052 — R$ 10 mil em 2 anos
c = Calc({"A": "meta * taxa / ((1 + taxa) ** 24 - 1)", "sem": "meta / 24", "dif": "sem - A", "aportado": "A * 24", "juros": "meta - aportado",
          "fvLeo": "300 * (((1 + alta) ** 24 - 1) / alta)", "fvBia": "380 * (((1 + taxa) ** 24 - 1) / taxa)", "balLeo": "fvLeo / fvBia * 100"},
         {"meta": 10000, "taxa": 0.008, "alta": 0.015}, livres=[300, 380, 24])
cenas = [
    cena(c, "hook", "versus", "Juntar dez mil reais em dois anos: o que pesa mais, guardar ou render?",
         {"a": "[[sem|R]]", "b": "[[A|R]]", "rotulo_a": "só guardando", "rotulo_b": "com rendimento", "centro": "por mês, em 24 meses"}),
    cena(c, "fluxo", "fluxo_setas",
         "Sem rendimento nenhum, dez mil dividido por vinte e quatro meses dá [[sem|R]] por mês. Com juros hipotéticos de zero vírgula oito por cento ao mês, cai para [[A|R]]. A diferença é de uns [[dif|R]].",
         {"caixas": [{"texto": "R$ 10 mil ÷ 24", "tom": "neutro"}, {"texto": "só guardando: [[sem|R]]", "tom": "cinza"}, {"texto": "com juros: [[A|R]]", "tom": "ok"}],
          "setas": [{"rotulo": "24 meses", "tom": "neutro"}, {"rotulo": "juros ajudam", "tom": "neutro"}]},
         leg="Sem rendimento nenhum, R$ 10 mil ÷ 24 meses dá [[sem|R]] por mês. Com juros hipotéticos de 0,8% ao mês, cai para [[A|R]]. A diferença é de uns [[dif|R]]."),
    cena(c, "barras", "barras",
         "Olha de onde vem o dinheiro. Dos dez mil, [[aportado|mil]] saem do seu bolso e só [[juros|R]] vêm dos juros. No prazo curto, quem faz o trabalho pesado é você.",
         {"titulo": ["De onde vêm", "os R$ 10 mil"], "itens": [{"rotulo": "do seu bolso", "valor": c.v("aportado"), "texto": "[[aportado|mil]]", "destaque": True}, {"rotulo": "dos juros", "valor": c.v("juros"), "texto": "[[juros|R]]"}],
          "nota": "juros hipotéticos de 0,8% ao mês, sem impostos"}),
    cena(c, "duo", "duo",
         "Olha a Bia e o Léo. O Léo guarda trezentos reais por mês e corre atrás de um rendimento bem maior. A Bia guarda trezentos e oitenta com um rendimento normal. Em dois anos, a Bia chega nos dez mil, e o Léo, só em [[fvLeo|R]].",
         {"leo": {"fala": "Quero render mais", "rotulo": "R$ 300 por mês", "valor": c.v("balLeo"), "texto": "[[fvLeo|R]]"}, "bia": {"fala": "Guardo mais", "rotulo": "R$ 380 por mês", "valor": 100, "texto": "[[fvBia|R]]"}},
         leg="Olha a Bia e o Léo. O Léo guarda R$ 300 por mês e corre atrás de um rendimento bem maior. A Bia guarda R$ 380 com um rendimento normal. Em 2 anos, a Bia chega nos R$ 10 mil, e o Léo, só em [[fvLeo|R]]."),
    cena(c, "moral", "titulo",
         "No curto prazo, o que manda é quanto você guarda, e não a busca pelo melhor rendimento. Rendimento alto costuma vir com risco alto, e você pode precisar do dinheiro numa data certa. Com o tempo, a história muda.",
         {"titulo": ["No curto prazo,", "manda o quanto guarda"], "subtitulo": "o rendimento ajuda mais com o passar dos anos"}),
    cena(c, "lista", "lista", "Para uma meta de dois anos: defina o valor e a data, divida por mês e escolha uma opção segura, com resgate fácil. Depois, é manter o hábito.",
         {"titulo": ["Meta de 2 anos"], "itens": ["valor e data definidos", "divida pelos meses", "opção segura e líquida"]}),
    cta(c, "cta", "Qual é a sua meta de dois anos? Conta aqui nos comentários.", ["Qual é a sua", "meta de 2 anos?"]),
    ASS,
]
escreve(c, "JQE-S052", "R$ 10 mil em 2 anos: guardar mais ou render mais?", "Metas", "escolha", "versus + personagens",
        "Exemplo ilustrativo · juros hipotéticos, sem impostos nem inflação",
        ["Cálculo próprio: aporte = meta × i ÷ ((1 + i)^n − 1), com i = 0,8% ao mês e n = 24", "Exemplo ilustrativo com taxas hipotéticas (1,5% ao mês para o Léo)"],
        {"linha1": "R$ 10 mil em", "linha2": "2 anos:", "destaque": "guardar ou render?"},
        ["Juntar R$ 10 mil em 2 anos: o que pesa mais, guardar ou render?", "Meta de 2 anos: quanto guardar por mês?"], cenas,
        posts(c, "R$ 10 mil em 2 anos: guardar mais ou render mais?", "Juntar R$ 10 mil em 2 anos: o que pesa mais, guardar ou render?",
              ["Só guardando: [[sem|R]] por mês", "Com juros hipotéticos de 0,8% ao mês: [[A|R]] por mês", "Dos R$ 10 mil, só [[juros|R]] vêm dos juros", "No curto prazo, manda o quanto você guarda."],
              "Qual é a sua meta de dois anos?", "Exemplo ilustrativo, juros hipotéticos, sem impostos nem inflação.",
              ["educacaofinanceira", "metas", "investimentos", "dinheiro"], "Juntar R$ 10 mil em 2 anos: guardar mais ou render mais? A conta."))
