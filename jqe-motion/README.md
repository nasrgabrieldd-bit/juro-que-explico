# jqe-motion — motor de vídeo com movimento (Remotion)

Renderiza os episódios a partir do mesmo `roteiro.json` + `tempos.json` + `narracao.wav` do pipeline Python.
- `python3 jqe-motion/render.py episodios/<ID>` → `episodios/<ID>/<ID>.mp4` (vertical 1080×1920 ou horizontal 1920×1080, conforme `formato` do roteiro)
- `python3 jqe-motion/render.py episodios/<ID> frames 0 6 14` → quadros PNG para revisão
- O `pipeline/render.py` chama este motor sozinho para roteiros novos (sem `"margem_segura": false`). `MOTOR=pillow` força o motor antigo.

O que tem: entradas com mola, números que contam, gráfico de linha que se desenha (com área e ponto que corre), barras que crescem, versus que desliza, fórmula digitada, lista com check desenhado, título palavra por palavra, CTA pulsando, assinatura; fundo com grade e brilho em movimento; legenda em blocos com a palavra falada em verde; whoosh sintético nas trocas de cena; barra de progresso; marca e selo; caixa segura de TikTok/Reels/Shorts (vertical) e do player (horizontal).

Requisitos: Node 22, `npm install` dentro de `jqe-motion/` (o `setup.sh` faz), Google Chrome em `/usr/bin/google-chrome`. Com 2 núcleos, ~6 s de render por segundo de vídeo.
Licença: Remotion é grátis para pessoa física e empresas de até 3 pessoas (remotion.dev/license).
Boas práticas: github.com/remotion-dev/skills.
