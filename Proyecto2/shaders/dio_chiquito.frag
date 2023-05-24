#version 460 core
in vec2 uvs;

uniform sampler2D tex;

void main(){
    gl_FragColor = texture(tex,uvs);
}