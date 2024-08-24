uniform vec2 resolution;
uniform float time;

void main() {
  vec2 uv = gl_FragCoord.xy / resolution;
  vec3 color = vec3(uv.x, uv.y, abs(sin(time)));
  gl_FragColor = vec4(color, 1.0);
}
