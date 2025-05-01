import random
import math
import statistics

media = float(input("Ingresa la media: "))
n = int(input("Cantidad de clientes: "))

matriz = []

for i in range(1, n + 1):
    u = random.random()
    tiempo = -media * math.log(1 - u)
    matriz.append([i, tiempo])

for fila in matriz:
    print(f"Cliente {fila[0]}: {fila[1]:.4f}")

# Calcular y mostrar el promedio
tiempos = [fila[1] for fila in matriz]
promedio = statistics.mean(tiempos)
print(f"Promedio de tiempos: {promedio:.4f}")
