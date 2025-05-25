import numpy as np
from random import randint, sample, uniform
import matplotlib.pyplot as plt
import os

# =======================
# Parâmetros do problema
# =======================
PESO_MAXIMO   = 1550
TAM_MOCHILA   = 100
TAM_POPULACAO = 200
TAXA_MUTACAO  = 0.05

N_GERACOES    = 100         # número de gerações por execução
N_EXECUCOES   = 20          # quantas vezes rodar o GA
VERBOSE       = False        # imprime estatísticas a cada geração?

# =======================
# Leitura do arquivo
# =======================
file_path      = 'knapsack-instance.txt'
lista_valores  = []
lista_pesos    = []

with open(file_path, 'r') as file:
    lines = file.readlines()[2:]          # ignora duas primeiras linhas
    for line in lines:
        v, p = map(int, line.split())
        lista_valores.append(v)
        lista_pesos.append(p)

# ================================================================
# Gravação da saida no terminal
# # ================================================================
import sys, os

log_path = "saida_execucoes.txt"          # nome do arquivo‐log
log_file = open(log_path, "w", buffering=1, encoding="utf-8")  # buffer=1 → flush automático

class Tee:                                # grava no arquivo e continua mostrando na tela
    def __init__(self, *streams):
        self.streams = streams
    def write(self, data):
        for s in self.streams:
            s.write(data)
    def flush(self):
        for s in self.streams:
            s.flush()

orig_stdout = sys.stdout                  # guarda o stdout original
sys.stdout   = Tee(orig_stdout, log_file) # duplica a saída
# ----------------------------------------------------------------

# =======================
# Funções auxiliares
# =======================
def calcular_valor_total(sol):
    return sum(v for i, v in enumerate(lista_valores) if sol[i])

def calcular_peso_total(sol):
    return sum(p for i, p in enumerate(lista_pesos) if sol[i])

def solucao_valida(sol):
    return calcular_peso_total(sol) <= PESO_MAXIMO

def gerar_solucao_aleatoria():
    while True:
        sol = [randint(0, 1) for _ in range(TAM_MOCHILA)]
        if solucao_valida(sol):
            return sol

def selecao_torneio(pop):
    candidatos = sample(pop, 5)
    return sorted(candidatos, key=calcular_valor_total, reverse=True)[:2]

def cruzamento(pais):
    return [pais[randint(0, 1)][i] for i in range(TAM_MOCHILA)]

def mutacao(filho):
    idx = randint(0, TAM_MOCHILA - 1)
    filho[idx] = 1 - filho[idx]
    return filho

# =======================
# Algoritmo genético
# =======================
def algoritmo_genetico():
    pop = [gerar_solucao_aleatoria() for _ in range(TAM_POPULACAO)]
    pop.sort(key=calcular_valor_total, reverse=True)

    historico_best = []
    historico_avg  = []

    for gen in range(N_GERACOES):
        nova_pop = [pop[0]]                       # elitismo
        while len(nova_pop) < TAM_POPULACAO:
            pais   = selecao_torneio(pop)
            filho  = cruzamento(pais)
            if uniform(0, 1) < TAXA_MUTACAO:
                filho = mutacao(filho)
            if solucao_valida(filho):
                nova_pop.append(filho)

        pop = sorted(nova_pop, key=calcular_valor_total, reverse=True)

        # métricas da geração
        valores = [calcular_valor_total(s) for s in pop]
        best    = valores[0]
        avg     = np.mean(valores)
        historico_best.append(best)
        historico_avg.append(avg)

        if VERBOSE:
            print(f"Geração {gen+1:3d}:  melhor = {best:5d}  "
                  f"média = {avg:7.2f}")

    melhor_solucao = pop[0]
    return {
        'melhor_valor'   : calcular_valor_total(melhor_solucao),
        'peso'           : calcular_peso_total(melhor_solucao),
        'solucao'        : melhor_solucao,
        'historico_best' : historico_best,
        'historico_avg'  : historico_avg
    }

# =======================
# Execuções múltiplas
# =======================
resultados_valor = []
historicos_exec  = []          # guarda histórico da melhor fitness de cada execução

for run in range(1, N_EXECUCOES + 1):
    print(f"\n========== Execução {run}/{N_EXECUCOES} ==========")
    resultado = algoritmo_genetico()
    resultados_valor.append(resultado['melhor_valor'])
    historicos_exec.append(resultado['historico_best'])

    print(f">>> Melhor valor: {resultado['melhor_valor']}  "
          f"(peso = {resultado['peso']})")

# =======================
# Estatísticas finais
# =======================
media         = np.mean(resultados_valor)
desvio_padrao = np.std(resultados_valor)
melhor_valor  = np.max(resultados_valor)
pior_valor    = np.min(resultados_valor)

print("\n========== Resumo das execuções ==========")
print(f"Média dos valores obtidos : {media:.2f}")
print(f"Desvio padrão dos valores : {desvio_padrao:.2f}")
print(f"Melhor valor obtido       : {melhor_valor}")
print(f"Pior valor obtido         : {pior_valor}")
print("==========================================")

# =======================
# Gráficos
# =======================
os.makedirs('figs', exist_ok=True)

# 1) Boxplot dos melhores valores de cada execução
plt.figure(figsize=(8, 4))
plt.boxplot(resultados_valor, vert=False, patch_artist=True,
            boxprops=dict(facecolor='lightblue', color='black'))
plt.title("Distribuição dos melhores valores (20 execuções)")
plt.xlabel("Valor da função objetivo")
plt.grid(True, axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('figs/boxplot_valores.png')
plt.show()

# 2) Evolução do melhor fitness ao longo das gerações (média)
media_best_por_gen = np.mean(historicos_exec, axis=0)
plt.figure(figsize=(8, 4))
plt.plot(range(1, N_GERACOES + 1), media_best_por_gen, linewidth=2)
plt.title("Média da melhor aptidão por geração (20 execuções)")
plt.xlabel("Geração")
plt.ylabel("Melhor valor médio")
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('figs/evolucao_melhor_fitness.png')
plt.show()


sys.stdout.flush()   # garante que tudo foi escrito
log_file.close()     # fecha o arquivo‐log
sys.stdout = orig_stdout  # restaura o stdout padrão
