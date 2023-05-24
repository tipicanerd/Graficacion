#Modelo DIO: "Dio Wry Pose" (https://skfb.ly/6uvVI) by 38badwolf is licensed under Creative Commons Attribution-NonCommercial (http://creativecommons.org/licenses/by-nc/4.0/).
#Modelo Libro: "Old Book" (https://skfb.ly/6WZHZ) by Lonit is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
#Modelo Mesa: "Coffee table" (https://skfb.ly/6wPQG) by Asia Matusik is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).

#Base textura: https://stackoverflow.com/q/58967457
#Base movimientos: https://stackoverflow.com/questions/59823131/how-to-rotate-a-cube-using-mouse-in-pyopengl

import ctypes
import numpy as np
import os
import pygame
from pygame.locals import *
from pyglet.gl import *
from pywavefront import visualization
from pywavefront import Wavefront
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

#### VARIABLES GLOBALES ###
sys.path.append('..')

################
#### CUARTO ####
################
# La lista de vertices que forman un cubo de lado 2
vertices=[
    (1.5, -1, -1), (1.5, 1, -1), (-1.5, 1, -1), (-1.5, -1, -1),
    (-1.5, -1, 1), (1.5, -1, 1), (1.5, 1, 1), (-1.5 ,1 ,1)
    ]

#La lista de las caras con el indice de los vertices que las conforman
caras = [
    (0, 1, 2, 3), #Cara trasera
    (3, 4, 5, 0), #Cara inferior
    (0, 1, 6, 5), #cara derecha
    (6, 1, 2, 7), #Cara superior
    (4, 7, 2, 3), #Cara izquierda
]


#Lista de las normales
normales = [
    (0.0, 0.0, -1.0), #Cara trasera
    (0.0, -1.0, 0.0), #Cara inferior
    (1.0, 0.0, 0.0), #Cara derecha
    (0.0, 1.0, 0.0), #Cara superior
    (-1.0, 0.0, 0.0), #Cara izquierda
]

#Vertices de texturas
vertices_textura = [
    (0.0, 0.0),
    (-1.0, 0.0),
    (-1.0, 1.0),
    (0.0, 1.0),
]

#Cargar textura
def cargar_textura(archivo):
    id =  glGenTextures(1)
    textureSurface = pygame.image.load(archivo)
    textureData = pygame.image.tostring(textureSurface, "RGBA")
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    glBindTexture(GL_TEXTURE_2D, id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
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
        id = cargar_textura("./media/Buff-Common-Architextures.jpg")
        glEnable(GL_TEXTURE_2D)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,[1.0,1.0, 1.0])
        glBindTexture(GL_TEXTURE_2D, id)
        glBegin(GL_QUADS)
        glNormal3fv(normales[i])
        for i,index in enumerate(cara):
            glVertex3fv(vertices[index])
            glTexCoord2fv(vertices_textura[i])
        glEnd()
        glDisable(GL_TEXTURE_2D)
    glFlush()

#################
#### OBJETOS ####
#################

def mesa():
    mesa_path = os.path.join(os.path.dirname(__file__), 'table/table.obj')
    mesa = Wavefront(mesa_path)
    visualization.draw(mesa)

def libro():
    libro_path = os.path.join(os.path.dirname(__file__), 'oldbook/oldbook.obj')
    libro = Wavefront(libro_path)
    visualization.draw(libro)

def Dio():
    DIO_path = os.path.join(os.path.dirname(__file__), 'dio-wry-pose/wry.obj')
    DIO = Wavefront(DIO_path).materials.pop(0)
    return DIO

###############
#### LUCES ####
###############

def luzRoja():
    color = (1.0, 0.0, 0.0, 0.75)
    pos = (1.0, -0.75, 0.75)
    glEnable(GL_LIGHT1)
    glMaterialfv(GL_FRONT, GL_DIFFUSE,color)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, color)
    glLightfv(GL_LIGHT1, GL_SPECULAR, color)
    glLightfv(GL_LIGHT1, GL_POSITION, pos)

def luzVerde():
    color = (0.0, 1.0, 0.0, 0.75)
    pos = (-1.0, 0.75, 0.75)
    glEnable(GL_LIGHT2)
    glMaterialfv(GL_FRONT, GL_DIFFUSE,color)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, color)
    glLightfv(GL_LIGHT2, GL_SPECULAR, color)
    glLightfv(GL_LIGHT2, GL_POSITION, pos)

def luzAzul():
    color = (0.0, 0.0, 1.0, 0.75)
    pos = (-1.0, -0.75, 0.75)
    glEnable(GL_LIGHT3)
    glMaterialfv(GL_FRONT, GL_DIFFUSE,color)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, color)
    glLightfv(GL_LIGHT3, GL_SPECULAR, color)
    glLightfv(GL_LIGHT3, GL_POSITION, pos)

#################
#### SHADERS ####
#################

vert_shader = '''
#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;
void main() {
    gl_Position = vec4(in_position, 1.0);
}
'''

