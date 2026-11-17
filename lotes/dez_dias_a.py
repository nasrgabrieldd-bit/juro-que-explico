"""Lote 21–30/11/2026 (parte A): JQE-S033 a S037. Skill 2.2: tom honesto/amigo, personagens e setas, alguns em loop."""
import sys
sys.path.insert(0, "/home/claude/juro-que-explico/lotes")
from _lib import *

M = json.load(open(f"{REPO}/marca/marca.json"))
ASS = assinatura()

# ====================================================== S033 — quanto por mês para R$ 1 milhão (LOOP)
c = Calc({"meses": "anos * 12",
          "A25": "meta * taxa_mes / ((1 + taxa_mes) ** 300 - 1)",
          "A15": "meta * taxa_mes / ((1 + taxa_mes) ** 180 - 1)",
          "A35": "meta * taxa_mes / ((1 + taxa_mes) ** 420 - 1)",
          "aportado": "A25 * 300", "juros": "meta - aportado", "razao": "A15 / A25",
          "ben": "A25 / A15 * 100"},
         {"meta": 1000000, "taxa_mes": 0.008, "anos": 25}, livres=[15, 35, 300])
HOOK = {"valor": "R$ 1 milhão", "linhas": ["em [[anos|n0]] anos:", "quanto por mês?"]}
cenas = [
    cena(c, "hook", "numero_grande", "Quanto por mês vira um milhão de reais em [[anos|n0]] anos? Menos do que você imagina.", HOOK),
    cena(c, "fluxo", "fluxo_setas",
         "Papo reto: ninguém fica milionário de um dia pro outro. Mas o caminho é uma conta. Com juros hipotéticos de [[taxa_mes|pf]] ao mês, guardar [[A25|R]] por mês, durante [[meses|n0]] meses, chega lá.",
         {"caixas": [{"texto": "[[A25|R]] por mês", "tom": "neutro"}, {"texto": "[[meses|n0]] meses", "tom": "cinza"}, {"texto": "R$ 1 milhão", "tom": "ok"}],
          "setas": [{"rotulo": "[[taxa_mes|pf]] ao mês", "tom": "neutro"}, {"rotulo": "juros compostos", "tom": "neutro"}]}),
    cena(c, "tempo", "barras",
         "E quem manda aqui é o tempo. Em quinze anos, o valor sobe pra [[A15|R]] por mês. Em vinte e cinco, [[A25|R]]. Em trinta e cinco, só [[A35|R]].",
         {"titulo": ["Aporte mensal para", "chegar ao milhão"],
          "itens": [{"rotulo": "15 anos", "valor": c.v("A15"), "texto": "[[A15|R]]"}, {"rotulo": "25 anos", "valor": c.v("A25"), "texto": "[[A25|R]]", "destaque": True},
                    {"rotulo": "35 anos", "valor": c.v("A35"), "texto": "[[A35|R]]"}], "nota": "juros hipotéticos, sem impostos"}),
    cena(c, "origem", "formula",
         "Desse milhão, quanto saiu do seu bolso? Só [[aportado|mil]]. O resto, [[juros|mil]], foi o dinheiro trabalhando.",
         {"titulo": "De onde vem o milhão", "linha1": "[[aportado|mil]] dos seus aportes", "resultado": "[[juros|mil]]", "nota": "vieram dos juros"}),
    cena(c, "duo", "duo",
         "Agora olha a Bia e o Léo. A Bia começou hoje. O Léo esperou dez anos. Pra chegar no mesmo milhão, ele precisa guardar [[razao|x]] mais por mês.",
         {"leo": {"fala": "Começo ano que vem", "rotulo": "começa em 10 anos", "valor": 100, "texto": "[[A15|R]]"},
          "bia": {"fala": "Começo hoje!", "rotulo": "começa hoje", "valor": c.v("ben"), "texto": "[[A25|R]]"}}),
    cena(c, "moral", "lista",
         "Sem promessa: a taxa é hipotética e o mercado oscila. O ponto é outro. Começar cedo, com o que cabe no bolso, vale mais do que esperar o valor perfeito.",
         {"titulo": ["O que importa"], "itens": ["começar com o que cabe", "constância todo mês", "dar tempo ao tempo"]}),
    cena(c, "volta", "numero_grande", "E se alguém disser que um milhão é coisa de rico, pergunta:", HOOK),
]
escreve(c, "JQE-S033", "Quanto por mês vira R$ 1 milhão em 25 anos?", "Investimentos", "pergunta com número", "explicador + personagens (loop)",
        "Exemplo ilustrativo · juros hipotéticos, sem impostos nem inflação",
        ["Cálculo próprio: aporte = meta × i ÷ ((1 + i)^n − 1), com i = 0,8% ao mês", "Exemplo ilustrativo com taxa hipotética"],
        {"linha1": "Quanto por mês", "linha2": "vira R$ 1 milhão?", "destaque": "em 25 anos"},
        ["Um milhão em 25 anos custa menos do que você imagina.", "Quanto por mês vira R$ 1 milhão em 25 anos?"], cenas,
        posts(c, "Quanto por mês vira R$ 1 milhão em 25 anos? A conta", "Quanto por mês vira R$ 1 milhão em [[anos|n0]] anos? Menos do que você imagina.",
              ["15 anos → [[A15|R]] por mês", "25 anos → [[A25|R]] por mês", "35 anos → [[A35|R]] por mês", "Só [[aportado|mil]] saem do seu bolso."],
              "Quanto você consegue guardar por mês?", "Exemplo ilustrativo, juros hipotéticos de 0,8% ao mês, sem impostos.",
              ["educacaofinanceira", "investimentos", "jurocomposto", "dinheiro"], "Quanto por mês vira R$ 1 milhão em 25 anos? A conta com o Léo e a Bia."),
        loop=True)

