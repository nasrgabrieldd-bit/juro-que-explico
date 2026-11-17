# Referências e skills enviadas pelo fundador

Toda novidade que o fundador mandar entra aqui (data, origem, o que é, decisão, onde foi integrada). Lei completa em `producao-de-video/SKILL.md`.

| # | Data | Origem | O que é | Avaliação | Integração |
|---|---|---|---|---|---|
| 1 | 16/11/2026 | Link plugueia.com.br/isca-estilo (Pedro Barros, @pedrobarros.ia) | Skill **Lemo-Opuscar**: filmes animados em 99 estilos, feitos em código, com voz, trilha e mix | Código MIT, instala sem scripts suspeitos (setup.sh só clona, roda npm/pip e baixa o Chromium do Playwright). Guias em CC BY-NC 4.0: não copiados para este repositório público; baixados em tempo de execução. Exige ffmpeg 7+ (resolvido). Estilos com estrela precisam de gerador de imagens (não usados). O site também oferece serviços pagos (mentoria, empresa): sem relação com a skill gratuita. | Skill 2.0, Motor B. `REGISTRO.json`, `atualizar_skills.sh`. Testada: instalação e render de teste |
| 2 | 17/11/2026 | Link alavancax.com/skill-watch-claude | Skill **/watch** (bradautomates/claude-video, autor Bradley Bonanno): o Claude assiste vídeos baixando, tirando quadros e lendo legenda/transcrição | MIT. Código lido: sem comportamento malicioso; usa yt-dlp e ffmpeg; o motor Gemini opcional envia o vídeo ao Google. Testada em arquivo local. YouTube é bloqueado na rede da nuvem (403 do proxy, não contornado): para redes sociais, rodar no computador do fundador | Skill 2.2. `REGISTRO.json` (`git-clone`), `atualizar_skills.sh`, seção "Pesquisa por vídeo" da SKILL.md |
