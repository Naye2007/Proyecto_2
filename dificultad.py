class Dificultad:
    def __init__(self, nivel="normal"):
        self.nivel = nivel
        self.configurar_nivel(nivel)
    
    def configurar_nivel(self, nivel):
        if nivel == "facil":
            self.cantidad_enemigos = 2
            self.velocidad_enemigos = 0.2
            self.multiplicador_puntos = 1.0
            self.nombre = "Fácil"
        elif nivel == "normal":
            self.cantidad_enemigos = 3
            self.velocidad_enemigos = 0.5
            self.multiplicador_puntos = 1.5
            self.nombre = "Normal"
        elif nivel == "dificil":
            self.cantidad_enemigos = 4
            self.velocidad_enemigos = 0.8
            self.multiplicador_puntos = 2.0
            self.nombre = "Difícil"
        elif nivel == "extremo":
            self.cantidad_enemigos = 5
            self.velocidad_enemigos = 1
            self.multiplicador_puntos = 3.0
            self.nombre = "Extremo"
    
    def get_configuracion(self):
        return {
            'cantidad_enemigos': self.cantidad_enemigos,
            'velocidad_enemigos': self.velocidad_enemigos,
            'multiplicador_puntos': self.multiplicador_puntos,
            'nombre': self.nombre
        }