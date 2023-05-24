#version 460 core
layout (location = 0) in vec2 texcoord;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec3 pos;

 
out vec2 uvs;


uniform mat4 m_proj;
uniform mat4 m_model_view;

void main(){
    uvs = vec2(texcoord.x, texcoord.y);
    gl_Position = m_proj * m_model_view * vec4(pos.x, pos.y, pos.z, 1.0);
}