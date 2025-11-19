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

        self.generar_mapa()
        self.colocar_salidas()
        self.asegurar_camino_valido(0, 0)

    # ------------------------
    # GENERACIÓN DEL MAPA
    # ------------------------
    def generar_mapa(self):
        self.grid = []

        clases = {
            "Camino": Camino,
            "Muro": Muro,
            "Liana": Liana,
            "Tunel": Tunel
        }

        for f in range(self.filas):
            fila = []

            for c in range(self.columnas):
                tipo = random.choice(list(self.tipos.keys()))
                fila.append(Casilla(clases[tipo]()))

            self.grid.append(fila)
    # ------------------------
    # COLOCAR SALIDAS
    # ------------------------
    def colocar_salidas(self):
        cantidad = random.randint(1, 5)
        self.salidas = []

        while len(self.salidas) < cantidad:
            f = random.randint(0, self.filas - 1)
            c = random.randint(0, self.columnas - 1)

            # Solo colocar en casillas transitables
            if self.grid[f][c].es_camino() or self.grid[f][c].es_liana() or self.grid[f][c].es_tunel():
                self.grid[f][c] = Casilla(Salida())
                self.salidas.append((f, c))


    def hay_camino(self, f, c, visitados):
        if (f, c) in visitados:
            return False

        visitados.add((f, c))

        # Si es una salida → camino encontrado
        if self.grid[f][c].es_salida():
            return True

        if self.grid[f][c].es_muro():
            return False

        # mover arriba, abajo, izq, der
        movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for df, dc in movimientos:
            nf = f + df
            nc = c + dc

            if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                if self.hay_camino(nf, nc, visitados):
                    return True

        return False
    def asegurar_camino_valido(self, fila0, col0):
        while not self.hay_camino(fila0, col0, set()):
            # regenerar salidas hasta que alguna sea alcanzable
            self.colocar_salidas()

    def imprimir(self):
        simb = {
            "Camino": ".",
            "Muro": "#",
            "Liana": "L",
            "Tunel": "T",
            "Salida": "S",
        }

        for f in range(self.filas):
            fila = ""
            for c in range(self.columnas):
                t = self.grid[f][c].terreno.__class__.__name__
                fila += simb[t] + " "
            print(fila)