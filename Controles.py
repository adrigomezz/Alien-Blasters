import pygame
import sys

# Inicializar pygame
pygame.init()

# Inicializar pygame y el mixer de audio
pygame.mixer.init()

# Dimensiones iniciales de la ventana (esto se ajustará después)
ANCHO = 700
ALTO = 700

# Crear la ventana del juego (redimensionable)
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Controles - Alien Blasters")

# Definir colores
BLANCO = (255, 255, 255)

# Cargar la tipografía
tipografia_pixel = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 25)
tipografia_pequeña = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 15)

# Cargar imágenes
imagen_nave = pygame.image.load("Assets/Nave espacial.png")  # Asegúrate de que la ruta sea correcta
imagen_fuego = pygame.image.load("Assets/Fuego azul.png")  # Asegúrate de que la ruta sea correcta

# Función para redimensionar las imágenes
def redimensionar_imagenes():
    global imagen_nave, imagen_fuego
    # Redimensionar imágenes
    imagen_nave = pygame.transform.scale(imagen_nave, (100, 100))  # Ajusta el tamaño según sea necesario
    imagen_fuego = pygame.transform.scale(imagen_fuego, (100, 100))  # Ajusta el tamaño según sea necesario

# Función principal de la pantalla de controles
def mostrar_controles(volver_funcion):
    global ventana  # Declarar ventana como global
    redimensionar_imagenes()  # Redimensionar imágenes al inicio
    while True:
        # Ajustar el tamaño de la ventana
        ANCHO, ALTO = ventana.get_size()
        ventana.fill((0, 0, 0))  # Fondo negro

        # Texto de controles en el centro
        texto_controles = tipografia_pixel.render("Controles de teclas", True, BLANCO)
        ventana.blit(texto_controles, (ANCHO // 2 - texto_controles.get_width() // 2, ALTO // 8))

        # Columna izquierda: Nave (centrar imagen y texto)
        posicion_columna_izquierda_x = ANCHO // 4  # Posición x para la columna izquierda
        ventana.blit(imagen_nave, (posicion_columna_izquierda_x - imagen_nave.get_width() // 2, ALTO // 2 - imagen_nave.get_height() // 2))
        
        texto_izquierda_1 = tipografia_pequeña.render("A: izquierda", True, BLANCO)
        texto_izquierda_2 = tipografia_pequeña.render("D: derecha", True, BLANCO)
        ventana.blit(texto_izquierda_1, (posicion_columna_izquierda_x - texto_izquierda_1.get_width() // 2, ALTO // 2 + imagen_nave.get_height() // 2 + 10))
        ventana.blit(texto_izquierda_2, (posicion_columna_izquierda_x - texto_izquierda_2.get_width() // 2, ALTO // 2 + imagen_nave.get_height() // 2 + 30))

        # Columna derecha: Fuego (centrar imagen y texto)
        posicion_columna_derecha_x = 3 * ANCHO // 4  # Posición x para la columna derecha
        ventana.blit(imagen_fuego, (posicion_columna_derecha_x - imagen_fuego.get_width() // 2, ALTO // 2 - imagen_fuego.get_height() // 2))
        
        texto_derecha = tipografia_pequeña.render("L: disparar", True, BLANCO)
        ventana.blit(texto_derecha, (posicion_columna_derecha_x - texto_derecha.get_width() // 2, ALTO // 2 + imagen_fuego.get_height() // 2 + 10))

        # Texto "Atrás" en la esquina superior izquierda
        texto_atras = tipografia_pequeña.render("Atrás", True, BLANCO)
        ventana.blit(texto_atras, (10, 10))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se hace clic en "Atrás"
                if 10 <= pygame.mouse.get_pos()[0] <= 10 + texto_atras.get_width() and \
                        10 <= pygame.mouse.get_pos()[1] <= 10 + texto_atras.get_height():
                    volver_funcion()  # Volver a la pantalla de capítulos

            elif evento.type == pygame.VIDEORESIZE:
                ventana = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)

        pygame.display.update()

if __name__ == "__main__":
    mostrar_controles(lambda: None)  # Pasa una función vacía si se ejecuta directamente
