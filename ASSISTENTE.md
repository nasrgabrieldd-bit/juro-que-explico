# Assistente de crescimento e monetização — Juro que Explico

Roda a cada 15 dias (dias 9 e 24 de cada mês, 08:50, horário de Brasília). Cada relatório fecha um ciclo de 15 dias de posts e define o ciclo seguinte. A rotina diária lê o último relatório antes de escrever qualquer roteiro.

## 1. Coleta (só dados reais; o que não vier da API fica como "indisponível", nunca como zero)
- **YouTube** (Composio, conta youtube): `YOUTUBE_GET_CHANNEL_STATISTICS` (mine=true) para inscritos, views e nº de vídeos; `YOUTUBE_LIST_CHANNEL_VIDEOS` + `YOUTUBE_GET_VIDEO_DETAILS_BATCH` (snippet, statistics, contentDetails) para views, likes e comentários por vídeo. Horas de exibição e retenção: tentar a YouTube Analytics API (`proxy_execute` GET `https://youtubeanalytics.googleapis.com/v2/reports?ids=channel==MINE&metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained&dimensions=video&startDate=...&endDate=...`). Se não houver permissão, estimar horas = Σ(views × duração × 0,35) e marcar como **estimativa**.
- **Instagram** (Composio, conta instagram): `INSTAGRAM_GET_USER_INFO` (ig_user_id "me": followers_count, media_count) e `INSTAGRAM_GET_IG_USER_MEDIA` (views, likes, comentários, salvamentos, compartilhamentos por reel).
- **TikTok** e todos os canais: Buffer `list_posts` com `includeMetrics: true` (status sent, últimos 15 dias) e `get_aggregated_post_metrics`. Seguidores do TikTok: usar o que o Buffer devolver; se não houver, pedir ao fundador o número no próximo aviso.
- Guardar os números brutos em `relatorios/dados_AAAA-MM-DD.json` (vale como histórico para comparar ciclos).

## 2. Análise
- Tabela por vídeo e plataforma: views, curtidas, comentários, salvamentos/compartilhamentos, views por seguidor; ranking do ciclo.
- Padrões: que tipo de gancho (cena 1), tema, duração e horário puxaram mais views e comentários; que vídeos morreram nos primeiros segundos (views baixas no TikTok/Shorts = gancho fraco). Comparar com o ciclo anterior.
- Leitura da audiência: perguntas e pedidos nos comentários (YouTube `YOUTUBE_LIST_COMMENT_THREADS2`, Instagram media) viram pautas.

## 3. Monetização — metas, distância e prazo
Requisitos (conferidos em 10/11/2026; reconferir em fonte oficial a cada relatório, porque mudam):

| Plataforma | Programa | Requisito |
|---|---|---|
| TikTok | Programa de Recompensas do Criador (Brasil) | 18+, **conta pessoal** (conta empresa não entra), 10 mil seguidores, 100 mil views nos últimos 30 dias, vídeos com mais de 1 min |
| YouTube | YPP nível 1 (financiamento por fãs; inalterado em 2027) | 500 inscritos, 3 envios públicos em 90 dias, 3.000 h de exibição em 12 meses **ou** 3 mi de views de Shorts em 90 dias |
| YouTube | YPP anúncios — até 31/01/2027 | 1.000 inscritos + 4.000 h em 12 meses **ou** 10 mi de views de Shorts em 90 dias |
| YouTube | YPP anúncios — a partir de 01/02/2027 | 1.000 inscritos + **8.000 h** em 365 dias **ou** **20 mi** de views de Shorts em 90 dias; receita de Shorts só com 10 mi de views de Shorts em 90 dias |
| Instagram | Presentes em Reels | 500 seguidores, conta profissional |
| Instagram | Assinaturas / bônus (convite) | 10 mil seguidores; não há pagamento por view garantido no Brasil |

