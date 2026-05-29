Avaliação de Desempenho — Algoritmos MVA

Implementação em Python dos algoritmos apresentados no Capítulo 6 para análise de modelos de filas multiclasses utilizando técnicas de Mean Value Analysis (MVA).

Objetivo

O projeto implementa os principais algoritmos de MVA estudados em sala:

MVA Exato para modelos fechados multiclasses
MVA Aproximado para modelos fechados multiclasses
MVA para modelos multiclasses mistos (classes abertas e fechadas)

Além disso, o projeto executa automaticamente os exercícios do Capítulo 6, imprimindo:

estados do MVA exato
iterações do MVA aproximado
resultados finais
comparações entre técnicas
Estrutura do Projeto
AvaliaçãoDesempenho/
│
├── main.py
├── mva_exato.py
├── mva_aproximado.py
├── mva_mixed_multiclass.py
├── output_utils.py
└── README.md
Arquivos
mva_exato.py

Implementa o algoritmo de MVA Exato para modelos fechados multiclasses.

Baseado no pseudocódigo da Figura 6.3 do Capítulo 6.

Função principal:

exact_mva(...)
mva_aproximado.py

Implementa o algoritmo de MVA Aproximado para modelos fechados multiclasses.

O algoritmo executa iterações sucessivas até atingir o critério de parada definido por epsilon.

Função principal:

approximate_mva_closed(...)
mva_mixed_multiclass.py

Implementa o algoritmo da Figura 6.9 do Capítulo 6 para modelos multiclasses mistos.

O modelo permite:

classes abertas (com λ)
classes fechadas (com N e Z)

Função principal:

mixed_multiclass_model(...)
output_utils.py

Responsável pela impressão dos resultados.

Funções:

print_final_result(...)
print_iteration_table(...)
print_all_states(...)
main.py

Executa automaticamente os exercícios implementados no trabalho.

Exercícios Implementados
Exercício 1

Sistema multiclasses fechado contendo:

classe Update
classe Query

São calculados:

MVA aproximado
MVA exato
comparação entre técnicas
esforço computacional
Exercício 2

Balanceamento de I/O da classe Query entre os discos D1 e D2.

São comparados:

modelo original
modelo balanceado
Exercício 3

Modelo multiclasses misto contendo:

classes abertas: Q e U
classe fechada interativa: I

São analisados:

situação original
aumento da taxa de chegada de Query
upgrade do disco D1
upgrade da CPU
variação do número de terminais
Como Executar
1. Clone o repositório
git clone https://github.com/WaldeneyForte/mva-exato.git
2. Entre na pasta
cd mva-exato
3. Execute o programa
python main.py
Saídas Geradas

O programa imprime:

estados do MVA exato
iterações do MVA aproximado
tempos de resposta
throughput
número médio de clientes
comparação entre algoritmos
Tecnologias Utilizadas
Python 3
Algoritmos de Mean Value Analysis (MVA)
Autor

Waldeney Forte

Projeto desenvolvido para a disciplina de Avaliação de Desempenho
