import time

class Trampa:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tiempo_colocacion = time.time()
        self.activa = True
    
    def esta_activa(self):
        return self.activa
    
    def desactivar(self):
        self.activa = False
    
    def get_posicion(self):
        return (self.fila, self.columna)
    
    def __str__(self):
        return f"Trampa({self.fila}, {self.columna}) - {'Activa' if self.activa else 'Inactiva'}"