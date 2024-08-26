import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js'
import GUI from 'lil-gui'
import particlesVertexShader from './shaders/particles/vertex.glsl'
import particlesFragmentShader from './shaders/particles/fragment.glsl'
import { GPUComputationRenderer } from 'three/examples/jsm/misc/GPUComputationRenderer.js'
import gpgpuFragmentShader from './shaders/gpgpu/gpgpu_fragment_shader.glsl'
import Stats from 'stats-gl';


/**
 * Base
 */
// Debug
// const gui = new GUI({ width: 340 })
const debugObject = {}

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()

// Loaders
const dracoLoader = new DRACOLoader()
dracoLoader.setDecoderPath('/draco/')

const gltfLoader = new GLTFLoader()
gltfLoader.setDRACOLoader(dracoLoader)

/**
 * Sizes
 */
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight,
    pixelRatio: Math.min(window.devicePixelRatio, 2)
}

window.addEventListener('resize', () =>
{
    // Update sizes
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight
    sizes.pixelRatio = Math.min(window.devicePixelRatio, 2)

    // Materials
    particles.material.uniforms.uResolution.value.set(sizes.width * sizes.pixelRatio, sizes.height * sizes.pixelRatio)

    // Update camera
    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    // Update renderer
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(sizes.pixelRatio)
})

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(35, sizes.width / sizes.height, 0.1, 100)
camera.position.set(0, 4, 15)
scene.add(camera)

// Controls
const controls = new OrbitControls(camera, canvas)
controls.enableDamping = true
GPUComputationRenderer

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(sizes.pixelRatio)

debugObject.clearColor = '#fff'
// debugObject.clearColor = '#29191f'
renderer.setClearColor(debugObject.clearColor)


/**
 * Load model
 */
// const model = await gltfLoader.loadAsync('./model.glb')
const loadedModel = await gltfLoader.loadAsync('./full-scene-compressed2.glb')
// const model = await gltfLoader.loadAsync('./scene2.glb')
// console.log(loadedModel.scene.children[0].geometry.count);

/**
 * Geometry
 */
const model = {}
model.geometry = loadedModel.scene.children[0].geometry
model.geometry.scale(2, 2, 2)
model.count = model.geometry.attributes.position.count // wylicza liczbe czasteczek

console.log(model.geometry);


/**
 * GPGPU
 */
// setup
const gpgpu = {}
gpgpu.size = Math.ceil(Math.sqrt(model.count)) // rozmiar fbo tekstury
gpgpu.computation = new GPUComputationRenderer(gpgpu.size, gpgpu.size, renderer)
console.log(model.count * 5);


// particels
const initialParticlesTexture = gpgpu.computation.createTexture()

for(let i = 0; i < model.count; i++)
{
    const i3 = i * 3 
    const i4 = i * 4

    initialParticlesTexture.image.data[i4 + 0] = model.geometry.attributes.position.array[i3 + 0]
    initialParticlesTexture.image.data[i4 + 1] = model.geometry.attributes.position.array[i3 + 1]
    initialParticlesTexture.image.data[i4 + 2] = model.geometry.attributes.position.array[i3 + 2]
    initialParticlesTexture.image.data[i4 + 3] = Math.random()
}

// particels variables
gpgpu.particleVariable = gpgpu.computation.addVariable('uParticlesSampler', gpgpuFragmentShader, initialParticlesTexture) 
gpgpu.computation.setVariableDependencies(gpgpu.particleVariable, [gpgpu.particleVariable])

// uniforms
gpgpu.particleVariable.material.uniforms.uTime = new THREE.Uniform(0)
gpgpu.particleVariable.material.uniforms.uDeltaTime = new THREE.Uniform(0)
gpgpu.particleVariable.material.uniforms.uInitial = new THREE.Uniform(initialParticlesTexture)

gpgpu.computation.init()


// debug
gpgpu.debug = new THREE.Mesh(
    new THREE.PlaneGeometry(3, 3),
    new THREE.MeshBasicMaterial({
        map: gpgpu.computation.getCurrentRenderTarget(gpgpu.particleVariable).texture
    })
)
gpgpu.debug.position.x = 5
// scene.add(gpgpu.debug)




/**
 * Particles
 */
const particlesUVArray = new Float32Array(model.count * 2)
const sizeArray = new Float32Array(model.count)

for(let u = 0; u < gpgpu.size; u++){
    for(let v = 0; v < gpgpu.size; v++){
        const i = (v * gpgpu.size) + u
        const i2 = i * 2;

        particlesUVArray[i2] = (u + 0.5) / gpgpu.size       // u value
        particlesUVArray[i2 + 1] = (v + 0.5) / gpgpu.size   // v value
    
        sizeArray[i] = Math.random()
    }
}

const particles = {}
particles.geometry = new THREE.BufferGeometry()
particles.geometry.setDrawRange(0, model.count)
particles.geometry.setAttribute('aParticlesUV', new THREE.BufferAttribute(particlesUVArray, 2))
particles.geometry.setAttribute('aColor', model.geometry.attributes.color)
particles.geometry.setAttribute('aSize', new THREE.BufferAttribute(sizeArray, 1))


