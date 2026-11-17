"""Master de áudio: loudnorm em duas passagens a -14 LUFS, pico real <= -1,5 dBTP, 48 kHz estéreo; vídeo copiado sem recodificar.
Técnica do mux da Lemo-Opuscar, adaptada. O motor Remotion não normaliza o volume (a narração sai a ~-31 LUFS): rode depois de todo render.
Uso: python3 pipeline/masteriza.py arquivo.mp4  (sobrescreve o arquivo)"""
import json, os, re, subprocess, sys
mp4 = os.path.abspath(sys.argv[1]); tmp = mp4 + ".master.mp4"
alvo = "I=-14:TP=-1.5:LRA=7"
m = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-af", f"loudnorm={alvo}:print_format=json", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", m, re.S).group())
filtro = (f"loudnorm={alvo}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}"
          f":offset={j['target_offset']}:linear=true,alimiter=limit=0.84:level=false,aresample=48000,aformat=channel_layouts=stereo")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", mp4, "-c:v", "copy", "-af", filtro, "-c:a", "aac", "-b:a", "192k", tmp], check=True)
os.replace(tmp, mp4)
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mp4, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print("master:", re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1], "LUFS; pico", re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1], "dBFS")