# ====================================================== S034 — 3 perguntas antes de investir
c = Calc({"queda": "1000 * (1 - 0.1)"}, {"valor": 1000, "queda_pct": 0.1}, livres=[3, 20])
cenas = [
    cena(c, "hook", "numero_grande", "Quase todo mundo escolhe onde investir antes de responder três perguntas. Papo reto: isso dá dor de cabeça.",
         {"valor": "3", "linhas": ["perguntas antes de", "escolher onde investir"]}),
    cena(c, "p1", "titulo", "A primeira: pra quê é esse dinheiro? Viagem, reserva, casa, aposentadoria. Sem objetivo, qualquer investimento parece bom, e a gente acaba escolhendo pelo que o amigo falou. Cada objetivo pede um tipo de investimento diferente.",
         {"titulo": ["1. Pra quê", "é esse dinheiro?"], "subtitulo": "viagem · reserva · casa · aposentadoria"}),
    cena(c, "p2", "versus", "A segunda: quando você vai precisar dele? Se é em seis meses, o dinheiro não pode ficar balançando, porque você pode precisar tirar justo num dia ruim. Se é em vinte anos, dá tempo de passar por altos e baixos.",
         {"a": "6 meses", "b": "20 anos", "rotulo_a": "precisa de segurança", "rotulo_b": "aguenta oscilar", "centro": "prazo"}),
    cena(c, "p3", "formula", "A terceira: você dorme bem se o saldo cair? Imagina mil reais virando novecentos. Se isso tira o seu sono, tudo bem: é só um sinal para escolher um risco menor.",
         {"titulo": "O teste do sono", "linha1": "[[valor|R]] − 10%", "resultado": "[[queda|R]]", "nota": "você aguentaria?"},
         leg="Imagina [[valor|R]] virando [[queda|R]]. Se isso tira o seu sono, tudo bem: é só um sinal para escolher um risco menor."),
    cena(c, "resumo", "fluxo_setas", "Objetivo, prazo e risco, nessa ordem. Depois disso, a escolha do investimento fica bem mais fácil, e você para de se comparar com o resultado dos outros. Não existe o investimento perfeito, existe o que combina com você.",
         {"caixas": [{"texto": "Objetivo", "tom": "neutro"}, {"texto": "Prazo", "tom": "cinza"}, {"texto": "Risco", "tom": "ok"}],
          "setas": [{"rotulo": "define", "tom": "neutro"}, {"rotulo": "define", "tom": "neutro"}]}),
    cena(c, "hoje", "lista", "Então faz hoje: escreve o objetivo, define o prazo dele e vê que risco você aguenta. Leva dez minutos e evita muito arrependimento.",
         {"titulo": ["Faça hoje"], "itens": ["escreva o seu objetivo", "defina o prazo dele", "veja o risco que aguenta"]}),
    cta(c, "cta", "Qual é o seu objetivo agora? Conta aqui nos comentários.", ["Qual é o seu", "objetivo agora?"]),
    ASS,
]
escreve(c, "JQE-S034", "3 perguntas antes de escolher onde investir", "Investimentos", "erro comum", "passo a passo (conselho de amigo)",
        "Conteúdo educativo · exemplo ilustrativo, sem citar investimento",
        ["Conceitos gerais de planejamento financeiro (objetivo, prazo e tolerância a risco)", "Exemplo ilustrativo: R$ 1.000 − 10% = R$ 900"],
        {"linha1": "3 perguntas antes", "linha2": "de investir", "destaque": "objetivo · prazo · risco"},
        ["3 perguntas antes de escolher onde investir.", "Antes de escolher o investimento, responda isto."], cenas,
        posts(c, "3 perguntas antes de escolher onde investir", "Quase todo mundo escolhe onde investir antes de responder 3 perguntas.",
              ["1. Pra quê é esse dinheiro?", "2. Quando você vai precisar dele?", "3. Você dorme bem se o saldo cair?", "Objetivo, prazo e risco: nessa ordem."],
              "Qual é o seu objetivo agora?", "Exemplo ilustrativo. Não é recomendação de investimento.",
              ["educacaofinanceira", "investimentos", "comecar", "dinheiro"], "3 perguntas antes de escolher onde investir: objetivo, prazo e risco."))

