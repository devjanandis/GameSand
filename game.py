import numpy as np
import random
import pygame

def make_2d_array(cols, rows):
    return [[0 for _ in range(rows)] for _ in range(cols)]

def within_cols(i):
    return 0 <= i <= cols - 1

def within_rows(j):
    return 0 <= j <= rows - 1

# Init para o jogo iniciar
pygame.init()

# Setagem valores e gravidade
w = 5
hue_value = 200
gravity = 0.1

# Display setado
width, height = 600, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulação de Areia/Sand Simulation")

# Variaveis
cols, rows = width // w, height // w
grid = make_2d_array(cols, rows)
velocity_grid = make_2d_array(cols, rows)

# Loop
running = True
while running:
    screen.fill((0, 0, 0))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Interação do mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_col, mouse_row = mouse_x // w, mouse_y // w
    if pygame.mouse.get_pressed()[0]:
        matrix = 5
        extent = matrix // 2
        for i in range(-extent, extent + 1):
            for j in range(-extent, extent + 1):
                if random.random() < 0.75:
                    col = mouse_col + i
                    row = mouse_row + j
                    if within_cols(col) and within_rows(row):
                        grid[col][row] = hue_value
                        velocity_grid[col][row] = 1

        hue_value += 0.5
        if hue_value > 360:
            hue_value = 1

    # Código para a areia aparecer branca
    for i in range(cols):
        for j in range(rows):
            if grid[i][j] > 0:
                pygame.draw.rect(screen, (255, 255, 255), (i * w, j * w, w, w))


    next_grid = make_2d_array(cols, rows)
    next_velocity_grid = make_2d_array(cols, rows)

    # Física de toda a areia
    for i in range(cols):
        for j in range(rows):
            state = grid[i][j]
            velocity = velocity_grid[i][j]
            moved = False

            if state > 0:
                new_pos = int(j + velocity)
                new_pos = max(0, min(new_pos, rows - 1)) 
                for y in range(new_pos, j, -1):
                    below = grid[i][y]
                    direction = 1 if random.random() < 0.5 else -1
                    below_a = grid[i + direction][y] if within_cols(i + direction) else -1
                    below_b = grid[i - direction][y] if within_cols(i - direction) else -1

                    if below == 0:
                        next_grid[i][y] = state
                        next_velocity_grid[i][y] = velocity + gravity
                        moved = True
                        break
                    elif below_a == 0:
                        next_grid[i + direction][y] = state
                        next_velocity_grid[i + direction][y] = velocity + gravity
                        moved = True
                        break
                    elif below_b == 0:
                        next_grid[i - direction][y] = state
                        next_velocity_grid[i - direction][y] = velocity + gravity
                        moved = True
                        break

            if state > 0 and not moved:
                next_grid[i][j] = grid[i][j]
                next_velocity_grid[i][j] = velocity_grid[i][j] + gravity

    grid = next_grid
    velocity_grid = next_velocity_grid

    pygame.display.flip()

pygame.quit()
