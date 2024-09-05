import random
from collections import deque

a = 1664525
c = 1013904223
M = 2**32
seed = 123456789

# último número gerado
previous = seed

count = 100000

K = 5  # capacidade da fila
num_servidores = 2  # altere para 1 no caso de G/G/1/5

TIPO_CHEGADA = 1
TIPO_SAIDA = 2

fila = deque()

tempo_atual = 0

proximo_tempo_chegada = 2.0  # primeiro cliente chega no tempo 2.0
proximos_tempos_saida = [float('inf')] * num_servidores 

tempo_global = 0

tempos_acumulados = [0] * (K + 1)

clientes_perdidos = 0

# pseudoaleatórios
def NextRandom():
    global previous
    previous = (a * previous + c) % M
    return previous / M

# intervalo de tempo de chegada e atendimento
def gerar_tempo_chegada():
    return 2 + NextRandom() * 3  

def gerar_tempo_atendimento():
    return 3 + NextRandom() * 2  

def atualizar_tempos_acumulados():
    global tempo_atual, tempo_global

    delta_tempo = tempo_atual - tempo_global
    num_clientes = len(fila)
    
    num_clientes = min(num_clientes, K)
    
    tempos_acumulados[num_clientes] += delta_tempo
    
    tempo_global = tempo_atual

def CHEGADA():
    global proximo_tempo_chegada, clientes_perdidos

    atualizar_tempos_acumulados()

    if len(fila) < K:
        fila.append(tempo_atual)
        print(f"Cliente chegou às {tempo_atual:.2f}")
        
        for i in range(num_servidores):
            if proximos_tempos_saida[i] == float('inf'):
                proximos_tempos_saida[i] = tempo_atual + gerar_tempo_atendimento()
                break
    else:
        clientes_perdidos += 1
        print(f"Cliente perdido às {tempo_atual:.2f}")

    proximo_tempo_chegada = tempo_atual + gerar_tempo_chegada()

def SAIDA():
    atualizar_tempos_acumulados()

    for i in range(num_servidores):
        if proximos_tempos_saida[i] == tempo_atual and fila:
            cliente = fila.popleft()
            print(f"Cliente atendido às {tempo_atual:.2f}, esperou {tempo_atual - cliente:.2f} unidades de tempo")
            
            if fila:
                proximos_tempos_saida[i] = tempo_atual + gerar_tempo_atendimento()
            else:
                proximos_tempos_saida[i] = float('inf')


def NextEvent():
    global tempo_atual
    prox_evento = min(proximo_tempo_chegada, *proximos_tempos_saida)
    tempo_atual = prox_evento

    if prox_evento == proximo_tempo_chegada:
        return TIPO_CHEGADA
    else:
        return TIPO_SAIDA

def main():
    global count

    while count > 0:
        evento = NextEvent()
        if evento == TIPO_CHEGADA:
            CHEGADA()
        else:
            SAIDA()
        count -= 1

    print("\nDistribuição de probabilidade dos estados da fila:")
    for i in range(K + 1):
        probabilidade = (tempos_acumulados[i] / tempo_global) * 100
        print(f"{i} clientes: {tempos_acumulados[i]:.2f} unidades de tempo ({probabilidade:.2f}%)")

    print(f"\nTotal de clientes perdidos: {clientes_perdidos}")
    print(f"Tempo global de simulação: {tempo_global:.2f}")

if __name__ == "__main__":
    main()

    
