#!/usr/bin/env bash
# Prepara um ambiente novo: dependências Python e modelo de voz Kokoro (baixado do GitHub, não versionado).
set -euo pipefail
MODELOS="${MODELOS:-/home/claude/tts}"
pip install -q --break-system-packages kokoro-onnx soundfile pillow numpy
mkdir -p "$MODELOS"
base="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
[ -s "$MODELOS/kokoro-v1.0.onnx" ] || curl -sL -o "$MODELOS/kokoro-v1.0.onnx" "$base/kokoro-v1.0.onnx"
[ -s "$MODELOS/voices-v1.0.bin" ]  || curl -sL -o "$MODELOS/voices-v1.0.bin"  "$base/voices-v1.0.bin"
[ -d /usr/share/fonts/opentype/inter ] || { apt-get install -y -q fonts-inter >/dev/null 2>&1 || sudo apt-get install -y -q fonts-inter >/dev/null 2>&1 || echo "AVISO: fonte Inter ausente"; }
command -v ffmpeg >/dev/null || { echo "ffmpeg ausente"; exit 1; }
( cd "$(dirname "$0")/jqe-motion" && npm install --no-audit --no-fund --silent ) || echo "AVISO: npm install do jqe-motion falhou"
[ -x /usr/bin/google-chrome ] || echo "AVISO: Google Chrome ausente (jqe-motion precisa dele)"
echo "ok: modelos em $MODELOS"
