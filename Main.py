import pygame
import sys
from Capitulos import mostrar_capitulos

# Inicializar pygame
pygame.init()

# Inicializar pygame y el mixer de audio
pygame.mixer.init()  # Inicializar el mezclador de audio

# Cargar la música de fondo desde la carpeta OST
pygame.mixer.music.load("OST/OST Alien Blasters 3.mp3")

# Reproducir la música en bucle (-1 significa que se repetirá indefinidamente)
pygame.mixer.music.play(-1)

# Cargar el sonido que se reproducirá al hacer clic en el botón
sonido_click = pygame.mixer.Sound("OST/Toca para iniciar.mp3")  # Reemplaza con el nombre de tu archivo de sonido

# Función para detener la música si es necesario
def detener_musica():
    pygame.mixer.music.stop()

# Dimensiones iniciales de la ventana
ANCHO = 700
ALTO = 700

# Cargar la imagen de fondo
fondo = pygame.image.load("Assets/Alien Blasters.jpg")

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Crear la ventana del juego (redimensionable)
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Alien Blasters - Pantalla de Inicio")

# Tipografía
tipografia_pixel_grande = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 30)  # Título del juego
tipografia_pixel = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 10)  # Texto del botón
tipografia_pequeña = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 12)  # Texto del autor

# Función para redimensionar componentes
def redimensionar_componentes():
    global ANCHO, ALTO
    ANCHO, ALTO = ventana.get_size()

# Función para dibujar la imagen de fondo sin estirarla
def dibujar_fondo(ventana):
    fondo_ratio = fondo.get_width() / fondo.get_height()  # Relación de aspecto de la imagen
    ventana_ratio = ANCHO / ALTO  # Relación de aspecto de la ventana

    # Ajustar tamaño de la imagen manteniendo la proporción
    if ventana_ratio > fondo_ratio:
        nuevo_alto = ALTO
        nuevo_ancho = int(nuevo_alto * fondo_ratio)
    else:
        nuevo_ancho = ANCHO
        nuevo_alto = int(nuevo_ancho / fondo_ratio)

    fondo_escalado = pygame.transform.scale(fondo, (nuevo_ancho, nuevo_alto))
    ventana.blit(fondo_escalado, ((ANCHO - nuevo_ancho) // 2, (ALTO - nuevo_alto) // 2))

# Función para dibujar el botón con bordes redondeados y animación de agrandarse
def dibujar_boton(ventana, texto, x, y, ancho, alto, hover=False):
    # Cambiar el tamaño del botón si está en hover
    if hover:
        ancho *= 1.1  # Aumenta el ancho en 10%
        alto *= 1.1   # Aumenta el alto en 10%

    # Dibujar rectángulo redondeado
    boton_rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(ventana, BLANCO, boton_rect, border_radius=15, width=2)

    # Dibujar texto en el botón
    texto_boton = tipografia_pixel.render(texto, True, BLANCO)
    ventana.blit(texto_boton, (x + (ancho - texto_boton.get_width()) // 2, y + (alto - texto_boton.get_height()) // 2))

# Función principal de la pantalla de inicio
def pantalla_inicio():
    while True:
        redimensionar_componentes()  # Ajustar dimensiones dinámicamente
        dibujar_fondo(ventana)  # Dibujar la imagen de fondo ajustada

        # Título del juego (centrado y un poco más abajo)
        texto_titulo = tipografia_pixel_grande.render("Alien Blasters", True, BLANCO)
        ventana.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 3 - texto_titulo.get_height() // 2))

        # Texto "By Argo Studio" debajo del título
        texto_autor = tipografia_pequeña.render("By ARGO Studio", True, BLANCO)
        ventana.blit(texto_autor, (ANCHO // 2 - texto_autor.get_width() // 2, ALTO // 3 + texto_titulo.get_height()))

        # Dimensiones y posición del botón
        boton_ancho = ANCHO // 3  # Botón ocupa 1/3 del ancho de la pantalla
        boton_alto = ALTO // 10   # Botón ocupa 1/10 del alto de la pantalla
        boton_x = ANCHO // 2 - boton_ancho // 2
        boton_y = ALTO // 2

        # Obtener la posición del ratón
        mouse_pos = pygame.mouse.get_pos()

        # Verificar si el ratón está sobre el botón
        hover = boton_x <= mouse_pos[0] <= boton_x + boton_ancho and boton_y <= mouse_pos[1] <= boton_y + boton_alto

        # Cambiar el cursor a mano si está sobre el botón
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Cursor de mano
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Cursor de flecha

        # Dibujar el botón con la animación de agrandarse
        dibujar_boton(ventana, "Toca para iniciar", boton_x, boton_y, boton_ancho, boton_alto, hover=hover)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_f:  # Presionar 'F' para pantalla completa
                    pygame.display.toggle_fullscreen()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if hover:  # Si se hace clic en el botón
                    sonido_click.play()  # Reproducir el sonido al hacer clic en el botón
                    mostrar_capitulos()  # Ir a la pantalla de capítulos

            elif evento.type == pygame.VIDEORESIZE:  # Evento para redimensionar la ventana
                redimensionar_componentes()

        pygame.display.update()

if __name__ == "__main__":
    pantalla_inicio()