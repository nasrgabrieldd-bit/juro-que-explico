"""Monta agenda_pendente.json: posts já produzidos que esperam vaga no Buffer (limite de 10 agendados por canal).
Uso: python3 lotes/gera_agenda.py ID:AAAA-MM-DD[:HH:MM][:canais] ...   (canais = yt,ig,tt; padrão os três; hora padrão 12:00)
Acrescenta à lista existente sem duplicar (chave = id + canal)."""
import json, os, sys

BASE = "/home/claude/juro-que-explico"
RAW = "https://raw.githubusercontent.com/nasrgabrieldd-bit/juro-que-explico/main/episodios"
CANAIS = {
    "yt": ("6af240c662b70b94b0d6dc1b", 0),
    "ig": ("6af2406162b70b94b0d6d913", 5),
    "tt": ("6af240ab62b70b94b0d6db65", 10),
}
arq = f"{BASE}/agenda_pendente.json"
lista = json.load(open(arq)) if os.path.exists(arq) else []
chaves = {(i["episodio"], i["canal"]) for i in lista}

for arg in sys.argv[1:]:
    partes = arg.split(":")
    ep, dia = partes[0], partes[1]
    hh, mm = (int(partes[2]), int(partes[3])) if len(partes) >= 4 else (12, 0)
    quais = partes[4].split(",") if len(partes) >= 5 else ["yt", "ig", "tt"]
    r = json.load(open(f"{BASE}/episodios/{ep}/roteiro.json"))
    url = f"{RAW}/{ep}/{ep}.mp4"
    for c in quais:
        if (ep, c) in chaves:
            continue
        cid, off = CANAIS[c]
        m = mm + off
        due = f"{dia}T{hh + m // 60:02d}:{m % 60:02d}:00-03:00"
        p = {"channelId": cid, "schedulingType": "automatic", "mode": "customScheduled", "dueAt": due}
        if c == "yt":
            t = r["posts"]["youtube"]
            p.update(text=t["texto"], assets=[{"video": {"url": url, "metadata": {"title": t["titulo"]}}}],
                     metadata={"youtube": {"title": t["titulo"], "categoryId": "27", "privacy": "public",
                                           "isAiGenerated": True, "madeForKids": False}})
        elif c == "ig":
            p.update(text=r["posts"]["instagram"]["texto"], assets=[{"video": {"url": url}}],
                     metadata={"instagram": {"type": "reel", "shouldShareToFeed": True, "isAiGenerated": True}})
        else:
            p.update(text=r["posts"]["tiktok"]["texto"], assets=[{"video": {"url": url}}],
                     metadata={"tiktok": {"isAiGenerated": True}})
        lista.append({"episodio": ep, "canal": c, "create_post": p})
        chaves.add((ep, c))

lista.sort(key=lambda i: i["create_post"]["dueAt"])
json.dump(lista, open(arq, "w"), ensure_ascii=False, indent=1)
print(len(lista), "itens pendentes")
for i in lista:
    print(" ", i["episodio"], i["canal"], i["create_post"]["dueAt"])
