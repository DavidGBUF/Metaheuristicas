import random
import copy

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

def gerar_solucao_aleatoria():
    solucao = []
    lista_projetos_livres = [0,1,2,3,4,5,6,7,8]
    for i in range(9):
        empresa = [0,0,0,0,0,0,0,0,0]
        projeto = random.choice(lista_projetos_livres)
        empresa[projeto] = 1
        lista_projetos_livres.pop(lista_projetos_livres.index(projeto))
        solucao.append(empresa)
    return solucao

def trocar_posicoes(lista_maior, index1, index2):
    if index1 < len(lista_maior) and index2 < len(lista_maior):
        lista_maior[index1], lista_maior[index2] = lista_maior[index2], lista_maior[index1]
    return lista_maior

def gerar_vizinhos(solucao):
    vizinhos = []
    for i in range(9):
        for j in range(i + 1, 9):  
            vizinho = copy.deepcopy(solucao)
            vizinho = trocar_posicoes(vizinho, i, j)  
            vizinhos.append(vizinho)
    return vizinhos

def avaliar_solucao(solucao):
    custo_total = 0
    for i in range(num_empresas):
        for j in range(num_projetos):
            if solucao[i][j] == 1:
                custo_total += matriz_custo[i][j]  
    return custo_total

def busca_local():
    solucao = gerar_solucao_aleatoria()
    while True:
        vizinhos = gerar_vizinhos(solucao)
        vizinhos = sorted(vizinhos, key=avaliar_solucao)
        if avaliar_solucao(solucao) > avaliar_solucao(vizinhos[0]):
            solucao = vizinhos[0]
        else:
            break
    return solucao, avaliar_solucao(solucao)

solucao = gerar_solucao_aleatoria()
print(f"Solução Original: ")
for i in solucao:
    print(i)

print("Custo total:", avaliar_solucao(solucao))

melhor_solucao, melhor_custo = busca_local()

print(f"Solução Heurística: ")
for i in melhor_solucao:
    print(i)

print("Custo total:", melhor_custo)
