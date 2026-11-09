"""Motor de render genérico — Juro que Explico (9:16, 1080x1920).
Lê episodios/<ID>/roteiro.json (cenas tipadas) + tempos.json (da narração) e gera <ID>.mp4 e capa.png.
Uso: python3 pipeline/render.py episodios/<ID> [frames t1 t2 ...]"""
import hashlib
import json
import math
import re
import subprocess
import sys
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

EP = sys.argv[1].rstrip("/")
W, H, FPS = 1080, 1920, 30
BG, LIME, MOSS = (8, 11, 9), (182, 242, 59), (57, 70, 61)
WHITE, GRAY = (244, 247, 243), (170, 179, 170)
FONTS = "/usr/share/fonts/opentype/inter/"

rot = json.load(open(f"{EP}/roteiro.json"))
tempos = json.load(open(f"{EP}/tempos.json"))
CAUDA = 1.2
DUR = tempos["total"] + CAUDA
NFRAMES = int(DUR * FPS)
cenas_rot = {c["id"]: c for c in rot["cenas"]}
cenas = tempos["cenas"]
for k, c in enumerate(cenas):
    c["fim"] = cenas[k + 1]["inicio"] if k + 1 < len(cenas) else DUR
    c["spec"] = cenas_rot[c["id"]]

# variação controlada entre episódios (evita template idêntico): derivada do ID
SEMENTE = int(hashlib.md5(rot["id"].encode()).hexdigest(), 16)
GRADE = [90, 72, 108][SEMENTE % 3]
HOOK_Y = [640, 700, 600][(SEMENTE >> 3) % 3]


# ---------------- utilitários ----------------
@lru_cache(maxsize=None)
def fonte(peso, tam):
    nome = {"black": "InterDisplay-Black.otf", "xb": "InterDisplay-ExtraBold.otf", "bold": "Inter-Bold.otf",
            "semi": "Inter-SemiBold.otf", "med": "Inter-Medium.otf", "reg": "Inter-Regular.otf"}[peso]
    return ImageFont.truetype(FONTS + nome, max(8, int(tam)))


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def jan(t, ini, dur=0.45):
    return ease((t - ini) / dur)


def texto(d, xy, s, peso, tam, cor, a=1.0, anchor="mm"):
    if a > 0.01 and s:
        d.text(xy, s, font=fonte(peso, tam), fill=cor + (int(255 * a),), anchor=anchor)


def cabe(d, s, peso, tam, largura):
    """Reduz o tamanho até o texto caber na largura."""
    while tam > 20 and d.textlength(s, font=fonte(peso, tam)) > largura:
        tam -= 2
    return tam


def caixa(d, xy, s, tam, a, cheia=False, cor=LIME, peso="bold"):
    if a <= 0.01:
        return
    f = fonte(peso, tam)
    l, t_, r, b = d.textbbox(xy, s, font=f, anchor="mm")
    if cheia:
        d.rounded_rectangle([l - 28, t_ - 20, r + 28, b + 20], radius=16, fill=cor + (int(255 * a),))
        d.text(xy, s, font=f, fill=BG + (int(255 * a),), anchor="mm")
    else:
        d.rounded_rectangle([l - 26, t_ - 18, r + 26, b + 18], radius=14, fill=BG + (int(235 * a),),
                            outline=cor + (int(255 * a),), width=3)
        d.text(xy, s, font=f, fill=(WHITE if cor == GRAY else cor) + (int(255 * a),), anchor="mm")


def fmt(v, estilo="brl", casas=None):
    if estilo == "brl":
        c = 2 if casas is None and abs(v - round(v)) > 0.004 else (casas or 0)
        s = f"{v:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return "R$ " + s
    if estilo == "pct":
        c = 1 if casas is None else casas
        return f"{v:.{c}f}".replace(".", ",") + "%"
    c = 0 if casas is None else casas
    return f"{v:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------- fundo fixo ----------------
