# Comparação entre ordenação por inserção e por intercalação

Implementação da ordenação por inserção e da ordenação por intercalação (merge sort) em Python,
com medição de tempo e de número de comparações para listas aleatórias, e comparação com o
`sorted()` do Python. A análise dos resultados está em [RELATORIO.md](RELATORIO.md).

## Arquivos

| arquivo | o que é |
|---|---|
| `ordenacao.py` | os dois métodos (`insercao` e `intercalacao`) e o contador de comparações |
| `medir.py` | roda todas as medições e gera o CSV e os gráficos |
| `dados.csv` | os números brutos das medições (uma linha por medição) |
| `RELATORIO.md` | a análise |

## Requisitos

- Python 3.8 ou mais novo (testado no 3.14).
- `matplotlib`, só para desenhar os gráficos. O resto usa apenas a biblioteca padrão.

### O que é o `requirements.txt`

É a lista das bibliotecas externas que o projeto precisa e que não vêm junto com o Python. É um
arquivo de texto comum, com uma biblioteca por linha. Aqui ele tem uma linha só:

```
matplotlib
```

O comando `python -m pip install -r requirements.txt` lê esse arquivo e instala tudo o que está
nele (o `-r` quer dizer "ler a lista deste arquivo"). Dá no mesmo que rodar
`python -m pip install matplotlib`, mas com o arquivo quem baixa o projeto não precisa adivinhar
o que falta: basta um comando, e se um dia o projeto precisar de outra biblioteca, é só
acrescentar uma linha.

O `testes.py` não precisa de nada do `requirements.txt`. Só o `medir.py` usa o matplotlib, e
apenas na parte dos gráficos.

## Como rodar

Na pasta do projeto:

```bash
# 1. instalar a dependência (uma vez só)
python -m pip install -r requirements.txt

# 2. rodar os testes
python testes.py

# 3. refazer as medições, o CSV e os gráficos do zero
python medir.py
```

No Linux/macOS, troque `python` por `python3` se for o caso.

### O que `python medir.py` faz

1. Apaga `dados.csv`, `grafico_tempos.png` e `grafico_comparacoes.png`, se existirem.
2. Para cada n em 5, 10, 20, 30, 50, 75, 100, 200, 500 e 1000, gera 10 listas aleatórias
   (semente fixa 2026, valores de 0 a 1.000.000). Cada lista é ordenada pela inserção, pela
   intercalação e pelo `sorted()`, medindo o tempo (`time.perf_counter`) e contando as
   comparações.
3. Grava `dados.csv` com as colunas `metodo, n, repeticao, tempo_s, comparacoes`.
4. Imprime as tabelas de médias (já em Markdown) e o n em que a intercalação passa a ganhar.
5. Desenha os dois gráficos com eixos em escala logarítmica.

Leva poucos segundos. Os tempos dependem da máquina e mudam um pouco a cada execução; as
comparações são sempre as mesmas, porque as listas saem da mesma semente.

Se o matplotlib não estiver instalado, o `medir.py` grava o CSV mesmo assim e avisa para rodar o
`pip install -r requirements.txt`.

## Como as comparações são contadas

Os dois métodos comparam os elementos só com `<`. A função `contar_comparacoes` (em
`ordenacao.py`) embrulha cada valor num objeto `Comparavel`, cujo `__lt__` soma 1 num contador
antes de comparar. Como o `sorted()` também usa `<`, a mesma função conta as comparações dele.
