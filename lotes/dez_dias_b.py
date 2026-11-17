"""Lote 21–30/11/2026 (parte B): JQE-S038 a S042."""
import sys
sys.path.insert(0, "/home/claude/juro-que-explico/lotes")
from _lib import *
ASS = assinatura()

# ====================================================== S038 — R$ 6 mil por ano ou R$ 500 por mês (LOOP)
c = Calc({"fvM": "500 * (((1 + taxa_mes) ** 120 - 1) / taxa_mes)",
          "fvAfim": "6000 * (((1 + taxa_mes) ** 120 - 1) / ((1 + taxa_mes) ** 12 - 1))",
          "fvAini": "fvAfim * (1 + taxa_mes) ** 12", "total": "500 * 120", "dif": "fvM - fvAfim",
          "balM": "fvM / fvAini * 100", "balA": "fvAfim / fvAini * 100"},
         {"taxa_mes": 0.008, "mensal": 500, "anual": 6000}, livres=[60])
HOOK = {"a": "R$ 6 mil", "b": "R$ 500", "rotulo_a": "uma vez por ano", "rotulo_b": "todo mês", "centro": "qual rende mais?"}
cenas = [
    cena(c, "hook", "versus", "Seis mil reais uma vez por ano ou quinhentos todo mês: qual rende mais?", HOOK),
    cena(c, "mesmo", "numero_grande",
         "Em dez anos, nos dois jeitos, você coloca a mesma coisa: [[total|mil]]. Seis mil por ano é igual a quinhentos por mês. A única diferença é quando o dinheiro entra.",
         {"valor": "[[total|mil]]", "linhas": ["é o que você coloca", "nos dois jeitos"]}),
    cena(c, "duo", "duo",
         "Olha o Léo e a Bia. O Léo deixa o dinheiro na gaveta e investe tudo no fim do ano, quando cai o décimo terceiro. A Bia investe quinhentos reais todo mês. Quem chega na frente?",
         {"leo": {"fala": "Invisto no fim do ano", "rotulo": "1× por ano, no fim", "valor": c.v("balA"), "texto": "[[fvAfim|mil]]"},
          "bia": {"fala": "Invisto todo mês", "rotulo": "todo mês", "valor": c.v("balM"), "texto": "[[fvM|mil]]"}}),
    cena(c, "barras", "barras",
         "A Bia, mas por pouco: [[fvM|mil]] contra [[fvAfim|mil]], porque o dinheiro dela começa a render mais cedo. E se o Léo investisse os seis mil em janeiro, ele ganharia: [[fvAini|mil]].",
         {"titulo": ["Depois de 10 anos"], "itens": [{"rotulo": "6 mil no fim do ano", "valor": c.v("fvAfim"), "texto": "[[fvAfim|mil]]"}, {"rotulo": "500 por mês", "valor": c.v("fvM"), "texto": "[[fvM|mil]]", "destaque": True},
                                                  {"rotulo": "6 mil em janeiro", "valor": c.v("fvAini"), "texto": "[[fvAini|mil]]"}], "nota": "juros hipotéticos de 0,8% ao mês, sem impostos"}),
    cena(c, "moral", "titulo",
         "Ou seja, não existe jeito certo. Existe o que você consegue manter. Quem guarda todo mês cria um hábito e não depende de sobrar dinheiro no fim do ano. Quanto antes o dinheiro entra, mais ele trabalha.",
         {"titulo": ["Quanto antes entra,", "mais ele trabalha"], "subtitulo": "o melhor jeito é o que você mantém"}),
    cena(c, "lista", "lista", "Resumindo: invista assim que o dinheiro entrar, escolha um ritmo que caiba no bolso e mantenha por anos. Sem pressa e sem promessa de ganho.",
         {"titulo": ["O resumo"], "itens": ["invista logo que entrar", "ritmo que cabe no bolso", "mantenha por anos"]}),
    cena(c, "volta", "versus", "E quando bater a dúvida de como guardar, pergunta:", HOOK),
]
escreve(c, "JQE-S038", "R$ 6 mil por ano ou R$ 500 por mês: qual rende mais?", "Investimentos", "escolha", "versus + personagens (loop)",
        "Exemplo ilustrativo · juros hipotéticos, sem impostos nem inflação",
        ["Cálculo próprio: valor futuro de aportes mensais e anuais, juros hipotéticos de 0,8% ao mês", "Exemplo ilustrativo"],
        {"linha1": "R$ 6 mil por ano", "linha2": "ou R$ 500 por mês?", "destaque": "qual rende mais"},
        ["R$ 6 mil por ano ou R$ 500 por mês?", "Aportar todo mês ou uma vez por ano?"], cenas,
        posts(c, "R$ 6 mil por ano ou R$ 500 por mês: qual rende mais?", "Seis mil reais uma vez por ano ou quinhentos todo mês: qual rende mais?",
              ["Em 10 anos você coloca [[total|mil]] nos dois jeitos", "R$ 500 por mês → [[fvM|mil]]", "R$ 6 mil no fim do ano → [[fvAfim|mil]]", "R$ 6 mil em janeiro → [[fvAini|mil]]", "Quanto antes o dinheiro entra, mais ele trabalha."],
              "Como você guarda: todo mês ou de uma vez?", "Exemplo ilustrativo, juros hipotéticos de 0,8% ao mês, sem impostos.",
              ["educacaofinanceira", "investimentos", "aporte", "dinheiro"], "R$ 6 mil por ano ou R$ 500 por mês? A conta com o Léo e a Bia."),
        loop=True)

