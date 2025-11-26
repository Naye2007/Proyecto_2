from tkinter import *
import random
from mapa import Mapa
from camino import Camino
from muro import Muro
from tunel import Tunel
from liana import Liana
from jugador import Jugador
from casilla import Casilla

class Main:
    def __init__(self):
        # Configuración inicial
        self.TAM_CELDA = 25
        self.FILAS = 20
        self.COLUMNAS = 25
        self.TIPOS = {"Camino": Camino, "Muro": Muro, "Tunel": Tunel, "Liana": Liana}
        self.juego_activo = True
        
        # Crear ventana principal
        self.ventana = Tk()
        self.ventana.title("Laberinto - Modo Escape")
        self.ventana.geometry("1100x750")
        self.ventana.resizable(True, True)
        
        # Crear widgets
        self.crear_interfaz()
        
        # Generar y mostrar mapa
        self.generar_mapa()
        
        # Iniciar bucle de actualización de energía
        self.actualizar_energia()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = Frame(self.ventana)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Panel de controles
        control_frame = Frame(main_frame)
        control_frame.pack(fill=X, pady=5)
        
        Button(control_frame, text="Nuevo Mapa", command=self.reiniciar_juego).pack(side=LEFT, padx=5)
        
        # Información del juego
        info_frame = Frame(main_frame)
        info_frame.pack(fill=X, pady=5)
        
        self.label_info = Label(info_frame, 
                               text="Usa FLECHAS para mover, ESPACIO para correr. ¡Llega a la SALIDA!",
                               font=("Arial", 11), fg="blue", wraplength=800)
        self.label_info.pack()
        
        # Barra de energía
        energia_frame = Frame(info_frame)
        energia_frame.pack(fill=X, pady=8)
        
        Label(energia_frame, text="Energía:", font=("Arial", 10, "bold")).pack(side=LEFT)
        
        # Frame para la barra de energía
        self.barra_energia_frame = Frame(energia_frame, bg="lightgray", height=22, width=250)
        self.barra_energia_frame.pack(side=LEFT, padx=8)
        self.barra_energia_frame.pack_propagate(False)
        
        # Barra de energía interior
        self.barra_energia = Frame(self.barra_energia_frame, bg="green", height=22)
        self.barra_energia.pack(side=LEFT)
        
        # Label de porcentaje
        self.label_energia = Label(energia_frame, text="100%", font=("Arial", 10, "bold"), width=5)
        self.label_energia.pack(side=LEFT, padx=5)
        
        # Estado de correr
        self.label_correr = Label(energia_frame, text="Modo: CAMINANDO", font=("Arial", 10, "bold"), 
                                 fg="blue", padx=10)
        self.label_correr.pack(side=LEFT)

        # Frame para contenido principal
        contenido_frame = Frame(main_frame)
        contenido_frame.pack(fill=BOTH, expand=True)
        
        # Leyenda a la IZQUIERDA (SOLO NOMBRES)
        leyenda_frame = Frame(contenido_frame, width=150, bg="lightgray")
        leyenda_frame.pack(side=LEFT, fill=Y, padx=(0, 15))
        leyenda_frame.pack_propagate(False)
        
        # Título de la leyenda
        Label(leyenda_frame, text="LEGENDA", font=("Arial", 12, "bold"), 
              bg="lightgray", pady=15).pack()
        
        # Solo nombres de los bloques
        bloques = [
            "Gris - Camino",
            "Negro - Muro", 
            "Azul - Túnel",
            "Verde - Lianas",
            "Amarillo - Salida",
            "Rojo - Posición salida",
            "Azul - Jugador caminando",
            "Rojo - Jugador corriendo"
        ]
        
        for bloque in bloques:
            Label(leyenda_frame, text=bloque, font=("Arial", 9), 
                  bg="lightgray", justify=LEFT, anchor="w", 
                  padx=10, pady=5).pack(fill=X)
            
            # Separador simple
            Frame(leyenda_frame, bg="darkgray", height=1).pack(fill=X, padx=5)
        
        # Frame para el mapa (ocupa el resto del espacio)
        mapa_frame = Frame(contenido_frame, bg="white")
        mapa_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Scrollbars para el mapa
        v_scrollbar = Scrollbar(mapa_frame, orient=VERTICAL)
        h_scrollbar = Scrollbar(mapa_frame, orient=HORIZONTAL)
        
        v_scrollbar.pack(side=RIGHT, fill=Y)
        h_scrollbar.pack(side=BOTTOM, fill=X)
        
        # Canvas con scrollbars
        self.canvas = Canvas(mapa_frame, 
                            width=self.COLUMNAS * self.TAM_CELDA,
                            height=self.FILAS * self.TAM_CELDA,
                            bg="white", 
                            yscrollcommand=v_scrollbar.set,
                            xscrollcommand=h_scrollbar.set,
                            scrollregion=(0, 0, self.COLUMNAS * self.TAM_CELDA, self.FILAS * self.TAM_CELDA))
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
        
        # Bind de teclado
        self.ventana.bind('<KeyPress>', self.manejar_teclado)
        self.ventana.focus_set()
    
    def actualizar_energia(self):
        """Actualiza la barra de energía cada 100ms"""
        if hasattr(self, 'jugador') and self.juego_activo:
            # Recuperar energía gradualmente
            self.jugador.recuperar_energia()
            
            # Actualizar barra visual
            porcentaje = self.jugador.get_energia_porcentaje()
            ancho_barra = int(250 * (porcentaje / 100))
            
            self.barra_energia.config(width=ancho_barra)
            
            # Cambiar color según el nivel de energía
            if porcentaje > 60:
                color = "green"
            elif porcentaje > 25:
                color = "orange"
            else:
                color = "red"
            self.barra_energia.config(bg=color)
            
            # Actualizar texto
            self.label_energia.config(text=f"{int(porcentaje)}%")
            
            # Actualizar estado de correr
            if self.jugador.corriendo:
                self.label_correr.config(text="Modo: CORRIENDO 🏃", fg="red")
            else:
                if self.jugador.puede_correr():
                    self.label_correr.config(text="Modo: CAMINANDO 🚶", fg="blue")
                else:
                    self.label_correr.config(text="Modo: CAMINANDO (sin energía)", fg="gray")
        
        # Programar siguiente actualización
        self.ventana.after(100, self.actualizar_energia)
    
    def generar_mapa(self):
        print("Generando nuevo mapa...")
        self.mapa = Mapa(self.FILAS, self.COLUMNAS, self.TIPOS)
        self.crear_jugador_aleatorio()
        self.juego_activo = True
        self.dibujar_mapa()
        
        if self.mapa.salidas and hasattr(self, 'jugador'):
            info_text = f"Jugador en: ({self.jugador.fila}, {self.jugador.columna}) | Salida en: {self.mapa.salidas[0]} | ¡Llega a la SALIDA roja!"
            self.label_info.config(text=info_text, fg="blue")
        else:
            self.label_info.config(text="Mapa generado - Busca la salida roja!", fg="blue")
        
        print(f"Mapa generado con {len(self.mapa.salidas)} salida(s)")
    
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
    
    def verificar_victoria(self):
        if not hasattr(self, 'jugador') or not self.juego_activo:
            return False
        
        for f, c in self.mapa.salidas:
            if self.jugador.fila == f and self.jugador.columna == c:
                return True
        return False
    
    def mostrar_victoria(self):
        self.juego_activo = False
        mensaje = f"¡VICTORIA! 🎉\nLlegaste a la salida en ({self.jugador.fila}, {self.jugador.columna})\nPresiona 'Nuevo Mapa' para jugar otra vez"
        self.label_info.config(text=mensaje, fg="green")
        
        # Dibujar celebración
        self.dibujar_mapa()
        
        print("¡VICTORIA! Jugador llegó a la salida")
    
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
                estado = "CORRIENDO" if self.jugador.corriendo else "Caminando"
                info_text = f"Jugador: ({self.jugador.fila}, {self.jugador.columna}) | {estado} | Energía: {int(self.jugador.get_energia_porcentaje())}% | Salida: {self.mapa.salidas[0]}"
                self.label_info.config(text=info_text, fg="blue")
    
    def reiniciar_juego(self):
        self.generar_mapa()
    
    def dibujar_mapa(self):
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
            
            # Círculo rojo grande para salida
            self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, 
                                   fill="red", outline="darkred", width=3)
            self.canvas.create_text(x, y, text="SAL", fill="white", 
                                   font=("Arial", 9, "bold"))
        
        # Dibujar jugador
        if hasattr(self, 'jugador'):
            x = self.jugador.columna * self.TAM_CELDA + self.TAM_CELDA // 2
            y = self.jugador.fila * self.TAM_CELDA + self.TAM_CELDA // 2
            radio = self.TAM_CELDA // 2 - 2
            
            # Color diferente si está corriendo
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
        
        # Actualizar región de scroll
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    print("Laberinto - Sistema de Energía y Correr Implementado")
    print("=" * 50)
    app = Main()
    app.ejecutar()