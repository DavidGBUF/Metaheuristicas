from random import randint, sample, uniform

# Definição do problema da mochila
PESO_MAXIMO = 6404180
TAM_MOCHILA = 24
NUM_TRILHAS = 100
lista_valores = [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902492, 1849296, 1049289, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261]
lista_pesos = [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823069, 909359, 853665, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]

ALFA = 1
BETA = 0.2
feromonio = [1] * TAM_MOCHILA
def solucao_valida(solucao, lista_pesos):
    """
    Verifica se a solução proposta é válida, ou seja, se o peso total não excede
    o peso máximo da mochila.
    """
    peso_acumulado = sum(peso for i, peso in enumerate(lista_pesos) if solucao[i])
    return peso_acumulado <= PESO_MAXIMO

def calcular_valor_total(solucao, lista_valores):
    """
    Calcula o valor total da solução, somando os valores dos itens
    presentes na solução (onde o item tem valor 1).
    """
    return sum(valor for i, valor in enumerate(lista_valores) if solucao[i])

def calcular_peso_total(solucao, lista_pesos):
    """
    Calcula o peso total da solução, somando os pesos dos itens
    presentes na solução (onde o item tem valor 1).
    """
    return sum(peso for i, peso in enumerate(lista_pesos) if solucao[i])

def gerar_lista_componentes(solucao_atual):
    lista_componentes = []
    for index, item in enumerate(solucao_atual):
        if item == 0:
            aux = solucao_atual[:]
            aux[index] = 1
            if solucao_valida(aux, lista_pesos):
                lista_componentes.append(index)
    return lista_componentes

def gerar_solucao_aleatoria(lista_pesos):
     while True:
        solucao_proposta = [randint(0, 1) for _ in range(TAM_MOCHILA)]
        if solucao_valida(solucao_proposta, lista_pesos):
            return solucao_proposta
        
def selecionar_componente(lista_componente, feromonios):
    visibilidade = [lista_valores[i] for i in lista_componentes]
    total_feromonio = sum([feromonio[i]**ALFA * visibilidade[i]**BETA for i in lista_componente])

    probabilidade = []
    for i in lista_componente:
        probabilidade_item = (feromonio[i]**ALFA) *(visibilidade[i]**BETA )/total_feromonio
        probabilidade.append(probabilidade_item)

solucao = gerar_solucao_aleatoria(lista_pesos)
lista_componentes = gerar_lista_componentes(solucao)

