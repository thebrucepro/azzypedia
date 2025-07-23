import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

size = 11
maze = [[1 for _ in range(size)] for _ in range(size)]
player_pos = [1, 1]
goal_pos = [size-2, size-2]
win_text = None  # Variable para almacenar el mensaje de victoria

# Generación del laberinto con Prim's Algorithm
def generate_maze():
    start_x, start_y = 1, 1
    maze[start_x][start_y] = 0
    maze[goal_pos[0]][goal_pos[1]] = 0

    walls = [(start_x + dx, start_y + dy) for dx, dy in [(2,0), (0,2)] if 0 <= start_x+dx < size and 0 <= start_y+dy < size]
    
    while walls:
        x, y = random.choice(walls)
        walls.remove((x, y))

        neighbors = [(x + dx, y + dy) for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)] if 0 <= x+dx < size and 0 <= y+dy < size and maze[x+dx][y+dy] == 0]

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[x][y] = 0
            maze[(x+nx)//2][(y+ny)//2] = 0
            walls.extend([(x + dx, y + dy) for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)] if 0 <= x+dx < size and 0 <= y+dy < size and maze[x+dx][y+dy] == 1])

generate_maze()

def draw_cube(x, y, color):
    glColor3f(*color)
    vertices = [
        (x, y, 0), (x+1, y, 0), (x+1, y+1, 0), (x, y+1, 0),
        (x, y, 1), (x+1, y, 1), (x+1, y+1, 1), (x, y+1, 1)
    ]
    
    edges = [
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7)
    ]
    
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_maze():
    for x in range(size):
        for y in range(size):
            if maze[x][y] == 1:
                draw_cube(x, y, (1, 1, 1))

def draw_player():
    draw_cube(player_pos[0], player_pos[1], (1, 0, 0))

def draw_goal():
    draw_cube(goal_pos[0], goal_pos[1], (0, 1, 0))

def move_player(dx, dy):
    global win_text
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < size and 0 <= new_y < size and maze[new_x][new_y] == 0:
        player_pos[:] = [new_x, new_y]
        if player_pos == goal_pos:
            win_text = "¡Felicidades! Has encontrado la salida."

def render_text(surface, text):
    font = pygame.font.Font(None, 36)  # Fuente predeterminada de pygame
    text_surface = font.render(text, True, (255, 255, 255))
    surface.blit(text_surface, (10, 10))

def main():
    global win_text
    pygame.init()
    display = (800,600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(-size//2, -size//2, -size)

    pygame.font.init()  # Inicializar sistema de fuentes
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_player(-1, 0)
                elif event.key == pygame.K_d:
                    move_player(1, 0)
                elif event.key == pygame.K_w:
                    move_player(0, 1)
                elif event.key == pygame.K_s:
                    move_player(0, -1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_maze()
        draw_goal()
        draw_player()
        pygame.display.flip()


        if win_text:
            screen.fill((0, 0, 0))  # Fondo negro para el mensaje
            render_text(screen, win_text)
            pygame.display.flip()
            pygame.time.wait(3000)  # Esperar 3 segundos y cerrar
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
