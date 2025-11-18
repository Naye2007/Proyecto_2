import tkinter as tk
from casilla import Casilla
from terreno import Terreno

TAM = 40  # tamaño de cada casilla

ventana = tk.Tk()
canvas = tk.Canvas(ventana, width=400, height=400)
canvas.pack()

# Definir tipos de terreno una sola vez
TIPOS = {
    "Muro": Terreno("Muro", "gray"),
    "Camino": Terreno("Camino", "white"),
    "Liana": Terreno("Liana", "green"),
    "Tunel": Terreno("Tunel", "brown"),
}

# Crear matriz 10x10
matriz = []

for i in range(10):
    fila = []
    for j in range(10):
        # elegir terreno según patrón o aleatorio
        terreno = TIPOS["Camino"] if (i+j) % 2 == 0 else TIPOS["Muro"]

        casilla = Casilla(terreno)
        casilla.dibujar(canvas, j*TAM, i*TAM, TAM)
        fila.append(casilla)

    matriz.append(fila)

ventana.mainloop()