base = Image.new("RGB", (W, H), BG)
bd = ImageDraw.Draw(base, "RGBA")
for x in range(0, W, GRADE):
    bd.line([(x, 0), (x, H)], fill=MOSS + (55,), width=1)
for y in range(0, H, GRADE):
    bd.line([(0, y), (W, y)], fill=MOSS + (55,), width=1)
bd.text((70, 215), "JURO QUE EXPLICO", font=fonte("bold", 34), fill=LIME, anchor="lm")
bd.rectangle([70, 245, 150, 250], fill=LIME)
if rot.get("nota_tela"):
    bd.text((70, 288), rot["nota_tela"], font=fonte("med", 28), fill=GRAY, anchor="lm")
# marca d'água anti-recorte (D14)
bd.text((W / 2, 1530), "J%  Juro que Explico", font=fonte("bold", 34), fill=WHITE + (95,), anchor="mm")


# ---------------- tipos de cena ----------------
def c_numero_grande(d, t, dur, D):
    s = 0.85 + 0.15 * jan(t, 0, 0.5)
    tam = cabe(d, D["valor"], "black", 210, 960)
    texto(d, (W / 2, HOOK_Y), D["valor"], "black", tam * s, WHITE, jan(t, 0))
    for k, lin in enumerate(D.get("linhas", [])):
        texto(d, (W / 2, HOOK_Y + 200 + k * 110), lin, "xb", cabe(d, lin, "xb", 92, 960),
              LIME if k == 0 else WHITE, jan(t, 1.2 + k * 0.9))
    if D.get("pergunta"):
        texto(d, (W / 2, HOOK_Y + 200 + len(D.get("linhas", [])) * 110 + 90), D["pergunta"], "bold",
              cabe(d, D["pergunta"], "bold", 72, 960), WHITE, jan(t, max(1.5, dur * 0.6)))


def c_titulo(d, t, dur, D):
    linhas = D["titulo"] if isinstance(D["titulo"], list) else [D["titulo"]]
    y0 = 720 - (len(linhas) - 1) * 50
    for k, lin in enumerate(linhas):
        texto(d, (W / 2, y0 + k * 100), lin, "xb", cabe(d, lin, "xb", 84, 960),
              LIME if k == len(linhas) - 1 and len(linhas) > 1 else WHITE, jan(t, k * 0.25))
    if D.get("subtitulo"):
        texto(d, (W / 2, y0 + len(linhas) * 100 + 40), D["subtitulo"], "med", cabe(d, D["subtitulo"], "med", 48, 960),
              GRAY, jan(t, 0.9))


def c_versus(d, t, dur, D):
    a1, a2 = jan(t, 0.2), jan(t, 0.9)
    dx1, dx2 = (1 - a1) * -120, (1 - a2) * 120
    for (txt, x0, x1, a, dx, cor, cheio) in [(D["a"], 90, 500, a1, dx1, GRAY, False),
                                              (D["b"], 580, 990, a2, dx2, LIME, True)]:
        d.rounded_rectangle([x0 + dx, 640, x1 + dx, 860], radius=22, outline=cor + (int(255 * a),), width=4,
                            fill=(LIME + (int(28 * a),)) if cheio else None)
        texto(d, ((x0 + x1) / 2 + dx, 750), txt, "xb", cabe(d, txt, "xb", 64, 360), cor, a)
    texto(d, (W / 2, 1010), D.get("centro", "?"), "black", 150, WHITE, jan(t, 1.8))


def c_formula(d, t, dur, D):
    if D.get("titulo"):
        texto(d, (W / 2, 470), D["titulo"], "bold", 56, GRAY, jan(t, 0))
    texto(d, (W / 2, 620), D["linha1"], "xb", cabe(d, D["linha1"], "xb", 96, 960), WHITE, jan(t, 0.6))
    texto(d, (W / 2, 770), D["resultado"], "black", cabe(d, D["resultado"], "black", 140, 960), LIME,
          jan(t, min(2.2, dur * 0.35)))
    if D.get("nota"):
        texto(d, (W / 2, 900), D["nota"], "med", cabe(d, D["nota"], "med", 50, 960), GRAY, jan(t, min(3.8, dur * 0.6)))


