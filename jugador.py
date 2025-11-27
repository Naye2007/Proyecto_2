class Jugador:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.energia = 100
        self.energia_maxima = 100
        self.corriendo = False
        self.movimientos_pendientes = 0 
        self.trampas = [] 
        self.ultima_trampa_tiempo = 0
        self.cooldown_trampas = 5  

        
    def colocar_trampa(self, tiempo_actual):
        if len(self.trampas) >= 3:
            print("Máximo de 3 trampas activas alcanzado")
            return False
        tiempo_desde_ultima = tiempo_actual - self.ultima_trampa_tiempo
        if tiempo_desde_ultima < self.cooldown_trampas:
            tiempo_restante = self.cooldown_trampas - tiempo_desde_ultima
            print(f"Trampa en cooldown. Espera {tiempo_restante:.1f} segundos")
            return False
        from trampa import Trampa  
        nueva_trampa = Trampa(self.fila, self.columna)
        self.trampas.append(nueva_trampa)
        self.ultima_trampa_tiempo = tiempo_actual 
        print(f"Trampa colocada en ({self.fila}, {self.columna}). Trampas activas: {len(self.trampas)}/3")
        return True
    
    def eliminar_trampa(self, trampa):
        if trampa in self.trampas:
            self.trampas.remove(trampa)
            print(f"Trampa eliminada. Trampas activas: {len(self.trampas)}/3")
    
    def get_trampas_activas(self):
        return [trampa for trampa in self.trampas if trampa.activa]
    
    def get_cooldown_restante(self, tiempo_actual):
        tiempo_desde_ultima = tiempo_actual - self.ultima_trampa_tiempo
        if tiempo_desde_ultima < self.cooldown_trampas:
            return self.cooldown_trampas - tiempo_desde_ultima
        return 0
    
    def mover(self, df, dc, mapa):
        movimientos = 2 if self.corriendo else 1
        
        for i in range(movimientos):
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            if (0 <= nueva_fila < len(mapa.grid) and 
                0 <= nueva_columna < len(mapa.grid[0]) and
                mapa.grid[nueva_fila][nueva_columna].terreno.permite_jugador()):
                
                self.fila = nueva_fila
                self.columna = nueva_columna
                if self.corriendo and i == 0:  
                    self.energia -= 4 
                    if self.energia <= 0:
                        self.corriendo = False
                        self.energia = 0
            else:
                break
        
        return True 
    
    def toggle_correr(self):
        if self.energia > 15: 
            self.corriendo = not self.corriendo
            return True
        elif self.corriendo:
            self.corriendo = False  
        return False
    
    def recuperar_energia(self):
        if not self.corriendo and self.energia < self.energia_maxima:
            self.energia += 2 
            if self.energia > self.energia_maxima:
                self.energia = self.energia_maxima
    
    def get_energia_porcentaje(self):
        return (self.energia / self.energia_maxima) * 100
    
    def puede_correr(self):
        return self.energia > 15
    
