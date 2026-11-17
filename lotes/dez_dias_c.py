"""Lote 21–30/11/2026 (parte C): JQE-S043 a S047."""
import sys
sys.path.insert(0, "/home/claude/juro-que-explico/lotes")
from _lib import *
ASS = assinatura()

# ====================================================== S043 — R$ 800 hoje ou R$ 1.000 em 5 anos
c = Calc({"vp": "1000 / (1 + taxa) ** 5", "fv800": "800 * (1 + taxa) ** 5", "vp3": "1000 / (1.03) ** 5", "dif": "fv800 - 1000",
          "balvp": "vp / 800 * 100"},
         {"taxa": 0.10}, livres=[800, 1000, 3, 1.1])
cenas = [
    cena(c, "hook", "versus", "Mil reais daqui a cinco anos ou oitocentos reais hoje: o que vale mais?",
         {"a": "R$ 800", "b": "R$ 1.000", "rotulo_a": "hoje", "rotulo_b": "daqui a 5 anos", "centro": "o que vale mais?"}),
    cena(c, "fluxo", "fluxo_setas",
         "Parece óbvio: mil é mais que oitocentos. Mas o dinheiro tem um ingrediente escondido: o tempo. Se você investe os oitocentos a dez por cento ao ano, que é uma taxa hipotética, em cinco anos eles viram [[fv800|R]].",
         {"caixas": [{"texto": "hoje: R$ 800", "tom": "neutro"}, {"texto": "investe 5 anos", "tom": "cinza"}, {"texto": "[[fv800|R]]", "tom": "ok"}],
          "setas": [{"rotulo": "10% ao ano", "tom": "neutro"}, {"rotulo": "juros compostos", "tom": "neutro"}]}),
    cena(c, "formula", "formula",
         "O caminho inverso também funciona. Pra saber quanto vale hoje o mil que só chega daqui a cinco anos, você divide por um vírgula um elevado a cinco. O resultado é [[vp|R]].",
         {"titulo": "Valor presente", "linha1": "R$ 1.000 ÷ 1,1⁵", "resultado": "[[vp|R]]", "nota": "é o que o R$ 1.000 vale hoje"},
         leg="O caminho inverso também funciona. Pra saber quanto vale hoje os R$ 1.000 que só chegam daqui a 5 anos, você divide por 1,1 elevado a 5. O resultado é [[vp|R]]."),
    cena(c, "duo", "duo",
         "Olha o Léo e a Bia. O Léo escolheu esperar pelos mil reais. A Bia pegou os oitocentos e investiu. No fim, a Bia ficou com [[fv800|R]], mais que os mil do Léo.",
         {"leo": {"fala": "Prefiro os R$ 1.000", "rotulo": "esperou 5 anos", "valor": 78, "texto": "R$ 1.000"},
          "bia": {"fala": "Levo R$ 800 hoje", "rotulo": "investiu os R$ 800", "valor": 100, "texto": "[[fv800|R]]"}}),
    cena(c, "depende", "titulo",
         "Mas atenção, isso depende da taxa. Se o seu dinheiro rende só três por cento ao ano, os mil reais futuros valem [[vp3|R]] hoje, e aí esperar compensa. O tempo tem preço, e o preço é a taxa.",
         {"titulo": ["O tempo tem preço,", "e o preço é a taxa"], "subtitulo": "com taxa menor, esperar pode compensar"}),
    cena(c, "lista", "lista", "Então, antes de aceitar um dinheiro futuro, pergunta: quanto eu conseguiria ganhar com ele hoje, o quanto eu confio em quem vai pagar e se eu preciso dele agora.",
         {"titulo": ["Pergunte antes"], "itens": ["quanto renderia hoje?", "confio em quem vai pagar?", "preciso dele agora?"]}),
    cta(c, "cta", "Você prefere o dinheiro hoje ou depois? Responde nos comentários.", ["Dinheiro hoje", "ou depois?"]),
    ASS,
]
escreve(c, "JQE-S043", "R$ 800 hoje ou R$ 1.000 em 5 anos: o que vale mais?", "Investimentos", "escolha", "versus + personagens",
        "Exemplo ilustrativo · taxa hipotética de 10% ao ano, sem impostos",
        ["Cálculo próprio: valor presente = VF ÷ (1 + i)^n; valor futuro = VP × (1 + i)^n", "Exemplo ilustrativo com taxas hipotéticas"],
        {"linha1": "R$ 800 hoje ou", "linha2": "R$ 1.000 em 5 anos", "destaque": "valor presente"},
        ["R$ 800 hoje ou R$ 1.000 daqui a 5 anos?", "Quanto vale hoje o dinheiro do futuro?"], cenas,
        posts(c, "R$ 800 hoje ou R$ 1.000 em 5 anos: o que vale mais?", "Mil reais daqui a cinco anos ou oitocentos reais hoje: o que vale mais?",
              ["R$ 800 investidos a 10% ao ano → [[fv800|R]] em 5 anos", "R$ 1.000 em 5 anos valem [[vp|R]] hoje (a 10% ao ano)", "Com taxa de 3% ao ano, valem [[vp3|R]] hoje", "O tempo tem preço, e o preço é a taxa."],
              "Dinheiro hoje ou depois: o que você escolhe?", "Exemplo ilustrativo, taxas hipotéticas, sem impostos.",
              ["educacaofinanceira", "investimentos", "valorpresente", "dinheiro"], "R$ 800 hoje ou R$ 1.000 em 5 anos? A conta do valor presente."))