# ====================================================== S035 — dá para começar com R$ 30 (LOOP)
c = Calc({"f10": "aporte * (((1 + taxa_mes) ** 120 - 1) / taxa_mes)", "f20": "aporte * (((1 + taxa_mes) ** 240 - 1) / taxa_mes)",
          "f30": "aporte * (((1 + taxa_mes) ** 360 - 1) / taxa_mes)", "dado10": "aporte * 120", "bia": "10"},
         {"aporte": 30, "taxa_mes": 0.008}, livres=[10, 20, 30])
HOOK = {"valor": "R$ 30", "linhas": ["por mês já é", "um começo de verdade"]}
cenas = [
    cena(c, "hook", "numero_grande", "Dá para começar a investir com trinta reais por mês. Sem enrolação.", HOOK),
    cena(c, "fluxo", "fluxo_setas",
         "Eu sei: trinta reais parece pouco. Mas olha. Trinta reais por mês, durante dez anos, são só [[dado10|R]] saindo do seu bolso. Com os juros hipotéticos, viram [[f10|mil]].",
         {"caixas": [{"texto": "[[aporte|R]] por mês", "tom": "neutro"}, {"texto": "10 anos", "tom": "cinza"}, {"texto": "[[f10|mil]]", "tom": "ok"}],
          "setas": [{"rotulo": "todo mês", "tom": "neutro"}, {"rotulo": "juros hipotéticos", "tom": "neutro"}]}),
    cena(c, "barras", "barras",
         "E o tempo faz o resto. Em dez anos, [[f10|mil]]. Em vinte, [[f20|mil]]. Em trinta anos, [[f30|mil]], sempre com os mesmos trinta reais por mês.",
         {"titulo": ["R$ 30 por mês,", "sem aumentar nada"], "itens": [{"rotulo": "10 anos", "valor": c.v("f10"), "texto": "[[f10|mil]]"}, {"rotulo": "20 anos", "valor": c.v("f20"), "texto": "[[f20|mil]]"},
                                                                  {"rotulo": "30 anos", "valor": c.v("f30"), "texto": "[[f30|mil]]", "destaque": True}], "nota": "juros hipotéticos de 0,8% ao mês, sem impostos"}),
    cena(c, "duo", "duo",
         "Olha a Bia e o Léo. O Léo disse: vou esperar sobrar mais dinheiro pra começar. Só que sempre aparece uma conta nova. A Bia começou com trinta reais. Dez anos depois, um tem zero. A outra tem [[f10|mil]].",
         {"leo": {"fala": "Espero sobrar mais", "rotulo": "esperou", "valor": 6, "texto": "R$ 0"},
          "bia": {"fala": "Começo com R$ 30", "rotulo": "começou", "valor": 100, "texto": "[[f10|mil]]"}}),
    cena(c, "habito", "titulo",
         "O valor é o de menos. O que pesa é o hábito: guardar todo mês, sem falhar, mesmo nos meses apertados. Depois, quando der, você aumenta, e ninguém precisa saber o quanto você guarda.",
         {"titulo": ["O hábito pesa", "mais que o valor"], "subtitulo": "comece pequeno, aumente depois"}),
    cena(c, "passos", "lista", "O primeiro passo é simples: escolhe um valor que não aperta, programa pra sair todo mês e aumenta quando puder. Sem promessa de ganho, só método.",
         {"titulo": ["O primeiro passo"], "itens": ["escolha um valor leve", "automatize todo mês", "aumente quando puder"]}),
    cena(c, "volta", "numero_grande", "Então, se alguém disser que precisa de muito dinheiro pra começar, lembra:", HOOK),
]
escreve(c, "JQE-S035", "Dá para começar a investir com R$ 30 por mês", "Investimentos", "contradição", "explicador + personagens (loop)",
        "Exemplo ilustrativo · juros hipotéticos, sem impostos nem inflação",
        ["Cálculo próprio: valor futuro de aportes mensais, VF = A × ((1 + i)^n − 1) ÷ i, com i = 0,8% ao mês", "Exemplo ilustrativo com taxa hipotética"],
        {"linha1": "Dá para começar", "linha2": "com R$ 30", "destaque": "por mês"},
        ["Dá para começar a investir com R$ 30 por mês.", "R$ 30 por mês ainda vale a pena?"], cenas,
        posts(c, "Dá para começar a investir com R$ 30 por mês", "Dá para começar a investir com R$ 30 por mês. Sem enrolação.",
              ["10 anos → [[f10|mil]] (você coloca [[dado10|R]])", "20 anos → [[f20|mil]]", "30 anos → [[f30|mil]]", "O hábito pesa mais que o valor."],
              "Com quanto você começaria?", "Exemplo ilustrativo, juros hipotéticos de 0,8% ao mês, sem impostos.",
              ["educacaofinanceira", "investimentos", "comecar", "dinheiro"], "Dá para começar a investir com R$ 30 por mês. A conta com a Bia e o Léo."),
        loop=True)

