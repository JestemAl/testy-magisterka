uniform vec2 resolution;
uniform float time;
varying vec3 vColor;
varying vec4 vGrassData;
varying vec3 vNormal;
varying vec3 vWorldPosition;

float inverseLerp(float v, float minValue, float maxValue) {
  return (v - minValue) / (maxValue - minValue);
}

float remap(float v, float inMin, float inMax, float outMin, float outMax) {
  float t = inverseLerp(v, inMin, inMax);
  return mix(outMin, outMax, t);
}

float saturate(float x) {
  return clamp(x, 0.0, 0.5);
}

float easeOut(float x, float t) {
	return 1.0 - pow(1.0 - x, t);
}

vec3 lambertLight(vec3 normal, vec3 viewDir, vec3 lightDir, vec3 lightColour) {
  float wrap = 0.5;
  float dotNL = saturate((dot(normal, lightDir) + wrap) / (1.0 + wrap));
  vec3 lighting = vec3(dotNL);
  
  float backlight = saturate((dot(viewDir, -lightDir) + wrap) / (1.0 + wrap));
  vec3 scatter = vec3(pow(backlight, 2.0));

  lighting += scatter;

  return lighting * lightColour;  
}

vec3 ambientLight(vec3 normal, vec3 groundColour, vec3 skyColour) {
  return mix(groundColour, skyColour, 0.5 * normal.y + 0.5);
}

vec3 phongSpecular(vec3 normal, vec3 lightDir, vec3 viewDir) {
  float dotNL = saturate(dot(normal, lightDir));
  
  vec3 r = normalize(reflect(-lightDir, normal));
  float phongValue = max(0.0, dot(viewDir, r));
  phongValue = pow(phongValue, 32.0);

  vec3 specular = dotNL * vec3(phongValue);
  return specular;
}

void main() {
  float xValueGrass = vGrassData.x;
  float yValueGrass = vGrassData.y;
  vec3 grassColor = mix(vColor * 0.9, vColor, smoothstep(0.2, 0.0, abs(xValueGrass)));
  // vec3 lightColour = vec3(1.0, 0.4, 0.8);
  // vec3 lightColour = vec3(1.0, 1.0, 1.0);
  vec3 lightColour = vec3(1.0, 0.0, 0.0);

  vec3 c1 = vec3(0.5, 1.0, 0.2);
  vec3 c2 = vec3(0.25, 0.05, 0.25);

  vec3 normal = normalize(vNormal);

  vec3 viewDirection = normalize(cameraPosition - vWorldPosition);
  vec3 lightDirection = normalize(vec3(1.0, 0.5, 0.5));

  vec3 ambientLighting = ambientLight(normal, c2, c1);
  vec3 diffuseLighting = lambertLight(normal, viewDirection, lightDirection, lightColour);
  vec3 specular = phongSpecular(normal, lightDirection, viewDirection) * easeOut(yValueGrass, 4.0);

  vec3 lighting = diffuseLighting * 0.5 + ambientLighting * 0.4;

  float ambientOclusion = remap(pow(yValueGrass, 2.0), 0.0, 1.0, 0.0625, 1.0);


  vec3 color = grassColor.xyz * lighting + specular * grassColor.xyz;
  color *= ambientOclusion;

  gl_FragColor = vec4(pow(color, vec3(1.0 / 2.2)), 1.0);
}