# ====================================================== S044 — CET (LOOP)
def _cet():
    pmt, rec = 472.45, 4650.0
    lo, hi = 0.0, 0.2
    for _ in range(80):
        r = (lo + hi) / 2
        v = pmt * (1 - (1 + r) ** -12) / r
        lo, hi = (r, hi) if v > rec else (lo, r)
    return round((lo + hi) / 2, 6)
CET = _cet()
c = Calc({"pmt": "valor * taxa / (1 - (1 + taxa) ** (-12))", "recebe": "valor - extras", "devolve": "pmt * 12",
          "extra_pago": "devolve - recebe", "anual_anunciada": "((1 + taxa) ** 12 - 1) * 100", "anual_cet": "((1 + cet) ** 12 - 1) * 100",
          "confere": "pmt * (1 - (1 + cet) ** (-12)) / cet"},
         {"valor": 5000, "taxa": 0.0199, "extras": 350, "cet": CET}, livres=[12])
HOOK = {"valor": "1,99%", "linhas": ["ao mês parece pouco,", "mas o custo é maior"]}
cenas = [
    cena(c, "hook", "numero_grande", "Taxa de um vírgula noventa e nove por cento ao mês parece pouco. Mas o custo de verdade é maior.", HOOK,
         leg="Taxa de 1,99% ao mês parece pouco. Mas o custo de verdade é maior."),
    cena(c, "fluxo", "fluxo_setas",
         "Exemplo hipotético. Você contrata cinco mil reais, mas o banco desconta trezentos e cinquenta de tarifa e seguro. Na sua conta, entram só [[recebe|R]].",
         {"caixas": [{"texto": "contrata R$ 5.000", "tom": "neutro"}, {"texto": "tarifa e seguro −R$ 350", "tom": "erro"}, {"texto": "recebe [[recebe|R]]", "tom": "cinza"}],
          "setas": [{"rotulo": "desconta", "tom": "erro"}, {"rotulo": "cai na conta", "tom": "neutro"}]},
         leg="Exemplo hipotético. Você contrata R$ 5.000, mas o banco desconta R$ 350 de tarifa e seguro. Na sua conta, entram só [[recebe|R]]."),
    cena(c, "formula", "formula",
         "Só que as doze parcelas são calculadas sobre os cinco mil. Cada uma sai por [[pmt|R]], e no total você devolve [[devolve|R]] por um dinheiro que realmente recebeu de [[recebe|R]].",
         {"titulo": "O que você devolve", "linha1": "12 × [[pmt|R]]", "resultado": "[[devolve|R]]", "nota": "por R$ 4.650 recebidos"},
         leg="Só que as 12 parcelas são calculadas sobre os R$ 5.000. Cada uma sai por [[pmt|R]], e no total você devolve [[devolve|R]] por um dinheiro que realmente recebeu de [[recebe|R]]."),
    cena(c, "versus", "versus",
         "Esse custo real é o CET, o custo efetivo total. Ele junta juros, tarifa e seguro numa taxa só. Na conta, o um vírgula noventa e nove vira [[cet|pf]] ao mês.",
         {"a": "1,99%", "b": "[[cet|pf]]", "rotulo_a": "a taxa anunciada", "rotulo_b": "o CET, ao mês", "centro": "custo real"},
         leg="Esse custo real é o CET, o custo efetivo total. Ele junta juros, tarifa e seguro numa taxa só. Na conta, o 1,99% vira [[cet|pf]] ao mês."),
    cena(c, "barras", "barras",
         "Ao ano, a diferença aparece mais. A taxa anunciada dá [[anual_anunciada|p0]]. Com o CET, o custo passa de [[anual_cet|p0]].",
         {"titulo": ["Custo ao ano"], "itens": [{"rotulo": "taxa anunciada", "valor": c.v("anual_anunciada"), "texto": "[[anual_anunciada|p0]]"}, {"rotulo": "CET", "valor": c.v("anual_cet"), "texto": "[[anual_cet|p0]]", "destaque": True}],
          "nota": "exemplo hipotético; os valores reais variam"}),
    cena(c, "lista", "lista", "Por isso, antes de assinar, peça o CET, compare o CET e não só a taxa, e leia o que está sendo descontado. O CET precisa aparecer na proposta.",
         {"titulo": ["Antes de assinar"], "itens": ["peça o CET", "compare o CET, não a taxa", "leia o que é descontado"]}),
    cena(c, "volta", "numero_grande", "Então, quando uma taxa baixa parecer boa demais, lembra:", HOOK),
]
escreve(c, "JQE-S044", "CET: a taxa de 1,99% ao mês custa bem mais", "Crédito", "custo escondido", "passo a passo + setas (loop)",
        "Exemplo hipotético · valores inventados; taxas e tarifas reais variam",
        ["Cálculo próprio: parcela pela fórmula Price; CET = taxa mensal que iguala o valor recebido às parcelas (encontrada por bisecção)", "Exemplo hipotético"],
        {"linha1": "Taxa de 1,99%", "linha2": "custa bem mais", "destaque": "o CET"},
        ["Taxa de 1,99% ao mês parece pouco, mas o custo de verdade é maior.", "O que é CET?"], cenas,
        posts(c, "CET: por que a taxa de 1,99% ao mês custa bem mais", "Taxa de 1,99% ao mês parece pouco, mas o custo de verdade é maior.",
              ["Contrata R$ 5.000, recebe [[recebe|R]] (tarifa e seguro descontados)", "12 parcelas de [[pmt|R]] = [[devolve|R]]", "CET ≈ [[cet|pf]] ao mês, [[anual_cet|p0]] ao ano", "Compare o CET, não só a taxa."],
              "Você já olhou o CET do seu crédito?", "Exemplo hipotético; taxas e tarifas reais variam.",
              ["educacaofinanceira", "credito", "juros", "dinheiro"], "Taxa de 1,99% ao mês parece pouco, mas o custo de verdade é maior. Entenda o CET."),
        loop=True)

