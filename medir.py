"""Mede tempo e comparações da inserção, da intercalação e do sorted() do Python.

Rodar: python medir.py

Refaz do zero:
- dados.csv: uma linha por medição (método, n, repetição, tempo em segundos, comparações);
- grafico_tempos.png e grafico_comparacoes.png: as médias de cada n.
Também imprime as tabelas de médias e o n em que a intercalação passa a ganhar.
"""

import csv
import math
import random
import statistics
import sys
import time
from pathlib import Path

from ordenacao import contar_comparacoes, insercao, intercalacao

TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
REPETICOES = 10
SEMENTE = 2026
METODOS = {"insercao": insercao, "intercalacao": intercalacao, "sorted": sorted}
NOMES = {"insercao": "Inserção", "intercalacao": "Intercalação", "sorted": "sorted() do Python"}

PASTA = Path(__file__).resolve().parent
CSV = PASTA / "dados.csv"
GRAFICO_TEMPOS = PASTA / "grafico_tempos.png"
GRAFICO_COMPARACOES = PASTA / "grafico_comparacoes.png"


def cronometrar(ordenar, lista):
    """Tempo, em segundos, de uma chamada de `ordenar`."""
    inicio = time.perf_counter()
    ordenar(lista)
    return time.perf_counter() - inicio


def medir():
    """Todas as medições: uma lista aleatória nova por repetição, a mesma para os três métodos."""
    gerador = random.Random(SEMENTE)
    linhas = []
    for n in TAMANHOS:
        for repeticao in range(1, REPETICOES + 1):
            lista = [gerador.randint(0, 1_000_000) for _ in range(n)]
            for nome, ordenar in METODOS.items():
                tempo = cronometrar(ordenar, lista)
                comparacoes = contar_comparacoes(ordenar, lista)
                linhas.append({"metodo": nome, "n": n, "repeticao": repeticao, "tempo_s": tempo, "comparacoes": comparacoes})
        print(f"  n = {n} ok", file=sys.stderr)
    return linhas


def gravar_csv(linhas):
    with CSV.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["metodo", "n", "repeticao", "tempo_s", "comparacoes"])
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow({**linha, "tempo_s": f"{linha['tempo_s']:.9f}"})


def medias(linhas, campo):
    """{método: [média de `campo` para cada n de TAMANHOS]}."""
    return {
        nome: [statistics.fmean(l[campo] for l in linhas if l["metodo"] == nome and l["n"] == n) for n in TAMANHOS]
        for nome in METODOS
    }


def ponto_de_virada(insercao_, intercalacao_):
    """Menor n a partir do qual a intercalação fica abaixo da inserção em todos os n medidos."""
    for i, n in enumerate(TAMANHOS):
        if all(m < s for m, s in zip(intercalacao_[i:], insercao_[i:])):
            return n
    return None


def imprimir_tabelas(tempos, comparacoes):
    print("\nTempo médio (µs)\n")
    print("| n | Inserção | Intercalação | sorted() |")
    print("|---:|---:|---:|---:|")
    for i, n in enumerate(TAMANHOS):
        print(f"| {n} | {tempos['insercao'][i] * 1e6:.1f} | {tempos['intercalacao'][i] * 1e6:.1f} | {tempos['sorted'][i] * 1e6:.1f} |")

    print("\nComparações (média)\n")
    print("| n | Inserção | Intercalação | sorted() | n·log2(n) |")
    print("|---:|---:|---:|---:|---:|")
    for i, n in enumerate(TAMANHOS):
        print(
            f"| {n} | {comparacoes['insercao'][i]:.1f} | {comparacoes['intercalacao'][i]:.1f} | "
            f"{comparacoes['sorted'][i]:.1f} | {n * math.log2(n):.1f} |"
        )

    virada_tempo = ponto_de_virada(tempos["insercao"], tempos["intercalacao"])
    virada_comparacoes = ponto_de_virada(comparacoes["insercao"], comparacoes["intercalacao"])
    print(f"\nA intercalação passa a ser mais rápida a partir de n = {virada_tempo}")
    print(f"A intercalação passa a fazer menos comparações a partir de n = {virada_comparacoes}")
    return virada_tempo, virada_comparacoes


def desenhar(tempos, comparacoes, virada_tempo, virada_comparacoes):
    try:
        import matplotlib

        matplotlib.use("Agg")  # só gera arquivos, sem abrir janela
        import matplotlib.pyplot as plt
    except ImportError:
        sys.exit("\nFalta o matplotlib para os gráficos: rode  pip install -r requirements.txt  (o CSV já foi gravado).")

    estilos = {"insercao": "o-", "intercalacao": "s-", "sorted": "^-"}

    fig, eixo = plt.subplots(figsize=(8, 5.5))
    for nome in METODOS:
        eixo.plot(TAMANHOS, [t * 1e6 for t in tempos[nome]], estilos[nome], label=NOMES[nome])
    if virada_tempo:
        eixo.axvline(virada_tempo, color="gray", linestyle=":", label=f"Virada (n = {virada_tempo})")
    eixo.set(xscale="log", yscale="log", xlabel="n (tamanho da lista)", ylabel="Tempo médio (µs)")
    eixo.set_title(f"Tempo médio de ordenação ({REPETICOES} repetições por n)")
    eixo.grid(True, which="both", alpha=0.3)
    eixo.legend()
    fig.tight_layout()
    fig.savefig(GRAFICO_TEMPOS, dpi=150)
    plt.close(fig)

    fig, eixo = plt.subplots(figsize=(8, 5.5))
    for nome in METODOS:
        eixo.plot(TAMANHOS, comparacoes[nome], estilos[nome], label=NOMES[nome])
    eixo.plot(TAMANHOS, [n * math.log2(n) for n in TAMANHOS], "k--", alpha=0.6, label="n·log2(n)")
    if virada_comparacoes:
        eixo.axvline(virada_comparacoes, color="gray", linestyle=":", label=f"Virada (n = {virada_comparacoes})")
    eixo.set(xscale="log", yscale="log", xlabel="n (tamanho da lista)", ylabel="Comparações (média)")
    eixo.set_title(f"Número de comparações ({REPETICOES} repetições por n)")
    eixo.grid(True, which="both", alpha=0.3)
    eixo.legend()
    fig.tight_layout()
    fig.savefig(GRAFICO_COMPARACOES, dpi=150)
    plt.close(fig)


def main():
    for antigo in (CSV, GRAFICO_TEMPOS, GRAFICO_COMPARACOES):
        antigo.unlink(missing_ok=True)
    print(f"Medindo {len(TAMANHOS)} tamanhos x {REPETICOES} repetições x {len(METODOS)} métodos...", file=sys.stderr)
    linhas = medir()
    gravar_csv(linhas)
    tempos = medias(linhas, "tempo_s")
    comparacoes = medias(linhas, "comparacoes")
    virada_tempo, virada_comparacoes = imprimir_tabelas(tempos, comparacoes)
    desenhar(tempos, comparacoes, virada_tempo, virada_comparacoes)
    print(f"\nGravados: {CSV.name}, {GRAFICO_TEMPOS.name} e {GRAFICO_COMPARACOES.name}")


if __name__ == "__main__":
    main()
