from ctypes import sizeof, c_void_p
import numpy as np
import pygame
from pyglet.gl import *
from pywavefront import Wavefront, visualization
from OpenGL.GL import *
import os


class Base:
    def __init__(self, texture_path, obj_path, vertex_shader_path, fragment_shader_path, escala=1.0) :
        self.texture = os.path.join(os.path.dirname(__file__), texture_path)
        self.tex_id = glGenTextures(1)
        self.obj = self.cargar_obj(os.path.join(os.path.dirname(__file__), obj_path))
        self.escala = escala
        self.vertices = self.generar_vertices(self.obj)
        self.vertex_shader = self.cargar_shader(vertex_shader_path)
        self.fragment_shader = self.cargar_shader(fragment_shader_path)
        self.vao, self.program = self.generar_programa()

    def cargar_obj(self,obj_path):
        return  Wavefront(obj_path, collect_faces=True)
    
    def cargar_shader(self,shader_path):
        with open(shader_path, "r") as file: 
            shader = file.read()
        return shader
    
    def generar_vertices(self, obj):
        vertices = np.array(obj.mesh_list[0].materials[0].vertices, dtype='f4')*self.escala
        return (GLfloat * len(vertices))(*vertices)

    def generar_programa(self):
        # PROGRAMA
        program = glCreateProgram()


        # VERTEX SHADER
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, self.vertex_shader)
        glCompileShader(vertex_shader)


        # FRAGMENT SHADER
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, self.fragment_shader)
        glCompileShader(fragment_shader)


        # ENLACE
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

        glLinkProgram(program)


        # VBO
        vbo = None
        vbo = glGenBuffers(1, vbo)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.vertices), self.vertices, GL_STATIC_DRAW)


        # VAO
        vao = None
        vao = glGenVertexArrays(1, vao)
        
        glBindVertexArray(vao) 


        # DATOS
        #texcoord
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(0))
        glEnableVertexAttribArray(0)
        #normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(2 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)
        #pos
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(5 * sizeof(GLfloat)))
        glEnableVertexAttribArray(2)


        # TEXTURA
        textureSurface = pygame.image.load(self.texture)
        textureData = pygame.image.tostring(textureSurface, "RGBA")
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return vao, program
    
    def draw(self, m_proj,m_model_view,viewPos,ambiente, colores_fijos, pos_fijas, color_var, pos_var, lucesOn):
        glUseProgram(self.program)
        
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glUniform1i(glGetUniformLocation(self.program, 'tex'), 0)
        
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_proj',),  1, GL_FALSE, m_proj)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_model_view',),  1, GL_FALSE, m_model_view)
        glUniform3fv(glGetUniformLocation(self.program,"viewPos",), 1,viewPos)

        for i, color in enumerate(colores_fijos):
                    glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.position',),  1, pos_fijas[i])
                    glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Ia',),  1, ambiente)
                    glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Id',),  1, color)
                    glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Is',),  1, color)

        for i, inicial in enumerate(["R","G","B"]):
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.position',),  1, pos_var[i])
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Ia',),  1, ambiente)
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Id',),  1, color_var[i])
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Is',),  1, color_var[i])
            glUniform1f(glGetUniformLocation(self.program,f'On{inicial}',), lucesOn[i])
        glUseProgram(0)
    

    
         
class Libro(Base):
    def __init__(self, texture_path, obj_path, vertex_shader_path, fragment_shader_path, escala=0.2):
        super().__init__(texture_path, obj_path, vertex_shader_path, fragment_shader_path, escala)
        self.elevacion = 0.0

    
    def draw(self, m_proj, m_model_view, viewPos,ambiente, colores_fijos, pos_fijas, color_var, pos_var, lucesOn):
        glUseProgram(self.program)
        
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glUniform1i(glGetUniformLocation(self.program, 'tex'), 0)
        
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))

        glUniform1f(glGetUniformLocation(self.program, "elevacion"), self.elevacion)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_proj',),  1, GL_FALSE, m_proj)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_model_view',),  1, GL_FALSE, m_model_view)
        glUniform3fv(glGetUniformLocation(self.program,"viewPos",), 1,viewPos)

        for i, color in enumerate(colores_fijos):
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.position',),  1, pos_fijas[i])
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Ia',),  1, ambiente)
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Id',),  1, color)
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Is',),  1, color)

        for i, inicial in enumerate(["R","G","B"]):
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.position',),  1, pos_var[i])
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Ia',),  1, ambiente)
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Id',),  1, color_var[i])
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Is',),  1, color_var[i])
            glUniform1f(glGetUniformLocation(self.program,f'On{inicial}',), lucesOn[i])
        glUseProgram(0)




