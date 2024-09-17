import random
from collections import deque

# constantes para o gerador de números aleatórios
a = 1664525
c = 1013904223
M = 2**32
seed = 123456789

previous = seed

count = 100000  # número de eventos a serem simulados

K1 = 3  # capacidade da Fila 1
K2 = 5  # capacidade da Fila 2
num_servidores1 = 2  # número de servidores na Fila 1
num_servidores2 = 1  # número de servidores na Fila 2

TIPO_CHEGADA = 1
TIPO_SAIDA_FILA1 = 2
TIPO_SAIDA_FILA2 = 3

fila1 = deque()
fila2 = deque()

tempo_atual = 0
proximo_tempo_chegada = 1.5 
proximos_tempos_saida_fila1 = [float('inf')] * num_servidores1
proximos_tempos_saida_fila2 = [float('inf')] * num_servidores2

tempo_global = 0

tempos_acumulados_fila1 = [0] * (K1 + 1)
tempos_acumulados_fila2 = [0] * (K2 + 1)

clientes_perdidos_fila1 = 0
clientes_perdidos_fila2 = 0

def NextRandom():
    global previous
    previous = (a * previous + c) % M
    return previous / M

def gerar_tempo_chegada():
    return 1 + NextRandom() * 3

def gerar_tempo_atendimento_fila1():
    return 3 + NextRandom()  

def gerar_tempo_atendimento_fila2():
    return 2 + NextRandom()

def atualizar_tempos_acumulados_fila1():
    global tempo_atual, tempo_global
    delta_tempo = tempo_atual - tempo_global
    num_clientes_fila1 = min(len(fila1), K1)
    tempos_acumulados_fila1[num_clientes_fila1] += delta_tempo
    tempo_global = tempo_atual

def atualizar_tempos_acumulados_fila2():
    global tempo_atual, tempo_global
    delta_tempo = tempo_atual - tempo_global
    num_clientes_fila2 = min(len(fila2), K2)
    tempos_acumulados_fila2[num_clientes_fila2] += delta_tempo
    tempo_global = tempo_atual

def CHEGADA():
    global proximo_tempo_chegada, clientes_perdidos_fila1
    atualizar_tempos_acumulados_fila1()

    if len(fila1) < K1:
        fila1.append(tempo_atual)
        print(f"Cliente chegou à Fila 1 às {tempo_atual:.2f}")
        for i in range(num_servidores1):
            if proximos_tempos_saida_fila1[i] == float('inf'):
                proximos_tempos_saida_fila1[i] = tempo_atual + gerar_tempo_atendimento_fila1()
                break
    else:
        clientes_perdidos_fila1 += 1
        print(f"Cliente perdido na Fila 1 às {tempo_atual:.2f}")
    
    proximo_tempo_chegada = tempo_atual + gerar_tempo_chegada()

def SAIDA_FILA1():
    atualizar_tempos_acumulados_fila1()

    for i in range(num_servidores1):
        if proximos_tempos_saida_fila1[i] == tempo_atual and fila1:
            cliente = fila1.popleft()
            print(f"Cliente saiu da Fila 1 às {tempo_atual:.2f}, esperou {tempo_atual - cliente:.2f} unidades de tempo")
            
            if len(fila2) < K2:
                fila2.append(tempo_atual)
                for j in range(num_servidores2):
                    if proximos_tempos_saida_fila2[j] == float('inf'):
                        proximos_tempos_saida_fila2[j] = tempo_atual + gerar_tempo_atendimento_fila2()
                        break
            else:
                clientes_perdidos_fila2 += 1
                print(f"Cliente perdido na Fila 2 às {tempo_atual:.2f}")
            
            proximos_tempos_saida_fila1[i] = float('inf') if not fila1 else tempo_atual + gerar_tempo_atendimento_fila1()

def SAIDA_FILA2():
    atualizar_tempos_acumulados_fila2()

    for i in range(num_servidores2):
        if proximos_tempos_saida_fila2[i] == tempo_atual and fila2:
            cliente = fila2.popleft()
            print(f"Cliente saiu da Fila 2 às {tempo_atual:.2f}, esperou {tempo_atual - cliente:.2f} unidades de tempo")
            proximos_tempos_saida_fila2[i] = float('inf') if not fila2 else tempo_atual + gerar_tempo_atendimento_fila2()

def NextEvent():
    global tempo_atual
    prox_evento = min(proximo_tempo_chegada, *proximos_tempos_saida_fila1, *proximos_tempos_saida_fila2)
    tempo_atual = prox_evento

    if prox_evento == proximo_tempo_chegada:
        return TIPO_CHEGADA
    elif prox_evento in proximos_tempos_saida_fila1:
        return TIPO_SAIDA_FILA1
    else:
        return TIPO_SAIDA_FILA2

def main():
    global count

    while count > 0:
        evento = NextEvent()
        if evento == TIPO_CHEGADA:
            CHEGADA()
        elif evento == TIPO_SAIDA_FILA1:
            SAIDA_FILA1()
        elif evento == TIPO_SAIDA_FILA2:
            SAIDA_FILA2()
        count -= 1

    print("\nDistribuição de probabilidade dos estados da Fila 1:")
    for i in range(K1 + 1):
        probabilidade_fila1 = (tempos_acumulados_fila1[i] / tempo_global) * 100
        print(f"{i} clientes: {tempos_acumulados_fila1[i]:.2f} unidades de tempo ({probabilidade_fila1:.2f}%)")

    print("\nDistribuição de probabilidade dos estados da Fila 2:")
    for i in range(K2 + 1):
        probabilidade_fila2 = (tempos_acumulados_fila2[i] / tempo_global) * 100
        print(f"{i} clientes: {tempos_acumulados_fila2[i]:.2f} unidades de tempo ({probabilidade_fila2:.2f}%)")

    print(f"\nTotal de clientes perdidos na Fila 1: {clientes_perdidos_fila1}")
    print(f"Total de clientes perdidos na Fila 2: {clientes_perdidos_fila2}")
    print(f"Tempo global de simulação: {tempo_global:.2f}")

if __name__ == "__main__":
    main()
