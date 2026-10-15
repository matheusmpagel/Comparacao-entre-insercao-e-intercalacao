"""Testes da ordenação por inserção e por intercalação.

Rodar: python testes.py
"""

import random
import sys
import time
import unittest

from ordenacao import Contador, contar_comparacoes, insercao, intercalacao

METODOS = {"insercao": insercao, "intercalacao": intercalacao}


class TestaOrdenacao(unittest.TestCase):
    def confere(self, entrada):
        for nome, ordenar in METODOS.items():
            with self.subTest(metodo=nome, entrada=entrada):
                self.assertEqual(ordenar(list(entrada)), sorted(entrada))

    # Casos difíceis pedidos no enunciado
    def test_lista_vazia(self):
        """Lista vazia ([])"""
        self.confere([])

    def test_um_elemento(self):
        """Um elemento só ([42])"""
        self.confere([42])

    def test_todos_iguais(self):
        """Todos os elementos iguais ([7] * 10)"""
        self.confere([7] * 10)

    def test_ja_ordenada(self):
        """Lista já ordenada (0 a 19)"""
        self.confere(list(range(20)))

    def test_invertida(self):
        """Lista invertida em ordem decrescente (20 a 1)"""
        self.confere(list(range(20, 0, -1)))

    # Outros casos comuns
    def test_dois_elementos(self):
        """Dois elementos (ordenados e invertidos)"""
        self.confere([2, 1])
        self.confere([1, 2])

    def test_negativos_e_repetidos(self):
        """Números negativos, zero e repetidos"""
        self.confere([3, -1, 0, -1, 5, 3, -7, 0])

    def test_textos(self):
        """Lista de textos/strings (ordenação lexicográfica)"""
        self.confere(["pera", "abacate", "uva", "banana"])

    def test_aleatorias_de_varios_tamanhos(self):
        """Listas aleatórias de tamanhos variados (n = 5 a 100)"""
        gerador = random.Random(2026)
        for n in [5, 10, 30, 50, 100]:
            self.confere([gerador.randint(-100, 100) for _ in range(n)])

    def test_nao_altera_a_lista_original(self):
        """Preservação da lista original (imutabilidade)"""
        for nome, ordenar in METODOS.items():
            with self.subTest(metodo=nome):
                original = [5, 3, 9, 1]
                ordenar(original)
                self.assertEqual(original, [5, 3, 9, 1])


class TestaContagem(unittest.TestCase):
    """Testes da contagem de comparações."""

    def test_insercao_em_lista_ordenada_faz_n_menos_1(self):
        """Inserção em lista ordenada faz n - 1 comparações"""
        self.assertEqual(contar_comparacoes(insercao, list(range(10))), 9)

    def test_insercao_em_lista_invertida_faz_pior_caso(self):
        """Inserção em lista invertida faz o pior caso (n * (n - 1) / 2)"""
        self.assertEqual(contar_comparacoes(insercao, list(range(10, 0, -1))), 45)

    def test_casos_sem_comparacao(self):
        """Casos de 0 ou 1 elemento fazem 0 comparações"""
        for ordenar in (insercao, intercalacao, sorted):
            self.assertEqual(contar_comparacoes(ordenar, []), 0)
            self.assertEqual(contar_comparacoes(ordenar, [1]), 0)

    def test_sorted_tambem_e_contado(self):
        """sorted() do Python tem comparações contadas via __lt__"""
        self.assertEqual(contar_comparacoes(sorted, list(range(10))), 9)


class RunnerDidaticoResultado(unittest.TextTestResult):
    """Exibe cada teste executado com seu nome didático, status e tempo em ms."""

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream

    def startTest(self, test):
        self._inicio = time.perf_counter()
        classe = test.__class__.__name__
        if classe != getattr(self, "_classe_atual", None):
            self._classe_atual = classe
            titulo = (
                "1. Testes de Corretude (Casos Difíceis e Comuns)"
                if classe == "TestaOrdenacao"
                else "2. Testes de Contagem de Comparações"
            )
            self.stream.write(f"\n{titulo}\n" + "-" * len(titulo) + "\n")
            self.stream.flush()
        unittest.TestResult.startTest(self, test)

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        tempo_ms = (time.perf_counter() - self._inicio) * 1000
        desc = test.shortDescription() or test._testMethodName
        self.stream.write(f"  [OK] {desc:<58} ({tempo_ms:6.3f} ms)\n")
        self.stream.flush()

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        tempo_ms = (time.perf_counter() - self._inicio) * 1000
        desc = test.shortDescription() or test._testMethodName
        self.stream.write(f"  [FALHA] {desc:<55} ({tempo_ms:6.3f} ms)\n")
        self.stream.flush()

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        tempo_ms = (time.perf_counter() - self._inicio) * 1000
        desc = test.shortDescription() or test._testMethodName
        self.stream.write(f"  [ERRO] {desc:<56} ({tempo_ms:6.3f} ms)\n")
        self.stream.flush()


class LoaderDidatico(unittest.TestLoader):
    """Carrega os testes na ordem exata em que foram definidos no arquivo."""

    def getTestCaseNames(self, testCaseClass):
        return [
            m
            for m in testCaseClass.__dict__
            if m.startswith("test_") and callable(getattr(testCaseClass, m))
        ]


def main():
    loader = LoaderDidatico()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestaOrdenacao))
    suite.addTests(loader.loadTestsFromTestCase(TestaContagem))

    runner = unittest.TextTestRunner(
        stream=sys.stdout, verbosity=0, resultclass=RunnerDidaticoResultado
    )
    resultado = runner.run(suite)
    sys.exit(0 if resultado.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
