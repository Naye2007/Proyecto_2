class Dificultad:
    def __init__(self, nivel="normal"):
        self.nivel = nivel
        self.configurar_nivel(nivel)
    
    def configurar_nivel(self, nivel):
        if nivel == "facil":
            self.cantidad_enemigos = 2
            self.velocidad_enemigos = 1
            self.tiempo_reaparicion = 15
            self.multiplicador_puntos = 1.0
        elif nivel == "normal":
            self.cantidad_enemigos = 4
            self.velocidad_enemigos = 2
            self.tiempo_reaparicion = 10
            self.multiplicador_puntos = 1.5
        elif nivel == "dificil":
            self.cantidad_enemigos = 6
            self.velocidad_enemigos = 3
            self.tiempo_reaparicion = 7
            self.multiplicador_puntos = 2.0
        elif nivel == "extremo":
            self.cantidad_enemigos = 8
            self.velocidad_enemigos = 4
            self.tiempo_reaparicion = 5
            self.multiplicador_puntos = 3.0
    
    def get_configuracion(self):
        return {
            'cantidad_enemigos': self.cantidad_enemigos,
            'velocidad_enemigos': self.velocidad_enemigos,
            'tiempo_reaparicion': self.tiempo_reaparicion,
            'multiplicador_puntos': self.multiplicador_puntos
        }