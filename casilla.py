from terreno import Terreno

class Casilla:
    def __init__(self, terreno, tipo):
        self.terreno = terreno
        self.tipo = tipo 

    def es_muro(self):
        return self.tipo == "Muro"
    
    def es_liana(self):
        return self.tipo == "Liana"
    
    def es_tunel(self):
        return self.tipo == "Tunel"

    def es_camino(self):
        return self.tipo == "Camino"
    
    def dibujar(self, canvas, x, y, tam):
        canvas.create_rectangle(
            x, y, x+tam, y+tam,
            fill=self.terreno.color,
            outline="black"
        )