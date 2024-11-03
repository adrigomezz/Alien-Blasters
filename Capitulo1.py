import pygame
import sys
import random
import time
from PIL import Image  # Asegúrate de tener Pillow instalado para manejar el GIF

# Inicializar pygame
pygame.init()

# Crear la ventana del juego como redimensionable
ANCHO_INICIAL = 700
ALTO_INICIAL = 700
ventana = pygame.display.set_mode((ANCHO_INICIAL, ALTO_INICIAL), pygame.RESIZABLE)
pygame.display.set_caption("Alien Blasters - Capítulo 1")

# Cargar tipografía
tipografia_pixel = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 10)
tipografia_grande = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 15)

# Colores
BLANCO = (255, 255, 255)

# Cargar y ajustar las imágenes
nave_img = pygame.image.load("Assets/Nave espacial.png")
nave_img = pygame.transform.scale(nave_img, (100, 100))  # Nave más grande
alien_img = pygame.image.load("Assets/Nave alien.png")
alien_img = pygame.transform.scale(alien_img, (70, 70))  # Aliens más grandes
rayo_img = pygame.image.load("Assets/Fuego azul.png")
rayo_img = pygame.transform.scale(rayo_img, (20, 50))  # Rayos más grandes
explosion_img = pygame.image.load("Assets/Explosión.png")
explosion_img = pygame.transform.scale(explosion_img, (70, 70))  # Explosión más grande

# Cargar sonidos
sonido_disparo = pygame.mixer.Sound("OST/Disparo Nave Espacial.mp3")
sonido_explosion = pygame.mixer.Sound("OST/Explosión alien.mp3")
sonido_has_muerto = pygame.mixer.Sound("OST/Has muerto.mp3")
sonido_nivel_superado = pygame.mixer.Sound("OST/Nivel Superado.mp3")

# Cargar el GIF de fondo
gif = Image.open("Assets/Espacio1.gif")
frames = []
try:
    while True:
        frame = gif.copy().convert("RGBA")
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()

        # Convertir a formato de imagen de Pygame
        py_image = pygame.image.fromstring(data, size, mode)
        frames.append(py_image)
        gif.seek(len(frames))  # Pasar al siguiente frame del GIF
except EOFError:
    pass  # Cuando ya no hay más frames en el GIF

