from random import randint, randrange, uniform
import math

PESO_MAXIMO = 6404180
TAM_MOCHILA = 24
lista_valores = [6404180, 825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902492, 1849296, 1049289, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261]
lista_pesos = [382745, 382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823069, 909359, 853665, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]


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

# Ajustando a temperatura para um resfriamento mais controlado
temperatura = 300000
temperatura_parada = 0.0001 * temperatura  # Temperatura de parada mais alta
solucao = gerar_solucao_aleatoria()

while temperatura > temperatura_parada:
    for _ in range(10):  # Reduzido para 10 vizinhos
        vizinho = gerar_vizinho(solucao)
        delta_s = valor_total(vizinho, lista_valores) - valor_total(solucao, lista_valores)
        
        # Evita que delta_s se torne muito grande
        if delta_s > 0:
            solucao = vizinho
        else:
            probabilidade = math.exp(delta_s / temperatura)  # Usando a temperatura mais alta
            if probabilidade > uniform(0, 1):
                solucao = vizinho

    temperatura = atualiza_temperatura(temperatura)

print(f"\nSolução Encontrada: {solucao}")
print(f"Valor na mochila: {valor_total(solucao, lista_valores)}")
print(f"Peso Máximo: {PESO_MAXIMO} || Peso na mochila: {peso_total(solucao, lista_pesos)}")
