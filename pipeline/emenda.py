"""Confere a emenda de um vídeo em loop: compara o último quadro com o primeiro e mede o silêncio do áudio nas pontas.
Uso: python3 pipeline/emenda.py episodios/<ID>  -> imprime as diferenças e salva episodios/<ID>/emenda.png (último | primeiro)"""
import json, subprocess, sys, os
import numpy as np
from PIL import Image
EP = sys.argv[1].rstrip("/"); ID = json.load(open(f"{EP}/roteiro.json"))["id"]; mp4 = f"{EP}/{ID}.mp4"
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout)
def quadro(t, out):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1", out], check=True)
    return Image.open(out).convert("RGB")
a = quadro(max(0, d - 0.1), "/tmp/_ult.png"); b = quadro(0.0, "/tmp/_pri.png")
x, y = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
# a legenda muda de propósito entre o fim e o começo: ignora a faixa da legenda (y 935+260 a 1180+260) e a faixa do topo
mask = np.ones(x.shape[:2], bool); mask[1150:1500, :] = False
dif = np.abs(x - y).mean(axis=2)[mask]
print(f"diferença média por pixel (0-255), fora da legenda: {dif.mean():.2f}; pixels com diferença > 40: {(dif > 40).mean()*100:.2f}%")
s = Image.new("RGB", (a.width // 2 * 2, a.height // 2)); s.paste(a.resize((a.width // 2, a.height // 2)), (0, 0)); s.paste(b.resize((a.width // 2, a.height // 2)), (a.width // 2, 0))
s.save(f"{EP}/emenda.png")
w = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp4, "-vn", "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
au = np.frombuffer(w, dtype=np.float32)
fim, ini = au[-1600:], au[:1600]
print(f"áudio: nível do último 0,1 s = {20*np.log10(np.abs(fim).max()+1e-9):.1f} dBFS; do primeiro 0,1 s = {20*np.log10(np.abs(ini).max()+1e-9):.1f} dBFS; duração {d:.2f} s")
