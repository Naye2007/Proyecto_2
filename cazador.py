import random
import math

class Cazador:
    def __init__(self, fila, columna, velocidad=1.0):
        self.fila = fila
        self.columna = columna
        self.velocidad = velocidad
        self.vivo = True
        self.contador_movimiento = 0
        self.tiempo_muerte = 0
    
    def mover(self, jugador_fila, jugador_columna, mapa):
        if not self.vivo:
            return
        self.contador_movimiento += 1
        if self.contador_movimiento >= (1 / self.velocidad):
            self.contador_movimiento = 0
            mejor_movimiento = self._encontrar_mejor_movimiento(jugador_fila, jugador_columna, mapa)
            
            if mejor_movimiento:
                df, dc = mejor_movimiento
                self.fila += df
                self.columna += dc
    
    def _encontrar_mejor_movimiento(self, jugador_fila, jugador_columna, mapa):
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)] 
        movimientos_validos = []
        
        for df, dc in movimientos:
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            
            if (0 <= nueva_fila < len(mapa.grid) and 
                0 <= nueva_columna < len(mapa.grid[0]) and
                mapa.grid[nueva_fila][nueva_columna].terreno.permite_enemigo()):
                
                distancia = math.sqrt((nueva_fila - jugador_fila)**2 + (nueva_columna - jugador_columna)**2)
                movimientos_validos.append((distancia, df, dc))
        
        if movimientos_validos:
            movimientos_validos.sort(key=lambda x: x[0])
            return movimientos_validos[0][1], movimientos_validos[0][2]
        
        return None