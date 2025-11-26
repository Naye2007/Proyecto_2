import random
import math

class Cazador:
    def __init__(self, fila, columna, velocidad=1):
        self.fila = fila
        self.columna = columna
        self.velocidad = velocidad
        self.vivo = True
        self.tiempo_muerte = 0
    
    def mover(self, jugador_fila, jugador_columna, mapa, modo_cazador=False):
        if not self.vivo:
            return
        
        for _ in range(self.velocidad):
            if modo_cazador:
                self._huir(jugador_fila, jugador_columna, mapa)
            else:
                self._perseguir(jugador_fila, jugador_columna, mapa)
    
    def _perseguir(self, jugador_fila, jugador_columna, mapa):
        # Movimiento inteligente: busca el camino más corto hacia el jugador
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Calcular distancia a jugador para cada movimiento posible
        mejores_movimientos = []
        for df, dc in movimientos:
            nf, nc = self.fila + df, self.columna + dc
            if mapa.es_posicion_valida(nf, nc, es_jugador=False):
                dist = math.sqrt((nf - jugador_fila)**2 + (nc - jugador_columna)**2)
                mejores_movimientos.append((dist, df, dc))
        
        if mejores_movimientos:
            # Elegir el movimiento que acerque más al jugador
            mejores_movimientos.sort(key=lambda x: x[0])
            _, df, dc = mejores_movimientos[0]
            self.fila += df
            self.columna += dc
    
    def _huir(self, jugador_fila, jugador_columna, mapa):
        # Huir del jugador en modo cazador
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        mejores_movimientos = []
        for df, dc in movimientos:
            nf, nc = self.fila + df, self.columna + dc
            if mapa.es_posicion_valida(nf, nc, es_jugador=False):
                dist = math.sqrt((nf - jugador_fila)**2 + (nc - jugador_columna)**2)
                mejores_movimientos.append((dist, df, dc))
        
        if mejores_movimientos:
            # Elegir el movimiento que aleje más del jugador
            mejores_movimientos.sort(key=lambda x: x[0], reverse=True)
            _, df, dc = mejores_movimientos[0]
            self.fila += df
            self.columna += dc
    
    def morir(self, tiempo_actual):
        self.vivo = False
        self.tiempo_muerte = tiempo_actual
    
    def revivir(self, nueva_fila, nueva_columna):
        self.vivo = True
        self.fila = nueva_fila
        self.columna = nueva_columna