# ====================================================== S036 — preço × valor
c = Calc({"pl_a": "2 / 0.1", "pl_b": "50 / 10", "lucro_a": "0.1", "lucro_b": "10"}, {"preco_a": 2, "preco_b": 50}, livres=[20])
cenas = [
    cena(c, "hook", "versus", "Uma ação de [[preco_a|R]] pode ser mais cara que uma de [[preco_b|R]].",
         {"a": "R$ 2", "b": "R$ 50", "rotulo_a": "ação A", "rotulo_b": "ação B", "centro": "qual é mais cara?"}),
    cena(c, "fluxoa", "fluxo_setas",
         "Exemplo inventado, sem citar nenhuma empresa. A ação A custa dois reais e a empresa lucra dez centavos por ação ao ano. Dividindo o preço pelo lucro, dá vinte. É o P/L: quantos anos de lucro o preço representa.",
         {"caixas": [{"texto": "preço R$ 2", "tom": "neutro"}, {"texto": "lucro R$ 0,10", "tom": "cinza"}, {"texto": "P/L = [[pl_a|n0]]", "tom": "erro"}],
          "setas": [{"rotulo": "÷ lucro por ação", "tom": "neutro"}, {"rotulo": "anos de lucro", "tom": "neutro"}]},
         leg="Exemplo inventado. A ação A custa R$ 2 e a empresa lucra R$ 0,10 por ação ao ano. Dividindo o preço pelo lucro, dá 20. É o P/L: quantos anos de lucro o preço representa."),
    cena(c, "formulab", "formula",
         "Já a ação B custa cinquenta reais, mas a empresa lucra dez reais por ação ao ano. Cinquenta dividido por dez dá cinco. Ou seja, o preço dela se paga com cinco anos de lucro.",
         {"titulo": "A ação B", "linha1": "R$ 50 ÷ R$ 10", "resultado": "P/L = [[pl_b|n0]]", "nota": "5 anos de lucro"},
         leg="Já a ação B custa R$ 50, mas a empresa lucra R$ 10 por ação. R$ 50 ÷ R$ 10 = 5."),
    cena(c, "barras", "barras",
         "Pelo preço, a A parece barata. Pelo lucro que ela entrega, é quatro vezes mais cara. Preço de etiqueta não diz se é pechincha, assim como o preço de um carro não diz se ele é um bom negócio.",
         {"titulo": ["Anos de lucro para", "pagar o preço"], "itens": [{"rotulo": "ação A (R$ 2)", "valor": c.v("pl_a"), "texto": "[[pl_a|n0]] anos", "destaque": True}, {"rotulo": "ação B (R$ 50)", "valor": c.v("pl_b"), "texto": "[[pl_b|n0]] anos"}],
          "nota": "exemplo hipotético, sem citar empresa"}),
    cena(c, "ressalva", "titulo",
         "Mas atenção: P/L baixo não é sinal de compra. Pode ser que o lucro vá cair, ou que a empresa tenha uma dívida enorme. É uma régua pra comparar, não uma resposta pronta, e nada aqui é recomendação.",
         {"titulo": ["P/L é uma régua,", "não uma resposta"], "subtitulo": "serve para comparar, não para decidir sozinho"}),
    cena(c, "perguntas", "lista", "Antes de achar que algo está barato, pergunta: quanto a empresa lucra? Esse lucro se mantém? E quanto ela deve?",
         {"titulo": ["Antes de achar", "que está barato"], "itens": ["quanto ela lucra?", "o lucro se mantém?", "quanto ela deve?"]}),
    cta(c, "cta", "Você olha o preço ou o valor? Responde aqui.", ["Preço ou valor:", "o que você olha?"]),
    ASS,
]
escreve(c, "JQE-S036", "Ação de R$ 2 pode ser mais cara que uma de R$ 50", "Investimentos", "contradição", "versus (exemplo hipotético)",
        "Exemplo hipotético · sem citar empresa nem recomendar compra",
        ["Definição de P/L: preço ÷ lucro por ação", "Exemplo hipotético com empresas inventadas"],
        {"linha1": "R$ 2 pode ser", "linha2": "mais cara que R$ 50", "destaque": "preço ≠ valor"},
        ["Uma ação de R$ 2 pode ser mais cara que uma de R$ 50.", "Ação barata é pechincha? Depende da conta."], cenas,
        posts(c, "Ação de R$ 2 pode ser mais cara que uma de R$ 50", "Uma ação de R$ 2 pode ser mais cara que uma de R$ 50.",
              ["Ação A: R$ 2, lucro de R$ 0,10 → P/L 20", "Ação B: R$ 50, lucro de R$ 10 → P/L 5", "P/L = preço ÷ lucro por ação (anos de lucro)", "É uma régua para comparar, não uma resposta pronta."],
              "Você olha o preço ou o valor?", "Exemplo hipotético, sem citar empresa. Não é recomendação de compra ou venda.",
              ["educacaofinanceira", "investimentos", "bolsa", "acoes"], "Uma ação de R$ 2 pode ser mais cara que uma de R$ 50. Entenda o P/L."))

