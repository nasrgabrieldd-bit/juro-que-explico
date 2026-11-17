---
name: producao-de-video
description: Skill única de produção de vídeo dos canais do Gabriel (Juro que Explico e Só Sei Que Foi Assim). Use SEMPRE que for produzir, refazer ou planejar vídeos (curtos, longos, cortes), roteiro, narração IA, render, capa, agenda. Começa rodando skills/atualizar_skills.sh para usar a versão mais recente de tudo, inclusive a Lemo-Opuscar.
---

# Skill de produção de vídeo (versão 2.0, 16/11/2026)

Histórico de versões em `skills/producao-de-video/CHANGELOG.md`. Fontes externas em `skills/REGISTRO.json`. Tudo o que o fundador manda (skills, links, referências) entra por `skills/REFERENCIAS.md`.

## LEI DA SKILL ATUALIZADA (decisão D25, 16/11/2026)
1. **Antes de produzir qualquer vídeo**, rode `sh skills/atualizar_skills.sh` (baixa a versão mais recente das skills externas, instala o núcleo e grava o commit usado em `skills/versoes.json`), faça `git pull` e leia esta SKILL.md e o CHANGELOG. Produzir com cópia velha é violar a lei.
2. **Tudo que o fundador mandar** (skill, link, vídeo de referência, tutorial) é: registrado em `REFERENCIAS.md` → avaliado (utilidade, licença, segurança do código) → integrado aqui → versionado no CHANGELOG (sobe a versão) → commitado e enviado. Se for uma skill nova com repositório, entra também em `REGISTRO.json`.
3. **A versão vigente é a da branch main do repositório juro-que-explico.** A rotina diária lê o PRODUCAO.md, que aponta para cá.
4. **Marca, orçamento e publicação não mudam em silêncio.** Novidade que mude a cara dos vídeos (estilo visual, voz, formato) entra como opção e só vira padrão com decisão do fundador, registrada no Project (doc 11).
5. **Licença antes de copiar.** Material com licença restrita (CC BY-NC etc.) não é copiado para este repositório público; é baixado em tempo de execução e resumido em palavras nossas.
6. **Nunca afirmar render, upload ou publicação sem confirmação real** (ffprobe, HTTP 200, status `scheduled` do Buffer).

## Canais atendidos
| Canal | Marca e repositório | Situação |
|---|---|---|
| Juro que Explico | `marca/marca.json` (preto, verde-limão, cinza); repo nasrgabrieldd-bit/juro-que-explico; manual em PRODUCAO.md; Buffer org "My organization" | Em produção: 2 vídeos por dia (12:00 e 16:00), lotes de 15 dias |
| Só Sei Que Foi Assim | Marca própria, ainda sem `marca.json`, repositório ou manual neste ambiente. O Composio tem a conta de YouTube "sosei" desse canal | Usa este mesmo método. Antes do primeiro lote: fechar a Fase 0 do método (nome/@, paleta, voz, nicho), criar `marca.json` próprio e registrar em `REGISTRO`/doc 11 do Project |

Regra comum: um repositório e um `marca.json` por canal; nunca misturar paleta, nome ou agenda entre canais; o pipeline lê a marca do arquivo, não do código.

## Dois motores de render (escolha por vídeo)
**Motor A, padrão diário (já em produção):** `pipeline/` (checa, narracao, render, margens, capa_ig) e `jqe-motion/` (Remotion). É o que a rotina automática usa. Segue o PRODUCAO.md inteiro.

**Motor B, Lemo-Opuscar (novo, 16/11/2026):** biblioteca com 99 estilos de filme feitos em código (quadro a quadro, com narração, trilha e mix). Instalada por `atualizar_skills.sh` em `~/lemo-opuscar`; comandos em `$LEMO_LIB/core/README.md`. Quando usar: o fundador pediu um estilo, um vídeo de abertura de série, um vídeo de teste de formato, ou um longo que se beneficie de um estilo (quadro-negro, quadro branco, gráficos de dados, tabela animada, notícia). Estilos que combinam com finanças: Data Storytelling, Spreadsheet Film, Chalkboard, Whiteboard Explainer, Caption News, Blueprint, Isometric Infographic, Dark Tech Keynote, Swiss Motion Graphics. Estilos marcados com estrela exigem gerador de imagens externo (não temos, orçamento zero): não usar.

Regras do Motor B para os nossos canais:
- Vertical 1080×1920 para curtos (`--size 1080x1920`) e a mesma margem de segurança do PRODUCAO.md; marca d'água e selo do `marca.json` em todo vídeo.
- Paleta da marca: o estilo é fixo no que define o estilo, mas as cores vêm do `marca.json` (para criar um estilo próprio, o caminho está em `$LEMO_LIB/MY-STYLES.md`).
- Roteiro e checagens do Motor A continuam valendo (ganchos de retenção, `calculos` para todo número, só evergreen/baixo risco em finanças, aviso de não ser recomendação, narração por IA declarada). O `checa.py` roda sobre o `roteiro.json`; o Motor B só troca a forma de desenhar.
- Narração: Kokoro, a mesma mistura de vozes do Motor A (`pm_alex` + `pm_santa`); no `tts.py` da Lemo passe `"lang": "pt-br"` e a voz por linha. Testar uma amostra antes do primeiro vídeo (ainda não foi testada em português).
- ffmpeg 7+ obrigatório (o atualizador cuida disso). Renderização por software (sem GPU): estilos com WebGL/3D ficam lentos; preferir estilos 2D.
- Um vídeo do Motor B só vai ao ar depois de: ffprobe (resolução e áudio), `readcheck` (tempo de leitura das legendas), `asr_check` (voz bate com o texto) e prancha de quadros olhada com Read.

## O que aproveitar da Lemo-Opuscar em qualquer motor (técnicas)
1. **Tratamento antes do render:** escrever 3 estruturas candidatas e escolher uma, antes de desenhar (já combina com os 3 ganchos do roteiro).
2. **Checagem de tempo de leitura** (`readcheck`): todo texto na tela fica o tempo mínimo para ler (cerca de 15 caracteres por segundo, mais 1,5 s).
3. **Mixagem e master:** loudnorm em duas passagens, −14 LUFS, pico real ≤ −1 dBTP.
4. **Voz conferida por transcrição** (`asr_check`) para pegar palavra trocada ou número lido errado.
5. **Prancha de contato** (`sheet.py`) para revisar o vídeo todo em uma imagem.
6. **Estilo próprio guardado:** o visual de cada canal pode virar um estilo salvo (`MY-STYLES.md`), para todo vídeo novo nascer da mesma base.

## Fluxo de um vídeo
Atualizar skills (lei) → pauta e fontes → roteiro e cálculos → checa.py → narração → checa.py → render (A ou B) → margens/prancha → ffprobe → commit e push → HTTP 200 → agendamento no Buffer (ou agenda_pendente.json) → aviso ao fundador. O restante (IDs de canais, horários, limites do Buffer, longos pelo Composio) está no PRODUCAO.md e na skill `canal-faceless-automatizado`.
