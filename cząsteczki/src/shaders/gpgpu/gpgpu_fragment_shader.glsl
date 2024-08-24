#include ../includes/simplexsNoise4d.glsl

uniform float uTime;
uniform float uDeltaTime;
uniform sampler2D uInitial;

void main()
{
    float time = uTime * 0.2;
    vec2 uv = gl_FragCoord.xy / resolution.xy;
    vec4 particle = texture(uParticlesSampler, uv);
    vec4 initial = texture(uInitial, uv);

    // particle.x += 0.01;
    if(particle.a >= 1.0){
        particle.a = mod(particle.a, 1.0);
        particle.xyz = initial.xyz;
    }
    else{
        float volume = snoise(vec4(initial.xyz * 0.2, time + 1.0));
        volume = smoothstep(0.0, 1.0, volume);

         vec3 flowField = vec3(
            snoise(vec4(particle.xyz * 0.5 + 0.0, time)),
            snoise(vec4(particle.xyz * 0.5 + 1.0, time)),
            snoise(vec4(particle.xyz * 0.5 + 2.0, time))
        );
        flowField = normalize(flowField);
        particle.xyz += flowField * uDeltaTime * volume * 2.0;
    
        particle.a += uDeltaTime * 0.3;
    }
    



    gl_FragColor = particle;
}