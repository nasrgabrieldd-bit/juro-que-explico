"""Gera uma faixa de narração por cena (Kokoro pt-BR) e um áudio único com pausas, mais o mapa de tempos."""
import json
import sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

roteiro_path, saida_dir = sys.argv[1], sys.argv[2]
voz = sys.argv[3] if len(sys.argv) > 3 else "pm_alex"
velocidade = float(sys.argv[4]) if len(sys.argv) > 4 else 1.05

rot = json.load(open(roteiro_path))
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")

PAUSA = 0.35  # segundos entre cenas
INICIO = 0.3
trechos, tempos, t = [], [], INICIO
sr_final = 24000
trechos.append(np.zeros(int(INICIO * sr_final), dtype=np.float32))
for cena in rot["cenas"]:
    audio, sr = k.create(cena["tts"], voice=voz, speed=velocidade, lang="pt-br")
    sr_final = sr
    dur = len(audio) / sr
    tempos.append({"id": cena["id"], "inicio": round(t, 3), "dur": round(dur, 3), "texto": cena["tts"]})
    trechos.append(audio.astype(np.float32))
    trechos.append(np.zeros(int(PAUSA * sr), dtype=np.float32))
    t += dur + PAUSA
    print(cena["id"], round(dur, 2), "s")

audio = np.concatenate(trechos)
pico = np.max(np.abs(audio))
audio = audio / pico * 0.89  # normaliza com folga (~ -1 dBFS)
sf.write(f"{saida_dir}/narracao.wav", audio, sr_final)
json.dump({"voz": voz, "velocidade": velocidade, "total": round(len(audio) / sr_final, 3), "cenas": tempos},
          open(f"{saida_dir}/tempos.json", "w"), ensure_ascii=False, indent=1)
print("total", round(len(audio) / sr_final, 2), "s")