class Dio:
    def __init__(self):
        self.textures = ["dio-wry-pose/ntxr000.png", "dio-wry-pose/ntxr004.png"]
        self.tex_ids = [glGenTextures(1) for i in range(2)]
        self.obj = self.cargar_obj(os.path.join(os.path.dirname(__file__), "dio-wry-pose/wry.obj"))
        self.escala = 0.015
        self.lista_vertices = self.generar_vertices(self.obj)
        self.vertex_shader = self.cargar_shader("shaders/dio.vert")
        self.fragment_shader = self.cargar_shader("shaders/default.frag")
        self.lista_vaos, self.program = self.generar_programa()

    def cargar_obj(self,obj_path):
        return  Wavefront(obj_path, collect_faces=True)
    
    def cargar_shader(self,shader_path):
        with open(shader_path, "r") as file: 
            shader = file.read()
        return shader
    
    def generar_vertices(self, obj):
        lista_vertices = []
        for i in range(len(obj.mesh_list[0].materials[1:])):
            vertices = list(np.array(obj.mesh_list[0].materials[i].vertices, dtype='f4'))
            vertices = (GLfloat * len(vertices))(*vertices)
            lista_vertices.append(vertices)
        return lista_vertices

    def generar_programa(self):
        # PROGRAMA
        program = glCreateProgram()


        # VERTEX SHADER
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, self.vertex_shader)
        glCompileShader(vertex_shader)


        # FRAGMENT SHADER
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, self.fragment_shader)
        glCompileShader(fragment_shader)


        # ENLACE
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

        glLinkProgram(program)

        lista_vaos = []

        for i, vertices in enumerate(self.lista_vertices):
            # VBO
            vbo = None
            vbo = glGenBuffers(1, vbo)

            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW)


            # VAO
            vao = None
            vao = glGenVertexArrays(1, vao)
            
            glBindVertexArray(vao) 


            # DATOS
            #texcoord
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(0))
            glEnableVertexAttribArray(0)
            #normal
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(2 * sizeof(GLfloat)))
            glEnableVertexAttribArray(1)
            #pos
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(5 * sizeof(GLfloat)))
            glEnableVertexAttribArray(2)


            lista_vaos.append(vao)

            # TEXTURA
            textureSurface = pygame.image.load(self.textures[i])
            textureData = pygame.image.tostring(textureSurface, "RGBA")
            width = textureSurface.get_width()
            height = textureSurface.get_height()
            glBindTexture(GL_TEXTURE_2D, self.tex_ids[i])
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return lista_vaos, program
    
    def draw(self,m_proj, m_model_view, viewPos, ambiente, colores_fijos, pos_fijas, color_var, pos_var, lucesOn):
        glUseProgram(self.program)
        for i in range(len(self.lista_vaos)):
            glBindTexture(GL_TEXTURE_2D, self.tex_ids[i])
            glUniform1i(glGetUniformLocation(self.program, 'tex'), 0)
            glBindVertexArray(self.lista_vaos[i])
            glDrawArrays(GL_TRIANGLES, 0, len(self.lista_vertices[i]))
            
            #PROYECCION Y VISTA
            glUniformMatrix4fv(glGetUniformLocation(self.program,'m_proj',),  1, GL_FALSE, m_proj)
            glUniformMatrix4fv(glGetUniformLocation(self.program,'m_model_view',),  1, GL_FALSE, m_model_view)
            glUniform3fv(glGetUniformLocation(self.program,'viewPos',),  1, viewPos)

            #LUCES FIJAS
            for i, color in enumerate(colores_fijos):
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.position',),  1, pos_fijas[i])
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Ia',),  1, ambiente)
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Id',),  1, color)
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Is',),  1, color)

            for i, inicial in enumerate(["R","G","B"]):
                glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.position',),  1, pos_var[i])
                glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Ia',),  1, ambiente)
                glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Id',),  1, color_var[i])
                glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Is',),  1, color_var[i])
                glUniform1f(glGetUniformLocation(self.program,f'On{inicial}',), lucesOn[i])
        glUseProgram(0)




