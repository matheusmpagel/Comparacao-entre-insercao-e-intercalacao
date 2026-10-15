# Relatório: ordenação por inserção × ordenação por intercalação

## Como foi medido

- Tamanhos: n = 5, 10, 20, 30, 50, 75, 100, 200, 500 e 1000.
- Para cada n, 10 listas aleatórias diferentes (inteiros de 0 a 1.000.000, semente 2026). A
  mesma lista é dada aos três métodos (inserção, intercalação e `sorted()`), então eles são
  comparados sobre exatamente os mesmos dados.
- Tempo: `time.perf_counter()` em volta de uma chamada de ordenação. A tabela mostra a média das
  10 repetições.
- Comparações: cada valor é embrulhado num objeto cujo `__lt__` conta as chamadas (ver
  `ordenacao.py`). A tabela mostra a média das 10 repetições.
- Os números brutos (uma linha por medição) estão em [dados.csv](dados.csv). Para refazer tudo:
  `python medir.py`.

Os tempos abaixo são da máquina em que o CSV foi gerado (Windows 10, Python 3.14). Em outra
máquina os valores absolutos mudam, mas o formato das curvas e a ordem de grandeza da virada se
mantêm.

## Tempos

Tempo médio por ordenação, em microssegundos (µs):

| n | Inserção | Intercalação | sorted() |
|---:|---:|---:|---:|
| 5 | 1,2 | 3,2 | 0,4 |
| 10 | 2,1 | 6,0 | 0,5 |
| 20 | 6,1 | 13,2 | 1,0 |
| 30 | 12,6 | 21,8 | 1,5 |
| 50 | 34,8 | 38,5 | 2,4 |
| 75 | 71,0 | 61,7 | 4,0 |
| 100 | 126,8 | 84,1 | 6,2 |
| 200 | 502,0 | 206,8 | 12,8 |
| 500 | 3.029,7 | 490,2 | 37,4 |
| 1000 | 12.436,6 | 1.070,0 | 74,6 |

![Tempo médio de ordenação](grafico_tempos.png)

Os dois eixos estão em escala logarítmica. Nessa escala uma curva n² vira uma reta de inclinação
2 e uma curva n log n vira uma reta de inclinação pouco acima de 1. É o que se vê: a reta da
inserção é bem mais inclinada que a da intercalação. De n = 500 para n = 1000 (n dobra), o tempo
da inserção multiplica por 4,1 e o da intercalação por 2,2.

## Comparações

Número médio de comparações entre elementos:

| n | Inserção | Intercalação | sorted() | n·log₂(n) |
|---:|---:|---:|---:|---:|
| 5 | 7,5 | 7,1 | 8,7 | 11,6 |
| 10 | 29,6 | 22,6 | 24,9 | 33,2 |
| 20 | 106,0 | 61,8 | 63,6 | 86,4 |
| 30 | 240,4 | 110,3 | 111,6 | 147,2 |
| 50 | 677,4 | 219,9 | 218,6 | 282,2 |
| 75 | 1.427,9 | 375,5 | 374,6 | 467,2 |
| 100 | 2.527,4 | 543,7 | 537,2 | 664,4 |
| 200 | 10.152,9 | 1.283,2 | 1.275,5 | 1.528,8 |
| 500 | 62.481,3 | 3.855,6 | 3.824,9 | 4.482,9 |
| 1000 | 250.467,5 | 8.706,5 | 8.652,8 | 9.965,8 |

![Número de comparações](grafico_comparacoes.png)

As medições batem com a teoria:

- **Inserção**: numa lista aleatória, cada elemento anda em média metade do caminho até o
  início, o que dá cerca de n²/4 comparações. A razão entre o medido e n²/4 vai de 1,20 em n = 5
  para 1,00 a partir de n = 500 (para n pequeno pesa a parcela linear, que n²/4 ignora).
- **Intercalação**: sempre abaixo de n·log₂(n) (de 61% do valor em n = 5 a 87% em n = 1000) e
  quase sem variação entre listas diferentes. Em n = 1000, as 10 listas deram entre 8.682 e
  8.752 comparações, enquanto a inserção variou entre 239.533 e 260.820.

