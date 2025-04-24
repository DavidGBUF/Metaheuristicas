from random import randint, sample, uniform

# Definição do problema da mochila
PESO_MAXIMO = 6404180
TAM_MOCHILA = 24
TAM_POPULACAO = 100
lista_valores = [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902492, 1849296, 1049289, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261]
lista_pesos = [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823069, 909359, 853665, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]

taxa_aleatorio = 0.05

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


def selecao_torneio(populacao):
    solucoes_escolhidas = sample(populacao, 2)
    solucoes_escolhidas = sorted(solucoes_escolhidas, 
                                 key=lambda x: calcular_valor_total(x, lista_valores), 
                                 reverse=True)
    return solucoes_escolhidas[:2]

def mutacao(filho):
    index = randint(0, len(filho)-1)
    filho[index] = 1 - filho[index]
    return filho

def cruzamento(pai_e_mae):
    """
    Realiza o cruzamento entre dois indivíduos para gerar um filho.
    """
    filho = []
    for i in range(len(pai_e_mae[0])):
        sorteio = randint(0, 1)
        filho.append(pai_e_mae[sorteio][i])
    return filho
def solucao_valida(solucao, lista_pesos):
    """
    Verifica se a solução proposta é válida, ou seja, se o peso total não excede
    o peso máximo da mochila.
    """
    peso_acumulado = sum(peso for i, peso in enumerate(lista_pesos) if solucao[i])
    return peso_acumulado <= PESO_MAXIMO

def gerar_solucao_aleatoria(lista_pesos):
     while True:
        solucao_proposta = [randint(0, 1) for _ in range(TAM_MOCHILA)]
        if solucao_valida(solucao_proposta, lista_pesos):
            return solucao_proposta
        
populacao = [gerar_solucao_aleatoria(lista_pesos) for i in range(20)]
populacao = sorted(populacao, key=lambda x: calcular_valor_total(x, lista_valores), reverse=True)

for i in range(1000):
    nova_populacao = [populacao[0]]
    while True:
        pai_e_mae = selecao_torneio(populacao)
        filho = cruzamento(pai_e_mae)
        if uniform(0, 1) <= taxa_aleatorio:
            filho = mutacao(filho)
        if(solucao_valida(filho, lista_pesos)):
            nova_populacao.append(filho)
        if len(nova_populacao) >= TAM_POPULACAO:
            break
    populacao = nova_populacao
    populacao = sorted(populacao, key=lambda x: calcular_valor_total(x, lista_valores), reverse=True)



populacao = sorted(populacao, key=lambda x: calcular_valor_total(x, lista_valores), reverse=True)

# Exibindo o resultado
print(f"Solução Encontrada: {populacao[0]}")
print(f"Valor na mochila: {calcular_valor_total(populacao[0], lista_valores)}")
print(f"Peso Máximo: {PESO_MAXIMO} || Peso na mochila: {calcular_peso_total(populacao[0], lista_pesos)}")


