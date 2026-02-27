import pygame
import random
import math # ¡Nueva importación necesaria para el movimiento senoidal!

# --- DEFINICIÓN DE COLORES BASE ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

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
        self.cadencia = 250
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self):
        self.velocidad_x = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -5
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = 5
        
        self.rect.x += self.velocidad_x

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
        self.velocidad_y = -10

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.reiniciar() # Usamos un método para configurar los valores iniciales

    def reiniciar(self):
        """Configura o resetea la posición y el tipo de movimiento del enemigo."""
        self.rect.y = random.randrange(-150, -40)
        self.velocidad_y = random.randrange(2, 5)
        
        # 50% de probabilidad de ser un enemigo con movimiento senoidal o recto
        self.tipo_movimiento = random.choice(["recto", "senoidal"])

        if self.tipo_movimiento == "recto":
            self.rect.x = random.randrange(0, 800 - self.rect.width)
            self.velocidad_x = random.randrange(-2, 3)
        else: # Configuración para el movimiento senoidal
            self.amplitud = random.randrange(50, 150) # Qué tan ancha es la curva
            self.frecuencia = random.uniform(0.02, 0.06) # Qué tan rápido oscila
            # Calculamos un centro seguro para que no se salga de la pantalla al oscilar
            self.centro_x = random.randrange(self.amplitud, 800 - self.amplitud - self.rect.width)
            self.rect.x = self.centro_x
            self.tiempo = 0 # Variable para hacer avanzar la onda de la función seno

    def update(self):
        # El movimiento hacia abajo es constante para ambos tipos
        self.rect.y += self.velocidad_y

        if self.tipo_movimiento == "recto":
            self.rect.x += self.velocidad_x
            # Rebote en las paredes
            if self.rect.right > 800 or self.rect.left < 0:
                self.velocidad_x *= -1

        elif self.tipo_movimiento == "senoidal":
            self.tiempo += 1 # Avanzamos el "tiempo" de la onda
            # Aplicamos la fórmula del seno para la posición en X
            desplazamiento = int(self.amplitud * math.sin(self.frecuencia * self.tiempo))
            self.rect.x = self.centro_x + desplazamiento

        # Reaparecer arriba si cae de la pantalla
        if self.rect.top > 600 + 10:
            self.reiniciar()

# --- CONFIGURACIÓN INICIAL DE PYGAME ---
pygame.init()
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Prototipo Arcade - Movimiento Senoidal")
reloj = pygame.time.Clock()

todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()

jugador = Jugador()
todos_los_sprites.add(jugador)

for i in range(8):
    enemigo = Enemigo()
    todos_los_sprites.add(enemigo)
    enemigos.add(enemigo)

puntuacion = 0
running = True
fuente = pygame.font.SysFont("serif", 24)

# --- BUCLE PRINCIPAL ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.disparar(todos_los_sprites, balas)

    todos_los_sprites.update()

    impactos = pygame.sprite.groupcollide(enemigos, balas, True, True)

    for impacto in impactos:
        puntuacion += 10
        nuevo_enemigo = Enemigo()
        todos_los_sprites.add(nuevo_enemigo)
        enemigos.add(nuevo_enemigo)

    colision_jugador = pygame.sprite.spritecollide(jugador, enemigos, False)
    if colision_jugador:
        print(f"¡JUEGO TERMINADO! Puntuación final: {puntuacion}")
        running = False

    pantalla.fill(BLANCO)
    todos_los_sprites.draw(pantalla)

    texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, NEGRO)
    pantalla.blit(texto_puntos, (10, 10))
 
    pygame.display.flip()
    reloj.tick(60)

pygame.quit() 