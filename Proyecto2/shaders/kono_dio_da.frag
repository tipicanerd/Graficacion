#version 460 core
in vec2 uvs;

uniform sampler2D tex;
uniform float alpha;

void main(){
    vec3 color = texture(tex,uvs).rgb;
    gl_FragColor = vec4(color, alpha);
}