#version 460 core
layout (location = 0) in vec2 texcoord;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec3 pos;
 

out vec2 uvs;
out vec3 Normal;
out vec3 Fragpos;

uniform mat4 m_proj;
uniform mat4 m_model_view;


void main(){
    Normal = mat3(transpose(inverse(m_model_view))) * normalize(normal);
    uvs = vec2(texcoord.y, texcoord.x);
    Fragpos = vec3(m_model_view * vec4(pos.x, pos.y, pos.z, 1.0));
    
    gl_Position = m_proj * m_model_view * vec4(pos.x, pos.y, pos.z, 1.0);
    
}
