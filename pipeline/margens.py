"""Confere a margem de segurança: renderiza quadros e pinta por cima as zonas cobertas pela interface.
Uso: python3 pipeline/margens.py episodios/<ID> t1 t2 ...  -> /tmp/margens_<ID>.png (olhe com Read)
Vertical: união conservadora de TikTok, Reels e Shorts (topo 250, base 480, esquerda 60, direita 140 a partir de y 840).
Horizontal: título/botões do player no topo (90) e controles embaixo (120). Nada de texto pode cair no vermelho."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw
ep = sys.argv[1].rstrip("/"); ts = sys.argv[2:] or ["0"]
rot = json.load(open(f"{ep}/roteiro.json"))
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "render.py"), ep, "frames", *ts], check=True)
horiz = rot.get("formato", "").startswith("horizontal")
zonas = [(0, 0, 1920, 90), (0, 960, 1920, 1080)] if horiz else \
        [(0, 0, 1080, 250), (0, 1440, 1080, 1920), (0, 0, 60, 1920), (940, 840, 1080, 1920)]
ims = []
for t in ts:
    p = f"{ep}/frame_{t}.png"
    im = Image.open(p).convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for z in zonas:
        d.rectangle(z, fill=(255, 0, 0, 80))
    im.alpha_composite(ov); ims.append(im.convert("RGB").resize((im.width // 3, im.height // 3))); os.remove(p)
w, h = ims[0].size
s = Image.new("RGB", (w * min(4, len(ims)), h * ((len(ims) + 3) // 4)), (255, 255, 255))
for i, im in enumerate(ims):
    s.paste(im, ((i % 4) * w, (i // 4) * h))
s.save(f"/tmp/margens_{rot['id']}.png"); print(f"/tmp/margens_{rot['id']}.png")
