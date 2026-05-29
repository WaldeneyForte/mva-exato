# MVA Exato - Capítulo 6

Implementação em Python dos algoritmos apresentados no Capítulo 6 para análise de modelos de filas multiclasses utilizando técnicas de **Mean Value Analysis (MVA)**.

## 📋 Objetivo

Este projeto implementa os principais algoritmos de MVA estudados em sala:

- **MVA Exato** para modelos fechados multiclasses
- **MVA Aproximado** para modelos fechados multiclasses
- **MVA para modelos multiclasses mistos** (classes abertas e fechadas)

Além disso, o projeto executa automaticamente os exercícios do Capítulo 6, imprimindo:

- Estados do MVA exato
- Iterações do MVA aproximado
- Resultados finais
- Comparações entre técnicas

## 📁 Estrutura do Projeto

```
mva-exato/
├── main.py
├── mva_exato.py
├── mva_aproximado.py
├── mva_mixed_multiclass.py
├── output_utils.py
└── README.md
```

## 📄 Descrição dos Arquivos

### `mva_exato.py`
Implementa o algoritmo de **MVA Exato** para modelos fechados multiclasses.
- Baseado no pseudocódigo da Figura 6.3 do Capítulo 6
- **Função principal:** `exact_mva(...)`

### `mva_aproximado.py`
Implementa o algoritmo de **MVA Aproximado** para modelos fechados multiclasses.
- Executa iterações sucessivas até atingir o critério de parada definido por epsilon
- **Função principal:** `approximate_mva_closed(...)`

### `mva_mixed_multiclass.py`
Implementa o algoritmo da Figura 6.9 do Capítulo 6 para **modelos multiclasses mistos**.
- Permite classes abertas (com λ) e fechadas (com N e Z)
- **Função principal:** `mixed_multiclass_model(...)`

### `output_utils.py`
Responsável pela impressão dos resultados.
- **Funções:** `print_final_result()`, `print_iteration_table()`, `print_all_states()`

### `main.py`
Executa automaticamente os exercícios implementados no trabalho.

## 🎯 Exercícios Implementados

### Exercício 1
Sistema multiclasses fechado contendo:
- Classe Update
- Classe Query

Calcula:
- MVA aproximado
- MVA exato
- Comparação entre técnicas
- Esforço computacional

### Exercício 2
Balanceamento de I/O da classe Query entre os discos D1 e D2.

Compara:
- Modelo original
- Modelo balanceado

### Exercício 3
Modelo multiclasses misto contendo:
- Classes abertas: Q e U
- Classe fechada interativa: I

Analisa:
- Situação original
- Aumento da taxa de chegada de Query
- Upgrade do disco D1
- Upgrade da CPU
- Variação do número de terminais

## 🚀 Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/WaldeneyForte/mva-exato.git
```

### 2. Entre na pasta
```bash
cd mva-exato
```

### 3. Execute o programa
```bash
python main.py
```

## 📊 Saídas Geradas

O programa imprime:

- Estados do MVA exato
- Iterações do MVA aproximado
- Tempos de resposta
- Throughput
- Número médio de clientes
- Comparação entre algoritmos

## 🛠 Tecnologias Utilizadas

- **Python 3**
- **Algoritmos de Mean Value Analysis (MVA)**

## 👨‍💻 Autor

**Waldeney Forte**

Projeto desenvolvido para a disciplina de Avaliação de Desempenho
