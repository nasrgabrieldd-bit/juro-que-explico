# Juro que Explico — linha de produção

Canal de educação financeira: **"O dinheiro sem complicação."**
YouTube @JuroqueExplico · Instagram @juroqueexplicobr · TikTok @juro.que.explico

Este repositório guarda o código que produz os vídeos e os vídeos prontos para publicação. Tudo roda com ferramentas gratuitas.

## Estrutura
- `pipeline/checagem.py`: passada de checagem independente. Recalcula cada número do roteiro e reprova se algo divergir.
- `pipeline/narracao.py`: narração por cena com Kokoro TTS (vozes pt-BR, licença Apache 2.0).
- `pipeline/render_s001.py`: render 9:16 (Pillow + FFmpeg) com identidade visual, gráficos, legendas e marca d'água.
- `marca/`: foto de perfil, banner e textos dos perfis.
- `episodios/<ID>/`: roteiro, tempos, metadados por plataforma e vídeo final.

## Como rodar
```bash
./setup.sh                                   # instala dependências e baixa o modelo de voz
python3 pipeline/checagem.py episodios/JQE-S001/roteiro.json
python3 pipeline/narracao.py episodios/JQE-S001/roteiro.json episodios/JQE-S001 pm_alex 1.0
python3 pipeline/render_s001.py episodios/JQE-S001
```

## Regras de produção
- Vídeos verticais com mais de 1 minuto (alvo 65–90 s).
- Marca d'água em todos os vídeos.
- Todo número na tela vem de fonte registrada ou de cálculo verificado por `checagem.py`.
- Narração gerada por IA é declarada na descrição.
