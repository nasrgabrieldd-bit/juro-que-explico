"""Renderiza um episódio do Juro que Explico com o motor Remotion.
Uso: python3 render.py <pasta do episódio> [frames t1 t2 ...]  (frames = só quadros PNG para revisão)"""
import json, os, shutil, subprocess, sys
EP = os.path.abspath(sys.argv[1].rstrip("/")); AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, ".."))
rot = json.load(open(f"{EP}/roteiro.json")); tempos = json.load(open(f"{EP}/tempos.json"))
marca = json.load(open(f"{REPO}/marca/marca.json"))
shutil.copy(f"{EP}/narracao.wav", f"{AQUI}/public/narracao.wav")
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
print("ok", saida)
