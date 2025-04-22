from random import randint, randrange
import math

PESO_MAXIMO = 6404180
TAM_MOCHILA = 24
lista_valores = [6404180, 825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902492, 1849296, 1049289, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261]
lista_pesos = [382745, 382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823069, 909359, 853665, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]


# Função para validar se a solução é válida (não ultrapassa o peso máximo)
def solucao_valida(solucao_proposta, lista_pesos):
    peso_acumulado = 0
    for inserido, peso in zip(solucao_proposta, lista_pesos):
        if inserido:
            peso_acumulado += peso
        if peso_acumulado > PESO_MAXIMO:
            return False
    return True

# Função para retornar os índices dos dois maiores valores da lista
def indices_maiores_valores(lista):
    if len(lista) < 2:
        return None  
    maior_valor = max(lista)
    indice_maior = lista.index(maior_valor)
    
    lista_sem_maior = lista[:indice_maior] + lista[indice_maior+1:]
    segundo_maior_valor = max(lista_sem_maior)
    indice_segundo_maior = lista.index(segundo_maior_valor)
    
    return (indice_maior, indice_segundo_maior)

# Função que gera uma solução aleatória válida
def gerar_solucao_aleatoria():
    while True:
        solucao_proposta = [randint(0, 1) for _ in range(TAM_MOCHILA)]
        if solucao_valida(solucao_proposta, lista_pesos):
            return solucao_proposta

# Função para gerar um vizinho (solução ligeiramente alterada)
def gerar_vizinho(solucao):
    vizinho = solucao[:]
    indice_aleatorio = randrange(len(solucao))
    vizinho[indice_aleatorio] = 1 - vizinho[indice_aleatorio]  # Alterna entre 0 e 1
    if solucao_valida(vizinho, lista_pesos):
        return vizinho
    return solucao  # Retorna a solução original se o vizinho for inválido

# Função que calcula o valor total de uma solução
def valor_total(solucao, lista_valores):
    return sum(valor for i, valor in enumerate(lista_valores) if solucao[i])

# Função que calcula o peso total de uma solução
def peso_total(solucao, lista_pesos):
    return sum(peso for i, peso in enumerate(lista_pesos) if solucao[i])

# Função que encontra o índice da diferença entre duas soluções
def indice_diferente(solucao1, solucao2):
    for i in range(len(solucao1)):
        if solucao1[i] != solucao2[i]:
            return i

# Função para gerenciar a memória de médio prazo e memória tabu
def atualizar_memoria(memoria_tabu, memoria_medio_prazo, solucao, tabu_tamanho, tempo_memoria_medio):
    # Mover soluções tabu para a memória de médio prazo
    if len(memoria_tabu) > 0 and len(memoria_medio_prazo) < tempo_memoria_medio:
        memoria_medio_prazo.append(memoria_tabu.pop(0))

    if len(memoria_tabu) > tabu_tamanho:
        memoria_tabu.pop(0)

    return memoria_tabu, memoria_medio_prazo

# Execução principal
solucao = gerar_solucao_aleatoria()  # Solução inicial
melhor_solucao = solucao
melhor_valor = valor_total(solucao, lista_valores)

# Inicialização da memória Tabu e Memória de Médio Prazo
tabu_tamanho = 10  # Tamanho da memória Tabu
memoria_tabu = []  # Lista para armazenar soluções tabu
memoria_medio_prazo = []  # Lista para armazenar soluções de médio prazo
max_iteracoes = 1000  # Número máximo de iterações
iteracao_sem_melhora = 0  # Contador de iterações sem melhoria
tempo_memoria_medio = 5  # Tempo de "espera" para soluções na memória de médio prazo (em iterações)

# Busca Tabu com Memória de Médio Prazo
for iteracao in range(max_iteracoes):
    # Gera vizinhos e ordena do melhor para o pior
    vizinhos = [gerar_vizinho(solucao) for _ in range(10)]  # Gerando 10 vizinhos
    
    # Ordena os vizinhos pelo valor total (do melhor para o pior)
    vizinhos = sorted(vizinhos, key=lambda v: valor_total(v, lista_valores), reverse=True)
    
    # Se o melhor vizinho for melhor que a melhor solução encontrada, aplica a solução (Critério de Aspiração)
    if valor_total(vizinhos[0], lista_valores) > melhor_valor:
        melhor_solucao = vizinhos[0]
        melhor_valor = valor_total(vizinhos[0], lista_valores)
        iteracao_sem_melhora = 0  # Reinicia o contador de iterações sem melhoria
        solucao = melhor_solucao  # Assume o melhor vizinho como a nova solução
    else:
        iteracao_sem_melhora += 1
    
    # Para vizinhos ordenados, caso não estejam na lista tabu, atualiza a solução
    for vizinho in vizinhos:
        if not indice_diferente(vizinho, melhor_solucao) in memoria_tabu:
            solucao = vizinho
            memoria_tabu.append(indice_diferente(vizinho, melhor_solucao))
            break

    # Atualiza memória tabu e memória de médio prazo
    memoria_tabu, memoria_medio_prazo = atualizar_memoria(memoria_tabu, memoria_medio_prazo, solucao, tabu_tamanho, tempo_memoria_medio)
    
    # Caso tenha atingido iterações sem melhoria, parar
    if iteracao_sem_melhora > 10:
        iteracao_sem_melhora = 0
        solucao = [0, 0, 0, 0, 0]
        indices = indices_maiores_valores([0 for _ in range(len(solucao))])  # Usando uma lista de exemplo
        solucao[indices[0]], solucao[indices[1]] = 1, 1
        break

# Resultado final
print(f"Solução Encontrada: {melhor_solucao}")
print(f"Valor na mochila: {melhor_valor}")
print(f"Peso Máximo: {PESO_MAXIMO} || Peso na mochila: {peso_total(melhor_solucao, lista_pesos)}")