class Cuarto:
    def __init__(self,) :
        self.texture = os.path.join(os.path.dirname(__file__), "./media/Buff-Common-Architextures.jpg")
        self.tex_id = glGenTextures(1)
        self.escala = 1.0
        self.vertices = self.generar_vertices("modelos_propios/cuarto.npy")
        self.vertex_shader = self.cargar_shader("shaders/cuarto.vert")
        self.fragment_shader = self.cargar_shader("shaders/default.frag")
        self.vao, self.program = self.generar_programa()

    def cargar_obj(self,obj_path):
        return  Wavefront(obj_path, collect_faces=True)
    
    def cargar_shader(self,shader_path):
        with open(shader_path, "r") as file: 
            shader = file.read()
        return shader
    
    def generar_vertices(self, vertex_path):
        vertices = np.load(vertex_path)*self.escala
        return (GLfloat * len(vertices))(*vertices)

    def generar_programa(self):
        # PROGRAMA
        program = glCreateProgram()


        # VERTEX SHADER
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, self.vertex_shader)
        glCompileShader(vertex_shader)


        # FRAGMENT SHADER
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, self.fragment_shader)
        glCompileShader(fragment_shader)


        # ENLACE
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

        glLinkProgram(program)


        # VBO
        vbo = None
        vbo = glGenBuffers(1, vbo)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.vertices), self.vertices, GL_STATIC_DRAW)


        # VAO
        vao = None
        vao = glGenVertexArrays(1, vao)
        
        glBindVertexArray(vao) 


        # DATOS
        #texcoord
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(0))
        glEnableVertexAttribArray(0)
        #normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(2 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)
        #pos
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(5 * sizeof(GLfloat)))
        glEnableVertexAttribArray(2)


        # TEXTURA
        textureSurface = pygame.image.load(self.texture)
        textureData = pygame.image.tostring(textureSurface, "RGBA")
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return vao, program
    
    def draw(self,m_proj, m_model_view, viewPos, ambiente, colores_fijos, pos_fijas, color_var, pos_var, lucesOn):
        glUseProgram(self.program)
        
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glUniform1i(glGetUniformLocation(self.program, 'tex'), 0)
        
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, len(self.vertices))
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_proj',),  1, GL_FALSE, m_proj)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_model_view',),  1, GL_FALSE, m_model_view)
        glUniform3fv(glGetUniformLocation(self.program,"viewPos",), 1, viewPos)
        for i, color in enumerate(colores_fijos):
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.position',),  1, pos_fijas[i])
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Ia',),  1, ambiente)
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Id',),  1, color)
                glUniform3fv(glGetUniformLocation(self.program,f'light{i+1}.Is',),  1, color)

        for i, inicial in enumerate(["R","G","B"]):
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.position',),  1, pos_var[i])
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Ia',),  1, ambiente)
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Id',),  1, color_var[i])
            glUniform3fv(glGetUniformLocation(self.program,f'light{inicial}.Is',),  1, color_var[i])
            glUniform1f(glGetUniformLocation(self.program,f'On{inicial}',), lucesOn[i])
        glUseProgram(0)




