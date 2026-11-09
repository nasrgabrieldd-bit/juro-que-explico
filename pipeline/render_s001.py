"""Render do curto JQE-S001 (9:16) — Juro simples x composto.
Desenha cada quadro com Pillow e envia para o FFmpeg. Todos os números vêm das fórmulas, não de texto digitado."""
import json
import math
import subprocess
import sys
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

EP = sys.argv[1]
W, H, FPS = 1080, 1920, 30
BG, LIME, MOSS = (8, 11, 9), (182, 242, 59), (57, 70, 61)
WHITE, GRAY = (244, 247, 243), (170, 179, 170)
FONTS = "/usr/share/fonts/opentype/inter/"

rot = json.load(open(f"{EP}/roteiro.json"))
tempos = json.load(open(f"{EP}/tempos.json"))
P = rot["parametros"]
C, I, N = P["principal"], P["taxa_mensal"], P["meses"]
simples = lambda m: C * (1 + I * m)
composto = lambda m: C * (1 + I) ** m
CAUDA = 1.2
DUR = tempos["total"] + CAUDA
NFRAMES = int(DUR * FPS)

cenas = tempos["cenas"]
for k, c in enumerate(cenas):
    c["fim"] = cenas[k + 1]["inicio"] if k + 1 < len(cenas) else DUR


def brl(v, casas=0):
    s = f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s


@lru_cache(maxsize=None)
def fonte(peso, tam):
    nome = {"black": "InterDisplay-Black.otf", "bold": "Inter-Bold.otf", "semi": "Inter-SemiBold.otf",
            "med": "Inter-Medium.otf", "reg": "Inter-Regular.otf", "xb": "InterDisplay-ExtraBold.otf"}[peso]
    return ImageFont.truetype(FONTS + nome, int(tam))


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def janela(t, ini, dur=0.45):
    return ease((t - ini) / dur)


def texto(d, xy, s, peso, tam, cor, alpha=1.0, anchor="mm"):
    if alpha <= 0.01:
        return
    d.text(xy, s, font=fonte(peso, tam), fill=cor + (int(255 * alpha),), anchor=anchor)


# ---------- fundo fixo ----------
base = Image.new("RGB", (W, H), BG)
bd = ImageDraw.Draw(base, "RGBA")
for x in range(0, W, 90):
    bd.line([(x, 0), (x, H)], fill=MOSS + (55,), width=1)
for y in range(0, H, 90):
    bd.line([(0, y), (W, y)], fill=MOSS + (55,), width=1)
bd.text((70, 215), "JURO QUE EXPLICO", font=fonte("bold", 34), fill=LIME, anchor="lm")
bd.rectangle([70, 245, 150, 250], fill=LIME)
bd.text((70, 288), rot["nota_tela"], font=fonte("med", 28), fill=GRAY, anchor="lm")
# marca d'água anti-recorte: centralizada, abaixo das legendas, semitransparente
bd.text((W / 2, 1530), "J%  Juro que Explico", font=fonte("bold", 34), fill=WHITE + (95,), anchor="mm")

# ---------- gráfico ----------
GX0, GX1, GTOP, GBOT, VMAX = 190, 960, 430, 1150, 2400
gx = lambda m: GX0 + m / N * (GX1 - GX0)
gy = lambda v: GBOT - v / VMAX * (GBOT - GTOP)


def eixos(d, a):
    for v in (500, 1000, 1500, 2000):
        d.line([(GX0, gy(v)), (GX1, gy(v))], fill=GRAY + (int(40 * a),), width=2)
        texto(d, (GX0 - 18, gy(v)), brl(v), "med", 26, GRAY, a, "rm")
    d.line([(GX0, GBOT), (GX1, GBOT)], fill=GRAY + (int(160 * a),), width=3)
    for m in (0, 12, 24, 36):
        texto(d, (gx(m), GBOT + 34), str(m), "med", 28, GRAY, a)
    texto(d, ((GX0 + GX1) / 2, GBOT + 78), "meses", "med", 28, GRAY, a)


def curva(f, ate):
    pts, m = [], 0.0
    while m < ate:
        pts.append((gx(m), gy(f(m))))
        m += 0.25
    pts.append((gx(ate), gy(f(ate))))
    return pts


def linha(d, f, ate, cor, larg, a=1.0):
    if ate <= 0:
        return
    d.line(curva(f, ate), fill=cor + (int(255 * a),), width=larg, joint="curve")
    x, y = gx(ate), gy(f(ate))
    d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=cor + (int(255 * a),))


def caixa(d, xy, s, cor_txt, cor_borda, tam, a, peso="bold"):
    if a <= 0.01:
        return
    f = fonte(peso, tam)
    l, t_, r, b = d.textbbox(xy, s, font=f, anchor="mm")
    d.rounded_rectangle([l - 26, t_ - 18, r + 26, b + 18], radius=14, fill=BG + (int(235 * a),),
                        outline=cor_borda + (int(255 * a),), width=3)
    d.text(xy, s, font=f, fill=cor_txt + (int(255 * a),), anchor="mm")