# ====================================================== S039 — inflação 5% + 5% não é 10%
c = Calc({"acum2": "(fator ** 2 - 1) * 100", "acum1": "(fator - 1) * 100", "a5": "(fator ** 5 - 1) * 100", "a10": "(fator ** 10 - 1) * 100",
          "p1": "100 * fator", "p2": "100 * fator ** 2", "f2": "fator * fator"},
         {"fator": 1.05, "inflacao": 0.05}, livres=[10, 100])
cenas = [
    cena(c, "hook", "numero_grande", "Dois anos de inflação de cinco por cento não somam dez. Somam mais.",
         {"valor": "[[acum2|p]]", "linhas": ["não são 10%:", "a conta fecha"]}),
    cena(c, "fluxo", "fluxo_setas",
         "Pensa comigo. Uma coisa custa cem reais hoje. Com cinco por cento de inflação, no ano seguinte ela custa cento e cinco. No outro ano, mais cinco por cento, mas agora em cima dos cento e cinco. Dá cento e dez reais e vinte e cinco centavos.",
         {"caixas": [{"texto": "hoje: R$ 100", "tom": "neutro"}, {"texto": "ano 1: [[p1|R2]]", "tom": "cinza"}, {"texto": "ano 2: [[p2|R2]]", "tom": "erro"}],
          "setas": [{"rotulo": "+5%", "tom": "erro"}, {"rotulo": "+5% sobre R$ 105", "tom": "erro"}]},
         leg="Pensa comigo. Uma coisa custa R$ 100 hoje. Com 5% de inflação, no ano seguinte ela custa R$ 105. No outro ano, mais 5%, mas agora em cima dos R$ 105. Dá R$ 110,25."),
    cena(c, "formula", "formula",
         "A conta é multiplicar, não somar. Um vírgula zero cinco vezes um vírgula zero cinco dá um vírgula um zero dois cinco. Ou seja, dez vírgula vinte e cinco por cento.",
         {"titulo": "Multiplica, não soma", "linha1": "1,05 × 1,05", "resultado": "[[f2|n]]", "nota": "= +10,25%"},
         leg="A conta é multiplicar, não somar. 1,05 × 1,05 = 1,1025. Ou seja, 10,25%."),
    cena(c, "barras", "barras",
         "E o efeito vai crescendo. Em cinco anos, a inflação acumulada passa de [[a5|p0]]. Em dez anos, chega perto de [[a10|p0]]. Por isso o preço das coisas parece sempre subir mais do que a gente lembra.",
         {"titulo": ["Inflação acumulada", "com 5% ao ano"], "itens": [{"rotulo": "1 ano", "valor": c.v("acum1"), "texto": "[[acum1|p0]]"}, {"rotulo": "2 anos", "valor": c.v("acum2"), "texto": "[[acum2|p]]"},
                                                                {"rotulo": "5 anos", "valor": c.v("a5"), "texto": "[[a5|p0]]"}, {"rotulo": "10 anos", "valor": c.v("a10"), "texto": "[[a10|p0]]", "destaque": True}],
          "nota": "inflação hipotética e constante"}),
    cena(c, "porque", "titulo",
         "Por que isso importa? Porque o seu salário e o seu dinheiro guardado precisam acompanhar essa conta, e não a soma simples. Se o reajuste ou o rendimento ficar abaixo da inflação, você perde poder de compra sem perceber.",
         {"titulo": ["Salário e dinheiro", "precisam acompanhar"], "subtitulo": "senão, o poder de compra cai sem aviso"}),
    cena(c, "lista", "lista", "Três atitudes ajudam: olhar a inflação acumulada, comparar com o seu reajuste e comparar com o rendimento do que você guarda.",
         {"titulo": ["Três atitudes"], "itens": ["veja a inflação acumulada", "compare com o seu reajuste", "compare com o rendimento"]}),
    cta(c, "cta", "Seu último reajuste passou da inflação? Conta aqui nos comentários.", ["Seu reajuste passou", "da inflação?"]),
    ASS,
]
escreve(c, "JQE-S039", "Inflação: 5% + 5% não é 10%", "Inflação", "contradição", "passo a passo + setas",
        "Exemplo ilustrativo · inflação hipotética e constante de 5% ao ano",
        ["Cálculo próprio: inflação acumulada = (1 + i)^n − 1", "Exemplo ilustrativo, taxa hipotética"],
        {"linha1": "5% + 5%", "linha2": "não é 10%", "destaque": "a conta da inflação"},
        ["Dois anos de inflação de 5% não somam 10%.", "Inflação acumulada: por que soma não funciona."], cenas,
        posts(c, "Inflação: 5% + 5% não é 10% (a conta)", "Dois anos de inflação de 5% não somam 10%. Somam 10,25%.",
              ["R$ 100 → [[p1|R2]] → [[p2|R2]]", "5 anos → [[a5|p0]] acumulados", "10 anos → [[a10|p0]] acumulados", "A conta é multiplicar, não somar."],
              "Seu último reajuste passou da inflação?", "Exemplo ilustrativo, inflação hipotética e constante de 5% ao ano.",
              ["educacaofinanceira", "inflacao", "economia", "dinheiro"], "Dois anos de inflação de 5% somam 10,25%, não 10%. Entenda a conta."))

