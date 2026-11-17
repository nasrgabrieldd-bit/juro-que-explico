"""Biblioteca dos lotes (skill 2.2): escreve fala (tts), legenda (leg), dados de cena e posts a partir da MESMA conta.
Uso: c = Calc(calculos={...}, params={...}, livres=[...]); texto com marcadores [[nome|tipo]].
Tipos: R reais · R2 reais e centavos · mil "R$ 336 mil" · mi "R$ 1,75 milhão" · p percentual (valor já em %) ·
       pf percentual de fração (0,008 → 0,8%) · n número · x vezes ("4,7×").
Cada abreviação (mil, mi) vira um cálculo registrado, para o checa.py conferir de forma independente."""
import json, math, os, re
from num2words import num2words

REPO = "/home/claude/juro-que-explico"
AVISO_YT = "Conteúdo educativo, não é recomendação financeira.\nNarração gerada por inteligência artificial."
SEGURO = {k: getattr(math, k) for k in ("log", "log10", "exp", "sqrt", "floor", "ceil")}
SEGURO.update({"round": round, "min": min, "max": max, "abs": abs})


def pal(x):
    x = float(x)
    if x.is_integer():
        return num2words(int(x), lang="pt_BR").replace(", ", " e ")
    ip, fp = f"{x:.2f}".rstrip("0").split(".")
    dec = num2words(int(fp[0]), lang="pt_BR") if len(fp) == 1 else (("zero " + num2words(int(fp[1]), lang="pt_BR")) if fp[0] == "0" else num2words(int(fp), lang="pt_BR"))
    return num2words(int(ip), lang="pt_BR").replace(", ", " e ") + " vírgula " + dec


def fmt(x, dec=None, milhar=True):
    """número em pt-BR; dec=None → até 2 casas sem zeros à direita"""
    if dec is None:
        s = f"{x:.2f}".rstrip("0").rstrip(".")
        dec_s = s
        ip, _, fp = dec_s.partition(".")
    else:
        s = f"{x:.{dec}f}"
        ip, _, fp = s.partition(".")
    if milhar and len(ip.lstrip("-")) > 3:
        ip = f"{int(ip):,}".replace(",", ".")
    return ip + ("," + fp if fp else "")


class Calc:
    def __init__(self, calculos=None, params=None, livres=()):
        self.expr, self.params, self.livres, self.val = {}, dict(params or {}), list(livres), {}
        for k, e in (calculos or {}).items():
            self.reg(k, e)

    def reg(self, nome, expr):
        if nome in self.expr:
            return
        assert re.fullmatch(r"[\w\s\.\+\-\*/\(\),%]+", expr), expr
        self.expr[nome] = expr
        self.val[nome] = eval(expr, {"__builtins__": {}}, {**SEGURO, **self.params, **self.val})

    def v(self, nome):
        return self.val[nome] if nome in self.val else self.params[nome]

    # -------- formatação de um marcador: devolve (tts, leg)
    def _tok(self, nome, tipo):
        x = self.v(nome)
        if tipo == "R":
            r = round(x)
            return (("um real" if r == 1 else pal(r) + " reais"), f"R$ {fmt(r, 0)}")
        if tipo == "R2":
            r = round(x, 2); reais, cent = int(r), int(round((r - int(r)) * 100))
            t = ("um real" if reais == 1 else pal(reais) + " reais") + (f" e {pal(cent)} centavos" if cent else "")
            return t, f"R$ {fmt(r, 2)}"
        if tipo == "mil":
            self.reg(nome + "_mil", f"{nome} / 1000"); k = round(self.v(nome + "_mil"))
            return pal(k) + " mil reais", f"R$ {fmt(k, 0)} mil"
        if tipo == "mi":
            self.reg(nome + "_mi", f"{nome} / 1000000"); m = round(self.v(nome + "_mi"), 2)
            leg = f"R$ {fmt(m, 2)} " + ("milhão" if m < 2 else "milhões")
            return pal(round(x, -4)) + " reais", leg
        if tipo in ("p", "pf"):
            y = x * 100 if tipo == "pf" else x
            y = round(y, 2)
            return pal(y) + " por cento", fmt(y) + "%"
        if tipo == "p0":
            r = round(x)
            return pal(r) + " por cento", f"{fmt(r, 0)}%"
        if tipo == "x":
            y = round(x, 1)
            return pal(y) + (" vez" if y == 1 else " vezes"), fmt(y) + "×"
        if tipo == "n":
            y = round(x, 2)
            return pal(y), fmt(y)
        if tipo == "n0":
            r = round(x)
            return pal(r), fmt(r, 0)
        raise ValueError(tipo)

    def t(self, texto):
        """(tts, leg) a partir do mesmo texto com marcadores"""
        tts = re.sub(r"\[\[(\w+)\|(\w+)\]\]", lambda m: self._tok(m[1], m[2])[0], texto)
        leg = re.sub(r"\[\[(\w+)\|(\w+)\]\]", lambda m: self._tok(m[1], m[2])[1], texto)
        return tts, leg

    def L(self, texto):
        return self.t(texto)[1]

    def fmt_dados(self, o):
        if isinstance(o, str):
            return self.L(o) if "[[" in o else o
        if isinstance(o, dict):
            return {k: self.fmt_dados(v) for k, v in o.items()}
        if isinstance(o, list):
            return [self.fmt_dados(v) for v in o]
        return o


