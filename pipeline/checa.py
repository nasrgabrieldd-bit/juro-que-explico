"""Checagem genérica — passada independente da escrita.
Regras (reprova se qualquer uma falhar):
1. Todo cálculo em roteiro['calculos'] é avaliado de novo aqui (só matemática).
2. Todo número que aparece na tela (legendas, dados das cenas, capa) e nos textos das redes precisa
   bater com um cálculo, um parâmetro ou um dado de fonte registrado em roteiro['numeros_fonte'] (com URL e data).
3. Nenhum termo proibido (promessa de ganho, recomendação de compra/venda).
4. Se tempos.json existir: vídeo vertical com mais de 61 s (regra D15).
Uso: python3 pipeline/checa.py episodios/<ID>"""
import json
import math
import os
import re
import sys

EP = sys.argv[1].rstrip("/")
rot = json.load(open(f"{EP}/roteiro.json"))
erros = []


def ok(cond, msg):
    print(("OK   " if cond else "FALHA"), msg)
    if not cond:
        erros.append(msg)


# 1. cálculos
SEGURO = {k: getattr(math, k) for k in ("log", "log10", "exp", "sqrt", "floor", "ceil")}
SEGURO.update({"round": round, "min": min, "max": max, "abs": abs})
calc = {}
for nome, expr in rot.get("calculos", {}).items():
    ok(re.fullmatch(r"[\w\s\.\+\-\*/\(\),%]+", expr) is not None, f"expressão segura: {nome}")
    calc[nome] = eval(expr, {"__builtins__": {}}, {**SEGURO, **calc})
    print(f"      {nome} = {calc[nome]:.4f}")

permitidos = list(calc.values())
for v in rot.get("parametros", {}).values():
    if isinstance(v, (int, float)):
        permitidos += [v, v * 100]
for f in rot.get("numeros_fonte", []):
    ok(bool(f.get("url")) and bool(f.get("data_referencia")), f"fonte com URL e data: {f.get('descricao')}")
    permitidos.append(f["valor"])
permitidos += rot.get("numeros_livres", [])  # ex.: 72 (nome da regra), anos de calendário


def bate(x):
    if float(x).is_integer() and 0 <= x <= 12:
        return True  # contagens estruturais (3 anos, 5 itens)
    for p in permitidos:
        for cand in (p, round(p), round(p, 1), round(p, 2), math.floor(p), math.ceil(p)):
            if abs(x - cand) < 0.006:
                return True
    return False


def numeros(s):
    out = []
    for m in re.finditer(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?", s):
        t = m.group().replace(".", "").replace(",", ".")
        out.append((m.group(), float(t)))
    return out


def textos(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("pontos", "valor", "tts"):
                yield from textos(v)
    elif isinstance(o, list):
        for v in o:
            yield from textos(v)


# 2. números na tela e nos textos das redes
alvo = [c.get("leg", "") for c in rot["cenas"]] + list(textos([c.get("dados", {}) for c in rot["cenas"]]))
alvo += list(textos(rot.get("capa", {}))) + list(textos(rot.get("posts", {})))
soltos = sorted({bruto for s in alvo for bruto, v in numeros(s) if not bate(v)})
ok(not soltos, "todo número tem cálculo ou fonte" + (f" — sem lastro: {soltos}" if soltos else ""))

# 3. termos proibidos
tudo = " ".join([c["tts"] for c in rot["cenas"]] + alvo).lower()
for p in ["garantido", "garantia de lucro", "recomendo comprar", "compre agora", "venda agora", "invista em",
          "fique rico", "sem risco", "lucro certo"]:
    ok(p not in tudo, f"sem termo proibido '{p}'")
ok(bool(rot.get("fontes")), "fontes registradas")
ok(rot["cenas"][-1]["tipo"] == "assinatura", "termina com a assinatura")

# retenção (regras para episódios a partir do JQE-S010)
gancho = rot["cenas"][0]
primeira = re.split(r"(?<=[.?!])\s+", gancho["tts"].strip())[0]
ok(len(primeira.split()) <= 16, f"gancho: primeira frase com até 16 palavras ({len(primeira.split())})")
ok(gancho["tipo"] in ("numero_grande", "versus", "formula", "titulo"), "gancho: cena 1 mostra número, comparação ou conta")
ok(not re.match(r"(?i)\s*(ol[áa]|oi|fala|bem-vindo|neste v[íi]deo|hoje vamos)", gancho["tts"]), "gancho: sem saudação nem introdução")

# 4. duração
if os.path.exists(f"{EP}/tempos.json"):
    tj = json.load(open(f"{EP}/tempos.json"))
    total = tj["total"] + 1.2
    if len(tj["cenas"]) > 1:
        ok(tj["cenas"][1]["inicio"] <= 8.0, f"gancho: cena 2 começa até 8 s ({tj['cenas'][1]['inicio']:.1f} s)")
    ok(total > 61, f"duração {total:.1f} s > 61 s (TikTok Creator Rewards)")
    if rot.get("formato", "").startswith("horizontal"):
        ok(total >= 240, f"duração {total:.1f} s ≥ 4 min (vídeo longo)")
    else:
        ok(total < 175, f"duração {total:.1f} s < 3 min (Shorts)")

if erros:
    sys.exit(f"REPROVADO: {len(erros)} falha(s)")
print("APROVADO")
