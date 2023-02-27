#Base: https://stackoverflow.com/questions/66623528/drawing-a-cube-with-pygame-and-opengl-in-python-environment

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# La lista de vertices que forman un cubo de lado 2
vertices=[
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1 ,1 ,1)
    ]

#La lista de las caras con el indice de los vertices que las conforman
caras = [
    (0, 1, 2, 3),
    (0, 3, 4, 5),
    (0, 1, 6, 5),
    (1, 2, 7, 6),
    (2, 3, 4, 7),
    (4, 5, 6, 7)
]

#Lista de los colores usados. La paleta seleccionada es: https://coolors.co/palette/01befe-ffdd00-ff7d00-ff006d-adff02-8f00ff
colores = [
    (0.004, 0.745, 0.996), 
    (1.00, 0.867, 0),
    (1.00, 0.49, 0),
    (1.00, 0, 0.427),
    (0.678, 1.00, 0.008),
    (0.561, 0, 1.00)

]

#Funcion para dibujar el cubo
def cubo():
    """
    Para cada dibujamos un cuadrilatero del color correspondiente.
    Ademas vamos a contornearlas con un color gris para que sean mas
    distinguibles entre si
    """
    for color,cara in zip(colores,caras):
        #Lineas
        glLineWidth(7.0)
        glBegin(GL_LINE_LOOP)
        #Dibujamos un loop con los indices pertenecientes a la cara
        for index in cara:
            glColor3f(0.867, 0.867, 0.867)
            glVertex3fv(vertices[index])
        glEnd()
        
        #Caras
        #"""
        glBegin(GL_QUADS)
        for index in cara:
            glColor3fv(color)
            glVertex3fv(vertices[index])
        glEnd()
        #"""

##Define main function to draw a window for the openGL
def main():
    pygame.init()
    pygame.display.set_caption('Cubito') #Nombre de la ventana
    display=(600,600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)


    gluPerspective(53, (display[0] / display[1]), 0, 50.0)
    
    
    glTranslatef(0.0, 0.0, -5)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(0.97, -23, 7, -13)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cubo()
        pygame.display.flip()
        pygame.time.wait(10)


main()