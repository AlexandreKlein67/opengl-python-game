#shader vertex
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 2) in vec2 texCoords;

uniform mat4 u_MVP;

out vec2 v_texCoords;

void main()
{
  gl_Position = u_MVP * vec4(position, 1.0f);
  v_texCoords = texCoords;
}

#shader fragment
#version 330 core

in vec2 v_texCoords;


uniform sampler2D samplerTex;

out vec4 outColor;

void main()
{
  vec4 texel = texture(samplerTex, v_texCoords);
  outColor = texel;
}