# ====================================================== S040 — 3 erros de quem começa a investir (LOOP)
c = Calc({"saldo": "100 - perda", "ano": "(1.1 ** 12 - 1) * 100"}, {"perda": 8}, livres=[10, 100, 92, 200])
HOOK = {"valor": "3 erros", "linhas": ["atrapalham quem está", "começando a investir"]}
cenas = [
    cena(c, "hook", "numero_grande", "Três erros atrapalham quem está começando a investir.", HOOK),
    cena(c, "leo", "personagem_queda",
         "Todo mundo já sentiu isso. O primeiro: vender no susto. O Léo colocou cem reais, olhou o saldo e viu oito reais a menos. Entrou em pânico e vendeu. Só que oscilar faz parte, e vender na queda transforma a oscilação em prejuízo de verdade.",
         {"antes": 100, "depois": c.v("saldo"), "fala_antes": "Meus R$ 100!", "fala_depois": "Caiu... vendo tudo!", "badge": "−[[perda|n0]]%"},
         leg="Todo mundo já sentiu isso. O primeiro: vender no susto. O Léo colocou R$ 100, olhou o saldo e viu R$ 8 a menos. Entrou em pânico e vendeu. Só que oscilar faz parte, e vender na queda transforma a oscilação em prejuízo de verdade."),
    cena(c, "promessa", "versus",
         "O segundo: acreditar em ganho fácil. Esse golpe é antigo e funciona porque dá esperança. Se alguém garante dez por cento ao mês, está prometendo mais de duzentos por cento ao ano. Papo reto: se parece bom demais, desconfie.",
         {"a": "10% ao mês", "b": "[[ano|p0]] ao ano", "rotulo_a": "a promessa", "rotulo_b": "a conta", "centro": "desconfie"},
         leg="O segundo: acreditar em ganho fácil. Esse golpe é antigo e funciona porque dá esperança. Se alguém garante 10% ao mês, está prometendo mais de 200% ao ano. Papo reto: se parece bom demais, desconfie."),
    cena(c, "reserva", "fluxo_setas",
         "O terceiro: investir sem ter reserva. Aí vem um imprevisto, o carro quebra, a geladeira pifa, e você precisa tirar o dinheiro justo no dia em que ele está valendo menos. A reserva existe pra isso.",
         {"caixas": [{"texto": "sem reserva", "tom": "neutro"}, {"texto": "vem o imprevisto", "tom": "cinza"}, {"texto": "vende no prejuízo", "tom": "erro"}],
          "setas": [{"rotulo": "e então", "tom": "neutro"}, {"rotulo": "no dia ruim", "tom": "erro"}]}),
    cena(c, "plano", "titulo",
         "A boa notícia: todos esses erros têm cura, e ela se chama plano. Escreva, antes de a queda chegar, o que você vai fazer se ela vier. Quem já decidiu antes não decide no desespero.",
         {"titulo": ["Plano escrito", "antes da queda"], "subtitulo": "decidir com calma vale mais que decidir com medo"}),
    cena(c, "lista", "lista", "Então guarda: não venda no susto, desconfie de ganho fácil e monte uma reserva antes de investir. Ninguém acerta tudo, mas esses três evitam muita dor de cabeça.",
         {"titulo": ["Para lembrar"], "itens": ["não venda no susto", "desconfie de ganho fácil", "reserva antes de investir"]}),
    cena(c, "volta", "numero_grande", "Então, antes de colocar o primeiro real, guarda isso:", HOOK),
]
escreve(c, "JQE-S040", "3 erros de quem está começando a investir", "Comportamento", "erro comum", "lista + personagens (loop)",
        "Exemplo ilustrativo · valores hipotéticos, sem citar investimento",
        ["Conceitos gerais de finanças comportamentais e planejamento", "10% ao mês composto por 12 meses: (1,10^12 − 1) × 100 ≈ 214%", "Exemplo ilustrativo"],
        {"linha1": "3 erros de quem", "linha2": "está começando", "destaque": "a investir"},
        ["Três erros atrapalham quem está começando a investir.", "Os 3 erros que mais assustam quem começa."], cenas,
        posts(c, "3 erros de quem está começando a investir", "Três erros atrapalham quem está começando a investir.",
              ["1. Vender no susto da primeira queda", "2. Acreditar em ganho fácil (10% ao mês = [[ano|p0]] ao ano)", "3. Investir sem ter reserva", "Plano escrito antes da queda ajuda a decidir com calma."],
              "Qual desses erros você já cometeu?", "Exemplo ilustrativo. Não é recomendação de investimento.",
              ["educacaofinanceira", "investimentos", "comecar", "dinheiro"], "3 erros de quem está começando a investir. O Léo já cometeu os três."),
        loop=True)

