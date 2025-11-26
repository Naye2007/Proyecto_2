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
                fila.append(Casilla(Muro()))
            self.grid.append(fila)
    
        self._generar_caminos(0, 0)
        self._agregar_variedad_terrenos()
    
    def _generar_caminos(self, f, c):
        self.grid[f][c] = Casilla(Camino())
        direcciones = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(direcciones)
        
        for df, dc in direcciones:
            nf, nc = f + df, c + dc
            if (0 <= nf < self.filas and 0 <= nc < self.columnas and 
                isinstance(self.grid[nf][nc].terreno, Muro)):
                self.grid[f + df//2][c + dc//2] = Casilla(Camino())
                self._generar_caminos(nf, nc)
    
    def _agregar_variedad_terrenos(self):
        clases = {
            "Tunel": Tunel,
            "Liana": Liana,
            "Camino": Camino  
        }
        
        for f in range(self.filas):
            for c in range(self.columnas):
                if isinstance(self.grid[f][c].terreno, Camino):
                    if random.random() < 0.2:
                        tipo = random.choice(["Tunel", "Liana"])
                        self.grid[f][c] = Casilla(clases[tipo]())
    
    def colocar_salidas(self):
        cantidad = random.randint(1, 3)  
        self.salidas = []
        posiciones_borde = []
        for f in [0, self.filas-1]: 
            for c in range(self.columnas):
                if self.grid[f][c].permite_jugador():
                    posiciones_borde.append((f, c))
        
        for c in [0, self.columnas-1]:  
            for f in range(self.filas):
                if self.grid[f][c].permite_jugador():
                    posiciones_borde.append((f, c))
        if posiciones_borde:
            cantidad = min(cantidad, len(posiciones_borde))
            self.salidas = random.sample(posiciones_borde, cantidad)
            
            for f, c in self.salidas:
                self.grid[f][c] = Casilla(Salida())
    
    def hay_camino(self, f, c, visitados=None):
        if visitados is None:
            visitados = set()
        if not (0 <= f < self.filas and 0 <= c < self.columnas) or (f, c) in visitados:
            return False
        
        visitados.add((f, c))
        if self.grid[f][c].es_salida():
            return True
        if not self.grid[f][c].permite_jugador():
            return False
        movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for df, dc in movimientos:
            if self.hay_camino(f + df, c + dc, visitados):
                return True
        
        return False
    
    def asegurar_camino_valido(self, inicio_f, inicio_c):
        intentos = 0
        max_intentos = 10
        
        while not self.hay_camino(inicio_f, inicio_c) and intentos < max_intentos:
            self.colocar_salidas()
            intentos += 1
        
        if intentos == max_intentos:
            self._crear_ruta_forzada(inicio_f, inicio_c)
    
    def _crear_ruta_forzada(self, inicio_f, inicio_c):
        f, c = inicio_f, inicio_c
        while f < self.filas - 1:
            f += 1
            self.grid[f][c] = Casilla(Camino())
        
        while c < self.columnas - 1:
            c += 1
            self.grid[f][c] = Casilla(Camino())
        self.grid[f][c] = Casilla(Salida())
        self.salidas = [(f, c)]
    
    def dibujar(self, canvas, tam_celda):
        for f in range(self.filas):
            for c in range(self.columnas):
                x1 = c * tam_celda
                y1 = f * tam_celda
                x2 = x1 + tam_celda
                y2 = y1 + tam_celda
                
                color = self.grid[f][c].get_color()
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    