# ====================================================== S045 — diversificação
c = Calc({"saldoA": "100 - perda", "perdaB": "perda / 3", "saldoB": "100 - perdaB"}, {"perda": 30}, livres=[10, 100])
cenas = [
    cena(c, "hook", "numero_grande", "Ter dez investimentos não quer dizer que você diversificou.",
         {"valor": "10 ≠ diversificado", "linhas": ["a conta mostra", "por quê"]}),
    cena(c, "leo", "personagem_queda",
         "O Léo tem dez ações, mas todas do mesmo setor. Um dia, esse setor tem um problema, e todas caem juntas. Para cada cem reais, o Léo ficou com [[saldoA|R]].",
         {"antes": 100, "depois": c.v("saldoA"), "fala_antes": "Tenho 10 ações!", "fala_depois": "Caíram todas juntas", "badge": "−[[perda|n0]]%"},
         leg="O Léo tem 10 ações, mas todas do mesmo setor. Um dia, esse setor tem um problema, e todas caem juntas. Para cada R$ 100, o Léo ficou com [[saldoA|R]]."),
    cena(c, "fluxo", "fluxo_setas",
         "O problema é a causa em comum. Quando todos os investimentos dependem do mesmo motivo, eles sobem e caem juntos, e ter muitos não protege de nada. É como ter dez guarda-chuvas furados do mesmo modelo.",
         {"caixas": [{"texto": "10 investimentos", "tom": "neutro"}, {"texto": "mesmo setor", "tom": "cinza"}, {"texto": "caem juntos", "tom": "erro"}],
          "setas": [{"rotulo": "mesmo risco", "tom": "neutro"}, {"rotulo": "um tropeço", "tom": "erro"}]}),
    cena(c, "duo", "duo",
         "Já a Bia espalhou o dinheiro: um terço em ações, um terço em renda fixa e um terço de reserva. No mesmo dia ruim, só a parte das ações caiu trinta por cento. Para cada cem reais, ela ficou com [[saldoB|R]].",
         {"leo": {"fala": "Perdi 30%", "rotulo": "10 do mesmo setor", "valor": c.v("saldoA"), "texto": "[[saldoA|R]]"},
          "bia": {"fala": "Perdi só 10%", "rotulo": "3 tipos diferentes", "valor": c.v("saldoB"), "texto": "[[saldoB|R]]"}},
         leg="Já a Bia espalhou o dinheiro: um terço em ações, um terço em renda fixa e um terço de reserva. No mesmo dia ruim, só a parte das ações caiu 30%. Para cada R$ 100, ela ficou com [[saldoB|R]]."),
    cena(c, "ressalva", "titulo",
         "Mas papo reto: diversificar não elimina o risco, só espalha. Uma carteira diversificada também pode cair, e quem promete o contrário está vendendo ilusão. A diferença é que ela costuma sofrer menos de uma vez só.",
         {"titulo": ["Diversificar espalha", "o risco, não o tira"], "subtitulo": "exemplo hipotético, sem citar investimento"}),
    cena(c, "lista", "lista", "Para checar se você diversificou, pergunta: eles dependem do mesmo motivo? São do mesmo tipo? Eu tenho reserva fora disso? Se a resposta for sim, talvez seja só quantidade.",
         {"titulo": ["Teste rápido"], "itens": ["dependem do mesmo motivo?", "são todos do mesmo tipo?", "tenho reserva fora disso?"]}),
    cta(c, "cta", "Quantos tipos de investimento você tem? Conta nos comentários.", ["Quantos tipos", "você tem?"]),
    ASS,
]
escreve(c, "JQE-S045", "Ter 10 investimentos não é diversificar", "Investimentos", "erro comum", "personagens + exemplo hipotético",
        "Exemplo hipotético · valores inventados, sem citar investimento",
        ["Conceito de diversificação (correlação entre ativos)", "Exemplo hipotético: perda de 30% em 1/3 da carteira = 10% no total"],
        {"linha1": "10 investimentos", "linha2": "não é diversificar", "destaque": "a conta mostra"},
        ["Ter 10 investimentos não quer dizer que você diversificou.", "Diversificar de verdade."], cenas,
        posts(c, "Ter 10 investimentos não é diversificar (a conta)", "Ter 10 investimentos não quer dizer que você diversificou.",
              ["10 ações do mesmo setor: se o setor cai [[perda|n0]]%, sobram [[saldoA|R]] de R$ 100", "3 tipos diferentes: a mesma queda leva só [[perdaB|n0]]%", "Diversificar espalha o risco, não o tira"],
              "Quantos tipos de investimento você tem?", "Exemplo hipotético, sem citar investimento. Não é recomendação.",
              ["educacaofinanceira", "investimentos", "diversificacao", "bolsa"], "Ter 10 investimentos não quer dizer que você diversificou. Veja a conta."))

