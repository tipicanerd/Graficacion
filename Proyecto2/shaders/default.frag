#version 460 core
in vec2 uvs;
in vec3 Normal;
in vec3 Fragpos;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform sampler2D tex;
uniform vec3 viewPos;
uniform Light light1;
uniform Light light2;
uniform Light lightR;
uniform float OnR;
uniform Light lightG;
uniform float OnG;
uniform Light lightB;
uniform float OnB;



vec3 getLight(vec3 color, Light light) {
    vec3 normal = normalize(Normal);

    // ambient light
    vec3 ambient = light.Ia;

    // diffuse light
    vec3 lightDir = normalize(light.position - Fragpos);
    float diff = max(0, dot(lightDir, normal));
    vec3 diffuse = diff * light.Id;

    // specular light
    vec3 viewDir = normalize(viewPos - Fragpos);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    return color * (ambient + diffuse + specular);
}

void main(){
    float gamma = 2.2;
    vec3 color_base = texture(tex,uvs).rgb;
    color_base = pow(color_base, vec3(gamma));
    
    vec3 color1 = getLight(color_base, light1);
    //color1 = pow(color1, 1 / vec3(gamma));

    vec3 color2 = getLight(color_base, light2);
    //color2 = pow(color2, 1 / vec3(gamma));

    vec3 colorR = getLight(color_base, lightR);
    //colorR = pow(colorR, 1 / vec3(gamma));

    vec3 colorG = getLight(color_base, lightG);
    //colorG = pow(colorG, 1 / vec3(gamma));

    vec3 colorB = getLight(color_base, lightB);
    //colorB = pow(colorB, 1 / vec3(gamma));

    vec3 colorF = 0.45*color1 + 0.45*color2 + 0.2*OnR*colorR + 0.2*OnG*colorG + 0.2*OnB*colorB;
    colorF = pow(colorF, 1/vec3(gamma));
    gl_FragColor = vec4(colorF, 1.0) ;


}