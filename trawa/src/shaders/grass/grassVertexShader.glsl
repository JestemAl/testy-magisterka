
uniform vec4 params;
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

vec3 bezierCurve(float t, vec3 p0, vec3 p1, vec3 p2, vec3 p3) {
    float u = 1.0 - t;
    float tt = t * t;
    float uu = u * u;
    float uuu = uu * u;
    float ttt = tt * t;

    vec3 p = uuu * p0; // Pierwszy wyraz
    p += 3.0 * uu * t * p1; // Drugi wyraz
    p += 3.0 * u * tt * p2; // Trzeci wyraz
    p += ttt * p3; // Czwarty wyraz

    return p;
}

vec3 bezierGrad(vec3 P0, vec3 P1, vec3 P2, vec3 P3, float t) {
  return 3.0 * (1.0 - t) * (1.0 - t) * (P1 - P0) +
         6.0 * (1.0 - t) * t * (P2 - P1) +
         3.0 * t * t * (P3 - P2);
}


mat3 rotationMatrixY(float angle) {
    float cosAngle = cos(angle);
    float sinAngle = sin(angle);

    return mat3( 
        cosAngle, 0.0, sinAngle,
        0.0,     1.0, 0.0,
        -sinAngle, 0.0, cosAngle
    );
}

mat3 rotateAxis(vec3 axis, float angle) {
  float s = sin(angle);
  float c = cos(angle);
  float oc = 1.0 - c;

  return mat3(
    oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,
    oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,
    oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c
  );
}

vec2 hash(float n) {
    n = fract(n * 0.1031);
    n = n * (n + 33.33);
    n = fract(n * 0.001);
    float x = fract(sin(n) * 43758.5453123);
    float y = fract(cos(n) * 37534.5678901);
    return vec2(x, y);
}

vec2 hashwithoutsine21(float p)
{
	vec3 p3 = fract(vec3(p,p,p) * vec3(.1031, .1030, .0973));
	p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xx+p3.yz)*p3.zy);
}

vec3 hashVec3(vec3 p) {
    p = fract(p * 0.1031);
    p += dot(p, p.yzx + 33.33);
    p = fract((p.xxy + p.yzz) * p.zyx);
    return p;
}

uint murmurHash13(uvec3 src) {
    const uint M = 0x5bd1e995u;
    uint h = 1190494759u;
    src *= M; src ^= src>>24u; src *= M;
    h *= M; h ^= src.x; h *= M; h ^= src.y; h *= M; h ^= src.z;
    h ^= h>>13u; h *= M; h ^= h>>15u;
    return h;
}

float hash13(vec3 src) {
    uint h = murmurHash13(floatBitsToUint(src));
    return uintBitsToFloat(h & 0x007fffffu | 0x3f800000u) - 1.0;
}


vec2 perlinHash(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)),
             dot(p, vec2(269.5, 183.3)));
    return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
}

vec3 fade(vec3 t) {
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
}
float grad(int hash, vec3 p) {
    int h = hash & 15;
    float u = h < 8 ? p.x : p.y;
    float v = h < 4 ? p.y : h == 12 || h == 14 ? p.x : p.z;
    return ((h & 1) == 0 ? u : -u) + ((h & 2) == 0 ? v : -v);
}

float noise( in vec3 p )
{
  vec3 i = floor( p );
  vec3 f = fract( p );
	
	vec3 u = f*f*(3.0-2.0*f);

  return mix( mix( mix( dot( hashVec3( i + vec3(0.0,0.0,0.0) ), f - vec3(0.0,0.0,0.0) ), 
                        dot( hashVec3( i + vec3(1.0,0.0,0.0) ), f - vec3(1.0,0.0,0.0) ), u.x),
                   mix( dot( hashVec3( i + vec3(0.0,1.0,0.0) ), f - vec3(0.0,1.0,0.0) ), 
                        dot( hashVec3( i + vec3(1.0,1.0,0.0) ), f - vec3(1.0,1.0,0.0) ), u.x), u.y),
              mix( mix( dot( hashVec3( i + vec3(0.0,0.0,1.0) ), f - vec3(0.0,0.0,1.0) ), 
                        dot( hashVec3( i + vec3(1.0,0.0,1.0) ), f - vec3(1.0,0.0,1.0) ), u.x),
                   mix( dot( hashVec3( i + vec3(0.0,1.0,1.0) ), f - vec3(0.0,1.0,1.0) ), 
                        dot( hashVec3( i + vec3(1.0,1.0,1.0) ), f - vec3(1.0,1.0,1.0) ), u.x), u.y), u.z );
}

float perlinNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(mix(dot(perlinHash(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0)),
                   dot(perlinHash(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),
               mix(dot(perlinHash(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)),
                   dot(perlinHash(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0)), u.x), u.y);
}

vec3 terrainHeight(vec3 worldPos){
  return vec3(worldPos.x, noise(worldPos * 0.02) * 0.0, worldPos.z);
}

const float PI = 3.14;

const vec3 baseGrassColor = vec3(0.18, 0.21, 0.01);
const vec3 tipGrassColor = vec3(0.7, 0.5, 0.4);

// const vec3 baseGrassColor = vec3(0.05, 0.63, 0.16);
// const vec3 tipGrassColor = vec3(0.07, 0.7, 0.16);

// const vec3 baseGrassColor = vec3(0.36, 0.56, 0.15);
// const vec3 tipGrassColor = vec3(0.4, 0.65, 0.14);


void main() {
  float GRASS_AREA = params.y;
  float GRASS_WIDTH = params.z;
  float GRASS_HEIGHT = params.w;
  int GRASS_SEGMENTS = int(params.x);
  int GRASS_VERTICES = int(GRASS_SEGMENTS + 1) * 2;
  
  // grass offset
  vec2 randomizedInstanceID = hashwithoutsine21(float(gl_InstanceID)) * 2.0 - 1.0;
  vec3 offset = vec3(randomizedInstanceID.x, 0.0, randomizedInstanceID.y) * GRASS_AREA;
  offset = terrainHeight(offset);
  // 
  vec3 grassWorldPosition = (modelMatrix * vec4(offset, 1.0)).xyz;
  vec3 hashVec3Value = hashVec3(grassWorldPosition);  // float noiseValue = perlinNoise(vec2(grassWorldPosition.x * 0.1, grassWorldPosition.z * 0.1));
  
  float noiseValue = noise(grassWorldPosition * 0.05);
  float hashFloatValue = hash13(grassWorldPosition);

  float angle = remap(hashVec3Value.y, -1.0, 1.0, -PI, PI);
  
  
  // vertex id
  int vertFB_ID = gl_VertexID % (GRASS_VERTICES * 2);
  int vertID = vertFB_ID % GRASS_VERTICES;

  // vertex info
  int xTest = vertID & 0x1;
  int zTest = (vertFB_ID >= GRASS_VERTICES) ? 1 : -1;
  float xSide = float(xTest);
  float zSide = float(zTest);
  float heightPercent = float(vertID - xTest) / (float(GRASS_SEGMENTS) * 2.0);

  float width = GRASS_WIDTH * (smoothstep(1.0, 0.75, heightPercent));
  float height = GRASS_HEIGHT;

  float windStrength = noise(vec3(grassWorldPosition.xz * 0.05, 0.0) + time);
  float windAngle = 0.0;
  vec3 windAxis = vec3(cos(windAngle), 0.0, sin(windAngle));
  float windLeanAngle = windStrength * 1.0 * heightPercent;

  // randomLeanAnimation = 0.0;
  float grassAnimation = noise(
      vec3(grassWorldPosition.xz, time * 4.0)) * (windStrength * 0.5 + 0.125);

  float tiltFactorLow = remap(hashVec3Value.y, -1.0, 1.0, -0.4, 0.6) + grassAnimation;
  float tiltFactorHigh = remap(hashVec3Value.x, -1.0, 1.0, 0.0, 0.8) + grassAnimation; 


  // bazier controll points
  vec3 p1 = vec3(0.0);
  vec3 p2 = vec3(0.0, 0.3, 0.0);
  vec3 p3 = vec3(0.0, 0.7, 0.0);
  // vec3 p3 = vec3(0.0, sin(tiltFactorLow), 0.0);
  vec3 p4 = vec3(0.0, cos(tiltFactorLow), sin(tiltFactorLow));
  vec3 tilt = bezierCurve(heightPercent, p1, p2, p3, p4);
  
  vec3 curveGrad = bezierGrad(p1, p2, p3, p4, heightPercent);
  mat2 curveRot90 = mat2(0.0, 1.0, -1.0, 0.0) * -zSide;

  // Calculate the vertex position
  float x = (xSide - 0.5) * width;
  float y = heightPercent * height;
  float z = 0.0;

  y = tilt.y * height;
  z = tilt.z * height;

  // grass matrix
  mat3 grassMatrix = rotationMatrixY(angle) * rotateAxis(windAxis, windLeanAngle);

  vec3 grassLocalPosition = grassMatrix * vec3(x, y, z) + offset;
  vec3 grassLocalNormal = grassMatrix * vec3(0.0, curveRot90 * curveGrad.yz);
  vec4 modelViewPosition = modelViewMatrix * vec4(grassLocalPosition, 1.0);

  float distanceBlend = smoothstep(0.0, 10.0, distance(cameraPosition, grassWorldPosition));
  grassLocalNormal = mix(grassLocalNormal, vec3(0.0, 1.0, 0.0), distanceBlend * 0.5);
  grassLocalNormal = normalize(grassLocalNormal);

  vec3 color1 = mix(baseGrassColor, tipGrassColor, heightPercent);
  vec3 color2 = mix(vec3(0.3, 0.2, 0.2), vec3(0.98, 0.7, 0.6), heightPercent );
    // vColor = vec3(zSide);
    // vColor = grassLocalNormal;

  vColor = mix(color1, color2, smoothstep(-0.5, 1.0, noiseValue));
  // vColor = color1;
  // vColor = vec3(remap(round(hashFloatValue * 4.0) / 4.0, 0.0, 1.0, 0.5, 1.0));
  // vColor *= mix(vec3(1.0), vec3(1.0, 1.0, 0.25), remap(noiseValue, -1.0, 1.0, 0.0, 1.0)) * 0.5;

  vGrassData = vec4(x, heightPercent, z, 0.0);
  vNormal = normalize((modelMatrix * vec4(grassLocalNormal, 0.0)).xyz);
  vWorldPosition = (modelMatrix * vec4(grassLocalPosition, 1.0)).xyz;


  // gl_Position = projectionMatrix * modelViewMatrix * vec4(
  //     grassLocalPosition, 1.0);

  gl_Position = projectionMatrix * modelViewPosition;
}