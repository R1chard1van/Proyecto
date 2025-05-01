import random, math

media = float(input("Ingresa la media: "))
n = int(input("Cantidad de clientes: "))

matriz = []

for i in range(1, n + 1):
    u = random.random()
    tiempo = -media * math.log(1 - u)
    matriz.append([i, tiempo])

for fila in matriz:
    print(f"Cliente {fila[0]}: {fila[1]:.4f}")
1

