import pygame
import random
import math

# --- DEFINICIÓN DE COLORES BASE ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 50, 50)
AMARILLO = (255, 255, 0)
AZUL = (50, 150, 255)

# --- FUNCIONES PARA GENERAR "SPRITES" SIN ARCHIVOS EXTERNOS ---
def crear_sprite_jugador():
    """Dibuja una nave espacial básica."""
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.polygon(surf, AZUL, [(25, 0), (0, 50), (25, 40), (50, 50)])
    return surf

def crear_sprite_enemigo():
    """Dibuja un asteroide/enemigo redondo con 'cráteres'."""
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(surf, ROJO, (20, 20), 20)
    pygame.draw.circle(surf, (150, 0, 0), (12, 15), 5) 
    pygame.draw.circle(surf, (150, 0, 0), (28, 28), 7)
    return surf

def crear_sprite_bala():
    """Dibuja un láser ovalado."""
    surf = pygame.Surface((10, 20), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, AMARILLO, [0, 0, 10, 20])
    return surf

# --- CLASES ---

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = crear_sprite_jugador()
        self.rect = self.image.get_rect()
        self.rect.centerx = 400
        self.rect.bottom = 580
        self.velocidad_x = 0
        self.velocidad_y = 0 # Añadimos velocidad vertical
        
        self.cadencia = 250
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self):
        # Reiniciamos velocidades en cada fotograma
        self.velocidad_x = 0
        self.velocidad_y = 0 
        
        teclas = pygame.key.get_pressed()
        
        # Movimiento Horizontal
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -6
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = 6
            
        # Movimiento Vertical (¡Nuevo!)
        if teclas[pygame.K_UP]:
            self.velocidad_y = -6 # Negativo mueve hacia arriba en Pygame
        if teclas[pygame.K_DOWN]:
            self.velocidad_y = 6  # Positivo mueve hacia abajo
        
        # Aplicar el movimiento
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # --- LÍMITES DE LA PANTALLA ---
        # Límite horizontal
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0
            
        # Límite vertical (¡Nuevo!)
        # Evita que baje más allá de 600px
        if self.rect.bottom > 600:
            self.rect.bottom = 600
        # Evita que suba más allá del límite superior (0px)
        if self.rect.top < 0:
            self.rect.top = 0

    def disparar(self, todos_los_sprites, balas):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia:
            self.ultimo_disparo = ahora
            # La bala sale desde donde esté la nave actualmente (top)
            bala = Bala(self.rect.centerx, self.rect.top)
            todos_los_sprites.add(bala)
            balas.add(bala)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = crear_sprite_bala()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad_y = -12

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = crear_sprite_enemigo()
        self.rect = self.image.get_rect()
        self.reiniciar()

    def reiniciar(self):
        self.rect.y = random.randrange(-150, -40)
        self.velocidad_y = random.randrange(2, 5)
        self.tipo_movimiento = random.choice(["recto", "senoidal"])

        if self.tipo_movimiento == "recto":
            self.rect.x = random.randrange(0, 800 - self.rect.width)
            self.velocidad_x = random.randrange(-2, 3)
        else:
            self.amplitud = random.randrange(50, 150)
            self.frecuencia = random.uniform(0.02, 0.06)
            self.centro_x = random.randrange(self.amplitud, 800 - self.amplitud - self.rect.width)
            self.rect.x = self.centro_x
            self.tiempo = 0

    def update(self):
        self.rect.y += self.velocidad_y

        if self.tipo_movimiento == "recto":
            self.rect.x += self.velocidad_x
            if self.rect.right > 800 or self.rect.left < 0:
                self.velocidad_x *= -1
        elif self.tipo_movimiento == "senoidal":
            self.tiempo += 1
            desplazamiento = int(self.amplitud * math.sin(self.frecuencia * self.tiempo))
            self.rect.x = self.centro_x + desplazamiento

        if self.rect.top > 600 + 10:
            self.reiniciar()


