
from terreno import Terreno

class Muro(Terreno):
    def permite_jugador(self):
        return False
    
    def permite_enemigo(self):
        return False
    
    def get_color(self):
        return "black"