## Em que n a intercalação passa a ser mais rápida

**Em tempo, a intercalação passa a ser mais rápida a partir de n = 75.** Em n = 50 a inserção
ainda ganha por pouco (34,8 µs contra 38,5 µs); em n = 75 a intercalação já ganha (61,7 µs contra
71,0 µs) e não perde mais em nenhum n maior. Como só medimos esses tamanhos, o cruzamento real
fica em algum ponto entre 50 e 75. Pela proximidade dos valores em n = 50, ele está mais perto
de 50, e pode andar um pouco em outra máquina ou outra execução.

Para n pequeno a inserção chega a ser 2,8 vezes mais rápida (n = 5 e 10). Em n = 1000 a
intercalação é 11,6 vezes mais rápida.

## O gráfico de comparações e o de tempo dão o mesmo ponto de virada?

**Não.** Em comparações, a intercalação já faz menos (ou praticamente o mesmo número) desde
n = 5: 7,1 contra 7,5. Em n = 10 a diferença já é clara (22,6 contra 29,6) e em n = 30 a
inserção faz mais que o dobro. Em tempo, a intercalação só ganha a partir de n = 75.

O motivo é que o número de comparações não é o único custo. O tempo é, aproximadamente,
*comparações × custo de cada uma + todo o resto*, e o "resto" é muito maior na intercalação:

- **Chamadas recursivas.** A intercalação faz cerca de 2n chamadas de função. Em Python cada
  chamada é cara (cria um quadro de execução novo). A inserção é só dois laços dentro de uma
  única chamada.
- **Listas novas e cópias.** Cada nível da recursão fatia a lista (`lista[:meio]`,
  `lista[meio:]`) e monta uma lista nova no `_intercalar` com `append`. São alocações e cópias de
  memória que a inserção, que trabalha numa única lista, não faz.
- **Laço mais pesado por comparação.** No `_intercalar` cada passo do laço testa
  `i < len(esquerda) and j < len(direita)`, compara, faz `append` e incrementa um índice. Na
  inserção cada passo é uma comparação e uma cópia de posição.

Esse custo fixo por elemento é o "fator constante" que a notação O esconde. Com n pequeno,
n² e n log n são números próximos (em n = 10, 100 contra 33) e o fator constante decide; com n
grande, a diferença de crescimento domina e o fator constante deixa de importar. Por isso a
virada em tempo acontece depois da virada em comparações. A contagem de comparações mede o
algoritmo; o tempo mede o algoritmo *mais* a implementação.

## Por que a comparação com sorted() não serve para decidir entre os dois algoritmos

O `sorted()` é de 3 a 16 vezes mais rápido que o melhor dos nossos métodos em todos os tamanhos,
mas isso não diz nada sobre qual dos dois algoritmos é melhor, por três motivos:

1. **É outro algoritmo.** O `sorted()` usa o Timsort (Powersort, nas versões recentes), um
   híbrido que procura trechos já ordenados na lista, ordena trechos pequenos com inserção
   binária e depois intercala esses trechos com "galope". Não é nenhum dos dois que estamos
   comparando, então ele não pode desempatar entre eles.
2. **É escrito em C.** Nossos métodos rodam no interpretador do Python, onde cada operação
   (somar índice, acessar posição, chamar função) passa pelo interpretador. O `sorted()` roda
   como código de máquina compilado. A diferença de tempo vem principalmente da linguagem de
   implementação, não da ideia do algoritmo. Prova disso: em comparações o `sorted()` fica
   praticamente empatado com a nossa intercalação (8.652,8 contra 8.706,5 em n = 1000), mas em
   tempo é 14 vezes mais rápido.
3. **Ele ganha dos dois por igual.** Como fica abaixo das duas curvas em todos os n, colocá-lo
   como referência não muda a ordem entre inserção e intercalação nem o ponto de virada entre
   elas. Para decidir entre dois algoritmos, os dois precisam estar implementados nas mesmas
   condições (mesma linguagem, mesmo estilo de código), e é a comparação entre eles que importa.

O que a comparação com o `sorted()` mostra é outra coisa: na prática, em Python, para ordenar
uma lista use o `sorted()` (ou `list.sort()`), e não uma implementação própria.

