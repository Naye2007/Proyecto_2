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
from trampa import Trampa 

class Main:
    def __init__(self):
        self.TAM_CELDA = 25
        self.FILAS = 20
        self.COLUMNAS = 25
        self.TIPOS = {"Camino": Camino, "Muro": Muro, "Tunel": Tunel, "Liana": Liana}
        self.juego_activo = False
        self.modo_escape = True
        self.tiempo_inicio = 0
        self.puntaje = 0
        self.dificultad = None
        self.bucle_energia_id = None
        self.bucle_enemigos_id = None
        self.bucle_tiempo_id = None
        self.ventana = Tk()
        self.ventana.title("Laberinto - Modo Escapa")
        self.ventana.geometry("1200x800")
        self.ventana.resizable(True, True)
        
        self.crear_interfaz()
        
        self.mostrar_pantalla_inicio()
    
    def crear_interfaz(self):
        main_frame = Frame(self.ventana)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.control_frame = Frame(main_frame)
        self.control_frame.pack(fill=X, pady=5)
        self.control_frame.pack_forget()  

        self.info_frame = Frame(main_frame)
        self.info_frame.pack(fill=X, pady=5)
        self.info_frame.pack_forget()  
        
        self.label_info = Label(self.info_frame, text="", font=("Arial", 12), fg="blue", wraplength=1000)
        self.label_info.pack()

        self.stats_frame = Frame(main_frame)
        self.stats_frame.pack(fill=X, pady=8)
        self.stats_frame.pack_forget() 
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

        self.contenido_frame = Frame(main_frame)
        self.contenido_frame.pack(fill=BOTH, expand=True)

        self.leyenda_frame = None
        self.mapa_frame = None
        self.canvas = None

        self.ventana.bind('<KeyPress>', self.manejar_teclado)
        self.ventana.focus_set()
    
    def detener_bucles(self):
        self.juego_activo = False
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
        self.detener_bucles()
        self.control_frame.pack_forget()
        self.info_frame.pack_forget()
        self.stats_frame.pack_forget()
        self.limpiar_interfaz_juego()

        titulo = Label(self.contenido_frame, text="ESCAPA DEL LABERINTO", 
                    font=("Arial", 28, "bold"), fg="darkblue")
        titulo.pack(pady=30)

        modos_frame = Frame(self.contenido_frame)
        modos_frame.pack(pady=40)
        
        modo_escape_frame = Frame(modos_frame, bg="lightblue", padx=20, pady=20)
        modo_escape_frame.pack(side=LEFT, padx=30)
        
        Label(modo_escape_frame, text="MODO ESCAPA", font=("Arial", 16, "bold"), 
            bg="lightblue", fg="darkblue").pack(pady=10)
        
        desc_escape = """Huye de los cazadores
    Llega a la salida
    Usa trampas estratégicas
    +Puntos por tiempo rápido"""
        
        Label(modo_escape_frame, text=desc_escape, font=("Arial", 11), 
            bg="lightblue", justify=LEFT).pack(pady=10)
        
        Button(modo_escape_frame, text="JUGAR MODO ESCAPA", 
            font=("Arial", 12, "bold"), bg="blue", fg="white",
            command=lambda: self.mostrar_seleccion_dificultad("escape"),
            width=20, height=2).pack(pady=10)
        
        modo_cazador_frame = Frame(modos_frame, bg="lightgreen", padx=20, pady=20)
        modo_cazador_frame.pack(side=LEFT, padx=30)
        
        Label(modo_cazador_frame, text="MODO CAZADOR", font=("Arial", 16, "bold"), 
            bg="lightgreen", fg="darkgreen").pack(pady=10)
        
        desc_cazador = """Tú eres el cazador
    Atrapa a los enemigos
    Evita que escapen
    +Puntos por capturas"""
        
        Label(modo_cazador_frame, text=desc_cazador, font=("Arial", 11), 
            bg="lightgreen", justify=LEFT).pack(pady=10)
        
        Button(modo_cazador_frame, text="PRÓXIMAMENTE", 
            font=("Arial", 12, "bold"), bg="gray", fg="white",
            state="disabled", 
            width=20, height=2).pack(pady=10)
    

    def limpiar_interfaz_juego(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        self.leyenda_frame = Frame(self.contenido_frame, width=180, bg="lightgray")
        self.leyenda_frame.pack(side=LEFT, fill=Y, padx=(0, 15))
        self.leyenda_frame.pack_propagate(False)
        
        self.mapa_frame = Frame(self.contenido_frame, bg="white")
        self.mapa_frame.pack(side=RIGHT, fill=BOTH, expand=True)
    
    def crear_leyenda_juego(self):
        Label(self.leyenda_frame, text="MODO ESCAPA", font=("Arial", 12, "bold"), 
            bg="lightgray", pady=10).pack(fill=X)
        
        secciones = [
            ("CONTROLES", 
            "Flechas: Moverse\nEspacio: Correr\nT: Trampa\nR: Reiniciar\n\nMáx 3 trampas\nCooldown 5s"),
            
            ("PUNTUACIÓN", 
            "POR TIEMPO:\n<30s: 100 pts\n30-50s: 50 pts\n>50s: 25 pts\n\nPOR ELIMINACIONES:\nCada cazador: 100 pts"),
            
            ("COLORES",
            "Gris - Camino\nNegro - Muro\nAzul - Túnel\nVerde - Lianas\nAmarillo - Salida\nAzul - Jugador\nRojo - Corriendo\nNaranja - Cazadores\nMorado - Trampas")
        ]
        
        for titulo, contenido in secciones:

            frame_seccion = Frame(self.leyenda_frame, bg="white", relief="raised", bd=1)
            frame_seccion.pack(fill=X, padx=5, pady=3)

            Label(frame_seccion, text=titulo, font=("Arial", 10, "bold"), 
                bg="lightblue", fg="black").pack(fill=X, padx=2, pady=2)

            Label(frame_seccion, text=contenido, font=("Arial", 9), 
                bg="white", justify=LEFT, anchor="w").pack(fill=X, padx=8, pady=5)


    def mostrar_seleccion_dificultad(self, modo_juego):
        self.detener_bucles()
        self.control_frame.pack_forget()
        self.info_frame.pack_forget()
        self.stats_frame.pack_forget()
        self.limpiar_interfaz_juego()
        
        self.modo_juego_actual = modo_juego
        
        titulo_modo = "MODO ESCAPA" if modo_juego == "escape" else "MODO CAZADOR"
        color_modo = "darkblue" if modo_juego == "escape" else "darkgreen"

        titulo = Label(self.contenido_frame, text=titulo_modo, 
                    font=("Arial", 24, "bold"), fg=color_modo)
        titulo.pack(pady=20)
        
        descripcion = Label(self.contenido_frame, 
                            text="Selecciona la dificultad:\nMayor dificultad = más cazadores = más puntos", 
                            font=("Arial", 12), justify=CENTER)
        descripcion.pack(pady=20)
        
        dificultades_frame = Frame(self.contenido_frame)
        dificultades_frame.pack(pady=30)
        
        dificultades = [
            ("Fácil", "facil", "2 cazador"),
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

        Button(self.contenido_frame, text="Volver al Menú Principal", 
            font=("Arial", 10), command=self.mostrar_pantalla_inicio).pack(pady=20)
    
    def crear_mapa_juego(self):
        v_scrollbar = Scrollbar(self.mapa_frame, orient=VERTICAL)
        h_scrollbar = Scrollbar(self.mapa_frame, orient=HORIZONTAL)
        
        v_scrollbar.pack(side=RIGHT, fill=Y)
        h_scrollbar.pack(side=BOTTOM, fill=X)

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
        self.detener_bucles()
        
        self.dificultad = Dificultad(nivel_dificultad)
        config = self.dificultad.get_configuracion()
        self.control_frame.pack(fill=X, pady=5)
        self.info_frame.pack(fill=X, pady=5)
        self.stats_frame.pack(fill=X, pady=8)

        self.limpiar_interfaz_juego()
        self.crear_leyenda_juego()
        self.crear_mapa_juego()
        self.generar_mapa()
        self.mostrar_controles_juego()
        self.juego_activo = True
        self.tiempo_inicio = time.time()
        self.puntaje = 0
        self.actualizar_estadisticas()
        if hasattr(self, 'modo_juego_actual') and self.modo_juego_actual == "escape":
            self.label_info.config(text=f"¡Modo Escapa! {config['nombre']} - {config['cantidad_enemigos']} cazadores")
        else:
            self.label_info.config(text=f"¡Modo Cazador! {config['nombre']} - {config['cantidad_enemigos']} cazadores")
        self.actualizar_energia()
        self.actualizar_enemigos()
        self.actualizar_tiempo()
        
    
    def mostrar_controles_juego(self):
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
        if self.juego_activo:
            tiempo_actual = time.time() - self.tiempo_inicio
            self.label_tiempo.config(text=f"Tiempo: {tiempo_actual:.1f}s")
            self.actualizar_estadisticas()  
            self.bucle_tiempo_id = self.ventana.after(1000, self.actualizar_tiempo)
        
    def actualizar_estadisticas(self):
        if hasattr(self, 'dificultad') and hasattr(self, 'enemigos'):
            config = self.dificultad.get_configuracion()
            self.label_dificultad.config(text=f"Dificultad: {config['nombre']}")
            self.label_enemigos.config(text=f"Cazadores: {len(self.enemigos)}")
            self.label_puntaje.config(text=f"Puntos: {int(self.puntaje)}")
        
    def calcular_puntaje_victoria(self):
        tiempo_transcurrido = time.time() - self.tiempo_inicio

        if tiempo_transcurrido < 30:
            puntos_por_tiempo = 100
            bonificacion_tiempo = "Tiempo < 30s: +100 pts"
        elif tiempo_transcurrido < 50:
            puntos_por_tiempo = 50
            bonificacion_tiempo = "Tiempo 30-50s: +50 pts"
        else:
            puntos_por_tiempo = 25
            bonificacion_tiempo = "Tiempo > 50s: +25 pts"
        

        puntos_por_eliminaciones = self.puntaje
        
        puntos_final = puntos_por_tiempo + puntos_por_eliminaciones
        
        return {
            'puntos_final': int(puntos_final),
            'tiempo_transcurrido': tiempo_transcurrido,
            'puntos_tiempo': puntos_por_tiempo,
            'bonificacion_tiempo': bonificacion_tiempo,
            'puntos_eliminaciones': puntos_por_eliminaciones,
            'eliminaciones': self.puntaje // 100}
    def generar_mapa(self):
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

    
    def crear_jugador_aleatorio(self):
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
        else:
            self.jugador = Jugador(1, 1)
            self.mapa.grid[1][1] = Casilla(Camino())
    
    def crear_enemigos_aleatorios(self):
        self.enemigos = []
        config = self.dificultad.get_configuracion()
        posiciones_validas = []
    
        for f in range(self.FILAS):
            for c in range(self.COLUMNAS):
                if (self.mapa.es_posicion_valida(f, c, es_jugador=False) and
                    (f, c) != (self.jugador.fila, self.jugador.columna) and
                    (f, c) not in self.mapa.salidas):
                    
                    distancia = abs(f - self.jugador.fila) + abs(c - self.jugador.columna)
                    if distancia > 5:  
                        posiciones_validas.append((f, c))
        
        cantidad = min(config['cantidad_enemigos'], len(posiciones_validas))
        
        for i in range(cantidad):
            if posiciones_validas:
                fila, columna = random.choice(posiciones_validas)
                posiciones_validas.remove((fila, columna))  
                
                enemigo = Cazador(fila, columna, config['velocidad_enemigos'])
                self.enemigos.append(enemigo)
                print(f"Cazador {i+1} creado en posición: ({fila}, {columna})")
    
    def actualizar_enemigos(self):
        if hasattr(self, 'enemigos') and self.juego_activo and hasattr(self, 'jugador'):
            self.verificar_trampas_enemigos()
            self.reaparecer_enemigos()
            for enemigo in self.enemigos:
                if enemigo.vivo:
                    enemigo.mover(self.jugador.fila, self.jugador.columna, self.mapa)
            self.verificar_colision_enemigos()
            self.dibujar_mapa()
        if self.juego_activo:
            self.bucle_enemigos_id = self.ventana.after(700, self.actualizar_enemigos)
    
    def verificar_colision_enemigos(self):
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
        if not hasattr(self, 'jugador') or not self.juego_activo:
            return False
        
        for f, c in self.mapa.salidas:
            if self.jugador.fila == f and self.jugador.columna == c:
                return True
        return False
    
    def mostrar_victoria(self):
        self.detener_bucles()
        puntaje_detalle = self.calcular_puntaje_victoria()
        self.puntaje = puntaje_detalle['puntos_final']
        
        mensaje = f"""¡VICTORIA!

    Tiempo: {puntaje_detalle['tiempo_transcurrido']:.1f}s

    DESGLOSE DE PUNTOS:
    {puntaje_detalle['bonificacion_tiempo']}
    Eliminaciones: {puntaje_detalle['eliminaciones']} cazadores = +{puntaje_detalle['puntos_eliminaciones']} pts

    PUNTOS TOTALES: {puntaje_detalle['puntos_final']}

    Presiona 'Reiniciar' para jugar otra vez"""
        
        self.label_info.config(text=mensaje, fg="green", justify=LEFT)
        
        self.dibujar_mapa()
        self.actualizar_estadisticas()
        print(f"¡VICTORIA! Puntos: {puntaje_detalle['puntos_final']}")
    
    def reiniciar_juego(self):
        if self.dificultad:
            self.detener_bucles()
            config = self.dificultad.get_configuracion()
            self.iniciar_juego(self.dificultad.nivel)
        else:
            self.mostrar_pantalla_inicio()
    
    def dibujar_mapa(self):
        if not self.canvas:
            return
            
        self.canvas.delete("all")
        
        for f in range(self.FILAS):
            for c in range(self.COLUMNAS):
                x1 = c * self.TAM_CELDA
                y1 = f * self.TAM_CELDA
                x2 = x1 + self.TAM_CELDA
                y2 = y1 + self.TAM_CELDA
                
                color = self.mapa.grid[f][c].get_color()
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="darkgray", width=1)
        for f, c in self.mapa.salidas:
            x = c * self.TAM_CELDA + self.TAM_CELDA // 2
            y = f * self.TAM_CELDA + self.TAM_CELDA // 2
            radio = self.TAM_CELDA // 2 - 2
            
            self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, 
                                   fill="red", outline="darkred", width=3)
            self.canvas.create_text(x, y, text="SAL", fill="white", 
                                   font=("Arial", 9, "bold"))
        
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

        if hasattr(self, 'jugador'):
            for trampa in self.jugador.get_trampas_activas():
                x = trampa.columna * self.TAM_CELDA + self.TAM_CELDA // 2
                y = trampa.fila * self.TAM_CELDA + self.TAM_CELDA // 2
                radio = self.TAM_CELDA // 4
                self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio,
                                    fill="purple", outline="darkviolet", width=2)
                self.canvas.create_text(x, y, text="T", fill="white", 
                                    font=("Arial", 7, "bold"))
                

        if hasattr(self, 'enemigos'):
            for i, enemigo in enumerate(self.enemigos):
                if enemigo.vivo:
                    x = enemigo.columna * self.TAM_CELDA + self.TAM_CELDA // 2
                    y = enemigo.fila * self.TAM_CELDA + self.TAM_CELDA // 2
                    radio = self.TAM_CELDA // 3
                    
                    self.canvas.create_rectangle(x - radio, y - radio, x + radio, y + radio,
                                               fill="orange", outline="darkorange", width=2)
                    self.canvas.create_text(x, y, text="C", fill="white", 
                                           font=("Arial", 8, "bold"))
        
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def verificar_trampas_enemigos(self):
        if not hasattr(self, 'jugador') or not hasattr(self, 'enemigos'):
            return
        
        trampas_a_eliminar = []
        enemigos_a_eliminar = []

        for trampa in self.jugador.get_trampas_activas():
            for enemigo in self.enemigos:
                if (enemigo.vivo and 
                    enemigo.fila == trampa.fila and 
                    enemigo.columna == trampa.columna):
                    print(f" ¡Trampa activada! Cazador eliminado en ({enemigo.fila}, {enemigo.columna})")
                    enemigo.vivo = False
                    enemigo.tiempo_muerte = time.time()
                    enemigos_a_eliminar.append(enemigo)
                    trampa.desactivar()
                    trampas_a_eliminar.append(trampa)
                    bono_puntos = 100
                    self.puntaje += bono_puntos
                    print(f" +{bono_puntos} puntos por eliminar cazador")
                    self.actualizar_estadisticas()
                    
                    break  
        
        for trampa in trampas_a_eliminar:
            self.jugador.eliminar_trampa(trampa)


    def reaparecer_enemigos(self):
        if not hasattr(self, 'enemigos'):
            return
        
        tiempo_actual = time.time()
        
        for enemigo in self.enemigos:
            if not enemigo.vivo and hasattr(enemigo, 'tiempo_muerte'):
                if tiempo_actual - enemigo.tiempo_muerte >= 10:
                    nueva_posicion = self.buscar_posicion_valida_enemigo()
                    if nueva_posicion:
                        fila, columna = nueva_posicion
                        enemigo.fila = fila
                        enemigo.columna = columna
                        enemigo.vivo = True 

    def buscar_posicion_valida_enemigo(self):
        posiciones_validas = []
        for f in range(self.FILAS):
            for c in range(self.COLUMNAS):
                if (self.mapa.es_posicion_valida(f, c, es_jugador=False) and
                    (f, c) != (self.jugador.fila, self.jugador.columna) and
                    (f, c) not in self.mapa.salidas):
                    distancia = abs(f - self.jugador.fila) + abs(c - self.jugador.columna)
                    if distancia > 3: 
                        posiciones_validas.append((f, c))
        if posiciones_validas:
            return random.choice(posiciones_validas)
        return None
    
    def manejar_teclado(self, event):
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
            if self.jugador.toggle_correr():
                if self.jugador.corriendo:
                    print("Modo CORRER activado")
                else:
                    print("Modo CAMINAR activado")
            else:
                print("No hay suficiente energía para correr (mínimo 15%)")
            self.dibujar_mapa()
            return
        elif event.keysym.lower() == 't': 
            if self.jugador.colocar_trampa(time.time()):
                self.dibujar_mapa()
                self.actualizar_estadisticas()
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

    def manejar_teclado(self, event):
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
            if self.jugador.toggle_correr():
                if self.jugador.corriendo:
                    print("Modo CORRER activado - Moverás 2 casillas por vez")
                else:
                    print("Modo CAMINAR activado")
            else:
                print("No hay suficiente energía para correr (mínimo 15%)")
            self.dibujar_mapa()
            return
        elif event.keysym.lower() == 't': 

            if self.jugador.colocar_trampa(time.time()):
                self.dibujar_mapa()
                self.actualizar_estadisticas()
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

    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    print("Laberinto - Modo Escapa")
    print("=" * 50)
    app = Main()
    app.ejecutar()