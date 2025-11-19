from terreno import Terreno

class Salida(Terreno):
    def permite_jugador(self):
        return True

    def permite_enemigo(self):
        return False