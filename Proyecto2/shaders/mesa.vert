#version 460 core
layout (location = 0) in vec2 texcoord;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec3 pos;


out vec2 uvs;
out vec3 Normal;
out vec3 Fragpos;

uniform mat4 m_proj;
uniform mat4 m_model_view;

float scaleFactor = 2.0;

void main(){
    mat4 scaleMatrix = mat4(
        scaleFactor, 0.0, 0.0, 0.0,
        0.0, scaleFactor, 0.0, 0.0,
        0.0, 0.0, scaleFactor, 0.0,
        0.0, 0.0, 0.0, 1.0
    );
    Normal = mat3(transpose(inverse(m_model_view))) * normalize(normal);
    uvs = vec2(texcoord.x, texcoord.y);
    vec3 fpos = (scaleMatrix*vec4(pos.x, pos.y, pos.z, 1.0)).xyz;
    Fragpos = vec3(m_model_view * vec4(fpos.x, fpos.y, fpos.z, 1.0));
    gl_Position = m_proj * m_model_view *vec4(fpos.x, fpos.y, fpos.z, 1.0);
}