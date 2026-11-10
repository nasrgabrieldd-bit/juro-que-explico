"""Capa chamativa para a grade do Instagram + versão do vídeo com a capa no final (só para o Instagram).
Uso: python3 pipeline/capa_ig.py episodios/<ID>
Gera episodios/<ID>/capa_ig.png e episodios/<ID>/<ID>_ig.mp4 (vídeo original + 1 s de capa) e imprime o
thumbnailOffset (ms) a usar no Buffer. O vídeo original <ID>.mp4 não é alterado.
A grade do perfil corta em 3:4 (y 240–1680 no 1080x1920): todo o conteúdo fica nessa faixa."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

EP = sys.argv[1].rstrip("/")
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MARCA = json.load(open(os.path.join(RAIZ, "marca", "marca.json")))
C = MARCA["cores"]
BG, LIME, TX, GR, GRID = (tuple(C[k]) for k in ("fundo", "destaque", "texto", "secundaria", "grade"))
F = "/usr/share/fonts/opentype/inter/"
W, H = 1080, 1920
rot = json.load(open(f"{EP}/roteiro.json"))
ID = rot["id"]


def fonte(peso, tam):
    return ImageFont.truetype(F + {"black": "InterDisplay-Black.otf", "bold": "Inter-Bold.otf",
                                   "semi": "Inter-SemiBold.otf"}[peso], int(tam))


def cabe(d, s, peso, tam, larg):
    while tam > 30 and d.textlength(s, font=fonte(peso, tam)) > larg:
        tam -= 4
    return tam


def numero_gancho():
    """Número grande da capa: valor da cena 1 (numero_grande) ou o lado b do versus; senão nada."""
    c1 = rot["cenas"][0]
    dd = c1.get("dados", {})
    if c1["tipo"] == "numero_grande":
        return dd.get("valor", "")
    if c1["tipo"] == "versus":
        return dd.get("b", "")
    if c1["tipo"] == "formula":
        return dd.get("resultado", "")
    return ""


import re
NUM_INI = re.compile(r"^(R\$\s?)?[\d\.,/ ]+(%|×|milhões|milhão|mil)?(/mês)?\s*")


def sem_repetir(linha, num):
    """Tira da frente da linha o número que já está gigante na capa (evita 'R$ 15 / R$ 15 por dia')."""
    dn = re.sub(r"\D", "", num)
    dl = re.sub(r"\D", "", linha)
    if dn and dl == dn:
        resto = NUM_INI.sub("", linha, count=1).strip()
        if num.endswith("/mês") and resto.startswith("por mês"):
            resto = resto[len("por mês"):].strip()
        return resto
    return linha


def desenha():
    cp = dict(rot.get("capa", {}))
    n0 = numero_gancho()
    for k in ("linha1", "linha2", "destaque"):
        if cp.get(k):
            cp[k] = sem_repetir(cp[k], n0)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    # grade leve + brilho verde no canto (identidade dos vídeos)
    for x in range(0, W, 90):
        d.line([(x, 0), (x, H)], fill=GRID + (70,), width=1)
    for y in range(0, H, 90):
        d.line([(0, y), (W, y)], fill=GRID + (70,), width=1)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(520, 0, -20):
        gd.ellipse([W - r, 1680 - r, W + r, 1680 + r], fill=LIME + (int(3 + 40 * (1 - r / 520)),))
    img.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(img, "RGBA")

    # selo da marca no topo da área visível
    sel = MARCA.get("nome_topo", MARCA["nome"])
    d.text((80, 300), sel, font=fonte("bold", 40), fill=LIME, anchor="lm")
    d.rectangle([80, 336, 200, 344], fill=LIME)

    # número gigante (o que para o dedo na grade)
    num = numero_gancho()
    y = 720
    if num:
        t = cabe(d, num, "black", 250, 940)
        d.text((W / 2, y), num, font=fonte("black", t), fill=LIME, anchor="mm")
        y += t // 2 + 110
    else:
        y = 800
    # título em 2 linhas, branco, bem grande
    for s in (cp.get("linha1", ""), cp.get("linha2", "")):
        if s:
            t = cabe(d, s, "black", 118, 960)
            d.text((W / 2, y), s, font=fonte("black", t), fill=TX, anchor="mm")
            y += int(t * 1.12)
    # faixa de destaque
    dst = cp.get("destaque", "")
    if dst:
        y += 50
        t = cabe(d, dst, "black", 78, 860)
        f = fonte("black", t)
        l, tp, r, b = d.textbbox((W / 2, y), dst, font=f, anchor="mm")
        d.rounded_rectangle([l - 34, tp - 24, r + 34, b + 24], radius=18, fill=LIME)
        d.text((W / 2, y), dst, font=f, fill=BG, anchor="mm")
        y = b + 24
    # curva subindo no rodapé + chamada
    base_y = 1580
    pts = [(80 + i * 23, base_y - (1.085 ** i) * 9) for i in range(0, 41)]
    d.line(pts, fill=LIME + (230,), width=10, joint="curve")
    d.ellipse([pts[-1][0] - 16, pts[-1][1] - 16, pts[-1][0] + 16, pts[-1][1] + 16], fill=LIME)
    d.text((80, 1630), "A CONTA NA TELA  →", font=fonte("bold", 40), fill=GR, anchor="lm")
    img.save(f"{EP}/capa_ig.png")
    return img


def video_ig():
    src = f"{EP}/{ID}.mp4"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", src]).decode().strip())
    saida = f"{EP}/{ID}_ig.mp4"
    subprocess.run([
        "ffmpeg", "-loglevel", "error", "-y", "-i", src, "-loop", "1", "-t", "1", "-framerate", "30", "-i", f"{EP}/capa_ig.png",
        "-f", "lavfi", "-t", "1", "-i", "anullsrc=r=24000:cl=mono",
        "-filter_complex",
        "[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[v1];"
        "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[2:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
        "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", saida], check=True)
    off = int((dur + 0.5) * 1000)
    json.dump({"arquivo": f"{ID}_ig.mp4", "thumbnailOffset": off}, open(f"{EP}/capa_ig.json", "w"))
    print("ok", saida, "thumbnailOffset", off)


if __name__ == "__main__":
    desenha()
    if "--so-capa" not in sys.argv:
        video_ig()
