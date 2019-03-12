#shader vertex
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
layout(location = 2) in vec2 tex_coords;

uniform mat4 u_MVP;

out vec4 frag_color;
out vec2 frag_tex_coords;

void main()
{
  gl_Position = u_MVP * vec4(position, 1.0f);
  frag_color = vec4(color, 1.0);
  frag_tex_coords = tex_coords;
}

#shader fragment
#version 330 core

in vec2 frag_tex_coords;
in vec4 frag_color;
uniform sampler2D samplerTex;

out vec4 outColor;

void main()
{
  vec4 texel = texture(samplerTex, frag_tex_coords);
  outColor = texel + frag_color;
}
