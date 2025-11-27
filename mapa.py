import random
from casilla import Casilla
from camino import Camino
from muro import Muro
from liana import Liana
from tunel import Tunel
from salida import Salida

class Mapa:
    def __init__(self, filas, columnas, tipos):
        self.filas = filas
        self.columnas = columnas
        self.tipos = tipos
        self.grid = []
        self.salidas = []
        
        self.generar_mapa()
        self.colocar_salidas()
        self.asegurar_camino_valido(0, 0)
    
    def generar_mapa(self):

        self.grid = []
        for f in range(self.filas):
            fila = []
            for c in range(self.columnas):
                if random.random() < 0.8:  
                    fila.append(Casilla(Camino()))
                else:
                    fila.append(Casilla(Muro()))
            self.grid.append(fila)
        self._generar_caminos_principales()
        self._agregar_variedad_terrenos()
        self._hacer_bordes_transitables()
    
    def _generar_caminos_principales(self):
        self._crear_camino(0, 0, self.filas-1, self.columnas-1)
        for _ in range(3):
            f1 = random.randint(0, self.filas-1)
            c1 = random.randint(0, self.columnas-1)
            f2 = random.randint(0, self.filas-1)
            c2 = random.randint(0, self.columnas-1)
            self._crear_camino(f1, c1, f2, c2)
    
    def _crear_camino(self, f1, c1, f2, c2):
        f, c = f1, c1
        
        while f != f2:
            if f < f2:
                f += 1
            else:
                f -= 1
            self.grid[f][c] = Casilla(Camino())
        while c != c2:
            if c < c2:
                c += 1
            else:
                c -= 1
            self.grid[f][c] = Casilla(Camino())
    
    def _agregar_variedad_terrenos(self):
        for f in range(self.filas):
            for c in range(self.columnas):
                if isinstance(self.grid[f][c].terreno, Camino):
                    if random.random() < 0.2:
                        if random.random() < 0.5:
                            self.grid[f][c] = Casilla(Tunel())
                        else:
                            self.grid[f][c] = Casilla(Liana())
                    
                    elif random.random() < 0.05:
                        self.grid[f][c] = Casilla(Muro())
    
    def _hacer_bordes_transitables(self):
        for c in range(self.columnas):
            if isinstance(self.grid[0][c].terreno, Muro) and random.random() < 0.7:
                self.grid[0][c] = Casilla(Camino())
            if isinstance(self.grid[self.filas-1][c].terreno, Muro) and random.random() < 0.7:
                self.grid[self.filas-1][c] = Casilla(Camino())
        
        for f in range(self.filas):
            if isinstance(self.grid[f][0].terreno, Muro) and random.random() < 0.7:
                self.grid[f][0] = Casilla(Camino())
            if isinstance(self.grid[f][self.columnas-1].terreno, Muro) and random.random() < 0.7:
                self.grid[f][self.columnas-1] = Casilla(Camino())
    
    def colocar_salidas(self):
        self.salidas = []
        
        candidatas = []
        
        for c in range(1, self.columnas - 1):
            if self.es_posicion_valida(0, c, es_jugador=True):
                candidatas.append((0, c))
            if self.es_posicion_valida(self.filas - 1, c, es_jugador=True):
                candidatas.append((self.filas - 1, c))
        for f in range(1, self.filas - 1):
            if self.es_posicion_valida(f, 0, es_jugador=True):
                candidatas.append((f, 0))
            if self.es_posicion_valida(f, self.columnas - 1, es_jugador=True):
                candidatas.append((f, self.columnas - 1))
        if candidatas:
            salida = random.choice(candidatas)
            f, c = salida
            self.grid[f][c] = Casilla(Salida())
            self.salidas = [salida]
            print(f"Salida colocada en: ({f}, {c})")
        else:
            self._crear_salida_forzada()

    def _crear_salida_forzada(self):
        for c in [0, self.columnas-1]:
            for f in range(self.filas):
                self.grid[f][c] = Casilla(Salida())
                self.salidas = [(f, c)]
                return
        
        for f in [0, self.filas-1]:
            for c in range(self.columnas):
                self.grid[f][c] = Casilla(Salida())
                self.salidas = [(f, c)]
                return
    
    def hay_camino(self, f, c, visitados=None):
        if visitados is None:
            visitados = set()
        
        if not (0 <= f < self.filas and 0 <= c < self.columnas) or (f, c) in visitados:
            return False
        
        visitados.add((f, c))

        if isinstance(self.grid[f][c].terreno, Salida):
            return True

        if not self.grid[f][c].terreno.permite_jugador():
            return False

        movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for df, dc in movimientos:
            if self.hay_camino(f + df, c + dc, visitados):
                return True
        
        return False
    
    def asegurar_camino_valido(self, inicio_f, inicio_c):
        if not self.hay_camino(inicio_f, inicio_c):
            if self.salidas:
                f_salida, c_salida = self.salidas[0]
                self._crear_camino(inicio_f, inicio_c, f_salida, c_salida)
    
    def es_posicion_valida(self, f, c, es_jugador=True):
        if not (0 <= f < self.filas and 0 <= c < self.columnas):
            return False
        
        if es_jugador:
            return self.grid[f][c].terreno.permite_jugador()
        else:
            return self.grid[f][c].terreno.permite_enemigo()