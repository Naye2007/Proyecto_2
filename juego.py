import time
import random
from jugador import Jugador
from cazador import Cazador
from dificultad import Dificultad

class Juego:
    def __init__(self, mapa, modo_escape=True):
        self.mapa = mapa
        self.modo_escape = modo_escape
        self.jugador = None
        self.enemigos = []
        self.dificultad = None
        self.tiempo_inicio = 0
        self.tiempo_juego = 0
        self.puntaje = 0
        self.juego_activo = False
        self.initialize_posiciones()
    
    def initialize_posiciones(self):
        # Posición inicial del jugador (esquina superior izquierda)
        self.jugador = Jugador(1, 1)
    
    def iniciar_juego(self, nivel_dificultad="normal"):
        self.dificultad = Dificultad(nivel_dificultad)
        config = self.dificultad.get_configuracion()
        
        # Crear enemigos
        self.enemigos = []
        for i in range(config['cantidad_enemigos']):
            # Buscar posición aleatoria válida para enemigos
            fila, columna = self._buscar_posicion_valida_enemigo()
            enemigo = Cazador(fila, columna, config['velocidad_enemigos'])
            self.enemigos.append(enemigo)
        
        self.tiempo_inicio = time.time()
        self.juego_activo = True
        self.puntaje = 0
    
    def _buscar_posicion_valida_enemigo(self):
        # Buscar posición aleatoria donde puedan estar los enemigos
        intentos = 0
        while intentos < 100:
            fila = random.randint(1, self.mapa.filas - 2)
            columna = random.randint(1, self.mapa.columnas - 2)
            
            if (self.mapa.es_posicion_valida(fila, columna, es_jugador=False) and
                abs(fila - self.jugador.fila) + abs(columna - self.jugador.columna) > 10):
                return fila, columna
            intentos += 1
        
        # Fallback
        return self.mapa.filas - 2, self.mapa.columnas - 2
    
    def actualizar(self):
        if not self.juego_activo:
            return
        
        self.tiempo_juego = time.time() - self.tiempo_inicio
        
        # Mover enemigos
        for enemigo in self.enemigos:
            if enemigo.vivo:
                enemigo.mover(
                    self.jugador.fila, 
                    self.jugador.columna, 
                    self.mapa, 
                    not self.modo_escape
                )
        
        # Verificar colisiones
        self._verificar_colisiones()
        
        # Verificar si ganó
        self._verificar_victoria()
        
        # Reaparecer enemigos muertos
        self._reaparecer_enemigos()
        
        # Actualizar puntaje
        self._actualizar_puntaje()
    
    def _verificar_colisiones(self):
        # Colisión jugador-enemigo
        for enemigo in self.enemigos:
            if (enemigo.vivo and 
                enemigo.fila == self.jugador.fila and 
                enemigo.columna == self.jugador.columna):
                
                if self.modo_escape:
                    self.juego_activo = False  # Jugador pierde
                else:
                    # En modo cazador, jugador atrapa enemigo
                    enemigo.morir(time.time())
                    self.puntaje += 100 * self.dificultad.multiplicador_puntos
    
    def _verificar_victoria(self):
        # Verificar si jugador llegó a salida (modo escape)
        if self.modo_escape:
            for f, c in self.mapa.salidas:
                if self.jugador.fila == f and self.jugador.columna == c:
                    self.juego_activo = False
                    # Calcular puntaje final basado en tiempo
                    tiempo_bonus = max(0, 1000 - int(self.tiempo_juego))
                    self.puntaje += tiempo_bonus * self.dificultad.multiplicador_puntos
    
    def _reaparecer_enemigos(self):
        tiempo_actual = time.time()
        config = self.dificultad.get_configuracion()
        
        for enemigo in self.enemigos:
            if not enemigo.vivo and (tiempo_actual - enemigo.tiempo_muerte) >= config['tiempo_reaparicion']:
                nueva_fila, nueva_columna = self._buscar_posicion_valida_enemigo()
                enemigo.revivir(nueva_fila, nueva_columna)
    
    def _actualizar_puntaje(self):
        # Puntos por tiempo sobrevivido (modo escape)
        if self.modo_escape and self.juego_activo:
            self.puntaje += 1 * self.dificultad.multiplicador_puntos