def c_barras(d, t, dur, D):
    """Barras horizontais comparáveis: itens [{rotulo, valor, texto, destaque, grupo}]."""
    if D.get("titulo"):
        tl = D["titulo"] if isinstance(D["titulo"], list) else [D["titulo"]]
        for k, lin in enumerate(tl):
            texto(d, (W / 2, 420 + k * 85), lin, "xb", cabe(d, lin, "xb", 70, 960),
                  LIME if k == len(tl) - 1 and len(tl) > 1 else WHITE, jan(t, k * 0.2))
    itens = D["itens"]
    vmax = max(i["valor"] for i in itens) * 1.15
    x0, larg = 330, 440
    # encolhe as barras para que nenhum rótulo passe da margem direita (W - 60)
    for it in itens:
        tw = d.textlength(it.get("texto", fmt(it["valor"])), font=fonte("bold", 36))
        livre = W - 60 - x0 - 16 - tw
        larg = min(larg, livre * vmax / it["valor"])
    larg = max(160, larg)
    y = 640
    passo = min(140, 620 / max(1, len(itens)))
    ultimo_grupo = None
    for k, it in enumerate(itens):
        ini = 0.5 + k * min(0.7, (dur * 0.6) / max(1, len(itens)))
        a = jan(t, ini, 0.6)
        g = it.get("grupo")
        if g and g != ultimo_grupo:
            texto(d, (90, y + 10), g, "xb", 50, WHITE, jan(t, ini), "lm")
            ultimo_grupo = g
        cor = LIME if it.get("destaque") else GRAY
        w = larg * it["valor"] / vmax * a
        d.rounded_rectangle([x0, y - 22, x0 + max(4, w), y + 22], radius=8, fill=cor + (int(240 * a),))
        texto(d, (x0 + w + 16, y), it.get("texto", fmt(it["valor"])), "bold" if it.get("destaque") else "semi", 36,
              cor, a, "lm")
        if not g:
            texto(d, (x0 - 20, y), it["rotulo"], "semi", 34, WHITE, a, "rm")
        y += passo
    if D.get("nota"):
        texto(d, (W / 2, 1290), D["nota"], "med", cabe(d, D["nota"], "med", 34, 980), GRAY, jan(t, 0.8))


