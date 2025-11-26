class Jugador:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.energia = 100
        self.energia_maxima = 100
        self.corriendo = False
        self.movimientos_pendientes = 0  # Para movimiento rápido
    
    def mover(self, df, dc, mapa):
        # Si está corriendo, puede mover 2 casillas
        movimientos = 2 if self.corriendo else 1
        
        for i in range(movimientos):
            nueva_fila = self.fila + df
            nueva_columna = self.columna + dc
            
            # Verificar si la nueva posición es válida
            if (0 <= nueva_fila < len(mapa.grid) and 
                0 <= nueva_columna < len(mapa.grid[0]) and
                mapa.grid[nueva_fila][nueva_columna].terreno.permite_jugador()):
                
                self.fila = nueva_fila
                self.columna = nueva_columna
                
                # Consumir energía solo si se movió y está corriendo
                if self.corriendo and i == 0:  # Solo consumir una vez por movimiento
                    self.energia -= 4  # Más consumo por correr
                    if self.energia <= 0:
                        self.corriendo = False
                        self.energia = 0
            else:
                # Si no puede moverse, salir del bucle
                break
        
        return True  # Siempre retorna True si intentó moverse
    
    def toggle_correr(self):
        """Activa/desactiva el modo correr"""
        if self.energia > 15:  # Más energía requerida para empezar a correr
            self.corriendo = not self.corriendo
            return True
        elif self.corriendo:
            self.corriendo = False  # Forzar apagar si no tiene energía
        return False
    
    def recuperar_energia(self):
        """Recupera energía gradualmente cuando no está corriendo"""
        if not self.corriendo and self.energia < self.energia_maxima:
            self.energia += 2  # Más recuperación
            if self.energia > self.energia_maxima:
                self.energia = self.energia_maxima
    
    def get_energia_porcentaje(self):
        """Devuelve el porcentaje de energía"""
        return (self.energia / self.energia_maxima) * 100
    
    def puede_correr(self):
        """Verifica si el jugador puede correr"""
        return self.energia > 15