Reconferência de 10/11/2026 (relatório do ciclo 0): sem mudanças nos requisitos do YouTube e do TikTok. Fontes lidas: [YouTube Help 72851](https://support.google.com/youtube/answer/72851?hl=en), [YouTube Help 12843009 (mudanças de 01/02/2027)](https://support.google.com/youtube/answer/12843009?hl=en), [TikTok Newsroom](https://newsroom.tiktok.com/introducing-the-new-creator-rewards-program?lang=en) (a Creator Academy e os termos BR bloqueiam leitura automática). As linhas do Instagram não puderam ser confirmadas: a Central de Ajuda não renderiza na leitura automática; conferir no app (Painel profissional → Monetização). Acréscimo da política de monetização ([YouTube Help 1311392](https://support.google.com/youtube/answer/1311392?hl=en)): personas de IA que se apresentam como especialista humano em finanças não monetizam.

Para cada linha: valor atual, quanto falta, ritmo dos últimos 15 dias e **data projetada** (falta ÷ ritmo), comparando com a meta oficial abaixo. Se o ritmo não fecha a meta, dizer o que precisa mudar (ex.: "precisamos de X views/dia no TikTok").

**Metas oficiais (revisar a cada relatório com os dados reais):**
- Instagram 500 seguidores (presentes): fev/2027.
- TikTok Recompensas (10 mil seguidores + 100 mil views/30 dias): **maio/2027**.
- YouTube nível 1 (500 inscritos + 3.000 h ou 3 mi views de Shorts): ago/2027.
- YouTube anúncios (1.000 inscritos + 8.000 h, regra de 2027): **dez/2027**, pelo caminho dos vídeos longos.

## 4. Estimativa de ganho (sempre em faixa e marcada como estimativa)
- TikTok Recompensas: US$ 0,50 a US$ 1,00 por mil views qualificadas (views do Para Você com mais de 5 s), só depois de aprovado e só para vídeos postados após a aprovação.
- YouTube: RPM real só aparece no Studio após o YPP. Até lá, usar faixa ilustrativa de R$ 3 a R$ 15 por mil views em vídeo longo e dizer que é hipótese (finanças costuma pagar mais que a média).
- Instagram: sem pagamento por view; considerar só presentes, parcerias e afiliados quando houver.
- Mostrar: ganho que os views do ciclo **teriam gerado se** os canais já estivessem monetizados, e projeção mensal na data das metas.

## 5. Diretrizes que protegem a monetização (checar todo ciclo)
- YouTube "conteúdo inautêntico" (produzido em massa/repetitivo): variar formatos de cena, ganchos, estrutura e temas; cada vídeo com cálculo próprio e explicação, nada de modelo idêntico com troca de números; nada de persona sintética. Rótulo de conteúdo alterado/sintético ligado quando aplicável.
- Originalidade: sem trechos de terceiros, músicas sem licença, imagens de outros canais ou de pessoas reais.
- Linguagem simples para todas as classes sociais (ver PRODUCAO.md, "Linguagem"): conferir se algum roteiro do ciclo soou como aula ou usou jargão sem explicar.
- Finanças: sem recomendação de ativo, promessa de ganho ou "dinheiro fácil"; aviso educativo em todos os posts.
- TikTok: vídeos acima de 1 min, conta pessoal, sem marca d'água de outro app, nada de comprar seguidores ou engajamento.
- Postagem diária mantida (YouTube exige atividade para ficar no YPP).

## 6. Saídas
1. `relatorios/AAAA-MM-DD.md` com: resumo em 5 linhas, tabela de vídeos, padrões, metas e prazos, estimativa de ganho, riscos de política, **plano do próximo ciclo**.
2. **Plano do próximo ciclo (15 dias)**: 15 pautas de vídeos curtos em ordem + 4 vídeos longos HORIZONTAIS (2 por semana, até 4 min, para YouTube e feed do Instagram), cada longo com cortes verticais Parte 1/2/3, com o gancho sugerido e o motivo de cada uma vir do dado. Escrever essas 15 no topo da Fila do `PAUTAS.md` e registrar as regras novas em `PRODUCAO.md`, seção "Aprendizados do último ciclo" (substituir a anterior). A rotina diária segue isso.
3. Doc do Project "NEXO — Media Company": `claude/13_RELATORIOS_QUINZENAIS.md` (acrescentar o resumo do ciclo no topo; não reescrever ciclos antigos).
4. Commit e push.
5. Aviso ao fundador (push): 6–8 linhas com views do ciclo, seguidores por rede, distância de cada meta, data projetada vs meta, estimativa de ganho e as 3 mudanças para o próximo ciclo.

## 7. Banco de ideias
Toda vez, acrescentar ao fim da Fila do `PAUTAS.md` pelo menos 5 ideias novas tiradas de: comentários, vídeos que performaram melhor, dúvidas comuns de finanças pessoais e datas do calendário (13º, IR, Black Friday, volta às aulas), sempre evergreen e de baixo risco.