def c_linhas(d, t, dur, D):
    """Gráfico de linhas: series [{nome, pontos:[[x,y],...], destaque}], desenhadas progressivamente."""
    GX0, GX1, GTOP, GBOT = 190, 960, 430, 1150
    series = D["series"]
    xs = [p[0] for s in series for p in s["pontos"]]
    ys = [p[1] for s in series for p in s["pontos"]]
    xmin, xmax = min(xs), max(xs)
    ymax = D.get("ymax") or max(ys) * 1.15
    ymin = D.get("ymin", 0)
    gx = lambda x: GX0 + (x - xmin) / (xmax - xmin) * (GX1 - GX0)
    gy = lambda v: GBOT - (v - ymin) / (ymax - ymin) * (GBOT - GTOP)
    estilo = D.get("y_fmt", "brl")
    a0 = jan(t, 0)
    passo = D.get("y_passo") or 10 ** math.floor(math.log10(ymax)) / 2
    v = ymin + passo
    while v < ymax:
        d.line([(GX0, gy(v)), (GX1, gy(v))], fill=GRAY + (int(40 * a0),), width=2)
        texto(d, (GX0 - 18, gy(v)), fmt(v, estilo, 0), "med", 26, GRAY, a0, "rm")
        v += passo
    d.line([(GX0, GBOT), (GX1, GBOT)], fill=GRAY + (int(160 * a0),), width=3)
    for xt in D.get("x_ticks", [xmin, xmax]):
        texto(d, (gx(xt), GBOT + 34), fmt(xt, "num"), "med", 28, GRAY, a0)
    texto(d, ((GX0 + GX1) / 2, GBOT + 78), D.get("x_rotulo", ""), "med", 28, GRAY, a0)
    if D.get("titulo"):
        texto(d, (GX0, 360), D["titulo"], "bold", cabe(d, D["titulo"], "bold", 50, 860), WHITE, a0, "lm")
    for k, s in enumerate(series):
        ini = s.get("inicio", 0.3 + k * dur * 0.35)
        prog = ease((t - ini) / max(0.5, dur * s.get("velocidade", 0.6)))
        pts = s["pontos"]
        n = max(2, int(len(pts) * prog) + 1)
        sub = [(gx(x), gy(y)) for x, y in pts[:n]]
        cor = LIME if s.get("destaque") else GRAY
        if prog > 0 and len(sub) >= 2:
            d.line(sub, fill=cor + (255,), width=9 if s.get("destaque") else 7, joint="curve")
            x, y = sub[-1]
            d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=cor)
            if prog >= 0.999 and s.get("rotulo_final"):
                caixa(d, (min(x - 10, GX1 - 140), y - 60 if s.get("destaque") else y + 60), s["rotulo_final"],
                      40, jan(t, ini + dur * s.get("velocidade", 0.6)), cheia=bool(s.get("destaque")), cor=cor)
        texto(d, (GX0 + 10, 470 + k * 50), "● " + s["nome"], "semi", 32, cor, jan(t, ini), "lm")


def c_lista(d, t, dur, D):
    tl = D["titulo"] if isinstance(D["titulo"], list) else [D["titulo"]]
    for k, lin in enumerate(tl):
        texto(d, (W / 2, 560 + k * 90), lin, "xb", cabe(d, lin, "xb", 76, 960), WHITE, jan(t, k * 0.2))
    y0 = 560 + len(tl) * 90 + 80
    itens = D["itens"]
    tam_l = min(cabe(d, lbl, "xb", 64, 680) for lbl in itens)  # mesmo tamanho em todos os itens
    bloco = 130 + max(d.textlength(l, font=fonte("xb", tam_l)) for l in itens)
    xl = int((W - bloco) / 2)  # centraliza o bloco caixa + texto
    for k, lbl in enumerate(itens):
        ini = 1.0 + k * min(1.0, dur * 0.6 / max(1, len(itens)))
        a = jan(t, ini)
        y = y0 + k * 140
        d.rounded_rectangle([xl, y - 45, xl + 90, y + 45], radius=12, outline=LIME + (int(255 * a),), width=5)
        ck = jan(t, ini + 0.3)
        if ck > 0:
            d.line([(xl + 18, y), (xl + 40, y + 24), (xl + 75, y - 28)], fill=LIME + (int(255 * ck),), width=10, joint="curve")
        texto(d, (xl + 130, y), lbl, "xb", tam_l, WHITE, a, "lm")


def c_cta(d, t, dur, D):
    tl = D["linhas"]
    for k, lin in enumerate(tl):
        texto(d, (W / 2, 640 + k * 95), lin, "xb", cabe(d, lin, "xb", 72, 960), WHITE, jan(t, k * 0.2))
    caixa(d, (W / 2, 640 + len(tl) * 95 + 90), D["botao"], 56, jan(t, 1.2), cheia=True, peso="black")


def c_assinatura(d, t, dur, D):
    texto(d, (W / 2, 760), "Juro que", "black", 150, WHITE, jan(t, 0))
    texto(d, (W / 2, 920), "Explico.", "black", 170, LIME, jan(t, 0.25))
    texto(d, (W / 2, 1080), "O dinheiro sem complicação.", "med", 52, GRAY, jan(t, 0.8))


TIPOS = {"numero_grande": c_numero_grande, "titulo": c_titulo, "versus": c_versus, "formula": c_formula,
         "barras": c_barras, "linhas": c_linhas, "lista": c_lista, "cta": c_cta, "assinatura": c_assinatura}


