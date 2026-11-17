"""JQE-X001 — vídeo experimental em loop, com personagens (Léo e Bia), setas e trajetória.
Feito em 17/11/2026 com a skill de produção 2.1, só para o fundador ver e aprovar (não agendado).
Pauta: assimetria das perdas (fila do ciclo 26/11). Tom: conversa descontraída, em segunda pessoa.
Loop: a última frase fica aberta ("...lembra:") e fecha na primeira ("Cair 50% exige subir 100%...")."""
import json, os

REPO = "/home/claude/juro-que-explico"
EP = f"{REPO}/episodios/JQE-X001"
os.makedirs(EP, exist_ok=True)
AVISO_YT = "Conteúdo educativo, não é recomendação financeira.\nNarração gerada por inteligência artificial."
HOOK = {"de": "−50%", "valor": "+100%", "linhas": ["para voltar ao", "mesmo lugar"]}


def cena(id_, tipo, tts, leg, d):
    return {"id": id_, "tipo": tipo, "tts": tts, "leg": leg, "dados": d}


cenas = [
    cena("hook", "numero_grande",
         "Cair cinquenta por cento exige subir cem por cento para voltar. Parece mentira, mas a conta fecha.",
         "Cair 50% exige subir 100% para voltar. Parece mentira, mas a conta fecha.", HOOK),
    cena("leo", "personagem_queda",
         "Pensa comigo. O Léo botou cem reais na bolsa. Aí o mercado azedou e o dinheiro caiu pela metade. Sobraram cinquenta.",
         "Pensa comigo. O Léo botou R$ 100 na bolsa. Aí o mercado azedou e o dinheiro caiu pela metade. Sobraram R$ 50.",
         {"antes": 100, "depois": 50, "fala_antes": "Meus R$ 100!", "fala_depois": "Ih... caiu metade", "badge": "−50%"}),
    cena("intuicao", "fluxo_setas",
         "Ele pensa: caiu cinquenta por cento, é só subir cinquenta por cento e pronto. Só que não. Cinquenta por cento de cinquenta são vinte e cinco reais.",
         "Ele pensa: caiu 50%, é só subir 50% e pronto. Só que não. 50% de R$ 50 são R$ 25.",
         {"caixas": [{"texto": "R$ 100", "tom": "neutro"}, {"texto": "R$ 50", "tom": "cinza"}, {"texto": "R$ 75", "tom": "erro", "selo": "×"}],
          "setas": [{"rotulo": "−50%", "tom": "cinza"}, {"rotulo": "+50%", "tom": "erro"}]}),
    cena("trajeto", "trajetoria",
         "Ou seja, o Léo está com setenta e cinco. Faltam vinte e cinco. Pra voltar aos cem, ele precisa ganhar cinquenta em cima de uma base de cinquenta. Isso dá cem por cento.",
         "Ou seja, o Léo está com R$ 75. Faltam R$ 25. Pra voltar aos R$ 100, ele precisa ganhar R$ 50 em cima de uma base de R$ 50. Isso dá 100%.",
         {"topo": "R$ 100", "fundo": "R$ 50", "fim": "R$ 100", "rotulo_queda": "−50%", "rotulo_subida": "+100%", "nota_subida": "+R$ 50 sobre R$ 50"}),
    cena("conta", "formula",
         "A conta é fácil: divide o valor de antes pelo que sobrou e tira um. Cem dividido por cinquenta é dois. Menos um, um. Ou seja, cem por cento.",
         "A conta é fácil: divide o valor de antes pelo que sobrou e tira 1. 100 ÷ 50 = 2, e 2 − 1 = 1. Ou seja, 100%.",
         {"titulo": "A subida que falta", "linha1": "100 ÷ 50 − 1", "resultado": "100%", "nota": "é dobrar o que sobrou"}),
    cena("tabela", "tabela_setas",
         "E quanto maior o tombo, mais pesada a volta. Caiu vinte? Precisa subir vinte e cinco. Caiu oitenta? Precisa subir quatrocentos por cento.",
         "E quanto maior o tombo, mais pesada a volta. Caiu 20%? Precisa subir 25%. Caiu 80%? Precisa subir 400%.",
         {"titulo": "Mais queda, mais volta", "linhas": [{"queda": "20%", "sobe": "25%"}, {"queda": "50%", "sobe": "100%"}, {"queda": "80%", "sobe": "400%", "destaque": True}]}),
    cena("duo", "duo",
         "Agora olha a Bia e o Léo. Os dois perderam metade. O Léo subiu cinquenta e ficou com setenta e cinco. A Bia subiu cem e voltou aos cem.",
         "Agora olha a Bia e o Léo. Os dois perderam metade. O Léo subiu 50% e ficou com R$ 75. A Bia subiu 100% e voltou aos R$ 100.",
         {"leo": {"fala": "Subi 50%...", "rotulo": "subiu 50%", "valor": 75, "texto": "R$ 75"},
          "bia": {"fala": "Subi 100%!", "rotulo": "subiu 100%", "valor": 100, "texto": "R$ 100"}}),
    cena("moral", "lista",
         "A moral: percentual de perda e de ganho não se anulam. Quanto maior a queda, mais difícil voltar. Vale pra qualquer valor.",
         "A moral: percentual de perda e de ganho não se anulam. Quanto maior a queda, mais difícil voltar. Vale pra qualquer valor.",
         {"titulo": ["A moral", "da conta"], "itens": ["Perda e ganho não se anulam", "Queda grande, volta enorme", "Vale para qualquer valor"]}),
    # fecho do loop: mesma cena do gancho; a frase fica aberta e fecha na primeira frase do vídeo
    cena("volta", "numero_grande",
         "Então, da próxima vez que alguém falar em cair cinquenta por cento, lembra:",
         "Então, da próxima vez que alguém falar em cair 50%, lembra:", HOOK),
]

