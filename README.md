# Juro que Explico — linha de produção

Canal de educação financeira: **"O dinheiro sem complicação."**
Marca: Juro que Explico (@juroqueexplico). O rebrand estudado em 09–10/11 (Provento/Montante) foi descartado; arquivos em marca/*provento* ficam só como histórico.

Este repositório guarda o código que produz os vídeos e os vídeos prontos para publicação. Tudo roda com ferramentas gratuitas.

## Estrutura
- `pipeline/checagem.py`: passada de checagem independente. Recalcula cada número do roteiro e reprova se algo divergir.
- `pipeline/narracao.py`: narração por cena com Kokoro TTS (vozes pt-BR, licença Apache 2.0).
- `pipeline/render.py`: motor genérico de render 9:16 (Pillow + FFmpeg) com cenas tipadas, gráficos, legendas, capa e marca d'água.
- `pipeline/checa.py`: checagem genérica de números, termos proibidos e duração.
- `pipeline/render_s001.py` e `pipeline/checagem.py`: versões do piloto S001.
- `PRODUCAO.md`: manual da rotina diária automática. `PAUTAS.md`: fila e histórico de pautas.
- `marca/`: foto de perfil, banner e textos dos perfis.
- `episodios/<ID>/`: roteiro, tempos, metadados por plataforma e vídeo final.

## Como rodar
```bash
./setup.sh                                   # instala dependências e baixa o modelo de voz
python3 pipeline/checa.py episodios/JQE-S002
python3 pipeline/narracao.py episodios/JQE-S002/roteiro.json episodios/JQE-S002 pm_alex 1.0
python3 pipeline/render.py episodios/JQE-S002
```

## Regras de produção
- Vídeos verticais com mais de 1 minuto (alvo 65–90 s).
- Marca d'água em todos os vídeos.
- Todo número na tela vem de fonte registrada ou de cálculo verificado por `checagem.py`.
- Narração gerada por IA é declarada na descrição.
