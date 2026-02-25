import pygame
import random

# Inicialización
pygame.init()
pygame.font.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Juego - Contador de Colisiones")

# Fuentes
fuente = pygame.font.SysFont(None, 36)
fuente_grande = pygame.font.SysFont(None, 72)

# Clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_PANTALLA // 2
        self.rect.y = ALTO_PANTALLA - 60

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 8
        if teclas[pygame.K_RIGHT] and self.rect.x < ANCHO_PANTALLA - 50:
            self.rect.x += 8

# Clase Obstáculo
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - 50)
        self.rect.y = random.randint(-100, -40)
        self.velocidad_y = random.randint(5, 10)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.y > ALTO_PANTALLA:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, ANCHO_PANTALLA - 50)

# Crear sprites
jugador = Jugador()
obstaculos = pygame.sprite.Group()
todos_los_sprites = pygame.sprite.Group()

todos_los_sprites.add(jugador)

for _ in range(10):
    obstaculo = Obstaculo()
    obstaculos.add(obstaculo)
    todos_los_sprites.add(obstaculo)

# Contador de colisiones
colisiones_count = 0

# Función para contar colisiones
def contar_colisiones():
    global colisiones_count
    colisiones = pygame.sprite.spritecollide(jugador, obstaculos, True)
    for _ in colisiones:
        colisiones_count += 1
        nuevo = Obstaculo()
        obstaculos.add(nuevo)
        todos_los_sprites.add(nuevo)

# Función para reiniciar juego (Punto 6.2)
def reiniciar_juego():
    global colisiones_count
    colisiones_count = 0
    jugador.rect.x = ANCHO_PANTALLA // 2
    jugador.rect.y = ALTO_PANTALLA - 60

# Bucle principal
running = True
reloj = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    todos_los_sprites.update()
    contar_colisiones()

    pantalla.fill(BLANCO)
    todos_los_sprites.draw(pantalla)

    texto_colisiones = fuente.render(f"Colisiones: {colisiones_count} / 5", True, NEGRO)
    pantalla.blit(texto_colisiones, (10, 10))

    # 6.2 Game Over
    if colisiones_count >= 5:
        texto_go = fuente_grande.render("GAME OVER", True, ROJO)
        rect_go = texto_go.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2))
        pantalla.blit(texto_go, rect_go)
        pygame.display.flip()
        pygame.time.wait(3000)
        reiniciar_juego()

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
