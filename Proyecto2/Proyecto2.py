#Modelo DIO: "Dio Wry Pose" (https://skfb.ly/6uvVI) by 38badwolf is licensed under Creative Commons Attribution-NonCommercial (http://creativecommons.org/licenses/by-nc/4.0/).
#Modelo Libro: "Old Book" (https://skfb.ly/6WZHZ) by Lonit is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).
#Modelo Mesa: "Coffee table" (https://skfb.ly/6wPQG) by Asia Matusik is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).


#Base textura: https://stackoverflow.com/q/58967457
#Base movimientos: https://stackoverflow.com/questions/59823131/how-to-rotate-a-cube-using-mouse-in-pyopengl
#Base shaders: https://www.letsdevelopgames.com/2020/10/drawing-triangle-modern-opengl-with.html

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from modelos import Base, Cuarto, Dio,  Dio_chiquito, Kono_Dio_da,Libro

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(1)
alarido = pygame.mixer.Sound("media/wry.mp3")
presentacion = pygame.mixer.Sound("media/kono-dio-da.mp3")

pygame.display.set_caption('Dio en el calabazo afectado por el hamon'.upper()) #Nombre de la ventana
display_size=(1000,800)
pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)

###############
#### LUCES ####
###############

#LUCES FIJAS
#Luz blanca
colorl1 = np.array([1.0, 1.0, 1.0])
posl1 = np.array([1.0, 0.75, -0.75])

#Luz amarilla
colorl2 = np.array([1.0, 1.0, 0.22])
posl2 = np.array([0.0, 0.75, -1.25])

colores_fijos = [colorl1,colorl2]
pos_fijas = [posl1, posl2]

#Ambiente
ambiente = np.array([0.29, 0.392, 0.424])

#LUCES Variantes
# ROJA
Rcolor = np.array([1.0, 0.0, 0.0])
Rpos = np.array([1.0, -0.75, -1.75])

#VERDE
Gcolor = np.array([0.0, 1.0, 0.0])
Gpos = np.array([-1.0, 0.75, -1.75])

#AZUL
Bcolor = np.array([0.0, 0.0, 1.0])
Bpos = np.array([-1.0, -0.75, -1.75])

pos_var = [Rpos, Gpos, Bpos]
color_var = [Rcolor,Gcolor,Bcolor]

#################
#### MODELOS ####
#################

#LIBRO
texture_path = "oldbook/old_books_texture3011.jpg"
obj_path = "oldbook/oldbook.obj"
vertex_shader_path = "shaders/libro.vert"
fragment_shader_path = "shaders/default.frag"

libro = Libro(texture_path, obj_path, vertex_shader_path, fragment_shader_path)

#MESA
texture_path = "table/table_col01.tga.png"
obj_path = "table/table.obj"
vertex_shader_path = "shaders/mesa.vert"
fragment_shader_path = "shaders/default.frag"
mesa = Base(texture_path, obj_path, vertex_shader_path, fragment_shader_path)


#DIO
DIO = Dio()

#Cuarto
cuarto = Cuarto()


#DIO chiquito
DIO_chiquito = Dio_chiquito()

#Kono Dio Da
konoDioDa = Kono_Dio_da() 

#Auxiliares
cerca = 0
idx_tex = 0
seQueja = 0
sePresenta = 0
mover_cuarto = False
lucesOn = [1,1,1]
alphaDio = 0.0


# MATRICES PARA VISUALIZAR se obtuvieron por medio de:
#print(glGetFloatv(GL_MATRIZ-DE-INTERES))
m_proj = np.array([
    [ 1.9313709, 0.0, 0.0, 0.0],
    [ 0.0, 2.4142137, 0.0, 0.0],
    [ 0.0, 0.0, -1.004008, -1.0],
    [ 0.0, 0.0, -0.2004008, 0.0]
])

cam_pos = np.array([0.0,0.0,1.5])


