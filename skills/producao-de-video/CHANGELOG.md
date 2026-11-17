# Changelog da skill de produção de vídeo

## 2.0 — 16/11/2026
- Nova **lei da skill atualizada** (D25): atualizar antes de produzir; tudo que o fundador mandar é registrado, avaliado, integrado e versionado.
- Skill unificada para Juro que Explico e Só Sei Que Foi Assim (perfil do segundo ainda por preencher).
- Integrada a **Lemo-Opuscar** (commit 3a7132b, 12/11/2026) como Motor B opcional e fonte de técnicas (tratamento, readcheck, mix, asr_check, prancha, estilo próprio). Testada: instalação do núcleo e render de um vídeo de teste vertical aprovados (ffprobe H.264 540×960). Não testado ainda: narração em português com o Kokoro da biblioteca e um estilo completo.
- `skills/atualizar_skills.sh` e `skills/REGISTRO.json`: atualização automática e commit usado em `versoes.json`; garante ffmpeg 7+.

## 1.0 — 10 a 16/11/2026
- Método do Juro que Explico, publicado como a skill `canal-faceless-automatizado` (Fases 0 a 6) e o PRODUCAO.md.
