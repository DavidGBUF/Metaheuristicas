from random import randint, randrange, uniform
import math

# O problema que está sendo resolvido é o da mochila
PESO_MAXIMO = 10
TAM_MOCHILA = 5

lista_valores = [4, 6, 5, 3, 1]
lista_pesos = [5, 4 ,3, 2, 1]

def solucao_valida(solucao_proposta, lista_pesos):
    peso_acumulado = 0
    for inserido, peso in zip(solucao_proposta, lista_pesos):
        if inserido:
            peso_acumulado += peso
        if peso_acumulado > PESO_MAXIMO:
            return False
    return True

def gerar_solucao_aleatoria():
    while True:
        solucao_proposta = [randint(0, 1) for _ in range(TAM_MOCHILA)]
        if solucao_valida(solucao_proposta, lista_pesos):
            return solucao_proposta

def atualiza_temperatura(temperatura):
    return temperatura * 0.999  # Resfriamento mais suave

def gerar_vizinho(solucao):
    while True:
        vizinho = solucao[:]
        indice_aleatorio = randrange(len(solucao))
        vizinho[indice_aleatorio] = 1 - vizinho[indice_aleatorio]  # Alterna entre 0 e 1
        if solucao_valida(vizinho, lista_pesos):
            return vizinho

def valor_total(solucao, lista_valores):
    return sum(valor for i, valor in enumerate(lista_valores) if solucao[i])

def peso_total(solucao, lista_pesos):
    return sum(peso for i, peso in enumerate(lista_pesos) if solucao[i])

# Execução principal
print("Solução inicial válida:", gerar_solucao_aleatoria())

temperatura = 30000
temperatura_parada = temperatura * 0.0001
solucao = gerar_solucao_aleatoria()

while temperatura > temperatura_parada:
    for _ in range(10):  # Reduzido para 10 vizinhos
        vizinho = gerar_vizinho(solucao)
        delta_s = valor_total(vizinho, lista_valores) - valor_total(solucao, lista_valores)
        if delta_s > 0:
            solucao = vizinho
        else:
            probabilidade = math.exp(-delta_s / temperatura)
            if probabilidade > uniform(0, 1):
                solucao = vizinho
    temperatura = atualiza_temperatura(temperatura)

print(f"\nSolução Encontrada: {solucao}")
print(f"Valor na mochila: {valor_total(solucao, lista_valores)}")
print(f"Peso Máximo: {PESO_MAXIMO} || Peso na mochila: {peso_total(solucao, lista_pesos)}")
