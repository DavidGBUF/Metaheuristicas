import random
import copy

# Matriz de custo Empresa x Projeto
matriz_custo = [
    [12, 18, 15, 22, 9, 14, 20, 11, 17],
    [19, 8, 13, 25, 16, 10, 7, 21, 24],
    [6, 14, 27, 10, 12, 19, 23, 16, 8],
    [17, 11, 20, 9, 18, 13, 25, 14, 22],
    [10, 23, 16, 14, 7, 21, 12, 19, 15],
    [13, 25, 9, 17, 11, 8, 16, 22, 20],
    [21, 16, 24, 12, 20, 15, 9, 18, 10],
    [8, 19, 11, 16, 22, 17, 14, 10, 13],
    [15, 10, 18, 21, 13, 12, 22, 9, 16]
]

num_empresas = len(matriz_custo)
num_projetos = len(matriz_custo[0])

# Função para gerar uma solução inicial (matriz de 0s)
def gerar_solucao_inicial():
    solucao = [[0]*num_projetos for _ in range(num_empresas)]  # Empresas x Projetos
    return solucao

# Função para gerar vizinhos de uma solução, respeitando a alocação dos projetos
def gerar_vizinhos(solucao, empresa, projetos_alocados):
    vizinhos = []
    for projeto in range(num_projetos):
        if projeto in projetos_alocados:  # Verifica se o projeto já foi alocado
            continue
        # Cria uma cópia da solução e aloca o projeto para a empresa
        vizinho = copy.deepcopy(solucao)
        vizinho[empresa][projeto] = 1
        vizinhos.append(vizinho)
    
    return vizinhos

# Função para calcular o custo de uma solução
def calcular_custo(solucao):
    total_cost = 0
    for i in range(num_empresas):
        for j in range(num_projetos):
            total_cost += solucao[i][j] * matriz_custo[i][j]
    return total_cost

def busca_local():
    solucao = gerar_solucao_inicial()  
    projetos_alocados = set() 
    for empresa in range(num_empresas):
        
        vizinhos = gerar_vizinhos(solucao, empresa, projetos_alocados)
       
        solucao = min(vizinhos, key=calcular_custo, default=None)
    
        for projeto in range(num_projetos):
            if solucao[empresa][projeto] == 1:
                projetos_alocados.add(projeto)
                break 
    
    return solucao, calcular_custo(solucao)

# Executar a busca local
best_solution, best_cost = busca_local()
print("Melhor solução encontrada:")
for empresa in best_solution:
    print(empresa)
print("Custo total:", best_cost)
