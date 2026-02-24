import pygame 
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rebotar una Pelota")

# ===== CARGAR IMAGEN DE FONDO =====
# Opción 1: Si tu imagen está en la misma carpeta que el código
background = pygame.image.load("assets/dragon_gibli.jpg")  # Cambia "fondo.png" por el nombre de tu imagen

# Escalar la imagen al tamaño de la ventana (800x600)
background = pygame.transform.scale(background, (800, 600))

# ===== CONFIGURACIÓN DE COLORES ROTATIVOS =====
colores = [
    (255, 0, 0),      # Rojo (Red)
    (0, 0, 255),      # Azul (Blue)
    (165, 42, 42),    # Café (Brown)
    (255, 255, 0),    # Amarillo (Yellow)
    (255, 192, 203),  # Rosa (Pink)
    (0, 255, 0),      # Verde (Green)
    (128, 0, 128),    # Púrpura (Purple)
    (255, 165, 0)     # Naranja (Orange)
]
indice_color = 0  # Índice para rotar entre los colores

# Configuración de la pelota
ball = pygame.Rect(400, 300, 50, 50)
ball_speed = [0.8, 0.8]

# ===== CONTADOR DE CHOQUES =====
choques = 0  # Contador total de choques contra las paredes

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento de la pelota
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # ===== REBOTE EN LOS BORDES CON CAMBIO DE COLOR Y VELOCIDAD =====
    # Rebote horizontal (izquierda o derecha)
    if ball.left < 0 or ball.right > 800:
        ball_speed[0] = -ball_speed[0]
        choques += 1  # Incrementar contador de choques
        
        # Cambiar al siguiente color
        indice_color = (indice_color + 1) % len(colores)
        
        # ===== MODIFICAR VELOCIDAD SEGÚN CHOQUES =====
        # Si los choques son múltiplo de 5: INCREMENTAR velocidad
        if choques % 5 == 0:
            ball_speed[0] *= 1.2  # Aumenta 20% la velocidad horizontal
            ball_speed[1] *= 1.2  # Aumenta 20% la velocidad vertical
            print(f"¡Choque #{choques}! Velocidad AUMENTADA")
        
        # Si los choques son múltiplo de 7: DISMINUIR velocidad
        elif choques % 7 == 0:
            ball_speed[0] *= 0.8  # Disminuye 20% la velocidad horizontal
            ball_speed[1] *= 0.8  # Disminuye 20% la velocidad vertical
            print(f"¡Choque #{choques}! Velocidad REDUCIDA")
    
    # Rebote vertical (arriba o abajo)
    if ball.top < 0 or ball.bottom > 600:
        ball_speed[1] = -ball_speed[1]
        choques += 1  # Incrementar contador de choques
        
        # Cambiar al siguiente color
        indice_color = (indice_color + 1) % len(colores)
        
        # ===== MODIFICAR VELOCIDAD SEGÚN CHOQUES =====
        # Si los choques son múltiplo de 5: INCREMENTAR velocidad
        if choques % 5 == 0:
            ball_speed[0] *= 1.2  # Aumenta 20% la velocidad horizontal
            ball_speed[1] *= 1.2  # Aumenta 20% la velocidad vertical
            print(f"¡Choque #{choques}! Velocidad AUMENTADA")
        
        # Si los choques son múltiplo de 7: DISMINUIR velocidad
        elif choques % 7 == 0:
            ball_speed[0] *= 0.8  # Disminuye 20% la velocidad horizontal
            ball_speed[1] *= 0.8  # Disminuye 20% la velocidad vertical
            print(f"¡Choque #{choques}! Velocidad REDUCIDA")
    
    # ===== DIBUJAR FONDO =====
    screen.blit(background, (0, 0))  # Dibuja la imagen en posición (0, 0)
    
    # ===== DIBUJAR LA PELOTA CON COLOR ROTATIVO =====
    pygame.draw.ellipse(screen, colores[indice_color], ball)
    
    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()