# ====================================================== S046 — mito ou verdade (LOOP)
c = Calc({"f10": "100 * (((1 + taxa) ** 120 - 1) / taxa)", "dado10": "100 * 120",
          "cedo": "300 * (((1 + taxa) ** 300 - 1) / taxa)", "tarde": "300 * (((1 + taxa) ** 180 - 1) / taxa)", "baltarde": "tarde / cedo * 100",
          "fundo": "topo * 0.85", "sobe": "(topo / fundo - 1) * 100"},
         {"taxa": 0.008, "topo": 100}, livres=[15, 25, 85, 300])
HOOK = {"a": "MITO", "b": "VERDADE", "rotulo_a": "investir pouco", "rotulo_b": "não vale a pena?", "centro": "qual é?"}
cenas = [
    cena(c, "hook", "versus", "Mito ou verdade: investir pouco não vale a pena?", HOOK),
    cena(c, "m1", "formula",
         "Mito. Cem reais por mês, durante dez anos, são só [[dado10|R]] saindo do seu bolso. Com os juros hipotéticos, viram [[f10|mil]]. Pouco dinheiro, com tempo, vira bastante.",
         {"titulo": "Mito 1", "linha1": "R$ 100 por mês, 10 anos", "resultado": "[[f10|mil]]", "nota": "você coloca R$ 12 mil"},
         leg="Mito. R$ 100 por mês, durante 10 anos, são só [[dado10|R]] saindo do seu bolso. Com os juros hipotéticos, viram [[f10|mil]]. Pouco dinheiro, com tempo, vira bastante."),
    cena(c, "v2", "duo",
         "Verdade: quanto mais cedo, melhor. A Bia guardou trezentos reais por mês durante vinte e cinco anos. O Léo começou tarde e guardou por quinze. A Bia fica com [[cedo|mil]]. O Léo, com [[tarde|mil]].",
         {"leo": {"fala": "Comecei tarde", "rotulo": "15 anos", "valor": c.v("baltarde"), "texto": "[[tarde|mil]]"}, "bia": {"fala": "Comecei cedo", "rotulo": "25 anos", "valor": 100, "texto": "[[cedo|mil]]"}},
         leg="Verdade: quanto mais cedo, melhor. A Bia guardou R$ 300 por mês durante 25 anos. O Léo começou tarde e guardou por 15. A Bia fica com [[cedo|mil]]. O Léo, com [[tarde|mil]]."),
    cena(c, "tarde", "titulo",
         "Mas começar tarde ainda é bem melhor do que não começar. Os [[tarde|mil]] do Léo são muito mais que zero. O melhor momento já passou, e o segundo melhor é agora.",
         {"titulo": ["Tarde é melhor", "que nunca"], "subtitulo": "o segundo melhor momento é agora"}),
    cena(c, "m3", "trajetoria",
         "E um último mito: investimento sobe todo mês. Não sobe. Pode cair quinze por cento e depois recuperar, ou não. Por isso vale ter prazo e reserva, e não colocar o dinheiro que você vai precisar logo.",
         {"topo": "R$ 100", "fundo": "R$ 85", "fim": "R$ [[topo|n0]]", "rotulo_queda": "−15%", "rotulo_subida": "+[[sobe|p]]", "nota_subida": "recuperar não é certo"},
         leg="E um último mito: investimento sobe todo mês. Não sobe. Pode cair 15% e depois recuperar, ou não. Por isso vale ter prazo e reserva, e não colocar o dinheiro que você vai precisar logo."),
    cena(c, "lista", "lista", "Resumindo: pouco vale a pena, cedo ajuda muito e oscilar faz parte do jogo. Sem promessa, só realidade.",
         {"titulo": ["O resumo"], "itens": ["pouco vale a pena", "cedo ajuda muito", "oscilar faz parte"]}),
    cena(c, "volta", "versus", "Então, na próxima vez que ouvir isso, pergunta pra si mesmo:", HOOK),
]
escreve(c, "JQE-S046", "Mito ou verdade: investir pouco não vale a pena?", "Investimentos", "pergunta", "quiz mito ou verdade (loop)",
        "Exemplo ilustrativo · juros hipotéticos de 0,8% ao mês, sem impostos",
        ["Cálculo próprio: valor futuro de aportes mensais, VF = A × ((1 + i)^n − 1) ÷ i", "Exemplo ilustrativo; valores e taxas hipotéticos"],
        {"linha1": "Mito ou verdade:", "linha2": "investir pouco", "destaque": "não vale a pena?"},
        ["Mito ou verdade: investir pouco não vale a pena?", "3 mitos sobre investir."], cenas,
        posts(c, "Mito ou verdade: investir pouco não vale a pena?", "Mito ou verdade: investir pouco não vale a pena?",
              ["MITO: R$ 100 por mês por 10 anos → [[f10|mil]]", "VERDADE: quanto mais cedo, melhor ([[cedo|mil]] × [[tarde|mil]])", "Começar tarde ainda é melhor que nunca", "MITO: investimento sobe todo mês"],
              "Qual mito você já acreditou?", "Exemplo ilustrativo, juros hipotéticos de 0,8% ao mês, sem impostos.",
              ["educacaofinanceira", "investimentos", "mitoouverdade", "dinheiro"], "Mito ou verdade: investir pouco não vale a pena? O Léo e a Bia respondem."),
        loop=True)

