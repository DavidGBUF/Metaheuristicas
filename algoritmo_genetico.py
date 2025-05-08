import numpy as np
from random import randint, sample, uniform

# Definição do problema da mochila
PESO_MAXIMO = 1550
TAM_MOCHILA = 100
TAM_POPULACAO = 200
taxa_aleatorio = 0.05

# Leitura do arquivo
file_path = 'knapsack-instance.txt'
lista_valores = []
lista_pesos = []

# Leitura do arquivo a partir da terceira linha
with open(file_path, 'r') as file:
    lines = file.readlines()[2:]
    for line in lines:
        left, right = map(int, line.split())
        lista_valores.append(left)
        lista_pesos.append(right)

# Funções do Algoritmo Genético
def calcular_valor_total(solucao):
    return sum(valor for i, valor in enumerate(lista_valores) if solucao[i])

def selecao_torneio(populacao):
    solucoes_escolhidas = sample(populacao, 2)
    solucoes_escolhidas.sort(key=lambda x: calcular_valor_total(x), reverse=True)
    return solucoes_escolhidas[:2]

def mutacao(filho):
    index = randint(0, len(filho)-1)
    filho[index] = 1 - filho[index]
    return filho

def cruzamento(pai_e_mae):
    return [pai_e_mae[randint(0, 1)][i] for i in range(len(pai_e_mae[0]))]

def solucao_valida(solucao):
    peso_acumulado = sum(peso for i, peso in enumerate(lista_pesos) if solucao[i])
    return peso_acumulado <= PESO_MAXIMO

def gerar_solucao_aleatoria():
    while True:
        solucao = [randint(0, 1) for _ in range(TAM_MOCHILA)]
        if solucao_valida(solucao):
            return solucao

# Execução do Algoritmo Genético
def algoritmo_genetico():
    populacao = [gerar_solucao_aleatoria() for _ in range(TAM_POPULACAO)]
    populacao.sort(key=lambda x: calcular_valor_total(x), reverse=True)

    for _ in range(100):
        nova_populacao = [populacao[0]]
        while len(nova_populacao) < TAM_POPULACAO:
            pai_e_mae = selecao_torneio(populacao)
            filho = cruzamento(pai_e_mae)
            if uniform(0, 1) <= taxa_aleatorio:
                filho = mutacao(filho)
            if solucao_valida(filho):
                nova_populacao.append(filho)
        populacao = sorted(nova_populacao, key=lambda x: calcular_valor_total(x), reverse=True)

    return calcular_valor_total(populacao[0])

# Executando 20 vezes e coletando os resultados
resultados = [algoritmo_genetico() for _ in range(20)]

# Calculando métricas
media = np.mean(resultados)
desvio_padrao = np.std(resultados)
melhor_valor = np.max(resultados)
pior_valor = np.min(resultados)

# Exibindo resultados
print("========== Resultados das 20 Execuções ==========")
print(f"Média dos valores obtidos: {media}")
print(f"Desvio padrão dos valores: {desvio_padrao}")
print(f"Melhor valor obtido: {melhor_valor}")
print(f"Pior valor obtido: {pior_valor}")
print("=================================================")