class Dio_chiquito:
    def __init__(self):
        self.textures = [f"./media/DIOWalk{idx}.png" for idx in range(16)]
        self.tex_ids = [glGenTextures(1) for _ in range(16)]
        self.vertices = self.generar_vertices("./modelos_propios/DIO_chiquito.npy")
        self.vertex_shader = self.cargar_shader("shaders/dio_chiquito.vert")
        self.fragment_shader = self.cargar_shader("shaders/dio_chiquito.frag")
        self.vao, self.program = self.generar_programa()
        self.dx = 0.0

    def cargar_shader(self,shader_path):
        with open(shader_path, "r") as file: 
            shader = file.read()
        return shader
    
    def generar_vertices(self, vertex_path):
        vertices = np.load(vertex_path)
        return (GLfloat * len(vertices))(*vertices)

    def generar_programa(self):
        # PROGRAMA
        program = glCreateProgram()


        # VERTEX SHADER
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, self.vertex_shader)
        glCompileShader(vertex_shader)


        # FRAGMENT SHADER
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, self.fragment_shader)
        glCompileShader(fragment_shader)


        # ENLACE
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

        glLinkProgram(program)

        # VBO
        vbo = None
        vbo = glGenBuffers(1, vbo)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.vertices), self.vertices, GL_STATIC_DRAW)


        # VAO
        vao = None
        vao = glGenVertexArrays(1, vao)
        
        glBindVertexArray(vao) 


        # DATOS
        #texcoord
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(0))
        glEnableVertexAttribArray(0)
        #normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(2 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)
        #pos
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(5 * sizeof(GLfloat)))
        glEnableVertexAttribArray(2)

        # TEXTURAS
        for i in range(len(self.textures)):
            textureSurface = pygame.image.load(self.textures[i])
            textureData = pygame.image.tostring(textureSurface, "RGBA")
            width = textureSurface.get_width()
            height = textureSurface.get_height()
            glBindTexture(GL_TEXTURE_2D, self.tex_ids[i])
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return vao, program
    

    def draw(self, texi, m_proj, m_model_view):
        glUseProgram(self.program)
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.tex_ids[texi])
        glUniform1i(glGetUniformLocation(self.program, 'tex'), 0)
        
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, len(self.vertices))

        glUniform1f(glGetUniformLocation(self.program, 'dx'), self.dx)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_proj',),  1, GL_FALSE, m_proj)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_model_view',),  1, GL_FALSE, m_model_view)
        glUseProgram(0)
    
class Kono_Dio_da:
    def __init__(self):
        self.texture = "media/KonoDioDa.jpg"
        self.tex_id = glGenTextures(1)
        self.vertices = self.generar_vertices("modelos_propios/konoDioDa.npy")
        self.vertex_shader = self.cargar_shader("shaders/kono_dio_da.vert")
        self.fragment_shader = self.cargar_shader("shaders/kono_dio_da.frag")
        self.vao, self.program = self.generar_programa()

    def cargar_shader(self,shader_path):
        with open(shader_path, "r") as file: 
            shader = file.read()
        return shader

    def generar_vertices(self, vertex_path):
        vertices = np.load(vertex_path)
        return (GLfloat * len(vertices))(*vertices)

    def generar_programa(self):
        # PROGRAMA
        program = glCreateProgram()


        # VERTEX SHADER
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, self.vertex_shader)
        glCompileShader(vertex_shader)


        # FRAGMENT SHADER
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, self.fragment_shader)
        glCompileShader(fragment_shader)


        # ENLACE
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)

        glLinkProgram(program)

        # VBO
        vbo = None
        vbo = glGenBuffers(1, vbo)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.vertices), self.vertices, GL_STATIC_DRAW)


        # VAO
        vao = None
        vao = glGenVertexArrays(1, vao)

        glBindVertexArray(vao) 


        # DATOS
        #texcoord
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(0))
        glEnableVertexAttribArray(0)
        #normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(2 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)
        #pos
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), c_void_p(5 * sizeof(GLfloat)))
        glEnableVertexAttribArray(2)

        # TEXTURAS
        textureSurface = pygame.image.load(self.texture)
        textureData = pygame.image.tostring(textureSurface, "RGBA")
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return vao, program


    def draw(self, alpha, m_proj, m_model_view):
        glUseProgram(self.program)
        
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glUniform1i(glGetUniformLocation(self.program, 'tex'), 0)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, len(self.vertices))
        glUniform1f(glGetUniformLocation(self.program, 'alpha',), alpha)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_proj',),  1, GL_FALSE, m_proj)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'m_model_view',),  1, GL_FALSE, m_model_view)
        glUseProgram(0)
