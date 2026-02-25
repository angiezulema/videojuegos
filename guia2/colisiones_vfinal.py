import pygame
import random
import os

# Inicialización de Pygame y fuentes
pygame.init()
pygame.font.init()

# Definición de colores
BLANCO = (255, 255, 255)
FONDO_ESPACIO = (15, 15, 30)
ROJO_NEON = (255, 50, 50)
CYAN_NEON = (0, 255, 255)
VERDE = (50, 255, 50)
GRIS = (100, 100, 100)

# Definición de dimensiones de pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Sobreviviente Estelar - Edición Gráfica")

# Configuración de fuentes
fuente = pygame.font.SysFont("Arial", 28, bold=True)
fuente_grande = pygame.font.SysFont("Arial", 72, bold=True)

# ---------------------------------------------------------
# SISTEMA DE FONDO DE ESTRELLAS (PARALLAX)
# ---------------------------------------------------------
class SistemaEstrellas:
    def __init__(self, cantidad):
        self.estrellas = []
        for _ in range(cantidad):
            x = random.randint(0, ANCHO_PANTALLA)
            y = random.randint(0, ALTO_PANTALLA)
            velocidad = random.uniform(1, 4)
            tamaño = random.randint(1, 3)
            self.estrellas.append([x, y, velocidad, tamaño])

    def dibujar_y_actualizar(self, superficie, nivel_velocidad):
        for estrella in self.estrellas:
            estrella[1] += estrella[2] + (nivel_velocidad * 1.5)
            if estrella[1] > ALTO_PANTALLA:
                estrella[1] = 0
                estrella[0] = random.randint(0, ANCHO_PANTALLA)
            color_estrella = BLANCO if estrella[2] > 2.5 else GRIS
            pygame.draw.circle(superficie, color_estrella, (int(estrella[0]), int(estrella[1])), estrella[3])

# ---------------------------------------------------------
# SPRITES: JUGADOR Y OBSTÁCULO CON IMÁGENES
# ---------------------------------------------------------
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Intentamos cargar la imagen de la nave
        try:
            # convert_alpha() respeta las transparencias (el fondo invisible de la imagen)
            imagen_original = pygame.image.load("assets/nave.png").convert_alpha()
            # Escalar la imagen a 50x50 píxeles para mantener el balance del juego
            self.image = pygame.transform.scale(imagen_original, (50, 50))
        except FileNotFoundError:
            print("No se encontró 'nave.png'. Usando cuadrado temporal.")
            self.image = pygame.Surface((50, 50))
            self.image.fill(CYAN_NEON)
            
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_PANTALLA // 2
        self.rect.y = ALTO_PANTALLA - 70
        
        self.dash_cooldown = 0
        self.dash_cooldown_max = 90

    def update(self):
        teclas = pygame.key.get_pressed()
        velocidad_normal = 8
        velocidad_actual = velocidad_normal

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        if teclas[pygame.K_SPACE] and self.dash_cooldown == 0: 
            velocidad_actual = 45 
            self.dash_cooldown = self.dash_cooldown_max 

        if teclas[pygame.K_LEFT]: 
            self.rect.x = max(0, self.rect.x - velocidad_actual)
        if teclas[pygame.K_RIGHT]: 
            self.rect.x = min(ANCHO_PANTALLA - 50, self.rect.x + velocidad_actual)

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Intentamos cargar la imagen del meteorito
        try:
            imagen_original = pygame.image.load("assets/meteorito.png").convert_alpha()
            self.image = pygame.transform.scale(imagen_original, (50, 50))
        except FileNotFoundError:
            self.image = pygame.Surface((50, 50)) 
            self.image.fill(ROJO_NEON)
            
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - 50)
        self.rect.y = random.randint(-150, -50)
        self.velocidad_y = random.randint(5, 10)

    def update(self):
        global nivel_actual
        self.rect.y += self.velocidad_y + (nivel_actual * 2) 
        
        if self.rect.y > ALTO_PANTALLA:
            self.rect.y = random.randint(-150, -50)
            self.rect.x = random.randint(0, ANCHO_PANTALLA - 50)
            self.velocidad_y = random.randint(5, 10)