# ====================================================== S047 — dividendos pagando a conta de luz
c = Calc({"ano": "conta * 12", "base": "ano / dy", "base100": "100 * 12 / dy", "base500": "500 * 12 / dy",
          "aporte": "base * taxa_mes / ((1 + taxa_mes) ** 60 - 1)"},
         {"conta": 200, "dy": 0.06, "taxa_mes": 0.008}, livres=[100, 500, 5])
cenas = [
    cena(c, "hook", "numero_grande", "Quanto investir para os dividendos pagarem uma conta de luz de duzentos reais?",
         {"valor": "[[base|mil]]", "linhas": ["pagam R$ 200", "por mês, em exemplo"]}),
    cena(c, "fluxo", "fluxo_setas",
         "A conta é simples. Duzentos reais por mês são [[ano|R]] por ano. Se o investimento pagasse seis por cento ao ano em dividendos, taxa hipotética, você precisaria de [[base|mil]].",
         {"caixas": [{"texto": "R$ 200 × 12 = [[ano|R]]", "tom": "neutro"}, {"texto": "÷ 6% ao ano", "tom": "cinza"}, {"texto": "[[base|mil]]", "tom": "ok"}],
          "setas": [{"rotulo": "por ano", "tom": "neutro"}, {"rotulo": "dividendo hipotético", "tom": "neutro"}]},
         leg="A conta é simples. R$ 200 por mês são [[ano|R]] por ano. Se o investimento pagasse 6% ao ano em dividendos, taxa hipotética, você precisaria de [[base|mil]]."),
    cena(c, "barras", "barras",
         "E vale para qualquer conta. Para pagar cem reais por mês, uns [[base100|mil]]. Para duzentos, [[base|mil]]. Para quinhentos, [[base500|mil]]. É só multiplicar a conta por doze e dividir pela taxa.",
         {"titulo": ["Quanto precisa para", "pagar cada conta"], "itens": [{"rotulo": "R$ 100 por mês", "valor": c.v("base100"), "texto": "[[base100|mil]]"}, {"rotulo": "R$ 200 por mês", "valor": c.v("base"), "texto": "[[base|mil]]", "destaque": True},
                                                                      {"rotulo": "R$ 500 por mês", "valor": c.v("base500"), "texto": "[[base500|mil]]"}], "nota": "dividend yield hipotético de 6% ao ano"}),
    cena(c, "caminho", "formula",
         "Parece muito? Dá para chegar aos poucos. Guardando [[aporte|R]] por mês durante cinco anos, com juros hipotéticos, você junta essa base. Depois, é só deixar os dividendos pagarem a conta.",
         {"titulo": "O caminho", "linha1": "[[aporte|R]] por mês, 5 anos", "resultado": "[[base|mil]]", "nota": "juros hipotéticos de 0,8% ao mês"},
         leg="Parece muito? Dá para chegar aos poucos. Guardando [[aporte|R]] por mês durante 5 anos, com juros hipotéticos, você junta essa base. Depois, é só deixar os dividendos pagarem a conta."),
    cena(c, "ressalva", "titulo",
         "Mas papo reto: dividendos variam, podem diminuir e não têm garantia nenhuma. Seis por cento é só um exemplo. Esse cálculo serve para dar tamanho à meta, não para prometer renda.",
         {"titulo": ["Dividendos variam", "e não têm garantia"], "subtitulo": "a meta serve de norte, não de promessa"}),
    cena(c, "lista", "lista", "Para começar: escolha uma conta que você quer pagar, faça a conta da base e comece pelo que couber no bolso. Uma meta com nome é mais fácil de manter.",
         {"titulo": ["Para começar"], "itens": ["escolha uma conta", "calcule a base", "comece pelo que couber"]}),
    cta(c, "cta", "Qual conta você gostaria de ver paga pelos dividendos? Comenta.", ["Qual conta você", "quer ver paga?"]),
    ASS,
]
escreve(c, "JQE-S047", "Quanto investir para os dividendos pagarem a conta de luz", "Dividendos", "pergunta com número", "passo a passo (exemplo hipotético)",
        "Exemplo hipotético · dividend yield de 6% ao ano; dividendos variam e não têm garantia",
        ["Cálculo próprio: base = conta × 12 ÷ dividend yield", "Aporte mensal para juntar a base em 5 anos com juros de 0,8% ao mês"],
        {"linha1": "Dividendos pagando", "linha2": "a conta de luz", "destaque": "quanto investir?"},
        ["Quanto investir para os dividendos pagarem uma conta de luz de R$ 200?", "Quanto precisa para pagar uma conta com dividendos?"], cenas,
        posts(c, "Quanto investir para os dividendos pagarem a conta de luz", "Quanto investir para os dividendos pagarem uma conta de luz de R$ 200?",
              ["R$ 200 × 12 = [[ano|R]] por ano", "÷ 6% ao ano (hipotético) → [[base|mil]]", "Para R$ 100 por mês: [[base100|mil]]; para R$ 500: [[base500|mil]]", "Para juntar em 5 anos: [[aporte|R]] por mês (juros hipotéticos)"],
              "Qual conta você quer ver paga pelos dividendos?", "Exemplo hipotético; dividendos variam e não têm garantia. Não é recomendação.",
              ["educacaofinanceira", "dividendos", "rendapassiva", "bolsa"], "Quanto investir para os dividendos pagarem uma conta de luz de R$ 200? A conta."))
