class Terreno:
    def __init__(self, tipo, color):
        self.tipo = tipo
        self.color = color
    
    def permite_jugador(self):
        return self.tipo in ["Camino", "Liana", "Tunel"]

    def permite_enemigo(self):
        return self.tipo in ["Camino", "Tunel"]     