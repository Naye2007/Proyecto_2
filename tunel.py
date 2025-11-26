from terreno import Terreno

class Tunel(Terreno):
    def permite_jugador(self):
        return True  
    
    def permite_enemigo(self):
        return False  
    
    def get_color(self):
        return "blue"