m_model_view_cuarto = np.column_stack([np.vstack([np.eye(3), [0.0,0.0,-5.0]]), np.array([0.0,0.0,0.0,1.0])])
m_model_view_mesa = np.column_stack([np.vstack([np.eye(3), [-2.2, -2.2,  -10.0]]), np.array([0.0,0.0,0.0,1.0])])
m_model_view_libro = np.column_stack([np.vstack([np.eye(3), [-1.3, -0.425,  -5.8]]), np.array([0.0,0.0,0.0,1.0])])
m_model_view_dio = np.array([
    [ 0.6654062,  -0.08699439,  0.74139506,  0.],
    [-0.08699439 , 0.97738147,  0.19276272,  0.],
    [-0.74139506, -0.19276272,  0.64278764,  0.],
    [ 1.1, 0, -5.65, 1.]
])
m_model_view_dio_chiquito = np.column_stack([np.vstack([np.eye(3), [-1., -1.1,  -5.5]]), np.array([0.0,0.0,0.0,1.0])])

m_model_view_kono_dio_da = np.column_stack([np.vstack([np.eye(3), [0., 0.,  -5.5]]), np.array([0.0,0.0,0.0,1.0])])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEMOTION:
                if mover_cuarto == True:
                    angle = np.deg2rad(event.rel[0])
                    rotation_matrix = np.array([[1, 0, 0, 0],
                            [0, np.cos(angle), -np.sin(angle), 0],
                            [0, np.sin(angle), np.cos(angle), 0],
                            [0, 0, 0, 1]])
                    
        if event.type == pygame.KEYDOWN:
            # ZOOM
            if event.key == pygame.K_PLUS:
                m_model_view_cuarto[3,2] += 0.1
                m_model_view_mesa[3,2] += 0.1
                m_model_view_libro[3,2] += 0.1
                m_model_view_dio[3,2] += 0.1
                m_model_view_dio_chiquito[3,2] += 0.1
            if event.key == pygame.K_MINUS:
                m_model_view_cuarto[3,2] -= 0.1
                m_model_view_mesa[3,2] -= 0.1
                m_model_view_libro[3,2] -= 0.1
                m_model_view_dio[3,2] -= 0.1
                m_model_view_dio_chiquito[3,2] -= 0.1
            #LUCES
            elif event.key == pygame.K_r:
                lucesOn[0] = (lucesOn[0]+1)%2
            elif event.key == pygame.K_g:
                lucesOn[1] = (lucesOn[1]+1)%2
            elif event.key == pygame.K_b:
                lucesOn[2] = (lucesOn[2]+1)%2
            #DIO
            elif event.key == pygame.K_d:
                if alphaDio==0:
                    sePresenta = 1
                alphaDio = ((alphaDio+1)%2)/1
                
            elif event.key == pygame.K_w:
                seQueja = (seQueja+1)%2
            elif event.key == pygame.K_RIGHT:
                if DIO_chiquito.dx <= 1.5:
                    DIO_chiquito.dx += 0.03
                idx_tex = (idx_tex+1)%16
            elif event.key == pygame.K_LEFT:
                DIO_chiquito.dx -= 0.03
                idx_tex = (idx_tex-1)%16

    glClear(GL_COLOR_BUFFER_BIT)

    cuarto.draw(m_proj,m_model_view_cuarto,cam_pos,ambiente, colores_fijos, pos_fijas, color_var, pos_var, lucesOn)
    mesa.draw(m_proj,m_model_view_mesa,cam_pos,ambiente, colores_fijos, pos_fijas, color_var, pos_var, lucesOn)
    libro.draw(m_proj,m_model_view_libro, cam_pos, ambiente, colores_fijos, pos_fijas, color_var, pos_var, lucesOn)

    if seQueja:
        alarido.play()
    elif sePresenta:
        presentacion.play()
        sePresenta = 0
    else:
        pygame.mixer.Sound.stop(alarido)

    DIO.draw(m_proj,m_model_view_dio,cam_pos,ambiente, colores_fijos, pos_fijas, color_var, pos_var, lucesOn)
    DIO_chiquito.draw(idx_tex, m_proj, m_model_view_dio_chiquito)
    
    if alphaDio:
        konoDioDa.draw(alphaDio,m_proj,m_model_view_kono_dio_da)
    
    if DIO_chiquito.dx > 1.2:
        cerca = 1
    else:
        cerca = 0
    

    libro.elevacion = cerca*(libro.elevacion+0.007)
    pygame.display.flip()
