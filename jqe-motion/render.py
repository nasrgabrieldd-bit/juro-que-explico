"""Renderiza um episódio do Juro que Explico com o motor Remotion.
Uso: python3 render.py <pasta do episódio> [frames t1 t2 ...]  (frames = só quadros PNG para revisão)"""
import json, os, shutil, subprocess, sys
EP = os.path.abspath(sys.argv[1].rstrip("/")); AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, ".."))
rot = json.load(open(f"{EP}/roteiro.json")); tempos = json.load(open(f"{EP}/tempos.json"))
marca = json.load(open(f"{REPO}/marca/marca.json"))
shutil.copy(f"{EP}/narracao.wav", f"{AQUI}/public/narracao.wav")
if not os.path.exists(f"{AQUI}/public/whoosh.wav"):  # *.wav não vai ao git: gera o whoosh sintético (ambiente novo)
    import numpy as np, soundfile as sf
    sr = 44100; n = int(0.38 * sr); rng = np.random.default_rng(7); x = rng.standard_normal(n)
    f = np.linspace(300, 3800, n); ph = np.cumsum(f) / sr  # varredura de baixo para cima
    sweep = np.sin(2 * np.pi * ph); env = np.sin(np.linspace(0, np.pi, n)) ** 2
    y = (0.55 * x * np.convolve(rng.standard_normal(n), np.ones(24) / 24, "same") + 0.45 * sweep) * env
    sf.write(f"{AQUI}/public/whoosh.wav", (y / np.abs(y).max() * 0.6).astype("float32"), sr)
props = f"{AQUI}/props.json"; json.dump({"rot": rot, "tempos": tempos, "marca": marca, "audio": "narracao.wav", "sfx": True}, open(props, "w"), ensure_ascii=False)
npx = ["npx", "remotion"]
COMP = "Horizontal" if rot.get("formato", "").startswith("horizontal") else "Vertical"
if len(sys.argv) > 2 and sys.argv[2] == "frames":
    for t in sys.argv[3:]:
        f = int(float(t) * 30)
        subprocess.run(npx + ["still", "src/index.ts", COMP, f"{EP}/frame_{t}.png", f"--frame={f}", f"--props={props}", "--log=error"], cwd=AQUI, check=True)
    sys.exit()
saida = f"{EP}/{rot['id']}.mp4"
subprocess.run(npx + ["render", "src/index.ts", COMP, saida, f"--props={props}", "--codec=h264", "--crf=20",
                      "--audio-codec=aac", "--audio-bitrate=192k", "--log=error"], cwd=AQUI, check=True)
subprocess.run([sys.executable, os.path.join(REPO, "pipeline", "masteriza.py"), saida], check=True)  # volume -14 LUFS
print("ok", saida)
