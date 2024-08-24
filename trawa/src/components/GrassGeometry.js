import * as THREE from 'three'

export default function CreateGeometry(segments, count, area){
    const vertices = (segments + 1) * 2
    const indices = []

    for(let i = 0; i < segments; i++){
        const front_vi = i * 2;
        indices[i*12+0] = front_vi + 0;
        indices[i*12+1] = front_vi + 1;
        indices[i*12+2] = front_vi + 2;

        indices[i*12+3] = front_vi + 2;
        indices[i*12+4] = front_vi + 1;
        indices[i*12+5] = front_vi + 3;
  
        const back_vi = vertices + front_vi;
        indices[i*12+6] = back_vi + 2;
        indices[i*12+7] = back_vi + 1;
        indices[i*12+8] = back_vi + 0;

        indices[i*12+9] = back_vi + 3;
        indices[i*12+10] = back_vi + 1;
        indices[i*12+11] = back_vi + 2;
    }

    const geometry = new THREE.InstancedBufferGeometry()
    geometry.instanceCount = count
    geometry.setIndex(indices)
    geometry.boundingSphere = new THREE.Sphere(
        new THREE.Vector3(0, 0, 0),
        1 + area * 2
    )

    return geometry
}