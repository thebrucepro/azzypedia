import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import sys

def load_texture(image_path):
    try:
        img = Image.open(image_path).convert('RGBA')  # Asegura canal alfa
        img_data = np.array(img, dtype=np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        sys.exit(1)

def draw_textured_quad():
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)  # antes (0, 0)
    glVertex3f(-1, -1, 0)
    glTexCoord2f(1, 1)  # antes (1, 0)
    glVertex3f(1, -1, 0)
    glTexCoord2f(1, 0)  # antes (1, 1)
    glVertex3f(1, 1, 0)
    glTexCoord2f(0, 0)  # antes (0, 1)
    glVertex3f(-1, 1, 0)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, display[0]/display[1], 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)  # Activar buffer de profundidad

    texture_id = load_texture("logo_nuevo.jpg")

    angle = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)  # Rotar en eje Y
        glBindTexture(GL_TEXTURE_2D, texture_id)
        draw_textured_quad()
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)
        angle += 1

main()