# --- CONFIGURACIÓN INICIAL DE PYGAME ---
pygame.init()
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Arcade Completo - Movimiento en 4 Direcciones")
reloj = pygame.time.Clock()

# Fuentes para texto
fuente_hud = pygame.font.SysFont("serif", 24, bold=True)
fuente_titulos = pygame.font.SysFont("serif", 48, bold=True)
fuente_instrucciones = pygame.font.SysFont("serif", 20)

# Variables globales del juego
todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()
jugador = None
puntuacion = 0
vidas = 3

estado_juego = "INICIO"

def iniciar_nuevo_juego():
    global jugador, puntuacion, vidas
    todos_los_sprites.empty()
    enemigos.empty()
    balas.empty()
    
    puntuacion = 0
    vidas = 3
    
    jugador = Jugador()
    todos_los_sprites.add(jugador)
    
    for i in range(8):
        enemigo = Enemigo()
        todos_los_sprites.add(enemigo)
        enemigos.add(enemigo)

def dibujar_texto(superficie, texto, fuente, color, x, y, centrado=False):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect()
    if centrado:
        rect_texto.center = (x, y)
    else:
        rect_texto.topleft = (x, y)
    superficie.blit(superficie_texto, rect_texto)

running = True

# --- BUCLE PRINCIPAL ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if estado_juego == "INICIO" or estado_juego == "GAME_OVER":
                    iniciar_nuevo_juego()
                    estado_juego = "JUGANDO"
            
            elif event.key == pygame.K_SPACE and estado_juego == "JUGANDO":
                jugador.disparar(todos_los_sprites, balas)

    pantalla.fill(NEGRO) 

    if estado_juego == "INICIO":
        dibujar_texto(pantalla, "DEFENSOR ESPACIAL", fuente_titulos, BLANCO, ANCHO_PANTALLA//2, 200, centrado=True)
        dibujar_texto(pantalla, "Presiona ENTER para empezar", fuente_instrucciones, AMARILLO, ANCHO_PANTALLA//2, 350, centrado=True)
        dibujar_texto(pantalla, "Mover: Flechas | Disparar: Espacio", fuente_instrucciones, BLANCO, ANCHO_PANTALLA//2, 400, centrado=True)

    elif estado_juego == "JUGANDO":
        todos_los_sprites.update()

        impactos = pygame.sprite.groupcollide(enemigos, balas, True, True)
        for impacto in impactos:
            puntuacion += 10
            nuevo_enemigo = Enemigo()
            todos_los_sprites.add(nuevo_enemigo)
            enemigos.add(nuevo_enemigo)

        choques = pygame.sprite.spritecollide(jugador, enemigos, True) 
        for choque in choques:
            vidas -= 1
            nuevo_enemigo = Enemigo()
            todos_los_sprites.add(nuevo_enemigo)
            enemigos.add(nuevo_enemigo)
            
            if vidas <= 0:
                estado_juego = "GAME_OVER"

        todos_los_sprites.draw(pantalla)

        dibujar_texto(pantalla, f"Puntos: {puntuacion}", fuente_hud, BLANCO, 10, 10)
        dibujar_texto(pantalla, f"Vidas: {vidas}", fuente_hud, ROJO, ANCHO_PANTALLA - 110, 10)

    elif estado_juego == "GAME_OVER":
        dibujar_texto(pantalla, "¡JUEGO TERMINADO!", fuente_titulos, ROJO, ANCHO_PANTALLA//2, 200, centrado=True)
        dibujar_texto(pantalla, f"Puntuación final: {puntuacion}", fuente_hud, BLANCO, ANCHO_PANTALLA//2, 280, centrado=True)
        dibujar_texto(pantalla, "Presiona ENTER para jugar de nuevo", fuente_instrucciones, AMARILLO, ANCHO_PANTALLA//2, 350, centrado=True)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()