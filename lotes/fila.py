"""Fila de produção: para cada ID espera o roteiro.json e roda checa → narração → checa → leitura → render → capa/emenda → ffprobe.
Uso: python3 lotes/fila.py JQE-S033 JQE-S034 ...   (registra em episodios/<ID>/fila.log; resumo em fila_status.json fora do git)"""
import json, os, subprocess, sys, time
REPO = "/home/claude/juro-que-explico"
os.chdir(REPO)
env = dict(os.environ, PATH=f"{REPO}/skills/.bin:" + os.environ["PATH"])
STATUS = os.environ.get("FILA_STATUS", "/tmp/fila_status.json")
st = json.load(open(STATUS)) if os.path.exists(STATUS) else {}


def run(cmd, log):
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    log.write(f"$ {' '.join(cmd)}\n{r.stdout[-3000:]}{r.stderr[-1500:]}\n")
    log.flush()
    return r.returncode == 0


for ep_id in sys.argv[1:]:
    ep = f"episodios/{ep_id}"
    while not os.path.exists(f"{ep}/roteiro.json"):
        time.sleep(20)
    time.sleep(2)
    if st.get(ep_id) == "ok" and os.path.exists(f"{ep}/{ep_id}.mp4"):
        continue
    rot = json.load(open(f"{ep}/roteiro.json"))
    log = open(f"{ep}/fila.log", "w")
    t0 = time.time()
    passos = [
        ("checa-1", ["python3", "pipeline/checa.py", ep]),
        ("narracao", ["python3", "pipeline/narracao.py", f"{ep}/roteiro.json", ep]),
        ("checa-2", ["python3", "pipeline/checa.py", ep]),
        ("leitura", ["python3", "pipeline/leitura.py", ep]),
        ("render", ["python3", "pipeline/render.py", ep]),
    ]
    ok = True
    for nome, cmd in passos:
        if not run(cmd, log):
            st[ep_id] = f"FALHOU em {nome}"; ok = False
            json.dump(st, open(STATUS, "w"), indent=1); break
    if ok:
        if rot.get("loop"):
            run(["python3", "pipeline/emenda.py", ep], log)
            json.dump({"arquivo": f"{ep_id}.mp4", "thumbnailOffset": 0}, open(f"{ep}/capa_ig.json", "w"))
        else:
            ok = run(["python3", "pipeline/capa_ig.py", ep], log)
            if not ok:
                st[ep_id] = "FALHOU em capa_ig"
        if ok:
            pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "json", f"{ep}/{ep_id}.mp4"], capture_output=True, text=True, env=env)
            info = json.loads(pr.stdout)["format"]
            st[ep_id] = "ok"
            log.write(f"ffprobe duracao={float(info['duration']):.1f}s tamanho={int(info['size'])/1e6:.1f}MB tempo_de_producao={(time.time()-t0)/60:.1f}min\n")
    json.dump(st, open(STATUS, "w"), indent=1)
    for f in os.listdir(ep):
        if f.startswith("frame_"):
            os.remove(f"{ep}/{f}")
print("fila concluída", st)
