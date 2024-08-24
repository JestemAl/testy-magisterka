varying vec3 vWorldPosition;
varying vec3 vWorldNormal;
varying vec2 vUv;

vec3 hashVec3(vec3 p) {
    p = fract(p * 0.1031);
    p += dot(p, p.yzx + 33.33);
    p = fract((p.xxy + p.yzz) * p.zyx);
    return p;
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

vec3 terrainHeight(vec3 worldPos){
  return vec3(worldPos.x, noise(worldPos * 0.02) * 0.0, worldPos.z);
}

void main() {
  vec4 localSpacePosition = vec4(position, 1.0);
  vec4 worldPosition = modelMatrix * localSpacePosition;

  worldPosition.xyz = terrainHeight(worldPosition.xyz);

  vWorldPosition = worldPosition.xyz;
  vWorldNormal = normalize((modelMatrix * vec4(normal, 0.0)).xyz);
  vUv = uv;

  gl_Position = projectionMatrix * viewMatrix * worldPosition;
}