# ---------- cenas ----------
def c_hook(d, t, dur):
    s = 0.85 + 0.15 * janela(t, 0, 0.5)
    texto(d, (W / 2, 640), brl(C), "black", 210 * s, WHITE, janela(t, 0))
    texto(d, (W / 2, 840), "2% ao mês", "xb", 92, LIME, janela(t, 1.3))
    texto(d, (W / 2, 950), f"{N} meses", "xb", 92, WHITE, janela(t, 2.2))
    texto(d, (W / 2, 1140), "Quanto você deve?", "bold", 72, WHITE, janela(t, 3.6))


def c_pergunta(d, t, dur):
    a1, a2 = janela(t, 0.2), janela(t, 0.9)
    dx1, dx2 = (1 - a1) * -120, (1 - a2) * 120
    d.rounded_rectangle([90 + dx1, 640, 500 + dx1, 860], radius=22, outline=GRAY + (int(255 * a1),), width=4)
    texto(d, (295 + dx1, 750), "SIMPLES", "xb", 64, GRAY, a1)
    d.rounded_rectangle([580 + dx2, 640, 990 + dx2, 860], radius=22, outline=LIME + (int(255 * a2),), width=4,
                        fill=LIME + (int(28 * a2),))
    texto(d, (785 + dx2, 750), "COMPOSTO", "xb", 64, LIME, a2)
    texto(d, (540, 1010), "?", "black", 150, WHITE, janela(t, 1.8))


def c_simples1(d, t, dur):
    texto(d, (W / 2, 470), "Juro simples", "bold", 56, GRAY, janela(t, 0))
    texto(d, (W / 2, 620), f"2% × {brl(C)}", "xb", 96, WHITE, janela(t, 0.6))
    texto(d, (W / 2, 770), f"= {brl(C * I)}", "black", 140, LIME, janela(t, 2.2))
    texto(d, (W / 2, 900), "todo mês, sem mudar", "med", 50, GRAY, janela(t, 3.8))
    # 12 barras iguais: o juro não cresce
    for k in range(12):
        a = janela(t, 3.6 + k * 0.12, 0.3)
        x = 150 + k * 66
        h = 130 * a
        d.rectangle([x, 1180 - h, x + 44, 1180], fill=GRAY + (int(230 * a),))
    texto(d, (W / 2, 1225), "juro de cada mês", "med", 30, GRAY, janela(t, 4.4))


def c_simples2(d, t, dur):
    eixos(d, janela(t, 0))
    texto(d, (GX0, 360), "Juro simples", "bold", 52, GRAY, janela(t, 0), "lm")
    prog = ease((t - 0.3) / (dur * 0.75)) * N
    linha(d, simples, prog, GRAY, 8)
    if prog > 0:
        texto(d, (gx(prog) - 10, gy(simples(prog)) - 50), brl(simples(prog)), "xb", 46, WHITE, 1, "rm")


def c_composto1(d, t, dur):
    eixos(d, 1)
    linha(d, simples, N, GRAY, 6, 0.55)
    caixa(d, (gx(N) - 120, gy(simples(N)) + 60), brl(simples(N)), GRAY, GRAY, 38, 0.8, "semi")
    texto(d, (GX0, 360), "Juro composto: juro sobre juro", "bold", 50, LIME, janela(t, 0), "lm")
    prog = ease((t - 0.3) / (dur * 0.9)) * 18
    linha(d, composto, prog, LIME, 9)


def c_composto2(d, t, dur):
    eixos(d, 1)
    linha(d, simples, N, GRAY, 6, 0.55)
    caixa(d, (gx(N) - 120, gy(simples(N)) + 60), brl(simples(N)), GRAY, GRAY, 38, 0.8, "semi")
    texto(d, (GX0, 360), "Juro composto: juro sobre juro", "bold", 50, LIME, 1, "lm")
    prog = 18 + ease(t / (dur * 0.95)) * (N - 18)
    linha(d, composto, prog, LIME, 9)
    caixa(d, (450, 485), f"Juro no mês 1: {brl(C * I)}", WHITE, GRAY, 40, janela(t, 0.2))
    caixa(d, (450, 585), f"Juro no mês {N}: {brl(composto(N - 1) * I)}", LIME, LIME, 40, janela(t, 1.9))