# ---------------- legendas ----------------
def blocos(txt, maxc=30):
    frases = [f.strip() for f in re.split(r"(?<=[.?:!,])\s+", txt) if f.strip()]
    out = []
    for fr in frases:
        n = max(1, math.ceil(len(fr) / maxc))
        alvo = len(fr) / n
        cur = ""
        for p in fr.split():
            if cur and len(cur) + len(p) + 1 > max(alvo, 14):
                out.append(cur)
                cur = p
            else:
                cur = (cur + " " + p).strip()
        if cur:
            out.append(cur)
    final = []
    for b in out:
        if final and len(b) < 13 and len(final[-1]) + len(b) + 1 <= maxc + 6:
            final[-1] += " " + b
        else:
            final.append(b)
    return final


LEG = []
for c in cenas:
    if c["spec"]["tipo"] == "assinatura":
        continue
    bl = blocos(c["spec"].get("leg", c["spec"]["tts"]))
    total = sum(len(b) for b in bl)
    t0 = c["inicio"]
    for b in bl:
        dt = c["dur"] * len(b) / total
        LEG.append((t0, t0 + dt, b))
        t0 += dt


def legenda(d, t):
    for ini, fim, s in LEG:
        if ini <= t < fim + 0.05:
            f = fonte("bold", cabe(d, s, "bold", 54, 960))
            l, t_, r, b = d.textbbox((W / 2, 1420), s, font=f, anchor="mm")
            d.rounded_rectangle([l - 28, t_ - 20, r + 28, b + 20], radius=16, fill=(0, 0, 0, 170))
            d.text((W / 2, 1420), s, font=f, fill=WHITE, anchor="mm")
            return


def quadro(t):
    img = base.copy()
    d = ImageDraw.Draw(img, "RGBA")
    for c in cenas:
        if c["inicio"] - 0.001 <= t < c["fim"] or (c is cenas[0] and t < c["inicio"]):
            TIPOS[c["spec"]["tipo"]](d, max(0.0, t - c["inicio"]), c["dur"], c["spec"].get("dados", {}))
            sobra = c["fim"] - t
            if sobra < 0.2 and c is not cenas[-1]:
                d.rectangle([0, 300, W, 1300], fill=BG + (int(255 * (1 - sobra / 0.2) * 0.9),))
            break
    legenda(d, t)
    d.rectangle([0, 0, int(W * t / DUR), 8], fill=LIME)
    return img


def capa():
    """Capa 1080x1920 para Reels/TikTok a partir de rot['capa'] = {linha1, linha2, destaque}."""
    cp = rot.get("capa", {})
    img = base.copy()
    d = ImageDraw.Draw(img, "RGBA")
    l1, l2, dst = cp.get("linha1", ""), cp.get("linha2", ""), cp.get("destaque", "")
    texto(d, (W / 2, 620), l1, "black", cabe(d, l1, "black", 120, 960), WHITE)
    texto(d, (W / 2, 760), l2, "black", cabe(d, l2, "black", 120, 960), WHITE)
    if dst:
        caixa(d, (W / 2, 960), dst, cabe(d, dst, "black", 90, 860), 1, cheia=True, peso="black")
    img.save(f"{EP}/capa.png")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "frames":
        for ts in sys.argv[3:]:
            quadro(float(ts)).save(f"{EP}/frame_{ts}.png")
        sys.exit()
    capa()
    saida = f"{EP}/{rot['id']}.mp4"
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", f"{EP}/narracao.wav", "-filter_complex",
           "[1:a]loudnorm=I=-14:TP=-1.5:LRA=7,apad[a]", "-map", "0:v", "-map", "[a]", "-t", f"{DUR:.3f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", saida]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(NFRAMES):
        ff.stdin.write(quadro(k / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    print("ok", saida, f"{DUR:.1f}s")
