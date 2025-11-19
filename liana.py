from terreno import Terreno

class Liana(Terreno):
    def permite_jugador(self):
        return True

    def permite_enemigo(self):
        return False