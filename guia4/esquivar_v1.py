import pygame
import random

# --- DEFINICIÓN DE COLORES BASE ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0) # Color para la bala

# --- CLASES ---

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.bottom = 580
        self.velocidad_x = 0

        # Variables para el cooldown de disparo
        self.cadencia = 250 # Milisegundos entre disparos
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self):
        self.velocidad_x = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -5
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = 5
        
        self.rect.x += self.velocidad_x

        # Mantener al jugador dentro de la pantalla
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0

    def disparar(self, todos_los_sprites, balas):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia:
            self.ultimo_disparo = ahora
            bala = Bala(self.rect.centerx, self.rect.top)
            todos_los_sprites.add(bala)
            balas.add(bala)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 20])
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad_y = -10 # Se mueve hacia arriba

    def update(self):
        self.rect.y += self.velocidad_y
        # Eliminar la bala si sale de la pantalla superior
        if self.rect.bottom < 0:
            self.kill()

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 800 - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(2, 6)
        self.velocidad_x = random.randrange(-2, 3)

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Rebote en las paredes
        if self.rect.right > 800 or self.rect.left < 0:
            self.velocidad_x *= -1

        # Reaparecer arriba si cae de la pantalla
        if self.rect.top > 600 + 10:
            self.rect.x = random.randrange(0, 800 - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad_y = random.randrange(2, 6)

# --- CONFIGURACIÓN INICIAL DE PYGAME ---
pygame.init()
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Prototipo Arcade - Disparos y Colisiones")
reloj = pygame.time.Clock()

# Grupos de sprites
todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()

# Instancia del jugador
jugador = Jugador()
todos_los_sprites.add(jugador)

# Crear enemigos
for i in range(8):
    enemigo = Enemigo()
    todos_los_sprites.add(enemigo)
    enemigos.add(enemigo)

puntuacion = 0
running = True

# Fuente para el texto de la puntuación
fuente = pygame.font.SysFont("serif", 24)

# --- BUCLE PRINCIPAL ---
while running:
    # 1. GESTIÓN DE EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Escuchar la tecla de espacio para disparar
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.disparar(todos_los_sprites, balas)

    todos_los_sprites.update()

    # groupcollide(grupo1, grupo2, dokill1, dokill2) -> Si ambos son True, ambos se eliminan
    impactos = pygame.sprite.groupcollide(enemigos, balas, True, True)

    # Por cada enemigo destruido (cada elemento en el diccionario 'impactos')
    for impacto in impactos:
        puntuacion += 10
        # Instanciar un nuevo enemigo para que el juego no se quede vacío
        nuevo_enemigo = Enemigo()
        todos_los_sprites.add(nuevo_enemigo)
        enemigos.add(nuevo_enemigo)

    # Detección de colisiones: Jugador vs Enemigos
    colision_jugador = pygame.sprite.spritecollide(jugador, enemigos, False)
    if colision_jugador:
        print(f"¡JUEGO TERMINADO! Puntuación final: {puntuacion}")
        running = False

    pantalla.fill(BLANCO)
    todos_los_sprites.draw(pantalla)

    # Dibujar la puntuación en la esquina superior izquierda
    texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, NEGRO)
    pantalla.blit(texto_puntos, (10, 10))

    pygame.display.flip()

    reloj.tick(60)

pygame.quit()