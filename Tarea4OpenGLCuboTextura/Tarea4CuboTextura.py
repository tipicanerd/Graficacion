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
    (3, 4, 5, 0), #Cara inferior
    (0, 1, 6, 5), #cara derecha
    (6, 1, 2, 7), #Cara superior
    (4, 7, 2, 3), #Cara izquierda
    (5, 6, 7, 4) #Cara delantera
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

#Lista de texturas
texturas = [
    "./texturas/folklore.jpg", #Cara trasera
    "./texturas/redtv.jpg", #Cara inferior
    "./texturas/lover.jpg", #Cara derecha
    "./texturas/fearlesstv.png", #Cara superior
    "./texturas/evermore.jpg", #Cara izquierda
    "./texturas/midnights.jpg", #Cara delantera
]

#Vertices de texturas
vertices_textura = [
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0),
]

#Cargar textura
#Base: https://stackoverflow.com/q/58967457
def cargar_textura(archivo):
    id =  glGenTextures(1)
    textureSurface = pygame.image.load(archivo)
    textureData = pygame.image.tostring(textureSurface, "RGBA")
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    glBindTexture(GL_TEXTURE_2D, id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return id 
def cubo():
    """
    Para cada dibujamos un cuadrilatero del color correspondiente.
    Ademas vamos a contornearlas con un color gris para que sean mas
    distinguibles entre si
    """
    
    for i,cara in enumerate(caras):
        #Caras
        id = cargar_textura(texturas[i])
        glEnable(GL_TEXTURE_2D)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,[1.0,1.0,1.0])
        glBindTexture(GL_TEXTURE_2D, id)
        glBegin(GL_QUADS)
        glNormal3fv(normales[i])
        for i,index in enumerate(cara):
            glVertex3fv(vertices[index])
            glTexCoord2fv(vertices_textura[i])
        glEnd()
        glDisable(GL_TEXTURE_2D)
    glFlush()
        
    

##Define main function to draw a window for the openGL
def main():
    pygame.init()
    pygame.display.set_caption('Cubito con texturas') #Nombre de la ventana
    display=(600,600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    
    #Para que rote bien
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    
    #############
    ####LUCES####
    #############

    glEnable(GL_LIGHTING)

    ##LUZ 2
    colorl2 = (1.0, 1.0, 1.0, 0.75)
    posl2 = (1.2, 1.3, 4)
    glEnable(GL_LIGHT1)
    glMaterialfv(GL_FRONT, GL_DIFFUSE,colorl2)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, colorl2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, colorl2)
    glLightfv(GL_LIGHT1, GL_POSITION, posl2)

    glMatrixMode(GL_MODELVIEW)
    
    glTranslatef(0.0, 0.0, -5)
    
    #glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(7, 100.0, 100.0, 45.0)
        cubo()
        pygame.display.flip()
        pygame.time.wait(10)


main()