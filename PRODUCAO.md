# Manual da produção diária — Juro que Explico

Este arquivo é a fonte de verdade da rotina automática. Cada execução diária lê este manual, produz **um** vídeo vertical e agenda a publicação para o dia seguinte.

## Regras fixas (decisões do fundador)
- Orçamento zero. Só ferramentas gratuitas.
- Publicação automática, sem esperar aprovação. O fundador revisa só de vez em quando e pode vetar até a hora da postagem.
- Todo vídeo leva a marca d'água (o render já aplica).
- Duração: mais de 61 s e menos de 175 s (alvo: 65 a 90 s). Regra do TikTok Creator Rewards.
- Textos adaptados por plataforma (YouTube, Instagram, TikTok).
- Um vídeo por dia nas três redes.
- Narração por IA declarada nos textos e marcada como `isAiGenerated` no Buffer.

## Linha editorial da rotina automática
- Só pautas **evergreen** de baixo risco: conceitos, contas, regras de bolso, armadilhas comuns, como funciona X.
- Proibido: notícia do dia, previsão de mercado, recomendação de ativo, corretora, banco ou produto específico, promessa de ganho, conteúdo político.
- Números: preferir exemplos ilustrativos calculados (taxas hipotéticas, avisadas em `nota_tela`). Dado oficial (Selic, IPCA, etc.) só se buscado na hora com WebFetch na fonte oficial e registrado em `numeros_fonte` com `url` e `data_referencia`.
- Não repetir pauta já feita (ver `PAUTAS.md`).
- Tom: didático, direto, segunda pessoa, frases curtas. Abertura com pergunta ou número forte nos primeiros 3 s. Fechamento com pergunta para comentar e a assinatura "Juro que explico."

## Retenção nos primeiros segundos (obrigatório a partir do JQE-S010)
O gancho decide se a pessoa fica. Regras:
1. **Primeiro quadro já cheio.** O render monta a cena 1 inteira no quadro zero (número, linhas e pergunta já na tela) e a voz entra em 0,1 s. Nunca abrir com tela vazia, logo ou vinheta.
2. **Primeira frase com até 16 palavras**, com um número concreto e uma lacuna que só o vídeo fecha. Fórmulas que funcionam no nicho:
   - contradição: "1% ao mês não é 12% ao ano."
   - custo escondido: "Esperar 5 anos pode custar R$ 250 mil."
   - pergunta com número: "R$ 15 por dia vira quanto em 10 anos?"
   - escolha: "10× sem juros ou 10% à vista: qual sai mais barato?"
   - erro comum: "Quase todo mundo faz essa conta do jeito errado."
3. **Sem saudação, sem nome do canal, sem "neste vídeo".** A marca aparece só na assinatura final.
4. **Promessa e adiamento (open loop):** o gancho faz a pergunta; a resposta completa vem só a partir da cena 3 ou 4. Pode antecipar: "e a resposta muda conforme a taxa".
5. **Cena 2 começa em até 8 s.** Depois, troca visual a cada 4 a 8 s (nova cena ou novo elemento na tela).
6. **Clique coerente:** o título do YouTube, a capa e a primeira frase prometem a mesma coisa. Nada de promessa que o vídeo não cumpre.
7. **Fim que puxa replay:** a pergunta do CTA retoma o número do gancho, para o fim emendar no começo quando o Short repete.
O `checa.py` reprova: primeira frase com mais de 16 palavras, cena 1 sem número/comparação/conta, saudação no gancho e cena 2 depois de 8 s.

