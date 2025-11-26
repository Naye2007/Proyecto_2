from terreno import Terreno

class Liana(Terreno):
    def permite_jugador(self):
        return False  
    
    def permite_enemigo(self):
        return True  
    
    def get_color(self):
        return "green"