def tts_limpo(s):
    return re.sub(r"\s+", " ", s).strip()


def cena(c, id_, tipo, falado, dados=None, leg=None):
    """falado: texto com marcadores (vira tts e, se leg for None, também a legenda com algarismos).
    leg: texto de legenda diferente da fala (ex.: contas com ÷ e −)."""
    tts, legx = c.t(falado)
    tts = tts.replace("P/L", "P sobre L")  # a voz lê "barra"; a legenda mantém P/L
    if leg is not None:
        legx = c.L(leg)
    k = {"id": id_, "tipo": tipo, "tts": tts_limpo(tts), "leg": tts_limpo(legx)}
    if dados is not None:
        k["dados"] = c.fmt_dados(dados)
    return k


def posts(c, yt_titulo, hook, bullets, pergunta, nota, tags, tiktok):
    h = c.L(hook); b = [c.L(x) for x in bullets]
    tg = " ".join("#" + t for t in tags)
    return {
        "youtube": {"titulo": c.L(yt_titulo),
                    "texto": f"{h}\n\n" + "\n".join(b) + f"\n\n{nota}\n\n{AVISO_YT}\n\n{tg} #shorts"},
        "instagram": {"texto": f"{h}\n\n" + "\n".join("• " + x for x in b) + f"\n\n{c.L(pergunta)} 👇\n\n{nota}\n\nNarração gerada por IA.\n\n{tg} #financaspessoais"},
        "tiktok": {"texto": f"{c.L(tiktok)} {nota} Narração por IA. {tg}"},
    }


def serie(f, xs, dec=2):
    return [[x, round(f(x), dec)] for x in xs]


def escreve(c, id_, titulo, pilar, gancho, narrativo, nota_tela, fontes, capa, alternativos, cenas, posts_, loop=False, risco="baixo — conta ilustrativa"):
    rot = {"id": id_, "titulo": c.L(titulo), "formato": "vertical 9:16", "pilar": pilar, "tipo": "evergreen",
           "risco": risco, "tipo_gancho": gancho, "formato_narrativo": narrativo, "nota_tela": nota_tela,
           "parametros": c.params, "calculos": c.expr, "numeros_livres": c.livres, "numeros_fonte": [],
           "fontes": fontes, "capa": c.fmt_dados(capa), "ganchos_alternativos": alternativos, "cenas": cenas, "posts": posts_}
    if loop:
        rot["loop"] = True
    d = f"{REPO}/episodios/{id_}"
    os.makedirs(d, exist_ok=True)
    json.dump(rot, open(f"{d}/roteiro.json", "w"), ensure_ascii=False, indent=1)
    p = sum(len(k["tts"].split()) for k in cenas)
    print(f"ok {id_}: {p} palavras, {len(cenas)} cenas, tipos:", ",".join(k["tipo"] for k in cenas))
    return rot


def assinatura():
    m = json.load(open(f"{REPO}/marca/marca.json"))
    return {"id": "assinatura", "tipo": "assinatura", "tts": m["assinatura_tts"], "leg": m["assinatura_tts"]}


def cta(c, id_, falado, linhas, botao="Comenta aqui embaixo"):
    return cena(c, id_, "cta", falado, {"linhas": linhas, "botao": botao})
