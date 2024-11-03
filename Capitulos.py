import pygame
import sys
import random
import Capitulo1  # Asegúrate de que este módulo exista

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Dimensiones iniciales de la ventana (esto se ajustará después)
ANCHO = 700
ALTO = 700

# Crear la ventana del juego (redimensionable)
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Alien Blasters - Selección de Capítulos")

# Definir colores
BLANCO = (255, 255, 255)

# Cargar la tipografía pixel desde el archivo .ttf
tipografia_pixel = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 25)
tipografia_boton = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 15)

# Clase para las estrellas
class Estrella:
    def __init__(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(0, ALTO)
        self.velocidad = random.uniform(1, 3)

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, BLANCO, (self.x, self.y), 2)

    def mover(self):
        self.y += self.velocidad
        if self.y > ALTO:
            self.y = 0
            self.x = random.randint(0, ANCHO)

# Crear un grupo de estrellas
estrellas = [Estrella() for _ in range(100)]

# Función para ajustar el tamaño de las estrellas cuando la ventana cambia de tamaño
def redimensionar_estrellas():
    global estrellas
    estrellas = [Estrella() for _ in range(100)]

# Función para redimensionar componentes de la pantalla
def redimensionar_componentes():
    global ANCHO, ALTO
    ANCHO, ALTO = ventana.get_size()
    redimensionar_estrellas()  # Ajustar las estrellas al tamaño de la pantalla

# Función para dibujar el botón con bordes redondeados y la animación de agrandarse
def dibujar_boton(ventana, texto, x, y, ancho, alto, hover=False, radio_borde=15):
    if hover:
        ancho *= 1.1
        alto *= 1.1

    boton_rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(ventana, BLANCO, boton_rect, border_radius=radio_borde, width=2)

    # Dibujar el texto dentro del botón
    texto_boton = tipografia_boton.render(texto, True, BLANCO)
    ventana.blit(texto_boton, (x + (ancho - texto_boton.get_width()) // 2, y + (alto - texto_boton.get_height()) // 2))

# Función principal de la pantalla de capítulos
def mostrar_capitulos():
    while True:
        redimensionar_componentes()  # Ajustar el tamaño de los componentes

        ventana.fill((0, 0, 0))  # Fondo negro

        # Animar estrellas
        for estrella in estrellas:
            estrella.mover()
            estrella.dibujar(ventana)

        # Texto de selección de capítulos
        texto_seleccion = tipografia_pixel.render("Selección de capítulos", True, BLANCO)
        ventana.blit(texto_seleccion, (ANCHO // 2 - texto_seleccion.get_width() // 2, ALTO // 8))

        # Dimensiones del botón
        boton_ancho = ANCHO // 3
        boton_alto = ALTO // 10
        boton_x = ANCHO // 2 - boton_ancho // 2
        boton_y = ALTO // 2

        # Obtener la posición del ratón
        mouse_pos = pygame.mouse.get_pos()

        # Verificar si el ratón está sobre el botón
        hover = boton_x <= mouse_pos[0] <= boton_x + boton_ancho and boton_y <= mouse_pos[1] <= boton_y + boton_alto

        # Cambiar el cursor a mano si está sobre el botón
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Dibujar el botón
        dibujar_boton(ventana, "Capítulo 1", boton_x, boton_y, boton_ancho, boton_alto, hover=hover)

        # Texto "Controles" en la esquina inferior derecha
        texto_controles = tipografia_boton.render("Controles", True, BLANCO)
        ventana.blit(texto_controles, (ANCHO - texto_controles.get_width() - 10, ALTO - texto_controles.get_height() - 10))

        # Verificar si el ratón está sobre el texto de "Controles"
        hover_controles = ANCHO - texto_controles.get_width() - 10 <= mouse_pos[0] <= ANCHO - 10 and \
                          ALTO - texto_controles.get_height() - 10 <= mouse_pos[1] <= ALTO - 10

        # Cambiar el cursor a mano si está sobre el texto
        if hover_controles:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if hover:  # Si se hace clic en el botón de Capítulo 1
                    Capitulo1.mostrar_capitulo1()  # Cambia esto según la función que uses para abrir el capítulo 1
                if hover_controles:  # Si se hace clic en "Controles"
                    mostrar_controles()

            elif evento.type == pygame.VIDEORESIZE:
                redimensionar_componentes()

        pygame.display.update()

# Función para abrir la pantalla de controles
def mostrar_controles():
    import Controles  # Importar aquí para evitar el problema de importación circular
    Controles.mostrar_controles(mostrar_capitulos)  # Pasar la función de regreso

if __name__ == "__main__":
    mostrar_capitulos()
