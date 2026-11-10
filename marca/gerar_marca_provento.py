"""Gera foto de perfil e banner do YouTube da marca Provento a partir de marca/marca.json."""
import json, os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(AQUI, "marca.json")))
C = {k: tuple(v) for k, v in M["cores"].items()}
F = "/usr/share/fonts/opentype/inter/"
fonte = lambda n, s: ImageFont.truetype(F + n, s)


def centro(d, cx, cy, txt, f, cor):
    l, t, r, b = d.textbbox((0, 0), txt, font=f, anchor="lt")
    d.text((cx - (l + r) / 2, cy - (t + b) / 2), txt, font=f, fill=cor, anchor="lt")


# foto de perfil 1080x1080: fundo cobalto inteiro (o recorte redondo das redes vira um círculo azul)
p = Image.new("RGB", (1080, 1080), C["destaque"])
centro(ImageDraw.Draw(p), 540, 540, M["inicial"], fonte("InterDisplay-Black.otf", 640), C["fundo"])
p.save(os.path.join(AQUI, "perfil_provento.png"))

# banner YouTube 2560x1440 (área segura central 1546x423)
b = Image.new("RGB", (2560, 1440), C["fundo"])
d = ImageDraw.Draw(b, "RGBA")
for x in range(0, 2560, 80):
    d.line([(x, 0), (x, 1440)], fill=C["grade"] + (90,), width=2)
for y in range(0, 1440, 80):
    d.line([(0, y), (2560, y)], fill=C["grade"] + (90,), width=2)
# curvas: aporte linear (cinza) x juro composto (azul)
n, x0, x1, yb, alt = 360, 420, 2140, 1060, 220
vmax = ((1.008 ** n - 1) / 0.008)
gx = lambda m: x0 + m / n * (x1 - x0)
gy = lambda v: yb - v / vmax * alt
d.line([(gx(m), gy(m)) for m in range(0, n + 1, 3)], fill=C["secundaria"] + (150,), width=8)
cur = [(gx(m), gy((1.008 ** m - 1) / 0.008)) for m in range(0, n + 1, 3)]
d.line(cur, fill=C["destaque"] + (255,), width=10, joint="curve")
x, y = cur[-1]
d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=C["destaque"])
# logotipo
r = 120
cx, cy = 720, 650
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=C["destaque"])
centro(d, cx, cy, M["inicial"], fonte("InterDisplay-Black.otf", 170), C["fundo"])
d.line([(890, 545), (890, 755)], fill=C["secundaria"] + (120,), width=3)
d.text((940, 600), M["nome_topo"] + ".", font=fonte("InterDisplay-Black.otf", 150), fill=C["texto"], anchor="ls")
d.text((944, 690), M["tagline"], font=fonte("Inter-Medium.otf", 58), fill=C["destaque"], anchor="ls")
d.text((946, 760), "JUROS · DIVIDENDOS · INVESTIMENTOS · VIDA REAL", font=fonte("Inter-SemiBold.otf", 34),
       fill=C["secundaria"], anchor="ls")
b.save(os.path.join(AQUI, "banner_youtube_provento.png"))
b.convert("RGB").save(os.path.join(AQUI, "banner_youtube_provento.jpg"), quality=92)
print("ok")