// Material
particles.material = new THREE.ShaderMaterial({
    vertexShader: particlesVertexShader,
    fragmentShader: particlesFragmentShader,
    uniforms:
    {
        uParticleTexture: new THREE.Uniform(),
        uSize: new THREE.Uniform(0.08),
        uStrength: new THREE.Uniform(Math.random()),
        uResolution: new THREE.Uniform(new THREE.Vector2(sizes.width * sizes.pixelRatio, sizes.height * sizes.pixelRatio))
    }
})

// Points
particles.points = new THREE.Points(particles.geometry, particles.material)
scene.add(particles.points)

/**
 * Function to create and add model instances to the scene
 */
function addModelInstance(position, rotation, scale) {
    const modelInstance = new THREE.Points(particles.geometry, particles.material);

    // Apply transformations
    if (position) modelInstance.position.set(position.x, position.y, position.z);
    if (rotation) modelInstance.rotation.set(rotation.x, rotation.y, rotation.z);
    if (scale) modelInstance.scale.set(scale.x, scale.y, scale.z);

    scene.add(modelInstance);
}

// Add multiple instances with different transformations
// addModelInstance(new THREE.Vector3(0, 0, 0), new THREE.Euler(0, 0, 0), new THREE.Vector3(1, 1, 1));  // Original
addModelInstance(new THREE.Vector3(-30, 0, -70), new THREE.Euler(0, 0, 0), new THREE.Vector3(1, 1, 1));  // Scaled up and rotated
addModelInstance(new THREE.Vector3(30, 0, -70), new THREE.Euler(0, 0, 0), new THREE.Vector3(1, 1, 1));  // Scaled up and rotated
addModelInstance(new THREE.Vector3(0, 0, -70), new THREE.Euler(0, 0, 0), new THREE.Vector3(1, 1, 1));  // Scaled up and rotated
addModelInstance(new THREE.Vector3(-30, 0, -35), new THREE.Euler(0, 0, 0), new THREE.Vector3(1, 1, 1));  // Scaled up and rotated
addModelInstance(new THREE.Vector3(30, 0, -35), new THREE.Euler(0, 0, 0), new THREE.Vector3(1, 1, 1));  // Scaled up and rotated
addModelInstance(new THREE.Vector3(0, 0, -35), new THREE.Euler(0, 0, 0), new THREE.Vector3(1, 1, 1));  // Scaled up and rotated


// console.log(gpgpu.size);

/**
 * Tweaks
 */
// gui.addColor(debugObject, 'clearColor').onChange(() => { renderer.setClearColor(debugObject.clearColor) })
// gui.add(particles.material.uniforms.uSize, 'value').min(0).max(1).step(0.001).name('uSize')
const stats = new Stats({
    samplesLog: 100, 
    precision: 2,
    mode: 2
  });
  document.body.appendChild(stats.dom);
  stats.init(renderer);
  
  
  let fps = 0;
  window.frameCount = 0;
  window.totalCpuTime = 0;
  window.totalDrawCalls = 0;
  window.totalFrameTime = 0;
  window.modelCount = 0;
  
  /**
   * Animate
  */
 const clock = new THREE.Clock()
 let previousTime = 0
 let lastFrameTime = performance.now();

const animate = () =>
{
    performance.mark('cpu-started');
    const elapsedTime = clock.getElapsedTime()
    const deltaTime = elapsedTime - previousTime
    previousTime = elapsedTime

    const now = performance.now()
    const frameTime = now - lastFrameTime
    lastFrameTime = now

    const cpuStartTime = performance.now();
    
    gpgpu.particleVariable.material.uniforms.uTime.value = elapsedTime
    gpgpu.particleVariable.material.uniforms.uDeltaTime.value = deltaTime
    gpgpu.computation.compute()
    particles.material.uniforms.uParticleTexture.value = gpgpu.computation.getCurrentRenderTarget(gpgpu.particleVariable).texture // aktualizacja jest w animate po compute zeby nie brac tego samego gbo tylko dostac zawsze ten drugi zwracany fbo z ping-pong bufora co kamke (bo sa 2 a robienie tego przy deklaracji uniforma bierze sie ten zwracany w pierwszej ramce co jest nieprawodilowe bo to sie zmienia i mozna dostac dziwny framerate przez to)

    // Update controls
    controls.update()
    
    // Render normal scene
    renderer.render(scene, camera);

    // console.log(stats);
    
    stats.update()

    fps = 1000 / frameTime;

    performance.mark('cpu-ended');
    performance.measure('cpu-duration', 'cpu-started', 'cpu-ended');
  
    const measure = performance.getEntriesByName('cpu-duration').pop();
    
    window.statsData = {
        fps: fps,
        gpu: stats.totalGpuDuration,
        cpu: measure.duration,
    };

    window.renderInfo = {
        drawCalls: renderer.info.render.calls,
        totalFrameTime: frameTime,
    };

    // Call tick again on the next frame
    window.requestAnimationFrame(animate)
}

animate()