# Definir clase Nave Espacial
class NaveEspacial:
    def __init__(self, ancho_ventana, alto_ventana):
        self.x = ancho_ventana // 2 - 50  # Mitad del ancho de la ventana
        self.y = alto_ventana - 100  # A 100 píxeles del fondo
        self.velocidad = 5
        self.disparos = []
        self.vida = True
        self.ultimo_disparo = 0  # Tiempo del último disparo

    def dibujar(self):
        ventana.blit(nave_img, (self.x, self.y))

    def mover(self, direccion):
        if direccion == "izquierda" and self.x > 0:
            self.x -= self.velocidad
        if direccion == "derecha" and self.x + nave_img.get_width() < ventana.get_width():
            self.x += self.velocidad

    def disparar(self):
        # Controlar el tiempo de enfriamiento entre disparos
        tiempo_actual = time.time()
        if tiempo_actual - self.ultimo_disparo >= 1:  # 1 segundo de intervalo entre disparos
            rayo = pygame.Rect(self.x + nave_img.get_width() // 2 - 10, self.y, 10, 30)
            self.disparos.append(rayo)
            sonido_disparo.play()  # Reproduce el sonido de disparo
            self.ultimo_disparo = tiempo_actual

# Definir clase Alien
class Alien:
    def __init__(self, ancho_ventana):
        self.x = random.randint(0, ancho_ventana - 70)  # Generar aliens en toda la anchura de la ventana
        self.y = random.randint(-100, -40)
        self.velocidad = random.randint(1, 2)  # Aliens más lentos

    def dibujar(self):
        ventana.blit(alien_img, (self.x, self.y))

    def mover(self):
        self.y += self.velocidad

# Función para mostrar texto
def mostrar_texto(ventana, texto, tamanio, color, x, y):
    fuente = pygame.font.Font("Assets/PressStart2P-Regular.ttf", tamanio)
    texto_superficie = fuente.render(texto, True, color)
    ventana.blit(texto_superficie, (x, y))

# Función para mostrar texto centrado
def mostrar_texto_centrado(ventana, texto, tamanio, color):
    ancho_ventana, alto_ventana = ventana.get_size()
    fuente = pygame.font.Font("Assets/PressStart2P-Regular.ttf", tamanio)
    texto_superficie = fuente.render(texto, True, color)
    ancho_texto = texto_superficie.get_width()
    alto_texto = texto_superficie.get_height()
    ventana.blit(texto_superficie, ((ancho_ventana - ancho_texto) // 2, (alto_ventana - alto_texto) // 2))

# Pantalla del Capítulo 1
def mostrar_capitulo1():
    nave = NaveEspacial(ANCHO_INICIAL, ALTO_INICIAL)
    aliens = []
    puntos = 0
    reloj = pygame.time.Clock()

    animacion_completada = False
    pantalla_negra = False
    juego_terminado = False
    frame_index = 0  # Índice de frames del GIF

    # Mostrar el texto de inicio sin música
    while not animacion_completada:
        ventana.fill((0, 0, 0))
        mostrar_texto_centrado(ventana, "Capítulo 1 - ¡Comienza la aventura!", 15, BLANCO)
        pygame.display.update()
        pygame.time.delay(3000)  # Mantiene el texto durante 3 segundos
        animacion_completada = True

    # Iniciar la música del juego
    pygame.mixer.music.load("OST/OST Alien Blasters 1.mp3")  # Asegúrate de tener un archivo de música para el juego
    pygame.mixer.music.play(-1)  # Reproduce en bucle

    # Loop principal del juego
    while not juego_terminado:
        reloj.tick(60)  # 60 FPS

        # Mostrar el fondo del GIF (actualizando frames y escalando)
        ancho_ventana, alto_ventana = ventana.get_size()
        imagen_fondo = pygame.transform.scale(frames[frame_index], (ancho_ventana, alto_ventana))
        ventana.blit(imagen_fondo, (0, 0))
        frame_index = (frame_index + 1) % len(frames)

        # Generar aliens aleatoriamente con menor frecuencia
        if random.randint(0, 100) < 1:  # Muy pocos aliens
            aliens.append(Alien(ancho_ventana))

        # Eventos del teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento de la nave
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            nave.mover("izquierda")
        if keys[pygame.K_d]:
            nave.mover("derecha")
        if keys[pygame.K_l]:
            nave.disparar()

        # Mover y dibujar los disparos
        for rayo in nave.disparos[:]:
            rayo.y -= 7
            if rayo.y < 0:
                nave.disparos.remove(rayo)
            else:
                ventana.blit(rayo_img, (rayo.x, rayo.y))

        # Mover y dibujar los aliens
        for alien in aliens[:]:
            alien.mover()
            alien.dibujar()

            # Colisión con la nave
            if pygame.Rect(alien.x, alien.y, 70, 70).colliderect(nave.x, nave.y, 100, 100):
                pantalla_negra = True
                juego_terminado = True

            # Colisión con los disparos
            for rayo in nave.disparos[:]:
                if pygame.Rect(alien.x, alien.y, 70, 70).colliderect(rayo.x, rayo.y, 10, 30):
                    puntos += 100
                    nave.disparos.remove(rayo)
                    aliens.remove(alien)
                    sonido_explosion.play()  # Reproduce el sonido de explosión
                    ventana.blit(explosion_img, (alien.x, alien.y))
                    pygame.display.update()
                    pygame.time.delay(50)
                    break  # El disparo desaparece al golpear al alien

        # Dibuja la nave
        nave.dibujar()

        # Mostrar puntuación en la esquina superior derecha ajustada al tamaño de la ventana
        mostrar_texto(ventana, f"Puntos: {puntos}", 15, BLANCO, ancho_ventana - 180, 10)

        # Chequea si alcanzó los puntos de victoria
        if puntos >= 5000:
            pantalla_negra = True
            juego_terminado = True

        pygame.display.update()

    # Pantallas finales (Has Muerto o Capítulo Terminado)
    if pantalla_negra:
        pygame.mixer.music.stop()  # Detiene la música
        ventana.fill((0, 0, 0))
        if puntos >= 5000:
            sonido_nivel_superado.play()
            mostrar_texto_centrado(ventana, "CAPÍTULO SUPERADO", 25, BLANCO)
        else:
            sonido_has_muerto.play()
            mostrar_texto_centrado(ventana, "HAS MUERTO", 25, BLANCO)
        pygame.display.update()
        pygame.time.delay(3000)


if __name__ == "__main__":
    mostrar_capitulo1()