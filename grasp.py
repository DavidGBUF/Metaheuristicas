import random

# Definição do problema da mochila
PESO_MAXIMO = 6404180
TAM_MOCHILA = 24
lista_valores = [6404180, 825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902492, 1849296, 1049289, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261]
lista_pesos = [382745, 382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823069, 909359, 853665, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]

# Função para calcular o valor total de uma solução
def calcular_valor_total(solucao, lista_valores):
    """
    Calcula o valor total da solução, somando os valores dos itens
    presentes na solução (onde o item tem valor 1).
    """
    return sum(valor for i, valor in enumerate(lista_valores) if solucao[i])

# Função para calcular o peso total de uma solução
def calcular_peso_total(solucao, lista_pesos):
    """
    Calcula o peso total da solução, somando os pesos dos itens
    presentes na solução (onde o item tem valor 1).
    """
    return sum(peso for i, peso in enumerate(lista_pesos) if solucao[i])

# Função para verificar se uma solução é válida (não excede o peso máximo)
def solucao_valida(solucao, lista_pesos):
    """
    Verifica se a solução proposta é válida, ou seja, se o peso total não excede
    o peso máximo da mochila.
    """
    peso_acumulado = sum(peso for i, peso in enumerate(lista_pesos) if solucao[i])
    return peso_acumulado <= PESO_MAXIMO

# Função GRASP para resolver o problema da mochila
def grasp(lista_valores, lista_pesos, peso_maximo, max_iteracoes=10000):
    """
    Implementa a metaheurística GRASP para o problema da mochila.
    Retorna a melhor solução e seu valor.
    """
    melhor_solucao = None
    melhor_valor = 0

    for iteracao in range(max_iteracoes):
        # Construção da solução com uma estratégia gulosa aleatória
        solucao = [0] * len(lista_valores)  # Solução inicial (nenhum item incluído)
        
        # Criação de candidatos (valor, índice) para a construção da solução
        candidatos = [(valor, i) for i, valor in enumerate(lista_valores)]
        candidatos = sorted(candidatos, key=lambda x: x[0], reverse=True)  # Ordenação decrescente pelo valor

        while True:
            # Geração de uma solução parcialmente aleatória
            indice_poda = random.randint(1, len(candidatos))  # Limita o número de candidatos a considerar
            lista_restrita = candidatos[:indice_poda]  # Restringe os candidatos
            elemento = random.choice(lista_restrita)  # Escolhe aleatoriamente um candidato restrito
            
            # Cria uma nova solução com o item escolhido
            teste = solucao[:]
            teste[elemento[1]] = 1  # Inclui o item na solução

            # Se a solução for inválida (excede o peso máximo), sai do loop
            if not solucao_valida(teste, lista_pesos):
                break
            solucao = teste  # Caso contrário, aceita a nova solução

        # Busca local: Tentativa de melhoria da solução inicial
        for i in range(len(solucao)):
            vizinho = solucao[:]  # Copia da solução
            vizinho[i] = 1 - vizinho[i]  # Alterna entre incluir ou não o item na solução
            if solucao_valida(vizinho, lista_pesos) and calcular_valor_total(vizinho, lista_valores) > calcular_valor_total(solucao, lista_valores):
                solucao = vizinho  # Atualiza a solução se o valor aumentar

        # Se encontrar uma solução melhor, atualiza a melhor solução
        valor_solucao = calcular_valor_total(solucao, lista_valores)
        if valor_solucao > melhor_valor:
            melhor_solucao = solucao
            melhor_valor = valor_solucao
    
    return melhor_solucao, melhor_valor

# Executando o GRASP para o problema da mochila
melhor_solucao, melhor_valor = grasp(lista_valores, lista_pesos, PESO_MAXIMO)

# Exibindo o resultado
print(f"Solução Encontrada: {melhor_solucao}")
print(f"Valor na mochila: {melhor_valor}")
print(f"Peso Máximo: {PESO_MAXIMO} || Peso na mochila: {calcular_peso_total(melhor_solucao, lista_pesos)}")
