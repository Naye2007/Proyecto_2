from tkinter import *
from mapa import Mapa
from camino import Camino
from muro import Muro
from tunel import Tunel
from liana import Liana

TAM_CELDA = 30
TIPOS = {"Camino": Camino, "Muro": Muro, "Tunel": Tunel, "Liana": Liana}

def main():
    ventana = Tk()
    ventana.title("Escapa del Laberinto")
    
    canvas = Canvas(ventana, width=900, height=780, bg="white")
    canvas.pack()
    
    mapa = Mapa(26, 30, TIPOS)
    
    mapa.dibujar(canvas, TAM_CELDA)
    
    ventana.mainloop()

if __name__ == "__main__":
    main()