# ====================================================== S041 — yield on cost
c = Calc({"dy": "dividendo / preco * 100", "div10": "dividendo * (1 + cresc) ** anos", "yoc": "div10 / preco * 100",
          "preco10": "preco * (1 + cresc) ** anos", "dy_hoje": "div10 / preco10 * 100"},
         {"preco": 10, "dividendo": 0.6, "cresc": 0.1, "anos": 10})
cenas = [
    cena(c, "hook", "numero_grande", "Um yield de seis por cento pode passar de quinze sobre o preço pago.",
         {"de": "[[dy|p0]]", "valor": "[[yoc|p]]", "linhas": ["sobre o que", "você pagou"]}),
    cena(c, "formula", "formula",
         "Dividend yield é quanto a ação paga por ano em relação ao preço. Exemplo inventado: você paga dez reais e recebe sessenta centavos por ano. Sessenta centavos sobre dez reais dá seis por cento.",
         {"titulo": "Dividend yield", "linha1": "R$ 0,60 ÷ R$ 10", "resultado": "[[dy|p0]]", "nota": "por ano, sobre o preço pago"},
         leg="Dividend yield é quanto a ação paga por ano em relação ao preço. Exemplo inventado: você paga R$ 10 e recebe R$ 0,60 por ano. R$ 0,60 sobre R$ 10 dá 6%."),
    cena(c, "linhas", "linhas",
         "Agora imagina que a empresa aumente o dividendo em dez por cento ao ano. Depois de dez anos, aquele dividendo de sessenta centavos vira [[div10|R2]] por ação, sobre as mesmas ações que você comprou lá atrás.",
         {"titulo": "Dividendo por ação, +10% ao ano", "x_rotulo": "anos", "x_ticks": [0, 5, 10], "ymax": 1.8, "ymin": 0, "y_passo": 0.6, "y_fmt": "brl",
          "series": [{"nome": "dividendo por ação", "destaque": True, "pontos": [[a, round(0.6 * 1.1 ** a, 3)] for a in range(0, 11)], "velocidade": 0.8, "inicio": 0.2, "rotulo_final": "[[div10|R2]]"}]}),
    cena(c, "versus", "versus",
         "Sobre os dez reais que você pagou, são [[yoc|p]]. Esse é o yield on cost. Só que olha o outro lado: se o preço também subiu junto, o yield sobre o preço de hoje continua em [[dy_hoje|p0]].",
         {"a": "[[yoc|p]]", "b": "[[dy_hoje|p0]]", "rotulo_a": "sobre o que você pagou", "rotulo_b": "sobre o preço de hoje", "centro": "mesmo dividendo"}),
    cena(c, "ressalva", "titulo",
         "Então é só uma lente. Ela mostra como o seu dinheiro antigo está rendendo, mas não prova que foi uma boa compra. Dividendos variam, podem cair e não têm garantia nenhuma.",
         {"titulo": ["Uma lente,", "não uma garantia"], "subtitulo": "dividendos variam e podem cair"}),
    cena(c, "lista", "lista", "Para não se enganar: compare sempre com o preço de hoje, olhe vários anos de dividendos e lembre que isso é exemplo, não recomendação.",
         {"titulo": ["Para não se enganar"], "itens": ["compare com o preço de hoje", "olhe vários anos", "exemplo não é recomendação"]}),
    cta(c, "cta", "Você olha o yield sobre o preço pago ou o de hoje? Comenta.", ["Yield sobre o preço", "pago ou o de hoje?"]),
    ASS,
]
escreve(c, "JQE-S041", "Yield on cost: 6% que viram mais de 15%", "Dividendos", "pergunta com número", "explicador (exemplo hipotético)",
        "Exemplo hipotético · sem citar empresa; dividendos variam e não têm garantia",
        ["Definição: yield on cost = dividendo atual por ação ÷ preço pago", "Exemplo hipotético com crescimento de 10% ao ano do dividendo"],
        {"linha1": "Yield de 6% vira", "linha2": "mais de 15%?", "destaque": "yield on cost"},
        ["Um dividend yield de 6% pode virar mais de 15% sobre o que você pagou.", "O que é yield on cost?"], cenas,
        posts(c, "Yield on cost: de 6% para mais de 15% (a conta)", "Um dividend yield de 6% pode virar mais de 15% sobre o que você pagou.",
              ["Compra a R$ 10, dividendo de R$ 0,60 → 6%", "Dividendo +10% ao ano por 10 anos → [[div10|R2]]", "Sobre o que você pagou: [[yoc|p]]", "Sobre o preço de hoje: [[dy_hoje|p0]]"],
              "Você olha o yield sobre o preço pago ou o de hoje?", "Exemplo hipotético, sem citar empresa. Dividendos variam e não têm garantia. Não é recomendação.",
              ["educacaofinanceira", "dividendos", "investimentos", "bolsa"], "Um dividend yield de 6% pode virar mais de 15% sobre o que você pagou. É o yield on cost."))