## Um caso em que a inserção ainda é a escolha adequada

**Listas pequenas, e principalmente listas quase ordenadas.**

- Nas medições, para n até cerca de 50 a inserção é mais rápida que a intercalação, chegando a
  2,8 vezes em n = 5 e 10. Para ordenar muitas listas pequenas (por exemplo, os poucos itens de
  cada pedido, ou as 5 melhores notas de cada aluno), a inserção é a melhor das duas.
- Numa lista já ordenada a inserção faz só n − 1 comparações (o teste
  `test_insercao_em_lista_ordenada_faz_n_menos_1` confere isso), enquanto a intercalação faz as
  suas ~n log n de qualquer jeito. De forma geral, a inserção custa proporcionalmente a
  n + (número de pares fora de ordem). Se dados chegam quase em ordem (registros com data e hora
  que chegam com pequenos atrasos, ou uma lista ordenada onde se acrescentam alguns itens no
  fim), a inserção é linear na prática.
- Ela também ordena no lugar, sem memória extra, e é estável.

Não por acaso, é o que os algoritmos híbridos fazem: o próprio Timsort usado pelo `sorted()`
ordena os trechos pequenos (até algumas dezenas de elementos) com inserção e só usa intercalação
para juntar esses trechos. É exatamente a conclusão das nossas medições: inserção para o pequeno,
intercalação para o grande.

## Extra: comparações do sorted() e o limite de n log n

As comparações do `sorted()` foram contadas com a mesma classe que conta as chamadas de `__lt__`
(coluna `sorted()` da tabela de comparações). Pela teoria vista em aula, qualquer ordenação por
comparação precisa, no pior caso, de pelo menos log₂(n!) comparações, que é aproximadamente
n·log₂(n) − 1,44·n. A tabela compara o medido com os dois valores:

| n | sorted() (média) | n·log₂(n) | sorted() / n·log₂(n) | log₂(n!) |
|---:|---:|---:|---:|---:|
| 5 | 8,7 | 11,6 | 0,75 | 6,9 |
| 10 | 24,9 | 33,2 | 0,75 | 21,8 |
| 20 | 63,6 | 86,4 | 0,74 | 61,1 |
| 30 | 111,6 | 147,2 | 0,76 | 107,7 |
| 50 | 218,6 | 282,2 | 0,77 | 214,2 |
| 75 | 374,6 | 467,2 | 0,80 | 363,4 |
| 100 | 537,2 | 664,4 | 0,81 | 524,8 |
| 200 | 1.275,5 | 1.528,8 | 0,83 | 1.245,4 |
| 500 | 3.824,9 | 4.482,9 | 0,85 | 3.767,4 |
| 1000 | 8.652,8 | 9.965,8 | 0,87 | 8.529,4 |

O que se vê:

- O `sorted()` sempre fica **abaixo de n·log₂(n)** (entre 74% e 87% do valor). Isso não
  contradiz a teoria: n·log₂(n) é a ordem de grandeza do limite, não o valor exato. O limite
  exato é log₂(n!), que é menor que n·log₂(n) pela parcela −1,44·n. Essa parcela pesa mais com n
  pequeno, por isso a razão cresce com n e tende a 1 bem devagar.
- Ele fica **logo acima de log₂(n!)**, que é o mínimo teórico: apenas 1,4% acima em n = 1000 e
  2,4% em n = 100. Ou seja, numa lista aleatória o `sorted()` está praticamente no limite do que
  qualquer algoritmo baseado em comparação consegue.
- Em n = 5 o `sorted()` faz mais comparações que os nossos dois métodos (8,7 contra 7,5 e 7,1).
  Com tão poucos elementos, as comparações que ele gasta procurando trechos já ordenados na lista
  não se pagam. Esse trabalho extra é o que o torna muito rápido em listas parcialmente
  ordenadas, mas numa lista pequena e aleatória é custo puro.
- A nossa intercalação faz praticamente o mesmo número de comparações que o `sorted()` (diferença
  de no máximo 1,2% de n = 50 em diante) e também fica abaixo de n·log₂(n). A diferença de tempo entre
  eles, de 14 vezes, vem toda da implementação, o que reforça a seção anterior.