frag_shader = '''
#version 330 core

void main() {
    gl_FragColor = vec4(0.5f, 0.0f,0.5f,1.0f);
}
'''






def Main():
    ##############################
    #### VARIABLES AUXILIARES ####
    ##############################
    posz = -5.0 #Zoom

    luzRojaOn, luzVerdeOn, luzAzulOn = 1,1,1 #Luces variantes
    
    #DIO
    DIO = Dio()
    seRie = 0
    sePresenta = 0
    DIO_posx, DIO_posz = 0.5, -0.05
    DIO_rot = 0



    pygame.init()

    pygame.mixer.init()
    pygame.mixer.set_num_channels(1)
    risa = pygame.mixer.Sound("media/risa.mp3")
    presentacion = pygame.mixer.Sound("media/kono-dio-da.mp3")

    pygame.display.set_caption('Dio en el calabazo') #Nombre de la ventana
    display=(1000,800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    

    # LUCES FIJAS
    glEnable(GL_LIGHTING)
    colorl = (1.0, 1.0, 1.0, 0.75)
    posl = (1.0, 0.75, 0.75)
    glEnable(GL_LIGHT0)
    glMaterialfv(GL_FRONT, GL_DIFFUSE,colorl)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, colorl)
    glLightfv(GL_LIGHT0, GL_SPECULAR, colorl)
    glLightfv(GL_LIGHT0, GL_POSITION, posl)

    glEnable(GL_LIGHTING)
    colorl = (1.0, 1.0, 1.0, -0.1)
    posl = (0.0, 0.0, 1.25)
    glEnable(GL_LIGHT4)
    glMaterialfv(GL_FRONT, GL_DIFFUSE,colorl)
    glLightfv(GL_LIGHT4, GL_DIFFUSE, colorl)
    glLightfv(GL_LIGHT4, GL_SPECULAR, colorl)
    glLightfv(GL_LIGHT4, GL_POSITION, posl)

    

    # CUBO
    mover_cubo = False
    while True:
        # LUCES VARIANTES
        #Roja
        if luzRojaOn:
            luzRoja()
        else:
            glDisable(GL_LIGHT1)
        #Verde
        if luzVerdeOn:
            luzVerde()
        else:
            glDisable(GL_LIGHT2)
        #Azul
        if luzAzulOn:
            luzAzul()
        else:
            glDisable(GL_LIGHT3)

        glMatrixMode(GL_MODELVIEW)  
        modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        
        glPushMatrix()
        glLoadIdentity()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                if mover_cubo == True:
                    glRotatef(event.rel[1], 1, 0, 0)
                    glRotatef(event.rel[0], 0, 1, 0)

            if event.type == pygame.KEYDOWN:
                # ZOOM
                if event.key == pygame.K_PLUS:
                    posz += 0.05
                elif event.key == pygame.K_MINUS:
                    posz -= 0.05
                
                #LUCES
                elif event.key == pygame.K_r:
                    luzRojaOn = (luzRojaOn+1)%2
                elif event.key == pygame.K_g:
                    luzVerdeOn = (luzVerdeOn+1)%2
                elif event.key == pygame.K_b:
                    luzAzulOn = (luzAzulOn+1)%2
                
                #DIO
                elif event.key == pygame.K_d:
                    sePresenta = 1
                elif event.key == pygame.K_j:
                    seRie = (seRie+1)%2
                elif event.key == pygame.K_DOWN:
                    DIO_posz += 0.07
                elif event.key == pygame.K_UP:
                    DIO_posz -= 0.07
                elif event.key == pygame.K_RIGHT:
                    DIO_posx += 0.07
                elif event.key == pygame.K_LEFT:
                    DIO_posx -= 0.07
                
        for event in pygame.mouse.get_pressed():
            if pygame.mouse.get_pressed()[0] == 1:
                mover_cubo = True
            elif pygame.mouse.get_pressed()[0] == 0:
                mover_cubo = False

        


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMultMatrixf(modelMatrix)
        modelMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        

        glLoadIdentity()
        
        glTranslatef(0, 0, posz)
        glMultMatrixf(modelMatrix)

        #cubo()

        glPushMatrix()
        glTranslate(-1.2, -1.0, -0.5)
        mesa()
        glTranslate(0.0,0.725, 0.0)
        glScale(0.15,0.15,0.15)
        libro()
        glPopMatrix()
        

        
        glPushMatrix()
        glTranslate(DIO_posx, -1.1, DIO_posz)
        glScale(0.009,0.009,0.009)
        glRotate(50,0+(13*pow(-1,DIO_rot)),-50,0)
        if seRie:
            risa.play()
            DIO_rot = (DIO_rot+1)%2
        elif sePresenta:
            presentacion.play()
            sePresenta = 0
        else:
            pygame.mixer.Sound.stop(risa)
            DIO_rot = 0
        
        if DIO_posx < 0.1:
            visualization.draw(DIO)
        else:
            visualization.draw(DIO)
        glPopMatrix()

        glPopMatrix()
        

        pygame.display.flip()
        pygame.time.wait(10)

Main()