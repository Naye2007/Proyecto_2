class Jugador:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.energia = 100
        self.energia_maxima = 100
        self.corriendo = False
        self.trampas = []  # Lista de trampas activas
        self.trampas_colocadas = 0
        self.ultima_trampa_tiempo = 0
    
    def mover(self, df, dc, mapa):
        nueva_fila = self.fila + df
        nueva_columna = self.columna + dc
        
        if mapa.es_posicion_valida(nueva_fila, nueva_columna, es_jugador=True):
            self.fila = nueva_fila
            self.columna = nueva_columna

            if self.corriendo and self.energia > 0:
                self.energia -= 2
                if self.energia <= 0:
                    self.corriendo = False
                    self.energia = 0

            elif not self.corriendo and self.energia < self.energia_maxima:
                self.energia += 0.5
    
    def toggle_correr(self):
        if self.energia > 10:  
            self.corriendo = not self.corriendo
    
    def colocar_trampa(self, tiempo_actual):
        if (len(self.trampas) < 3 and 
            tiempo_actual - self.ultima_trampa_tiempo >= 5):
            self.trampas.append((self.fila, self.columna))
            self.ultima_trampa_tiempo = tiempo_actual
            return True
        return False