# ====================================================== S037 — dívida a 10% ao mês dobra em 7 meses
c = Calc({"m4": "divida * (1 + taxa) ** 4", "m8": "divida * (1 + taxa) ** 8", "m7": "divida * (1 + taxa) ** 7", "m12": "divida * (1 + taxa) ** 12",
          "simples12": "divida * (1 + taxa * 12)", "regra72": "72 / 10"},
         {"divida": 1000, "taxa": 0.10}, livres=[72])
pts_c = [[m, round(1000 * 1.1 ** m, 2)] for m in range(0, 13)]
pts_s = [[m, round(1000 * (1 + 0.1 * m), 2)] for m in range(0, 13)]
cenas = [
    cena(c, "hook", "numero_grande", "Mil reais de dívida a dez por cento ao mês dobram em menos de oito meses.",
         {"de": "R$ 1.000", "valor": "R$ 2.000", "linhas": ["em menos de", "8 meses"]}),
    cena(c, "fluxo", "fluxo_setas",
         "Sem julgamento: acontece com muita gente. É que os juros incidem sobre os juros. No quarto mês, a dívida já é [[m4|R]]. No oitavo, [[m8|R]].",
         {"caixas": [{"texto": "hoje: [[divida|R]]", "tom": "neutro"}, {"texto": "mês 4: [[m4|R]]", "tom": "cinza"}, {"texto": "mês 8: [[m8|R]]", "tom": "erro"}],
          "setas": [{"rotulo": "+10% ao mês", "tom": "erro"}, {"rotulo": "+10% ao mês", "tom": "erro"}]}),
    cena(c, "linhas", "linhas",
         "Olha a curva. A linha reta seria se os juros incidissem só sobre os mil reais iniciais. Mas eles incidem sobre tudo o que já foi somado, e em um ano a dívida passa de [[m12|mil]]. É por isso que ela foge do controle.",
         {"titulo": "Dívida de R$ 1.000 a 10% ao mês", "x_rotulo": "meses", "x_ticks": [0, 4, 8, 12], "ymax": 3400, "ymin": 0, "y_passo": 1000, "y_fmt": "brl",
          "series": [{"nome": "juros simples", "pontos": pts_s, "velocidade": 0.8, "inicio": 0.2},
                     {"nome": "juros compostos", "destaque": True, "pontos": pts_c, "velocidade": 0.8, "inicio": 0.4, "rotulo_final": "[[m12|mil]]"}]}),
    cena(c, "regra", "formula",
         "E tem um atalho de cabeça: divide setenta e dois pela taxa. Setenta e dois dividido por dez dá sete vírgula dois meses pra dívida dobrar.",
         {"titulo": "A regra dos 72", "linha1": "72 ÷ 10", "resultado": "[[regra72|n]] meses", "nota": "tempo para a dívida dobrar"},
         leg="E tem um atalho de cabeça: divide 72 pela taxa. 72 ÷ 10 = 7,2 meses pra dívida dobrar."),
    cena(c, "sem_julgar", "titulo", "A boa notícia: quanto antes você mexe, menor o estrago. Conversar com o credor e trocar a dívida cara por uma mais barata pode parar essa curva.",
         {"titulo": ["Quanto antes,", "menor o estrago"], "subtitulo": "conversar com o credor já ajuda"}),
    cena(c, "lista", "lista", "Três coisas ajudam: negociar a taxa, trocar a dívida cara por uma mais barata e evitar pagar só o mínimo, que deixa os juros crescerem.",
         {"titulo": ["O que ajuda"], "itens": ["negociar a taxa", "trocar por dívida mais barata", "evitar pagar só o mínimo"]}),
    cta(c, "cta", "Já passou por isso? Conta nos comentários, sem vergonha.", ["Já passou por isso?", "Sem vergonha."]),
    ASS,
]
escreve(c, "JQE-S037", "Dívida a 10% ao mês dobra em menos de 8 meses", "Dívidas", "custo escondido", "explicador + setas",
        "Exemplo ilustrativo · taxa hipotética de 10% ao mês, sem tarifas",
        ["Cálculo próprio: M = P × (1 + i)^n", "Regra dos 72: tempo ≈ 72 ÷ taxa (%)", "Exemplo ilustrativo, taxa hipotética"],
        {"linha1": "Dívida a 10%", "linha2": "ao mês dobra", "destaque": "em menos de 8 meses"},
        ["Mil reais de dívida a 10% ao mês passam de dois mil em oito meses.", "Quanto uma dívida cresce em um ano?"], cenas,
        posts(c, "Dívida a 10% ao mês dobra em menos de 8 meses", "Mil reais de dívida a 10% ao mês passam de dois mil em oito meses.",
              ["Mês 4 → [[m4|R]]", "Mês 8 → [[m8|R]]", "Em 1 ano → [[m12|mil]]", "Regra dos 72: 72 ÷ 10 = 7,2 meses para dobrar."],
              "Você já passou por isso?", "Exemplo ilustrativo, taxa hipotética de 10% ao mês.",
              ["educacaofinanceira", "dividas", "juros", "dinheiro"], "Mil reais a 10% ao mês passam de dois mil em oito meses. Entenda a conta."))
