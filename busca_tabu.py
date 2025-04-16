from random import randint, randrange, uniform
import math

# O problema que está sendo resolvido é o da mochila
PESO_MAXIMO = 10
TAM_MOCHILA = 5

lista_valores = [4, 6, 5, 3, 1]
lista_pesos = [5, 4 ,3, 2, 1]

# Função de validação da solução
def solucao_valida(solucao_proposta, lista_pesos):
    peso_acumulado = 0
    for inserido, peso in zip(solucao_proposta, lista_pesos):
        if inserido:
            peso_acumulado += peso
        if peso_acumulado > PESO_MAXIMO:
            return False
    return True

# Gera uma solução aleatória válida
def gerar_solucao_aleatoria():
    while True:
        solucao_proposta = [randint(0, 1) for _ in range(TAM_MOCHILA)]
        if solucao_valida(solucao_proposta, lista_pesos):
            return solucao_proposta

# Gera um vizinho (solução ligeiramente alterada)
def gerar_vizinho(solucao):
    vizinho = solucao[:]
    indice_aleatorio = randrange(len(solucao))
    vizinho[indice_aleatorio] = 1 - vizinho[indice_aleatorio]  # Alterna entre 0 e 1
    if solucao_valida(vizinho, lista_pesos):
        return vizinho
    return solucao  # Retorna a solução original se o vizinho for inválido

# Calcula o valor total de uma solução
def valor_total(solucao, lista_valores):
    return sum(valor for i, valor in enumerate(lista_valores) if solucao[i])

# Calcula o peso total de uma solução
def peso_total(solucao, lista_pesos):
    return sum(peso for i, peso in enumerate(lista_pesos) if solucao[i])

# Execução principal
solucao = gerar_solucao_aleatoria()  # Solução inicial
melhor_solucao = solucao
melhor_valor = valor_total(solucao, lista_valores)

# Inicialização da memória Tabu
tabu_tamanho = 10  # Tamanho da memória Tabu
memoria_tabu = []  # Lista para armazenar soluções tabu
max_iteracoes = 100  # Número máximo de iterações
iteracao_sem_melhora = 0  # Contador de iterações sem melhoria

# Busca Tabu
for iteracao in range(max_iteracoes):
    # Gera vizinhos e ordena do melhor para o pior
    vizinhos = []
    for _ in range(10):  # Gerando 10 vizinhos
        vizinhos.append(gerar_vizinho(solucao))
    
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
        if vizinho not in memoria_tabu:
            solucao = vizinho
            memoria_tabu.append(vizinho)
            if len(memoria_tabu) > tabu_tamanho:  # Limitar o tamanho da memória
                memoria_tabu.pop(0)  # Remove a solução mais antiga da memória
            break
    
    # Caso tenha atingido iterações sem melhoria, parar
    if iteracao_sem_melhora > 10:
        print(f"Parando busca após {iteracao_sem_melhora} iterações sem melhoria.")
        break

print(f"Solução Encontrada: {melhor_solucao}")
print(f"Valor na mochila: {melhor_valor}")
print(f"Peso Máximo: {PESO_MAXIMO} || Peso na mochila: {peso_total(melhor_solucao, lista_pesos)}")
