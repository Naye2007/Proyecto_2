from terreno import Terreno
from tkinter import  *
from tunel import Tunel
from muro import Muro
from camino import Camino
from liana import Liana
from salida import Salida



class Casilla:
    def __init__(self, terreno):
        self.terreno = terreno

    def es_muro(self):
        from muro import Muro
        return isinstance(self.terreno, Muro)

    def es_camino(self):
        from camino import Camino
        return isinstance(self.terreno, Camino)

    def es_liana(self):
        from liana import Liana
        return isinstance(self.terreno, Liana)

    def es_tunel(self):
        from tunel import Tunel
        return isinstance(self.terreno, Tunel)

    def es_salida(self):
        from salida import Salida
        return isinstance(self.terreno, Salida)
