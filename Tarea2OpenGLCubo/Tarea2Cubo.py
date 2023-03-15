"""
pip install pygame
pip install OpenGL
"""

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
    (0, 1, 2, 3), #Cara trasera
    (0, 3, 4, 5), #Cara inferior
    (0, 1, 6, 5), #cara derecha
    (1, 2, 7, 6), #Cara superior
    (2, 3, 4, 7), #Cara izquierda
    (4, 5, 6, 7) #Cara delantera
]

#Lista de las normales
normales = [
    (0.0, 0.0, -1.0), #Cara trasera
    (0.0, -1.0, 0.0), #Cara inferior
    (1.0, 0.0, 0.0), #Cara derecha
    (0.0, 1.0, 0.0), #Cara superior
    (-1.0, 0.0, 0.0), #Cara izquierda
    (0.0, 0.0, 1.0)  #Cara delantera
]

#Lista de los colores usados. La paleta seleccionada es: https://coolors.co/palette/01befe-ffdd00-ff7d00-ff006d-adff02-8f00ff
colores = [
    (0.004, 0.745, 0.996, 1), #Azul
    (1.00, 0.867, 0, 1), #Amarillo
    (1.00, 0.49, 0, 1), #Naranja
    (1.00, 0, 0.427, 1), #Rosa
    (0.678, 1.00, 0.008, 1), #Verde
    (0.561, 0, 1.00, 1) #Morado

]

#Funcion para dibujar el cubo
def cubo():
    """
    Para cada dibujamos un cuadrilatero del color correspondiente.
    Ademas vamos a contornearlas con un color gris para que sean mas
    distinguibles entre si
    """
    glBegin(GL_QUADS)
    for color,cara,normal in zip(colores,caras, normales):
        #Caras
        glNormal3fv(normal)
        for index in cara:
            glColor4fv(color)
            glVertex3fv(vertices[index])

    glEnd()
    glFlush()
        
    

##Define main function to draw a window for the openGL
def main():
    pygame.init()
    pygame.display.set_caption('Cubito') #Nombre de la ventana
    display=(600,600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)



    glMatrixMode(GL_MODELVIEW)
    
    glTranslatef(0.0, 0.0, -5)
    #glRotatef(45, 90.0, 120.0, 0.0)
    
    #glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 90.0, 120.0, 0.0)
        cubo()
        pygame.display.flip()
        pygame.time.wait(20)


main()