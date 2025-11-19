from tkinter import *
from mapa import Mapa

# Importar clases de terrenos
from camino import Camino
from muro import Muro
from tunel import Tunel
from liana import Liana

TAM = 30

# Diccionario: nombre → clase, NO instancias
TIPOS = {
    "Camino": Camino,
    "Muro": Muro,
    "Tunel": Tunel,
    "Liana": Liana
}

ventana = Tk()
canvas = Canvas(ventana, width=900, height=900)
canvas.pack()

mapa = Mapa(26, 30, TIPOS)
mapa.dibujar(canvas, TAM)

ventana.mainloop()

