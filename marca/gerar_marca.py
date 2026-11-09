"""Gera foto de perfil (3 opções), banner do YouTube e prancha de aprovação — identidade Juro que Explico."""
from PIL import Image, ImageDraw, ImageFont

BG, LIME, MOSS = (8, 11, 9), (182, 242, 59), (57, 70, 61)
WHITE, GRAY = (244, 247, 243), (170, 179, 170)
F = "/usr/share/fonts/opentype/inter/"
fonte = lambda n, s: ImageFont.truetype(F + n, s)
OUT = "/home/claude/jqe/marca/"


def centro(d, cx, cy, txt, f, cor):
    l, t, r, b = d.textbbox((0, 0), txt, font=f, anchor="lt")
    d.text((cx - (l + r) / 2, cy - (t + b) / 2), txt, font=f, fill=cor, anchor="lt")


def grade(img, passo, alpha=55):
    d = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    for x in range(0, w, passo):
        d.line([(x, 0), (x, h)], fill=MOSS + (alpha,), width=2)
    for y in range(0, h, passo):
        d.line([(0, y), (w, y)], fill=MOSS + (alpha,), width=2)


def curvas(d, x0, x1, ybase, altura, larg_s=10, larg_c=12, a=255):
    """Juro simples (reta cinza) x juro composto (curva verde) — o motivo gráfico da marca."""
    n = 36
    vmax = 1000 * 1.02 ** n
    gx = lambda m: x0 + m / n * (x1 - x0)
    gy = lambda v: ybase - (v - 1000) / (vmax - 1000) * altura
    s = [(gx(m / 4), gy(1000 * (1 + 0.02 * m / 4))) for m in range(0, n * 4 + 1)]
    c = [(gx(m / 4), gy(1000 * 1.02 ** (m / 4))) for m in range(0, n * 4 + 1)]
    d.line(s, fill=GRAY + (int(a * 0.7),), width=larg_s, joint="curve")
    d.line(c, fill=LIME + (a,), width=larg_c, joint="curve")
    x, y = c[-1]
    r = larg_c * 1.3
    d.ellipse([x - r, y - r, x + r, y + r], fill=LIME + (a,))


# ---------- foto de perfil: 3 opções (1080x1080, recorte circular nas redes) ----------
def perfil_a():  # J% em verde sobre preto
    im = Image.new("RGB", (1080, 1080), BG)
    grade(im, 108, 45)
    d = ImageDraw.Draw(im, "RGBA")
    centro(d, 540, 540, "J%", fonte("InterDisplay-Black.otf", 500), LIME)
    return im


def perfil_b():  # fundo verde, J% preto — mais visível no feed
    im = Image.new("RGB", (1080, 1080), LIME)
    d = ImageDraw.Draw(im, "RGBA")
    centro(d, 540, 540, "J%", fonte("InterDisplay-Black.otf", 500), BG)
    return im


def perfil_c():  # monograma JqE com as duas curvas
    im = Image.new("RGB", (1080, 1080), BG)
    grade(im, 108, 45)
    d = ImageDraw.Draw(im, "RGBA")
    centro(d, 540, 450, "JqE", fonte("InterDisplay-Black.otf", 300), WHITE)
    curvas(d, 270, 810, 820, 170, 14, 18, 255)
    return im


opcoes = {"A": perfil_a(), "B": perfil_b(), "C": perfil_c()}
for k, im in opcoes.items():
    im.save(f"{OUT}perfil_{k}.png")

# ---------- banner YouTube 2560x1440 (área segura central 1546x423) ----------
b = Image.new("RGB", (2560, 1440), BG)
grade(b, 80, 50)
d = ImageDraw.Draw(b, "RGBA")
# motivo gráfico ocupa a faixa toda, discreto, fora do texto
camada = Image.new("RGBA", b.size, (0, 0, 0, 0))
curvas(ImageDraw.Draw(camada), 120, 2440, 925, 120, 8, 10, 255)
camada.putalpha(camada.getchannel("A").point(lambda v: int(v * 0.45)))
b.paste(camada, (0, 0), camada)
d = ImageDraw.Draw(b, "RGBA")
# área segura: x 507–2053, y 509–932
l, t, r, bb = d.textbbox((1280, 620), "Juro que Explico.", font=fonte("InterDisplay-Black.otf", 150), anchor="mm")
# recolore "Explico." em verde
w_juro = d.textlength("Juro que ", font=fonte("InterDisplay-Black.otf", 150))
d.text((l, 640), "Juro que ", font=fonte("InterDisplay-Black.otf", 150), fill=WHITE, anchor="lm")
d.text((l + w_juro, 640), "Explico.", font=fonte("InterDisplay-Black.otf", 150), fill=LIME, anchor="lm")
d.text((1280, 775), "O dinheiro sem complicação.", font=fonte("Inter-Medium.otf", 64), fill=GRAY, anchor="mm")
b.save(f"{OUT}banner_youtube.png")

# ---------- prancha de aprovação ----------
p = Image.new("RGB", (2100, 1620), (30, 32, 30))
d = ImageDraw.Draw(p, "RGBA")
d.text((60, 60), "Juro que Explico — proposta de identidade nas redes", font=fonte("Inter-Bold.otf", 52), fill=WHITE)
for i, (k, im) in enumerate(opcoes.items()):
    x = 60 + i * 680
    m = Image.new("L", (460, 460), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 459, 459], fill=255)
    p.paste(im.resize((460, 460)), (x, 170), m)
    # prévia em tamanho real de feed (110 px)
    m2 = Image.new("L", (110, 110), 0)
    ImageDraw.Draw(m2).ellipse([0, 0, 109, 109], fill=255)
    p.paste(im.resize((110, 110)), (x + 480, 520), m2)
    d.text((x, 650), f"Opção {k}", font=fonte("Inter-Bold.otf", 44), fill=WHITE)
    d.text((x + 470, 640), "tamanho real", font=fonte("Inter-Medium.otf", 20), fill=GRAY)
d.text((60, 760), "Banner do YouTube (2560×1440; a faixa central aparece em todos os aparelhos)",
       font=fonte("Inter-Medium.otf", 32), fill=GRAY)
p.paste(b.resize((1440, 810)), (60, 810))
d.rectangle([60 + 507 * 1440 / 2560, 810 + 509 * 810 / 1440, 60 + 2053 * 1440 / 2560, 810 + 932 * 810 / 1440],
            outline=(255, 80, 80), width=2)
d.text((1540, 830), "Retângulo vermelho = área\nque aparece no celular.\nNão faz parte da imagem.",
       font=fonte("Inter-Medium.otf", 30), fill=GRAY, spacing=10)
p.save(f"{OUT}prancha_aprovacao.png")
print("ok")
