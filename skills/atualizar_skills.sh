#!/bin/sh
# Atualiza TODAS as skills externas registradas em skills/REGISTRO.json para a versão mais recente (branch main)
# e grava o commit usado em skills/versoes.json. Rodar no início de toda produção de vídeo:
#   sh skills/atualizar_skills.sh            # atualiza a biblioteca e instala o núcleo de dependências
#   sh skills/atualizar_skills.sh --sem-deps # só atualiza os arquivos
# Imprime LEMO_LIB=<pasta> e, se precisar, a linha de PATH com ffmpeg 7.
set -u
RAIZ=$(cd "$(dirname "$0")/.." && pwd)
DEPS=1; [ "${1:-}" = "--sem-deps" ] && DEPS=0

# ffmpeg 7+ (o mux da Lemo-Opuscar reprova com 6.x). Usa o binário do imageio-ffmpeg quando o do sistema é antigo.
ffv=$(ffmpeg -version 2>/dev/null | sed -n '1s/^ffmpeg version n\{0,1\}\([0-9][0-9]*\)\..*/\1/p')
if [ -z "$ffv" ] || [ "$ffv" -lt 7 ]; then
  python3 -c "import imageio_ffmpeg" 2>/dev/null || pip install -q --break-system-packages imageio-ffmpeg >/dev/null 2>&1
  bin=$(ls /usr/local/lib/python3*/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-* "$HOME"/.local/lib/python3*/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-* 2>/dev/null | head -1)
  if [ -n "$bin" ]; then
    mkdir -p "$RAIZ/skills/.bin"; ln -sf "$bin" "$RAIZ/skills/.bin/ffmpeg"
    export PATH="$RAIZ/skills/.bin:$PATH"
    echo "PATH_FFMPEG7: export PATH=$RAIZ/skills/.bin:\$PATH"
  else echo "! ffmpeg 7+ não encontrado: renders da Lemo-Opuscar podem falhar no mux"; fi
fi

python3 - "$RAIZ" "$DEPS" <<'PY'
import json, os, subprocess, sys, datetime
raiz, deps = sys.argv[1], sys.argv[2] == "1"
reg = json.load(open(f"{raiz}/skills/REGISTRO.json"))
vers_path = f"{raiz}/skills/versoes.json"
vers = json.load(open(vers_path)) if os.path.exists(vers_path) else {}
for f in reg["fontes"]:
    if f["tipo"] != "git-plugin":
        continue
    home = os.path.expanduser(f["pasta_local"])
    env = dict(os.environ, LEMO_OPUSCAR_HOME=home, LEMO_OPUSCAR_REPO=f["repo"])
    # o clone novo precisa do setup.sh: baixa só ele se ainda não existir
    setup = os.path.join(home, f["setup"])
    if not os.path.exists(setup):
        subprocess.run(["git", "clone", "--quiet", "--depth", "1", "--branch", f["branch"], f["repo"], home], check=False)
        setup = os.path.join(home, f["setup"])
    if not os.path.exists(setup):
        print(f"! {f['id']}: não consegui baixar {f['repo']}"); continue
    r = subprocess.run(["sh", setup], env=env, capture_output=True, text=True)
    print(f"[{f['id']}] " + (r.stdout.strip().splitlines() or ["(sem saída)"])[-1])
    if deps:
        subprocess.run(["sh", setup, f["instalar_deps"]], env=env)
    try:
        c = subprocess.run(["git", "-C", home, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        d = subprocess.run(["git", "-C", home, "log", "-1", "--format=%cs"], capture_output=True, text=True).stdout.strip()
    except Exception:
        c = d = ""
    antigo = vers.get(f["id"], {}).get("commit")
    vers[f["id"]] = {"commit": c, "data_do_commit": d, "verificado_em": datetime.date.today().isoformat()}
    print(f"[{f['id']}] commit {c[:10]} ({d})" + ("  <- NOVO desde a última verificação" if antigo and antigo != c else ""))
    print(f"LEMO_LIB={home}")
json.dump(vers, open(vers_path, "w"), indent=1, ensure_ascii=False)
PY
