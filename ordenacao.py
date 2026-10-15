"""Ordenação por inserção e por intercalação (merge sort).

As duas funções devolvem uma lista nova e não mexem na lista recebida. Os elementos são
comparados só com `<`, o que permite contar as comparações com `Contador` (mais abaixo).
"""


def insercao(lista):
    """Ordenação por inserção. O(n²) comparações no pior caso, O(n) com a lista já ordenada."""
    a = list(lista)
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        # Só anda enquanto o anterior é estritamente maior: iguais não trocam de lugar (estável).
        while j >= 0 and chave < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = chave
    return a


def intercalacao(lista):
    """Ordenação por intercalação (merge sort). O(n log n) comparações em qualquer caso."""
    if len(lista) <= 1:
        return list(lista)
    meio = len(lista) // 2
    return _intercalar(intercalacao(lista[:meio]), intercalacao(lista[meio:]))


def _intercalar(esquerda, direita):
    """Junta duas listas já ordenadas numa só, ordenada."""
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        # Pega da direita só se for estritamente menor: no empate vem o da esquerda (estável).
        if direita[j] < esquerda[i]:
            resultado.append(direita[j])
            j += 1
        else:
            resultado.append(esquerda[i])
            i += 1
    # Uma das duas acabou; o resto da outra já está em ordem.
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


# ---- contagem de comparações ----------------------------------------------------------------


class Contador:
    """Conta as comparações feitas entre os elementos que ele embrulha."""

    def __init__(self):
        self.comparacoes = 0

    def embrulhar(self, valores):
        return [Comparavel(v, self) for v in valores]


class Comparavel:
    """Guarda um valor e conta as comparações feitas com `<`."""

    def __init__(self, valor, contador):
        self.valor = valor
        self._contador = contador

    def __lt__(self, outro):
        self._contador.comparacoes += 1
        return self.valor < outro.valor


def contar_comparacoes(ordenar, valores):
    """Quantas comparações `ordenar` (insercao, intercalacao ou sorted) faz para ordenar `valores`."""
    contador = Contador()
    ordenar(contador.embrulhar(valores))
    return contador.comparacoes