def c_composto3(d, t, dur):
    eixos(d, 1)
    linha(d, simples, N, GRAY, 6, 0.55)
    caixa(d, (gx(N) - 120, gy(simples(N)) + 60), brl(simples(N)), GRAY, GRAY, 38, 0.8, "semi")
    texto(d, (GX0, 360), "Juro composto: juro sobre juro", "bold", 50, LIME, 1, "lm")
    a = janela(t, 0.6)
    y2 = gy(2 * C)
    for x in range(GX0, GX1, 28):
        d.line([(x, y2), (x + 14, y2)], fill=WHITE + (int(150 * a),), width=3)
    texto(d, (GX0 + 10, y2 - 30), "o dobro do valor inicial", "med", 30, WHITE, a, "lm")
    linha(d, composto, N, LIME, 9)
    # valor final em caixa verde
    if t > 0.2:
        f = fonte("black", 52)
        xy = (gx(N) - 150, gy(composto(N)) - 75)
        l, t_, r, b = d.textbbox(xy, brl(composto(N), 2), font=f, anchor="mm")
        aa = janela(t, 0.2)
        d.rounded_rectangle([l - 26, t_ - 18, r + 26, b + 18], radius=14, fill=LIME + (int(255 * aa),))
        d.text(xy, brl(composto(N), 2), font=f, fill=BG + (int(255 * aa),), anchor="mm")


def c_diferenca(d, t, dur):
    eixos(d, 1)
    a = janela(t, 0.3, 0.8)
    pts = curva(composto, N) + list(reversed(curva(simples, N)))
    d.polygon(pts, fill=LIME + (int(70 * a),))
    linha(d, simples, N, GRAY, 6, 0.8)
    linha(d, composto, N, LIME, 9)
    texto(d, (GX0, 360), "Mesma dívida, mesma taxa", "bold", 50, WHITE, janela(t, 0), "lm")
    texto(d, (GX0, 500), f"+ {brl(composto(N) - simples(N), 2)}", "black", 92, LIME, janela(t, 1.0), "lm")
    texto(d, (GX0, 575), "só pela forma de calcular", "med", 40, WHITE, janela(t, 1.4), "lm")
    caixa(d, (W / 2, 1290 - 0), "quanto maior o prazo, maior a diferença", WHITE, LIME, 36, janela(t, 3.6), "semi")


def c_prazo5(d, t, dur):
    texto(d, (W / 2, 420), "Quanto maior o prazo,", "xb", 70, WHITE, janela(t, 0))
    texto(d, (W / 2, 505), "maior a diferença", "xb", 70, LIME, janela(t, 0.2))
    x0, larg, vmax = 310, 460, 3400
    for k, (m, rot_, ini) in enumerate([(36, "3 anos", 0.6), (60, "5 anos", 2.0)]):
        y = 700 + k * 280
        a = janela(t, ini, 0.6)
        vs, vc = simples(m), composto(m)
        texto(d, (90, y + 40), rot_, "xb", 54, WHITE, janela(t, ini), "lm")
        d.rounded_rectangle([x0, y - 20, x0 + larg * vs / vmax * a, y + 30], radius=8, fill=GRAY + (int(230 * a),))
        d.rounded_rectangle([x0, y + 50, x0 + larg * vc / vmax * a, y + 100], radius=8, fill=LIME + (int(255 * a),))
        texto(d, (x0 + larg * vs / vmax * a + 16, y + 5), brl(vs), "semi", 36, GRAY, a, "lm")
        texto(d, (x0 + larg * vc / vmax * a + 16, y + 75), brl(vc, 2), "bold", 36, LIME, a, "lm")
        texto(d, (x0, y + 150), f"diferença: + {brl(vc - vs, 2)}", "bold", 40, WHITE, janela(t, ini + 0.8), "lm")
    texto(d, (W / 2, 1290), "cinza = juro simples · verde = juro composto", "med", 32, GRAY, janela(t, 0.6))


def c_comenta(d, t, dur):
    texto(d, (W / 2, 640), "Qual dívida você quer", "xb", 72, WHITE, janela(t, 0))
    texto(d, (W / 2, 735), "que eu explique?", "xb", 72, WHITE, janela(t, 0.2))
    caixa(d, (W / 2, 900), "Comenta aqui embaixo", BG, LIME, 56, janela(t, 1.2), "black")
    if t > 1.2:
        f = fonte("black", 56)
        l, t_, r, b = d.textbbox((W / 2, 900), "Comenta aqui embaixo", font=f, anchor="mm")
        aa = janela(t, 1.2)
        d.rounded_rectangle([l - 30, t_ - 22, r + 30, b + 22], radius=16, fill=LIME + (int(255 * aa),))
        d.text((W / 2, 900), "Comenta aqui embaixo", font=f, fill=BG + (int(255 * aa),), anchor="mm")


