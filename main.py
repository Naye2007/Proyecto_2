from tkinter import *
import random
import time
from mapa import Mapa
from camino import Camino
from muro import Muro
from tunel import Tunel
from liana import Liana
from jugador import Jugador
from cazador import Cazador
from dificultad import Dificultad
from casilla import Casilla

class Main:
    def __init__(self):
        # Configuración inicial
        self.TAM_CELDA = 25
        self.FILAS = 20
        self.COLUMNAS = 25
        self.TIPOS = {"Camino": Camino, "Muro": Muro, "Tunel": Tunel, "Liana": Liana}
        
        # Estado del juego
        self.juego_activo = False
        self.modo_escape = True
        self.tiempo_inicio = 0
        self.puntaje = 0
        self.dificultad = None
        self.bucle_energia_id = None
        self.bucle_enemigos_id = None
        self.bucle_tiempo_id = None
        # Crear ventana principal
        self.ventana = Tk()
        self.ventana.title("Laberinto - Modo Escapa")
        self.ventana.geometry("1200x800")
        self.ventana.resizable(True, True)
        
        # Crear widgets
        self.crear_interfaz()
        
        # Mostrar pantalla de inicio
        self.mostrar_pantalla_inicio()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = Frame(self.ventana)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Panel de controles superior
        self.control_frame = Frame(main_frame)
        self.control_frame.pack(fill=X, pady=5)
        
        # Información del juego
        self.info_frame = Frame(main_frame)
        self.info_frame.pack(fill=X, pady=5)
        
        self.label_info = Label(self.info_frame, text="Selecciona la dificultad para comenzar", 
                               font=("Arial", 12), fg="blue", wraplength=1000)
        self.label_info.pack()
        
        # Panel de estadísticas
        self.stats_frame = Frame(main_frame)
        self.stats_frame.pack(fill=X, pady=8)
        
        # Barra de energía
        self.energia_frame = Frame(self.stats_frame)
        self.energia_frame.pack(fill=X, pady=5)
        
        Label(self.energia_frame, text="Energía:", font=("Arial", 10, "bold")).pack(side=LEFT)
        
        self.barra_energia_frame = Frame(self.energia_frame, bg="lightgray", height=22, width=250)
        self.barra_energia_frame.pack(side=LEFT, padx=8)
        self.barra_energia_frame.pack_propagate(False)
        
        self.barra_energia = Frame(self.barra_energia_frame, bg="green", height=22)
        self.barra_energia.pack(side=LEFT)
        
        self.label_energia = Label(self.energia_frame, text="100%", font=("Arial", 10, "bold"), width=5)
        self.label_energia.pack(side=LEFT, padx=5)
        
        self.label_correr = Label(self.energia_frame, text="Modo: CAMINANDO", font=("Arial", 10, "bold"), 
                                 fg="blue", padx=10)
        self.label_correr.pack(side=LEFT)
        
        # Panel de tiempo y puntuación
        self.tiempo_frame = Frame(self.stats_frame)
        self.tiempo_frame.pack(fill=X, pady=5)
        
        self.label_tiempo = Label(self.tiempo_frame, text="Tiempo: 0.0s", font=("Arial", 10, "bold"))
        self.label_tiempo.pack(side=LEFT, padx=20)
        
        self.label_puntaje = Label(self.tiempo_frame, text="Puntos: 0", font=("Arial", 10, "bold"), fg="green")
        self.label_puntaje.pack(side=LEFT, padx=20)
        
        self.label_dificultad = Label(self.tiempo_frame, text="Dificultad: -", font=("Arial", 10, "bold"))
        self.label_dificultad.pack(side=LEFT, padx=20)
        
        self.label_enemigos = Label(self.tiempo_frame, text="Cazadores: 0", font=("Arial", 10, "bold"), fg="orange")
        self.label_enemigos.pack(side=LEFT, padx=20)

        # Frame para contenido principal
        self.contenido_frame = Frame(main_frame)
        self.contenido_frame.pack(fill=BOTH, expand=True)
        
        # Leyenda a la IZQUIERDA
        self.leyenda_frame = Frame(self.contenido_frame, width=180, bg="lightgray")
        self.leyenda_frame.pack(side=LEFT, fill=Y, padx=(0, 15))
        self.leyenda_frame.pack_propagate(False)
        
        # Frame para el mapa
        self.mapa_frame = Frame(self.contenido_frame, bg="white")
        self.mapa_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Canvas para el mapa (se crea después)
        self.canvas = None
        
        # Bind de teclado
        self.ventana.bind('<KeyPress>', self.manejar_teclado)
        self.ventana.focus_set()
    
    def detener_bucles(self):
        """Detiene todos los bucles de actualización"""
        self.juego_activo = False
        
        # Cancelar bucles programados
        if self.bucle_energia_id:
            self.ventana.after_cancel(self.bucle_energia_id)
            self.bucle_energia_id = None
        
        if self.bucle_enemigos_id:
            self.ventana.after_cancel(self.bucle_enemigos_id)
            self.bucle_enemigos_id = None
            
        if self.bucle_tiempo_id:
            self.ventana.after_cancel(self.bucle_tiempo_id)
            self.bucle_tiempo_id = None

    def mostrar_pantalla_inicio(self):
        """Muestra la pantalla de selección de dificultad"""
        self.detener_bucles()
        self.limpiar_interfaz_juego()
        
        # Título
        titulo = Label(self.contenido_frame, text="MODO ESCAPA", font=("Arial", 24, "bold"), fg="darkblue")
        titulo.pack(pady=20)
        
        # Descripción
        descripcion = Label(self.contenido_frame, text="Selecciona la dificultad:", font=("Arial", 12), justify=CENTER)
        descripcion.pack(pady=20)
        
        # Botones de dificultad
        dificultades_frame = Frame(self.contenido_frame)
        dificultades_frame.pack(pady=30)
        
        dificultades = [
            ("Fácil", "facil", "2 cazadores"),
            ("Normal", "normal", "3 cazadores"), 
            ("Difícil", "dificil", "4 cazadores"),
            ("Extremo", "extremo", "5 cazadores")
        ]
        
        for nombre, clave, desc in dificultades:
            btn_frame = Frame(dificultades_frame)
            btn_frame.pack(side=LEFT, padx=15)
            
            Button(btn_frame, text=nombre, font=("Arial", 11, "bold"),
                  command=lambda c=clave: self.iniciar_juego(c),
                  width=12, height=3, bg="lightblue").pack()
            
            Label(btn_frame, text=desc, font=("Arial", 8), justify=CENTER).pack(pady=5)
    
    def limpiar_interfaz_juego(self):
        """Limpia la interfaz para el juego"""
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        # Recrear leyenda y mapa frame
        self.leyenda_frame = Frame(self.contenido_frame, width=180, bg="lightgray")
        self.leyenda_frame.pack(side=LEFT, fill=Y, padx=(0, 15))
        self.leyenda_frame.pack_propagate(False)
        
        self.mapa_frame = Frame(self.contenido_frame, bg="white")
        self.mapa_frame.pack(side=RIGHT, fill=BOTH, expand=True)
    
    def crear_leyenda_juego(self):
        """Crea la leyenda durante el juego"""
        Label(self.leyenda_frame, text="MODO ESCAPA", font=("Arial", 12, "bold"), 
              bg="lightgray", pady=15).pack()
        
        bloques = [
            "Gris - Camino",
            "Negro - Muro", 
            "Azul - Túnel",
            "Verde - Lianas",
            "Amarillo - Salida",
            "Rojo - Posición salida",
            "Azul - Jugador caminando",
            "Rojo - Jugador corriendo",
            "Naranja - Cazadores"
        ]
        
        for bloque in bloques:
            Label(self.leyenda_frame, text=bloque, font=("Arial", 9), 
                  bg="lightgray", justify=LEFT, anchor="w", 
                  padx=10, pady=5).pack(fill=X)
            Frame(self.leyenda_frame, bg="darkgray", height=1).pack(fill=X, padx=5)
    
    def crear_mapa_juego(self):
        """Crea el canvas del mapa durante el juego"""
        # Scrollbars para el mapa
        v_scrollbar = Scrollbar(self.mapa_frame, orient=VERTICAL)
        h_scrollbar = Scrollbar(self.mapa_frame, orient=HORIZONTAL)
        
        v_scrollbar.pack(side=RIGHT, fill=Y)
        h_scrollbar.pack(side=BOTTOM, fill=X)
        
        # Canvas con scrollbars
        self.canvas = Canvas(self.mapa_frame, 
                            width=self.COLUMNAS * self.TAM_CELDA,
                            height=self.FILAS * self.TAM_CELDA,
                            bg="white", 
                            yscrollcommand=v_scrollbar.set,
                            xscrollcommand=h_scrollbar.set)
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
    
    def iniciar_juego(self, nivel_dificultad):
        """Inicia el juego con la dificultad seleccionada"""
        self.detener_bucles()
        self.dificultad = Dificultad(nivel_dificultad)
        config = self.dificultad.get_configuracion()
        
        # Configurar interfaz de juego
        self.limpiar_interfaz_juego()
        self.crear_leyenda_juego()
        self.crear_mapa_juego()
        
        # Generar juego
        self.generar_mapa()
        
        # Configurar botones de control
        self.mostrar_controles_juego()
        
        # Iniciar estado del juego
        self.juego_activo = True
        self.tiempo_inicio = time.time()
        self.puntaje = 0
        
        # Actualizar interfaz
        self.actualizar_estadisticas()
        self.label_info.config(text=f"¡Escapa! {config['nombre']} - {config['cantidad_enemigos']} cazadores")
        
        # Iniciar bucles de actualización
        self.actualizar_energia()
        self.actualizar_enemigos()
        self.actualizar_tiempo()
        
        print(f"Juego iniciado - Dificultad: {config['nombre']}")
    
    def mostrar_controles_juego(self):
        """Muestra los controles durante el juego"""
        for widget in self.control_frame.winfo_children():
            widget.destroy()
        
        Button(self.control_frame, text="Reiniciar", command=self.reiniciar_juego).pack(side=LEFT, padx=5)
        Button(self.control_frame, text="Menú Principal", command=self.mostrar_pantalla_inicio).pack(side=LEFT, padx=5)
    
    def actualizar_energia(self):
        if hasattr(self, 'jugador') and self.juego_activo:
            self.jugador.recuperar_energia()
            
            porcentaje = self.jugador.get_energia_porcentaje()
            ancho_barra = int(250 * (porcentaje / 100))
            
            self.barra_energia.config(width=ancho_barra)
            
            if porcentaje > 60:
                color = "green"
            elif porcentaje > 25:
                color = "orange"
            else:
                color = "red"
            self.barra_energia.config(bg=color)
            
            self.label_energia.config(text=f"{int(porcentaje)}%")
            
            if self.jugador.corriendo:
                self.label_correr.config(text="Modo: CORRIENDO ", fg="red")
            else:
                self.label_correr.config(text="Modo: CAMINANDO ", fg="blue")
        
        if self.juego_activo:
            self.bucle_energia_id = self.ventana.after(100, self.actualizar_energia)
    
    def actualizar_tiempo(self):
        """Actualiza el tiempo transcurrido"""
        if self.juego_activo:
            tiempo_actual = time.time() - self.tiempo_inicio
            self.label_tiempo.config(text=f"Tiempo: {tiempo_actual:.1f}s")
            self.bucle_tiempo_id = self.ventana.after(100, self.actualizar_tiempo)
    
    def actualizar_estadisticas(self):
        """Actualiza todas las estadísticas"""
        if hasattr(self, 'dificultad') and hasattr(self, 'enemigos'):
            config = self.dificultad.get_configuracion()
            self.label_dificultad.config(text=f"Dificultad: {config['nombre']}")
            self.label_enemigos.config(text=f"Cazadores: {len(self.enemigos)}")
            self.bucle_tiempo_id = self.ventana.after(100, self.actualizar_tiempo)
    
    def calcular_puntaje_victoria(self):
        """Calcula el puntaje basado en tiempo y dificultad"""
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        config = self.dificultad.get_configuracion()
        
        # Fórmula: Puntos base - tiempo + bonus por dificultad
        puntos_base = 1000
        puntos_tiempo = max(0, puntos_base - int(tiempo_transcurrido * 10))
        puntos_final = puntos_tiempo * config['multiplicador_puntos']
        
        return int(puntos_final), tiempo_transcurrido
    
    def generar_mapa(self):
        """Genera un nuevo mapa con jugador y enemigos"""
        print("Generando nuevo mapa...")
        self.mapa = Mapa(self.FILAS, self.COLUMNAS, self.TIPOS)
        self.crear_jugador_aleatorio()
        self.crear_enemigos_aleatorios()
        self.dibujar_mapa()
        
        if self.mapa.salidas and hasattr(self, 'jugador'):
            info_text = f"¡Encuentra la salida! Cazadores: {len(self.enemigos)}"
            self.label_info.config(text=info_text, fg="blue")
        else:
            self.label_info.config(text="Mapa generado - Busca la salida!", fg="blue")
        
        print(f"Mapa generado con {len(self.mapa.salidas)} salida(s) y {len(self.enemigos)} cazador(es)")
    
    def crear_jugador_aleatorio(self):
        """Crea un jugador en una posición aleatoria válida"""
        posiciones_validas = []
        
        for f in range(self.FILAS):
            for c in range(self.COLUMNAS):
                if self.mapa.es_posicion_valida(f, c, es_jugador=True):
                    posiciones_validas.append((f, c))
        
        if posiciones_validas:
            posiciones_sin_salida = [pos for pos in posiciones_validas if pos not in self.mapa.salidas]
            if posiciones_sin_salida:
                fila, columna = random.choice(posiciones_sin_salida)
            else:
                fila, columna = random.choice(posiciones_validas)
                
            self.jugador = Jugador(fila, columna)
            print(f"Jugador creado en posición: ({fila}, {columna})")
        else:
            self.jugador = Jugador(1, 1)
            self.mapa.grid[1][1] = Casilla(Camino())
            print("Jugador creado en posición forzada: (1, 1)")
    
    def crear_enemigos_aleatorios(self):
        """Crea enemigos en posiciones aleatorias válidas"""
        self.enemigos = []
        config = self.dificultad.get_configuracion()
        posiciones_validas = []
        
        # Buscar posiciones válidas para enemigos (lejos del jugador)
        for f in range(self.FILAS):
            for c in range(self.COLUMNAS):
                if (self.mapa.es_posicion_valida(f, c, es_jugador=False) and
                    (f, c) != (self.jugador.fila, self.jugador.columna) and
                    (f, c) not in self.mapa.salidas):
                    
                    # Calcular distancia al jugador
                    distancia = abs(f - self.jugador.fila) + abs(c - self.jugador.columna)
                    if distancia > 5:  # Solo posiciones lejanas al jugador
                        posiciones_validas.append((f, c))
        
        # Crear enemigos (máximo la cantidad configurada)
        cantidad = min(config['cantidad_enemigos'], len(posiciones_validas))
        
        for i in range(cantidad):
            if posiciones_validas:
                fila, columna = random.choice(posiciones_validas)
                posiciones_validas.remove((fila, columna))  # Evitar duplicados
                
                enemigo = Cazador(fila, columna, config['velocidad_enemigos'])
                self.enemigos.append(enemigo)
                print(f"Cazador {i+1} creado en posición: ({fila}, {columna})")
    
    def actualizar_enemigos(self):
        """Actualiza el movimiento de los enemigos cada 500ms"""
        if hasattr(self, 'enemigos') and self.juego_activo and hasattr(self, 'jugador'):
            for enemigo in self.enemigos:
                if enemigo.vivo:
                    enemigo.mover(self.jugador.fila, self.jugador.columna, self.mapa)
            
            # Verificar colisiones después de mover enemigos
            self.verificar_colision_enemigos()
            self.dibujar_mapa()
        
        # Programar siguiente actualización
        if self.juego_activo:
            self.ventana.after(500, self.actualizar_enemigos)
    
    def verificar_colision_enemigos(self):
        """Verifica si algún enemigo atrapó al jugador"""
        if not hasattr(self, 'jugador') or not self.juego_activo:
            return
        
        for enemigo in self.enemigos:
            if (enemigo.vivo and 
                enemigo.fila == self.jugador.fila and 
                enemigo.columna == self.jugador.columna):
                self.detener_bucles()
                self.juego_activo = False
                tiempo_transcurrido = time.time() - self.tiempo_inicio
                mensaje = f"¡PERDISTE! \nUn cazador te atrapó en {tiempo_transcurrido:.1f}s\nPuntos: {int(self.puntaje)}"
                self.label_info.config(text=mensaje, fg="red")
                print("¡PERDISTE! Jugador atrapado por un cazador")
                break
    
    def verificar_victoria(self):
        """Verifica si el jugador llegó a la salida"""
        if not hasattr(self, 'jugador') or not self.juego_activo:
            return False
        
        for f, c in self.mapa.salidas:
            if self.jugador.fila == f and self.jugador.columna == c:
                return True
        return False
    
    def mostrar_victoria(self):
        """Muestra la pantalla de victoria"""
        self.detener_bucles()
        self.juego_activo = False
        puntaje_final, tiempo_transcurrido = self.calcular_puntaje_victoria()
        self.puntaje = puntaje_final
        
        config = self.dificultad.get_configuracion()
        mensaje = f"¡VICTORIA! 🎉\nTiempo: {tiempo_transcurrido:.1f}s\nDificultad: {config['nombre']}\nPuntos: {puntaje_final}\nMultiplicador: {config['multiplicador_puntos']}x\nPresiona 'Reiniciar' para jugar otra vez"
        self.label_info.config(text=mensaje, fg="green")
        
        self.dibujar_mapa()
        self.actualizar_estadisticas()
        print(f"¡VICTORIA! Tiempo: {tiempo_transcurrido:.1f}s, Puntos: {puntaje_final}")
    
    def manejar_teclado(self, event):
        """Maneja el movimiento del jugador con teclado"""
        if not hasattr(self, 'jugador') or not self.juego_activo:
            return
        
        movimiento_realizado = False
        
        if event.keysym == 'Up':
            movimiento_realizado = self.jugador.mover(-1, 0, self.mapa)
        elif event.keysym == 'Down':
            movimiento_realizado = self.jugador.mover(1, 0, self.mapa)
        elif event.keysym == 'Left':
            movimiento_realizado = self.jugador.mover(0, -1, self.mapa)
        elif event.keysym == 'Right':
            movimiento_realizado = self.jugador.mover(0, 1, self.mapa)
        elif event.keysym == 'space':
            # Tecla ESPACIO para correr
            if self.jugador.toggle_correr():
                if self.jugador.corriendo:
                    print("Modo CORRER activado - Moverás 2 casillas por vez")
                else:
                    print("Modo CAMINAR activado")
            else:
                print("No hay suficiente energía para correr (mínimo 15%)")
            self.dibujar_mapa()
            return
        elif event.keysym.lower() == 'r':
            self.reiniciar_juego()
            return
        
        if movimiento_realizado:
            self.dibujar_mapa()
            
            if self.verificar_victoria():
                self.mostrar_victoria()
            else:
                self.actualizar_estadisticas()
    
    def reiniciar_juego(self):
        """Reinicia el juego con la misma dificultad"""
        if self.dificultad:
            self.detener_bucles()
            config = self.dificultad.get_configuracion()
            self.iniciar_juego(self.dificultad.nivel)
        else:
            self.mostrar_pantalla_inicio()
    
    def dibujar_mapa(self):
        """Dibuja el mapa completo con todos los elementos"""
        if not self.canvas:
            return
            
        self.canvas.delete("all")
        
        # Dibujar mapa completo
        for f in range(self.FILAS):
            for c in range(self.COLUMNAS):
                x1 = c * self.TAM_CELDA
                y1 = f * self.TAM_CELDA
                x2 = x1 + self.TAM_CELDA
                y2 = y1 + self.TAM_CELDA
                
                color = self.mapa.grid[f][c].get_color()
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="darkgray", width=1)
        
        # Marcar salidas
        for f, c in self.mapa.salidas:
            x = c * self.TAM_CELDA + self.TAM_CELDA // 2
            y = f * self.TAM_CELDA + self.TAM_CELDA // 2
            radio = self.TAM_CELDA // 2 - 2
            
            self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, 
                                   fill="red", outline="darkred", width=3)
            self.canvas.create_text(x, y, text="SAL", fill="white", 
                                   font=("Arial", 9, "bold"))
        
        # Dibujar jugador
        if hasattr(self, 'jugador'):
            x = self.jugador.columna * self.TAM_CELDA + self.TAM_CELDA // 2
            y = self.jugador.fila * self.TAM_CELDA + self.TAM_CELDA // 2
            radio = self.TAM_CELDA // 2 - 2
            
            if self.jugador.corriendo:
                color_jugador = "red"
                borde = "darkred"
                texto = "🏃"
            else:
                color_jugador = "blue"
                borde = "darkblue"
                texto = "J"
            
            self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, 
                                   fill=color_jugador, outline=borde, width=2)
            self.canvas.create_text(x, y, text=texto, fill="white", 
                                   font=("Arial", 10, "bold"))
        
        # Dibujar enemigos
        if hasattr(self, 'enemigos'):
            for i, enemigo in enumerate(self.enemigos):
                if enemigo.vivo:
                    x = enemigo.columna * self.TAM_CELDA + self.TAM_CELDA // 2
                    y = enemigo.fila * self.TAM_CELDA + self.TAM_CELDA // 2
                    radio = self.TAM_CELDA // 3
                    
                    # Cazador naranja
                    self.canvas.create_rectangle(x - radio, y - radio, x + radio, y + radio,
                                               fill="orange", outline="darkorange", width=2)
                    self.canvas.create_text(x, y, text="C", fill="white", 
                                           font=("Arial", 8, "bold"))
        
        # Actualizar región de scroll
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def ejecutar(self):
        """Inicia la aplicación"""
        self.ventana.mainloop()

if __name__ == "__main__":
    print("Laberinto - Modo Escapa")
    print("=" * 50)
    app = Main()
    app.ejecutar()