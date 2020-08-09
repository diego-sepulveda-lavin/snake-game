# Importaciones necesarias en el juego
import pygame
import random

# Inicializacion de pygame
pygame.init()

# Creacion objeto reloj para monitorear tiempo
clock = pygame.time.Clock()

# Se declaran colores del juego en RGB
snake_color = (0, 204, 0)
food_color = (204, 0, 0)
background_color = (0, 0, 0)
game_over_color = (255, 0, 0)
score_color = (0, 255, 0)
aviso_color = (255, 255, 0)

# Seteo de variables para tamaño de ventana
display_width = 600
display_height = 400

# Inicializacion de ventana de juego con tamaño definido
game_window = pygame.display.set_mode((display_width, display_height))

# Seteo de titulo de la ventana
pygame.display.set_caption('Snake Game')

# Framerate del juego
snake_speed = 15

# Definir tamaño bloque snake
snake_block = 10


# Define forma y posicion de la snake
def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_window, snake_color, [x[0], x[1], snake_block, snake_block])


# Funcion principal del juego
def snake_game():
    global snake_speed
    game_end = False  # Flag para terminar juego
    game_over = False  # Flag juego perdido

    # Coordenadas iniciales de la snake centro de pantalla 
    x1 = display_width / 2
    y1 = display_height / 2

    # Variables para capturar cambio de posicion snake
    x1_change = 0
    y1_change = 0

    # Seteo largo de snake
    snake_list = []
    snake_length = 1

    # genera coordenadas x,y random de la comida dentro de la pantalla
    food_pos_x = int(round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0)
    food_pos_y = int(round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0)

    while not game_end:

        # Bloque en caso de game over
        while game_over:

            # Relleno surface con color
            game_window.fill(background_color)

            # Mostrar perdiste al final del juego
            perdiste_font_style = pygame.font.SysFont("comicsansms", 40)
            msg_perdiste = perdiste_font_style.render("Perdiste!", True, game_over_color)
            game_window.blit(msg_perdiste, [int(display_width / 6), int(display_height / 6)])  # Dibuja mensaje sobre surface

            # Mostrar el puntaje al final de juego
            score = (snake_length - 1) * 10
            score_font_style = pygame.font.SysFont("comicsansms", 35)
            value = score_font_style.render(f"Tu puntaje fue: {str(score)}", True, score_color)
            game_window.blit(value, [int(display_width / 6), int(display_height / 4)]) # Dibuja mensaje sobre surface

            # Mostrar la opcion nuevo juego
            nuevo_juego_font_style = pygame.font.SysFont("comicsansms", 20)
            msg_nuevo_juego = nuevo_juego_font_style.render("Para jugar nuevamente presiona Enter o ESC para salir..", True, aviso_color)
            game_window.blit(msg_nuevo_juego, [int(display_width / 6), int(display_height / 2)]) # Dibuja mensaje sobre surface

            # Hace update de pantalla
            pygame.display.update()


            # Captura eventos en caso de seguir jugando o salir
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        snake_game()  # Revisa si se presiona Enter para nuevo juego
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit() # Cerrar ventana juego
                        quit() # Terminar programa
               
                # Termina el juego al cerrar
                if event.type == pygame.QUIT:
                    game_end = True
                    game_over = False

        # Bloque de juego
        for event in pygame.event.get():
            
            # Termina el juego
            if event.type == pygame.QUIT:
                game_end = True
            
            # Captura teclas de movimiento y cambia direccion de mov
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0
        
        # Condicion de game over al tocar bordes de la pantalla
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_over = True

        # Actualiza coordenadas segun input de teclas capturadas
        x1 += x1_change
        y1 += y1_change

        # Genera superficie y dibuja comida
        game_window.fill(background_color)
        pygame.draw.rect(game_window, food_color, [food_pos_x, food_pos_y, snake_block, snake_block])

        # Contador de score
        score = (snake_length - 1) * 10
        score_font_style = pygame.font.SysFont("comicsansms", 20)
        value = score_font_style.render(f"Puntos: {str(score)}", True, score_color)
        game_window.blit(value, [270, 1])

        # Mensaje de animo
        if score % 50 == 0 and score != 0:
            animo_font_style = pygame.font.SysFont("comicsansms", 20)
            animo = score_font_style.render(f"Wow {str(score)} puntos, sigue asi!", True, aviso_color)
            game_window.blit(animo, [220, 15])
        
        # Mensaje de velocidad
        velocidad_font_style = pygame.font.SysFont("comicsansms", 20)
        velocidad = score_font_style.render(f"Velocidad {str(snake_speed)}", True, aviso_color)
        game_window.blit(velocidad, [260, 380])

        # Se crea cabeza de snake
        snake_head = [x1, y1]

        # Se agrega la cabeza de snake al cuerpo
        snake_list.append(snake_head)

        # Mantiene largo de la snake y genera movimiento
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Condicion cuando la snake choca consigo misma, entonces game over
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True
        
        # Llamar a la funcion snake
        snake(snake_block, snake_list)

        # Hace update de pantalla
        pygame.display.update()

        # Condicion para incrementar el largo del cuerpo cuando encuentra comida y generar nuevo alimento
        if x1 == food_pos_x and y1 == food_pos_y:
            food_pos_x = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            food_pos_y = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            snake_length += 1 
            snake_speed += 1
        
        # Metodo para actualizar el objeto clock, recibe framerate para controlar velocidad
        clock.tick(snake_speed)  

    pygame.quit() # Cerrar ventana juego
    quit() # Terminar programa


snake_game()