hook_tts_ig = "Cair 50% exige subir 100% para voltar. Parece mentira, mas a conta fecha."
rot = {
    "id": "JQE-X001", "titulo": "Cair 50% exige subir 100% para voltar", "formato": "vertical 9:16", "pilar": "Investimentos",
    "tipo": "evergreen / história com personagens", "risco": "baixo", "loop": True,
    "tipo_gancho": "contradição", "formato_narrativo": "história com personagens + explicador",
    "nota_tela": "Exemplo ilustrativo · valores hipotéticos, sem impostos",
    "parametros": {"valor_inicial": 100, "queda": 0.5},
    "calculos": {"apos_queda": "100 * (1 - 0.5)", "sobe_errada": "apos_queda * 0.5", "apos_errada": "apos_queda + sobe_errada",
                 "falta": "100 - apos_errada", "sobe_certa_pct": "(100 / apos_queda - 1) * 100",
                 "t20": "(1/(1-0.2)-1)*100", "t50": "(1/(1-0.5)-1)*100", "t80": "(1/(1-0.8)-1)*100"},
    "numeros_livres": [20, 80, 1, 2],
    "numeros_fonte": [],
    "fontes": ["Matemática básica: subida necessária = valor de antes ÷ valor atual − 1", "Exemplo ilustrativo com valores hipotéticos, sem impostos"],
    "capa": {"linha1": "Perdeu metade?", "linha2": "A volta é maior", "destaque": "a conta fecha"},
    "ganchos_alternativos": ["Se seu investimento cai 50%, ele precisa subir 100% para voltar.", "R$ 100 viram R$ 50. Quanto precisa subir para voltar a R$ 100?"],
    "cenas": cenas,
    "posts": {
        "youtube": {"titulo": "Cair 50% exige subir 100% para voltar (a conta)",
                    "texto": f"{hook_tts_ig}\n\nO Léo tinha R$ 100 e perdeu metade. Subir 50% não basta: o que falta é 100%.\nConta: valor de antes ÷ valor atual − 1.\n\nExemplo ilustrativo, valores hipotéticos, sem impostos.\n\n{AVISO_YT}\n\n#educacaofinanceira #investimentos #bolsa #dinheiro #shorts"},
        "instagram": {"texto": f"{hook_tts_ig}\n\n• R$ 100 → cai 50% → R$ 50\n• sobe 50% → R$ 75 (ainda falta)\n• para voltar aos R$ 100: +100%\n\nQuanto maior a queda, mais pesada a volta. Isso vale para qualquer valor.\n\nVocê já tinha pensado nisso? 👇\n\nExemplo ilustrativo.\n\nNarração gerada por IA.\n\n#educacaofinanceira #investimentos #bolsa #dinheiro #financaspessoais"},
        "tiktok": {"texto": "Cair 50% exige subir 100% para voltar. O Léo e a Bia mostram a conta. Exemplo ilustrativo. Narração por IA. #educacaofinanceira #investimentos #bolsa #dinheiro"},
    },
}
json.dump(rot, open(f"{EP}/roteiro.json", "w"), ensure_ascii=False, indent=1)
palavras = sum(len(c["tts"].split()) for c in cenas)
print("palavras faladas:", palavras)