# ====================================================== S042 — Price × SAC
c = Calc({"pmt_price": "valor * taxa / (1 - (1 + taxa) ** (-meses))", "tot_price": "pmt_price * meses", "jur_price": "tot_price - valor",
          "amort": "valor / meses", "pmt_sac1": "amort + valor * taxa", "pmt_sacN": "amort * (1 + taxa)",
          "jur_sac": "valor * taxa * (meses + 1) / 2", "dif": "jur_price - jur_sac"},
         {"valor": 200000, "taxa": 0.01, "meses": 240}, livres=[20, 200])
pts_p = [[m, round(c.v("pmt_price"), 2)] for m in (0, 60, 120, 180, 240)]
pts_s = [[m, round(c.v("amort") + (200000 - c.v("amort") * m) * 0.01, 2)] for m in (0, 60, 120, 180, 240)]
cenas = [
    cena(c, "hook", "versus", "Financiamento de duzentos mil reais, mesma taxa: qual sistema cobra mais juros, Price ou SAC?",
         {"a": "Price", "b": "SAC", "rotulo_a": "parcela fixa", "rotulo_b": "parcela que cai", "centro": "quem cobra mais juros?"}),
    cena(c, "fluxo", "fluxo_setas",
         "Exemplo hipotético: duzentos mil, vinte anos, juros de um por cento ao mês. Na Price, a parcela é igual do começo ao fim, mas no começo ela é quase só juros. Por isso o saldo devedor demora a cair, e você paga juros por mais tempo.",
         {"caixas": [{"texto": "Price: parcela fixa", "tom": "neutro"}, {"texto": "começa quase só juros", "tom": "cinza"}, {"texto": "paga mais juros no total", "tom": "erro"}],
          "setas": [{"rotulo": "no começo", "tom": "neutro"}, {"rotulo": "resultado", "tom": "erro"}]}),
    cena(c, "formula", "formula",
         "Na SAC, você amortiza sempre o mesmo valor. Duzentos mil dividido por duzentos e quarenta meses dá oitocentos e trinta e três reais por mês. Em cima disso entram os juros, que diminuem a cada parcela.",
         {"titulo": "SAC: amortização fixa", "linha1": "R$ 200 mil ÷ 240", "resultado": "[[amort|R]]", "nota": "por mês, mais os juros do saldo"},
         leg="Na SAC, você amortiza sempre o mesmo valor. R$ 200 mil ÷ 240 meses = R$ 833 por mês. Em cima disso entram os juros, que diminuem a cada parcela."),
    cena(c, "linhas", "linhas",
         "Olha as parcelas. A Price fica em [[pmt_price|R]] o tempo todo. A SAC começa em [[pmt_sac1|R]], mais pesada, mas cai até [[pmt_sacN|R]] no fim.",
         {"titulo": "Parcela ao longo dos 240 meses", "x_rotulo": "meses", "x_ticks": [0, 60, 120, 180, 240], "ymax": 3000, "ymin": 0, "y_passo": 1000, "y_fmt": "brl",
          "series": [{"nome": "Price", "pontos": pts_p, "velocidade": 0.8, "inicio": 0.2}, {"nome": "SAC", "destaque": True, "pontos": pts_s, "velocidade": 0.8, "inicio": 0.4, "rotulo_final": "[[pmt_sacN|R]]"}]}),
    cena(c, "barras", "barras",
         "E a conta final dos juros: na Price, [[jur_price|mil]]. Na SAC, [[jur_sac|mil]]. A SAC custa uns [[dif|mil]] a menos de juros.",
         {"titulo": ["Juros pagos", "no total"], "itens": [{"rotulo": "Price", "valor": c.v("jur_price"), "texto": "[[jur_price|mil]]", "destaque": True}, {"rotulo": "SAC", "valor": c.v("jur_sac"), "texto": "[[jur_sac|mil]]"}],
          "nota": "taxa hipotética, sem seguros e tarifas"}),
    cena(c, "tradeoff", "titulo",
         "Mas atenção: a SAC pede uma parcela maior no começo. Se ela não cabe no seu orçamento, a mais barata no total pode ser a pior pra você. O melhor sistema é o que você consegue pagar até o fim.",
         {"titulo": ["O melhor é o que", "você paga até o fim"], "subtitulo": "parcela maior hoje × juros menores no total"}),
    cta(c, "cta", "Você prefere parcela menor agora ou menos juros no fim? Comenta.", ["Parcela menor agora", "ou menos juros?"]),
    ASS,
]
escreve(c, "JQE-S042", "Financiamento: Price ou SAC, qual cobra mais juros?", "Crédito", "escolha", "versus + explicador",
        "Exemplo hipotético · 1% ao mês, 20 anos, sem seguros nem tarifas",
        ["Price: PMT = VP × i ÷ (1 − (1 + i)^−n)", "SAC: amortização = VP ÷ n; juros totais = VP × i × (n + 1) ÷ 2", "Exemplo hipotético; as taxas reais variam"],
        {"linha1": "Price ou SAC:", "linha2": "quem cobra mais", "destaque": "juros?"},
        ["Financiamento de R$ 200 mil, mesma taxa: qual cobra mais juros?", "Price × SAC em 1 minuto."], cenas,
        posts(c, "Financiamento: Price ou SAC, qual cobra mais juros?", "Financiamento de R$ 200 mil, mesma taxa: qual sistema cobra mais juros?",
              ["Price: parcela fixa de [[pmt_price|R]], juros totais de [[jur_price|mil]]", "SAC: parcela de [[pmt_sac1|R]] caindo até [[pmt_sacN|R]], juros de [[jur_sac|mil]]", "A SAC custa uns [[dif|mil]] a menos de juros", "Mas pede parcela maior no começo."],
              "Parcela menor agora ou menos juros no fim?", "Exemplo hipotético, 1% ao mês por 20 anos, sem seguros nem tarifas. Taxas reais variam.",
              ["educacaofinanceira", "financiamento", "juros", "dinheiro"], "Price ou SAC: qual cobra mais juros num financiamento de R$ 200 mil? A conta."))
