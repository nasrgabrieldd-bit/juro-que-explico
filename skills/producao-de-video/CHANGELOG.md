# Changelog da skill de produção de vídeo

## 2.3 — 17/11/2026
- **Produção em lote**: `lotes/_lib.py` (fala, legenda, dados de cena e posts saem da MESMA conta, marcadores `[[nome|tipo]]`; números por extenso na voz, algarismos na tela) e `lotes/fila.py` (checa → narração → checa → leitura → render → capas, um ID por vez, status em `FILA_STATUS`). Usados para produzir 20 vídeos (JQE-S033 a S052) de uma vez, 8 deles em loop.
- `pipeline/checa.py` aceita nomes de `parametros` dentro de `calculos`.
- Componentes com **auto-escala de fonte** (`cenas2.tsx`: caixas do fluxo, rótulos de seta; `cenas.tsx`: Versus com texto em maiúsculas). Corrige estouro de caixa visto no S033/S046.
- Tom: honesto E inspirador, como um amigo que aconselha sobre investir (Investidor Sardinha como referência de inspiração, nunca de cópia).
- Armadilhas registradas: gancho que começa com "Oitocentos" dispara a regra de saudação ("oi"); aritmética visível precisa bater com o resultado mostrado (1,05 × 1,05 = 1,1025; usar R2 e "≈" quando houver arredondamento); nada de dígitos, "R$" ou "P/L" no texto falado.
- Buffer grátis: máximo de 10 posts agendados por canal. O excedente fica em `agenda_pendente.json` e a rotina diária o move conforme abrem vagas.

## 2.2 — 17/11/2026
- Integrada a skill **/watch** (bradautomates/claude-video, MIT, commit 03ceb42, 25/09/2026): permite ao Claude assistir vídeos (quadros + legenda/transcrição). Registrada em `REGISTRO.json`; `atualizar_skills.sh` aprendeu o tipo `git-clone` (clona ou atualiza a última versão e instala o yt-dlp). Testada aqui em arquivo local (6 quadros do JQE-X001). **YouTube é bloqueado na nuvem**: uso em redes sociais só no computador do fundador; limitação documentada, sem contorno.
- Nova seção "Pesquisa por vídeo" com protocolo de estudo de referências (sem copiar).
- Skill passa a ser multicanal de verdade: `skills/canais/` (perfil por canal + `_modelo.md` para canais futuros) e `skills/pesquisa/` (notas de estudo).
- Pesquisa inicial de tom (Investidor Sardinha) e de canais educativos (Só Sei Que Foi Assim) registrada como hipótese, a confirmar assistindo.

## 2.1 — 17/11/2026
- **Mais elementos, mesma linguagem visual** (pedido do fundador: os vídeos estavam repetitivos): cenas novas no `jqe-motion` (`cenas2.tsx`) com personagens originais Léo e Bia (SVG na paleta da marca), setas que se desenham, trajetória com personagem em movimento, tabela com setas, dupla de personagens e gancho com seta. Tipos: `personagem_queda`, `fluxo_setas`, `trajetoria`, `tabela_setas`, `duo`, e `numero_grande` com `dados.de` (gancho com seta). Receita completa em PRODUCAO.md ("Cenas com personagens e loop").
- **Vídeo em loop** (`"loop": true` no roteiro): a última frase fica aberta e fecha na primeira; a última cena repete o gancho; o fundo, o zoom e o áudio são periódicos; sem barra de progresso; a assinatura vira só o selo fixo. `checa.py` e `narracao.py` entendem o modo.
- **Tom mais próximo** (pedido do fundador): conversa descontraída, segunda pessoa, personagens que viram exemplo ("pensa comigo", "olha a Bia e o Léo"), foco em investir, juros, bolsa, juntar dinheiro e construir patrimônio de forma prática. A referência de tom são os canais Investidor Sardinha e outros da lista do projeto: inspiração de jeito de explicar, nunca de roteiro, frases ou exemplos copiados.
- **Checagem de leitura** (`pipeline/leitura.py`, técnica adaptada do `readcheck` da Lemo-Opuscar): todo texto da tela precisa de caracteres ÷ 15 s + 1,5 s.
- Primeiro vídeo da série: `JQE-X001` (em aprovação do fundador; não agendado).

## 2.0 — 16/11/2026
- Nova **lei da skill atualizada** (D25): atualizar antes de produzir; tudo que o fundador mandar é registrado, avaliado, integrado e versionado.
- Skill unificada para Juro que Explico e Só Sei Que Foi Assim (perfil do segundo ainda por preencher).
- Integrada a **Lemo-Opuscar** (commit 3a7132b, 12/11/2026) como Motor B opcional e fonte de técnicas (tratamento, readcheck, mix, asr_check, prancha, estilo próprio). Testada: instalação do núcleo e render de um vídeo de teste vertical aprovados (ffprobe H.264 540×960). Não testado ainda: narração em português com o Kokoro da biblioteca e um estilo completo.
- `skills/atualizar_skills.sh` e `skills/REGISTRO.json`: atualização automática e commit usado em `versoes.json`; garante ffmpeg 7+.

## 1.0 — 10 a 16/11/2026
- Método do Juro que Explico, publicado como a skill `canal-faceless-automatizado` (Fases 0 a 6) e o PRODUCAO.md.
