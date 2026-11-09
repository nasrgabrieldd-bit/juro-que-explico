"""Passada de checagem independente: recalcula cada número do roteiro e reprova se algo divergir."""
import json
import sys

rot = json.load(open(sys.argv[1]))
p = rot["parametros"]
C, i, n = p["principal"], p["taxa_mensal"], p["meses"]

simples = C * (1 + i * n)
composto = C * (1 + i) ** n
erros = []

def checa(cond, msg):
    print(("OK   " if cond else "FALHA"), msg)
    if not cond:
        erros.append(msg)

checa(abs(C * i - 20) < 1e-9, "juro simples mensal = 20")
checa(abs(simples - C - 720) < 1e-9, "juros simples totais = 720")
checa(abs(simples - 1720) < 1e-9, "montante simples = 1720")
checa(round(composto, 2) == 2039.89, f"montante composto = {composto:.4f}")
checa(round(C * (1 + i) ** (n - 1) * i) == 40, f"juro do último mês = {C*(1+i)**(n-1)*i:.4f}")
checa(composto >= 2 * C and C * (1 + i) ** (n - 1) < 2 * C, "dobra exatamente no mês 36")
checa(abs((composto - simples) - 319.89) < 0.01, f"diferença = {composto - simples:.4f}")
gaps = [C * (1 + i) ** k - C * (1 + i * k) for k in range(1, n + 1)]
checa(all(b > a for a, b in zip(gaps, gaps[1:])), "diferença cresce mês a mês")

s60, c60 = C * (1 + i * 60), C * (1 + i) ** 60
checa(abs(s60 - 2200) < 1e-9, "simples 60 meses = 2200")
checa(round(c60) == 3281, f"composto 60 meses = {c60:.4f}")
checa(c60 - s60 > 1000, f"diferença 60 meses = {c60 - s60:.4f} > 1000")

texto = " ".join(c["tts"] for c in rot["cenas"]).lower()
for termo in ["mil reais", "dois por cento", "vinte reais", "setecentos e vinte",
              "mil setecentos e vinte", "quarenta", "dois mil e trinta e nove", "trezentos e vinte",
              "dois mil e duzentos", "três mil duzentos e oitenta e um", "mais de mil reais"]:
    checa(termo in texto, f"narração contém '{termo}'")
for proibido in ["garantido", "recomendo", "compre", "venda", "invista em"]:
    checa(proibido not in texto, f"narração sem termo proibido '{proibido}'")

if erros:
    sys.exit(f"REPROVADO: {len(erros)} falha(s)")
print("APROVADO")
