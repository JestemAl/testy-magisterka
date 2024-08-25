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

mat3 rotationMatrixY(float angle) {
    float cosAngle = cos(angle);
    float sinAngle = sin(angle);

    return mat3(
        cosAngle, 0.0, sinAngle,
        0.0,     1.0, 0.0,
        -sinAngle, 0.0, cosAngle
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

vec2 perlinHash(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)),
             dot(p, vec2(269.5, 183.3)));
    return -1.0 + 2.0 * fract(sin(p) * 43758.5453123);
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
