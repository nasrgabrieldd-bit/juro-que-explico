"""Gera uma faixa de narração por cena (Kokoro pt-BR) e um áudio único com pausas, mais o mapa de tempos."""
import json
import sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

import os
roteiro_path, saida_dir = sys.argv[1], sys.argv[2]
MODELOS = os.environ.get("MODELOS", "/home/claude/tts")
# Voz padrão (escolhida pelo fundador em 10/11/2026, amostra 3): mistura 60% pm_alex + 40% pm_santa, 0,94×,
# frase a frase com pausas naturais e tratamento de áudio (EQ, compressor, ambiência leve) no fim.
voz = sys.argv[3] if len(sys.argv) > 3 else "pm_alex+pm_santa:0.6"
velocidade = float(sys.argv[4]) if len(sys.argv) > 4 else 0.94
if velocidade == 1.0 and voz == "pm_alex" and os.environ.get("VOZ_ANTIGA") != "1":
    # chamadas antigas (pm_alex 1.0) passam a usar a voz nova; VOZ_ANTIGA=1 mantém a antiga
    voz, velocidade = "pm_alex+pm_santa:0.6", 0.94
NATURAL = "+" in voz

rot = json.load(open(roteiro_path))
k = Kokoro(f"{MODELOS}/kokoro-v1.0.onnx", f"{MODELOS}/voices-v1.0.bin")
import re
import subprocess


def estilo(v):
    if "+" not in v:
        return v
    a, resto = v.split("+")
    b, peso = (resto.split(":") + ["0.5"])[:2]
    p = float(peso)
    return p * k.get_voice_style(a) + (1 - p) * k.get_voice_style(b)


VOZ = estilo(voz)


def fala(texto):
    """Natural: sintetiza frase a frase, com pausa maior depois de pergunta."""
    if not NATURAL:
        a, sr = k.create(texto, voice=VOZ, speed=velocidade, lang="pt-br")
        return a, sr
    partes = [p for p in re.split(r"(?<=[\.\?\!])\s+", texto) if p]
    out, sr = [], 24000
    for i, p in enumerate(partes):
        a, sr = k.create(p, voice=VOZ, speed=velocidade, lang="pt-br")
        out.append(a.astype(np.float32))
        if i < len(partes) - 1:
            out.append(np.zeros(int((0.42 if p.endswith("?") else 0.28) * sr), dtype=np.float32))
    return np.concatenate(out), sr

PAUSA = 0.35  # segundos entre cenas (0,45 na voz natural)
INICIO = 0.1  # retenção: a voz começa quase junto com o primeiro quadro
if NATURAL:
    PAUSA = 0.45
trechos, tempos, t = [], [], INICIO
sr_final = 24000
trechos.append(np.zeros(int(INICIO * sr_final), dtype=np.float32))
for cena in rot["cenas"]:
    audio, sr = fala(cena["tts"])
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
if NATURAL:  # mesmo tratamento da amostra aprovada; a duração não muda
    bruto = f"{saida_dir}/narracao_bruta.wav"
    os.replace(f"{saida_dir}/narracao.wav", bruto)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", bruto, "-af",
                    "highpass=f=70,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3500:t=q:w=1.5:g=1.5,"
                    "acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120,aecho=0.8:0.5:22:0.06",
                    "-ar", str(sr_final), f"{saida_dir}/narracao.wav"], check=True)
    os.remove(bruto)
json.dump({"voz": str(voz), "velocidade": velocidade, "total": round(len(audio) / sr_final, 3), "cenas": tempos},
          open(f"{saida_dir}/tempos.json", "w"), ensure_ascii=False, indent=1)
print("total", round(len(audio) / sr_final, 2), "s")