def c_dica(d, t, dur):
    texto(d, (W / 2, 560), "Antes de parcelar", "xb", 76, WHITE, janela(t, 0))
    texto(d, (W / 2, 650), "ou atrasar uma conta:", "xb", 76, WHITE, janela(t, 0.2))
    for k, (lbl, ini) in enumerate([("taxa ao mês", 1.8), ("prazo", 2.8)]):
        a = janela(t, ini)
        y = 820 + k * 150
        d.rounded_rectangle([250, y - 45, 340, y + 45], radius=12, outline=LIME + (int(255 * a),), width=5)
        ck = janela(t, ini + 0.3)
        if ck > 0:
            d.line([(268, y), (290, y + 24), (325, y - 28)], fill=LIME + (int(255 * ck),), width=10, joint="curve")
        texto(d, (380, y), lbl, "xb", 72, WHITE, a, "lm")


def c_assinatura(d, t, dur):
    texto(d, (W / 2, 760), "Juro que", "black", 150, WHITE, janela(t, 0))
    texto(d, (W / 2, 920), "Explico.", "black", 170, LIME, janela(t, 0.25))
    texto(d, (W / 2, 1080), "O dinheiro sem complicação.", "med", 52, GRAY, janela(t, 0.8))


CENAS = {"hook": c_hook, "pergunta": c_pergunta, "simples1": c_simples1, "simples2": c_simples2,
         "composto1": c_composto1, "composto2": c_composto2, "composto3": c_composto3,
         "diferenca": c_diferenca, "prazo5": c_prazo5, "dica": c_dica, "comenta": c_comenta, "assinatura": c_assinatura}


# ---------- legendas ----------
def blocos(txt, maxc=30):
    """Quebra em frases e depois em blocos de até maxc caracteres, equilibrados."""
    import re
    frases = [f.strip() for f in re.split(r"(?<=[.?:!,])\s+", txt) if f.strip()]
    out = []
    for fr in frases:
        palavras = fr.split()
        nblocos = max(1, math.ceil(len(fr) / maxc))
        alvo = len(fr) / nblocos
        cur = ""
        for p in palavras:
            if cur and len(cur) + len(p) + 1 > max(alvo, 14) and len(out) >= 0 and len(cur) + len(p) + 1 > alvo:
                out.append(cur)
                cur = p
            else:
                cur = (cur + " " + p).strip()
        if cur:
            out.append(cur)
    # junta blocos muito curtos ao anterior, se couber
    final = []
    for b in out:
        if final and len(b) < 13 and len(final[-1]) + len(b) + 1 <= maxc + 6:
            final[-1] += " " + b
        else:
            final.append(b)
    return final


LEG = []
for c in cenas:
    if c["id"] == "assinatura":
        continue
    leg = {x["id"]: x.get("leg", x["tts"]) for x in rot["cenas"]}[c["id"]]
    bl = blocos(leg)
    total = sum(len(b) for b in bl)
    t0 = c["inicio"]
    for b in bl:
        dt = c["dur"] * len(b) / total
        LEG.append((t0, t0 + dt, b))
        t0 += dt


def legenda(d, t):
    for ini, fim, s in LEG:
        if ini <= t < fim + 0.05:
            f = fonte("bold", 54)
            l, t_, r, b = d.textbbox((W / 2, 1420), s, font=f, anchor="mm")
            d.rounded_rectangle([l - 28, t_ - 20, r + 28, b + 20], radius=16, fill=(0, 0, 0, 170))
            d.text((W / 2, 1420), s, font=f, fill=WHITE, anchor="mm")
            return


def quadro(t):
    img = base.copy()
    d = ImageDraw.Draw(img, "RGBA")
    for c in cenas:
        if c["inicio"] - 0.001 <= t < c["fim"] or (c is cenas[0] and t < c["inicio"]):
            lt = max(0.0, t - c["inicio"])
            CENAS[c["id"]](d, lt, c["dur"])
            # transição: escurece nos últimos 0,2 s da janela da cena
            sobra = c["fim"] - t
            if sobra < 0.2 and c is not cenas[-1]:
                d.rectangle([0, 300, W, 1300], fill=BG + (int(255 * (1 - sobra / 0.2) * 0.9),))
            break
    legenda(d, t)
    # barra de progresso discreta no topo
    d.rectangle([0, 0, int(W * t / DUR), 8], fill=LIME)
    return img


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "frames":
        for ts in sys.argv[3:]:
            quadro(float(ts)).save(f"{EP}/frame_{ts}.png")
        sys.exit()
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", f"{EP}/narracao.wav", "-filter_complex",
           "[1:a]loudnorm=I=-14:TP=-1.5:LRA=7,apad[a]", "-map", "0:v", "-map", "[a]", "-t", f"{DUR:.3f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{EP}/{rot['id']}.mp4"]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(NFRAMES):
        ff.stdin.write(quadro(k / FPS).tobytes())
        if k % 300 == 0:
            print(f"{k}/{NFRAMES}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("ok", f"{EP}/{rot['id']}.mp4")
