import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import CreateGeometry from './components/GrassGeometry'

import grassVertexShader from './shaders/grass/grassVertexShader.glsl'
import grassFragmentShader from './shaders/grass/grassFragmentShader.glsl'
import groundVertexShader from './shaders/ground/groundVertexShader.glsl'
import groundFragmentShader from './shaders/ground/groundFragmentShader.glsl'
import skyVertexShader from './shaders/sky/skyVertexShader.glsl'
import skyFragmentShader from './shaders/sky/skyFragmentShader.glsl'

// import Stats from 'three/examples/jsm/libs/stats.module.js';
// import { GPUStatsPanel } from 'three/examples/jsm/utils/GPUStatsPanel.js';
import Stats from "stats-gl";


/**
 * Constants
 */
const GRASS_COUNT = 8 * 512
const GRASS_SEGMENTS = 4
const GRASS_WIDTH = 0.25
const GRASS_HEIGHT = 6
const GRASS_PATCH_SIZE = 25
const GRASS_GRID_SIZE = 5  // Adjust this to cover a larger area

/**
 * Base
 */
const debugObject = {}

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()
scene.background = new THREE.Color(0.7, 0.8, 1.0)

// Loaders
const textureLoader = new THREE.TextureLoader()

/**
 * Textures
 */
const environmentMap = textureLoader.load('/textures/background3.webp')
environmentMap.colorSpace = THREE.SRGBColorSpace
scene.background = environmentMap

const groundGrid = textureLoader.load('/textures/grid.png')
groundGrid.wrapS = THREE.RepeatWrapping;
groundGrid.wrapT = THREE.RepeatWrapping;

/**
 * Grass
 */
const uniforms = {
    params: { value: new THREE.Vector4(
        GRASS_SEGMENTS, GRASS_PATCH_SIZE, GRASS_WIDTH, GRASS_HEIGHT
    )},
    resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
    time: { value: 0 },
}
const grassGeometry = CreateGeometry(GRASS_SEGMENTS, GRASS_COUNT, GRASS_PATCH_SIZE)
const grassMaterial = new THREE.ShaderMaterial({
    uniforms: uniforms,
    vertexShader: grassVertexShader,
    fragmentShader: grassFragmentShader,
})

/**
 * Create a pool of grass tiles
 */
const grassGroup = new THREE.Group()
scene.add(grassGroup)

const createGrassTile = () => {
    const tile = new THREE.Mesh(grassGeometry, grassMaterial)
    grassGroup.add(tile)
    return tile
}
// createGrassTile()

// Function to populate the grass grid statically
const populateGrassGrid = () => {
    const baseCellPos = new THREE.Vector3(0, 0, 0)
    let tileCount = 0;
    for (let x = -GRASS_GRID_SIZE; x <= GRASS_GRID_SIZE; x++) {
        for (let z = -GRASS_GRID_SIZE; z <= GRASS_GRID_SIZE; z++) {
            const currentCell = new THREE.Vector3(
                baseCellPos.x + x * GRASS_PATCH_SIZE * 2, 
                0, 
                baseCellPos.z + z * GRASS_PATCH_SIZE * 2
            )

            const tile = createGrassTile()
            tile.position.copy(currentCell)
            tile.position.y = 0
            tileCount++
            // tile.rotateY(-Math.PI / 2)
        }
    }
    
}
populateGrassGrid()

// Populate the grass grid once
// populateGrassGrid()

/**
 * Ground
 */
const groundGeometry = new THREE.PlaneGeometry(1, 1, 512, 512)
const groundMaterial = new THREE.ShaderMaterial({
    uniforms: {
        resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
        time: { value: 0 },
        groundTexture: { value: groundGrid }
    },
    vertexShader: groundVertexShader,
    fragmentShader: groundFragmentShader
})

const plane = new THREE.Mesh(groundGeometry, groundMaterial)
plane.rotateX(-Math.PI / 2)
plane.scale.setScalar(550)
scene.add(plane)

/**
 * Sky
 */
// const skyGeometry = new THREE.SphereGeometry(5000, 32, 15);
// const skyMateral = new THREE.ShaderMaterial({
//     uniforms: {
//         time: { value: 0 },
//         resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) }
//     },
//     vertexShader: skyVertexShader,
//     fragmentShader: skyFragmentShader,
//     side: THREE.BackSide
// })
// const sky = new THREE.Mesh(skyGeometry, skyMateral)
// sky.castShadow = false
// sky.receiveShadow = false
// scene.add(sky)

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
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight
    sizes.pixelRatio = Math.min(window.devicePixelRatio, 2)

    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(sizes.pixelRatio)

    grassMaterial.uniforms.resolution.value.set(window.innerWidth, window.innerHeight)
    groundMaterial.uniforms.resolution.value.set(window.innerWidth, window.innerHeight)
    // skyMateral.uniforms.resolution.value.set(window.innerWidth, window.innerHeight)
})

/**
 * Camera
 */
const camera = new THREE.PerspectiveCamera(45, sizes.width / sizes.height, 0.1, 450)
camera.position.set(250, 20, -250)
scene.add(camera)

// Controls
const controls = new OrbitControls(camera, canvas)
// controls.enableDamping = true

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(sizes.pixelRatio)

/**
 * Stats
 */
// Inicjalizacja stats.js
// Dodane zmienne globalne
window.frameCount = 0;
window.totalCpuTime = 0; // Zapisywanie zmiennych globalnie
window.totalFrameTime = 0;
window.totalDrawCalls = 0;

// const stats = new Stats();
// document.body.appendChild(stats.domElement);

// // Inicjalizacja GPUStatsPanel
// const gpuPanel = new GPUStatsPanel(renderer.getContext());
// stats.addPanel(gpuPanel);
// stats.showPanel(0);

const stats = new Stats({
    // logsPerSecond: 20, 
    samplesLog: 100, 
    precision: 2,
    mode: 1
});
document.body.appendChild(stats.dom);
stats.init( renderer );

/**
 * Animate
 */
let lastFrameTime = performance.now();

const clock = new THREE.Clock()

const tick = () => {
    const now = performance.now();
    const frameTime = now - lastFrameTime;  // Czas trwania obecnej klatki
    lastFrameTime = now;

    grassMaterial.uniforms.time.value = clock.getElapsedTime();

    const cpuStartTime = performance.now();
    renderer.render(scene, camera);
    const cpuEndTime = performance.now();
    const cpuTime = cpuEndTime - cpuStartTime;

    stats.update();

    // Obliczanie FPS jako odwrotność czasu klatki (w sekundach)
    const fps = 1000 / frameTime;

    // Zbieranie danych w sposób globalny dla puppeteer
    window.statsData = {
        fps: fps,
        gpu: stats.totalGpuDuration,
        cpu: cpuTime
    };

    window.renderInfo = {
        drawCalls: renderer.info.render.calls,
        totalFrameTime: frameTime,
    };

    requestAnimationFrame(tick);
};

tick();

