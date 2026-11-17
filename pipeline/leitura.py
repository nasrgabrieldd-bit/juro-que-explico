"""Tempo de leitura dos textos na tela (técnica da Lemo-Opuscar 'readcheck', adaptada ao nosso roteiro).
Cada texto de cena precisa ficar na tela ao menos: caracteres ÷ 15 por segundo + 1,5 s (mínimo 1,5 s).
Uso: python3 pipeline/leitura.py episodios/<ID>   (precisa de tempos.json)"""
import json, sys
EP = sys.argv[1].rstrip("/")
rot = json.load(open(f"{EP}/roteiro.json")); tj = json.load(open(f"{EP}/tempos.json"))
tm = {c["id"]: c for c in tj["cenas"]}
ids = [c["id"] for c in rot["cenas"]]
falhas = 0


def textos(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("pontos", "tom", "pose", "quem", "variante"):
                yield from textos(v)
    elif isinstance(o, list):
        for v in o:
            yield from textos(v)


for i, c in enumerate(rot["cenas"]):
    ini = tm[c["id"]]["inicio"]
    fim = tm[ids[i + 1]]["inicio"] if i + 1 < len(ids) else tj["total"]
    vis = fim - ini
    # leitura de cada bloco de texto, em separado (blocos aparecem juntos na cena)
    for t in textos(c.get("dados", {})):
        t = t.strip()
        if len(t) < 4:
            continue
        need = max(1.5, len(t.replace(" ", "")) / 15 + 1.5)
        if vis < need:
            falhas += 1
            print(f"FALHA {c['id']}: '{t}' precisa de {need:.1f} s e a cena dura {vis:.1f} s")
print("APROVADO (leitura)" if not falhas else f"REPROVADO: {falhas} texto(s) rápido(s) demais")
sys.exit(1 if falhas else 0)