# ---------------------------------------------------------
# CONFIGURACIÓN Y BUCLE PRINCIPAL
# ---------------------------------------------------------
jugador = None
obstaculos = None
todos_los_sprites = None
estrellas = SistemaEstrellas(120) 
colisiones_count = 0
start_time = 0
nivel_actual = 0

def reiniciar_juego():
    global jugador, obstaculos, todos_los_sprites, colisiones_count, start_time, nivel_actual
    jugador = Jugador()
    obstaculos = pygame.sprite.Group()
    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(jugador)

    for _ in range(10):
        obstaculo = Obstaculo()
        obstaculos.add(obstaculo)
        todos_los_sprites.add(obstaculo)

    colisiones_count = 0
    nivel_actual = 0
    start_time = pygame.time.get_ticks()

reiniciar_juego()

running = True
reloj = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tiempo_actual = pygame.time.get_ticks()
    tiempo_jugado_segundos = (tiempo_actual - start_time) // 1000
    nivel_actual = tiempo_jugado_segundos // 20 

    todos_los_sprites.update()

    colisiones_detectadas = pygame.sprite.spritecollide(jugador, obstaculos, True)
    for c in colisiones_detectadas:
        colisiones_count += 1
        nuevo_obstaculo = Obstaculo()
        obstaculos.add(nuevo_obstaculo)
        todos_los_sprites.add(nuevo_obstaculo)

    pantalla.fill(FONDO_ESPACIO)
    estrellas.dibujar_y_actualizar(pantalla, nivel_actual)
    todos_los_sprites.draw(pantalla)

    texto_tiempo = fuente.render(f"Tiempo: {tiempo_jugado_segundos} s", True, BLANCO)
    texto_colisiones = fuente.render(f"Daños: {colisiones_count} / 5", True, BLANCO)
    texto_nivel = fuente.render(f"Nivel: {nivel_actual + 1}", True, CYAN_NEON)

    pantalla.blit(texto_tiempo, (20, 20))
    pantalla.blit(texto_colisiones, (20, 55))
    pantalla.blit(texto_nivel, (20, 90))

    ancho_barra = 150
    alto_barra = 15
    posX_barra = ANCHO_PANTALLA - ancho_barra - 20
    posY_barra = 25
    
    texto_dash = fuente.render("Dash (ESPACIO)", True, BLANCO)
    pantalla.blit(texto_dash, (posX_barra, posY_barra - 25))

    if jugador.dash_cooldown == 0:
        color_barra = VERDE 
        ancho_actual = ancho_barra
    else:
        color_barra = ROJO_NEON 
        porcentaje = 1 - (jugador.dash_cooldown / jugador.dash_cooldown_max)
        ancho_actual = ancho_barra * porcentaje

    pygame.draw.rect(pantalla, GRIS, (posX_barra, posY_barra, ancho_barra, alto_barra))
    pygame.draw.rect(pantalla, color_barra, (posX_barra, posY_barra, ancho_actual, alto_barra))
    pygame.draw.rect(pantalla, BLANCO, (posX_barra, posY_barra, ancho_barra, alto_barra), 2)

    if colisiones_count >= 5:
        texto_go = fuente_grande.render("¡NAVE DESTRUIDA!", True, ROJO_NEON)
        rect_go = texto_go.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 - 50))
        pantalla.blit(texto_go, rect_go)
        
        texto_puntos = fuente.render(f"Sobreviviste {tiempo_jugado_segundos} segundos", True, BLANCO)
        rect_puntos = texto_puntos.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 20))
        pantalla.blit(texto_puntos, rect_puntos)
        
        pygame.display.flip()
        pygame.time.wait(4000) 
        reiniciar_juego()      
        continue               

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