## Formato do roteiro (`episodios/<ID>/roteiro.json`)
Use `episodios/JQE-S002/roteiro.json` como modelo. Campos:
- `id` (JQE-S###, sequencial), `titulo`, `formato` ("vertical 9:16"), `pilar`, `tipo`, `risco`.
- `nota_tela`: aviso fixo pequeno no topo (ex.: "Exemplo ilustrativo · taxas hipotéticas, sem impostos").
- `parametros`: valores de entrada do exemplo.
- `calculos`: `nome: "expressão"` (só + - * / ** ( ) e log, exp, sqrt, floor, ceil, round, min, max, abs; pode usar cálculos anteriores pelo nome).
- `numeros_livres`: números que não são resultado de conta (ex.: 72 da regra dos 72, um ano de calendário).
- `numeros_fonte`: `[{descricao, valor, url, data_referencia}]` para dados reais.
- `fontes`: lista de textos com as fontes ou a fórmula usada.
- `capa`: `{linha1, linha2, destaque}`.
- `cenas`: lista. Cada cena tem `id`, `tipo`, `tts` (texto falado, números por extenso), `leg` (legenda com algarismos), `dados`.
- `posts`: `{youtube: {titulo, texto}, instagram: {texto}, tiktok: {texto}}`.

### Tipos de cena e `dados`
| tipo | dados |
|---|---|
| `numero_grande` | `valor` (texto curto, ex. "2×"), `linhas` [2 linhas], `pergunta` opcional |
| `titulo` | `titulo` (str ou [linha1, linha2 em verde]), `subtitulo` |
| `versus` | `a`, `b`, `rotulo_a`, `rotulo_b` (o que é cada caixa), `centro` |
| `formula` | `titulo`, `linha1` (conta), `resultado` (verde, grande), `nota` |
| `barras` | `titulo` (str ou lista), `itens` [{rotulo, valor, texto, destaque, grupo}], `nota` |
| `linhas` | `titulo`, `x_rotulo`, `x_ticks`, `ymax`, `ymin`, `y_passo`, `y_fmt` ("brl"/"num"/"pct"), `series` [{nome, pontos [[x,y]...], destaque, inicio, velocidade, rotulo_final}] |
| `lista` | `titulo` (lista), `itens` (3 itens curtos, até ~30 caracteres) |
| `cta` | `linhas` [2], `botao` |
| `assinatura` | sem dados; sempre a última cena, `tts`/`leg` = "Juro que explico." |

Limites de texto: títulos até ~22 caracteres por linha; `resultado` até ~14; legendas são quebradas automaticamente.
Para o vídeo passar de 61 s, o roteiro precisa de cerca de 150 a 190 palavras faladas em 8 a 10 cenas.

## Passo a passo
```bash
./setup.sh
python3 pipeline/checa.py episodios/<ID>            # antes da narração (só números e termos)
python3 pipeline/narracao.py episodios/<ID>/roteiro.json episodios/<ID> pm_alex 1.0
python3 pipeline/checa.py episodios/<ID>            # de novo, agora valida a duração
python3 pipeline/render.py episodios/<ID> frames <t1> <t2> ...   # um quadro no meio de cada cena
# abrir e olhar cada quadro: nada cortado, nada sobreposto, nada fora da tela
python3 pipeline/render.py episodios/<ID>           # vídeo completo + capa.png
```
Se a duração ficar abaixo de 61 s, acrescente conteúdo útil (outro exemplo, uma armadilha comum), nunca enrolação.
Apague os `frame_*.png` antes do commit.

## Publicação (Buffer, organização "My organization")
- YouTube `6af240c662b70b94b0d6dc1b`: 12:00, `metadata.youtube` = {title, categoryId "27", privacy "public", isAiGenerated true, madeForKids false}.
- Instagram `6af2406162b70b94b0d6d913`: 12:05, `metadata.instagram` = {type "reel", shouldShareToFeed true, isAiGenerated true}.
- TikTok `6af240ab62b70b94b0d6db65`: 12:10, `metadata.tiktok` = {isAiGenerated true}.
- `mode` customScheduled, `schedulingType` automatic, `dueAt` com offset -03:00 (America/Sao_Paulo).
- Vídeo: `https://raw.githubusercontent.com/nasrgabrieldd-bit/juro-que-explico/main/episodios/<ID>/<ID>.mp4` (confirmar HTTP 200 depois do push).
- Plano gratuito: no máximo 10 posts agendados por canal. Antes de agendar, liste os agendados; se já houver post para a data, não duplique.

## Data de publicação
A fila mantém cerca de uma semana agendada. Se algum canal tiver 9 ou mais posts agendados (limite do plano gratuito: 10), a rotina não produz nada naquele dia. Senão, agenda para o primeiro dia sem post no YouTube a partir de amanhã. Registre a data em `PAUTAS.md`.
