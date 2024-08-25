import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import Stats from 'stats-gl';

/**
 * Data
 */
let adding = true;
const maxDynamicInstances = 1000;
let dynamicInstances = 1;
const instances = [];
let instancesPerFrame = 2;
const fpsThreshold = 10; // Minimum FPS required to increase instancesPerFrame
const maxInstancesPerFrame = 50; // Maximum cap for instancesPerFrame
let lastIncreaseTime = 0; // Track the last time we increased instancesPerFrame
const increaseInterval = 5000; // Time interval in milliseconds between increments

/**
 * Seeded Random Function
 */
const seed = 10 
// const seed = 169 
// const seed = 4444 
// const seed = 77777
// const seed = 123456;


window.seedNumber = seed;

const random = seededRandom(seed);

function seededRandom(seed) {
  const a = 1664525;
  const c = 1013904223;
  const m = Math.pow(2, 32);
  let state = seed;

  return function () {
    state = (a * state + c) % m;
    return state / m;
  };
}

/**
 * Object Pool
 */
const objectPool = []; // Pool of reusable objects

function getRandomPosition(range) {
  return random() * range - range / 4; // Reducing the range
}

function getRandomInRange(min, max) {
  return random() * (max - min) + min;
}

function placeModelInFrontOfCamera(cameraZ, rangeX, minZDistance, maxZDistance) {
  const xPosition = getRandomInRange(-rangeX / 2, rangeX / 2);
  const zPosition = getRandomInRange(cameraZ - maxZDistance, cameraZ - minZDistance);
  const yPosition = 0;
  return new THREE.Vector3(xPosition, yPosition, zPosition);
}

/**
 * Models
 */
const modelData = [
  { path: '/models/tree-character/character-tree-baked.glb', texture: '/textures/tree-baked2.jpg' },
  { path: '/models/polelight/polelight-baked.glb', texture: '/textures/polelight-baked2.jpg' },
  { path: '/models/sign/sign-baked.glb', texture: '/textures/sign-baked2.jpg' },
  { path: '/models/portals/portal-baked.glb', texture: '/textures/portal-baked.jpg' },
  { path: '/models/portals/portalb-baked.glb', texture: '/textures/portalb-baked.jpg' },
  { path: '/models/rocks/rocks-bake.glb', texture: '/textures/rock-bake.jpg' },
  { path: '/models/rocks/bridge-bake.glb', texture: '/textures/bridge-baked.jpg' },
];

/**
 * Base
 */
// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0.9, 0.5, 0.2);

// canvas
const canvas = document.querySelector('canvas.webgl')


/**
 * Loaders
 */
const gltfLoader = new GLTFLoader();
const textureLoader = new THREE.TextureLoader();

/**
 * Cached Textures
 */
const cachedTextures = {};

/**
 * Hdr texture
 */
const environmentMap = textureLoader.load('/textures/background3.png');
environmentMap.colorSpace = THREE.SRGBColorSpace;
scene.background = environmentMap;

/**
 * Preload Textures
 */
const preloadTextures = (modelData, callback) => {
  let loadedTextures = 0;
  modelData.forEach((data) => {
    textureLoader.load(
      data.texture,
      (texture) => {
        texture.flipY = false;
        texture.colorSpace = THREE.SRGBColorSpace;
        cachedTextures[data.texture] = texture;
        loadedTextures++;
        if (loadedTextures === modelData.length) {
          callback(); // All textures are loaded
        }
      },
      undefined,
      (error) => {
        console.error(`Error loading texture: ${data.texture}`, error);
      }
    );
  });
};

/**
 * Apply Preloaded Texture to Model
 */
function applyTextureToModel(baseModel, texturePath) {
  const bakedTexture = cachedTextures[texturePath];
  baseModel.traverse((node) => {
    if (node.isMesh) {
      node.material = new THREE.MeshBasicMaterial({ map: bakedTexture });
    }
  });
}

function loadInitialModels() {
  for (let i = 0; i < dynamicInstances; i++) {
    addOrRemoveInstance(true); // Add initial instances
  }
}

/**
 * Scene
 */
const surfaceTexture = textureLoader.load('/textures/surface7.jpg');
surfaceTexture.colorSpace = THREE.SRGBColorSpace;
const material = new THREE.MeshBasicMaterial({ map: surfaceTexture });

const plane = new THREE.Mesh(
  new THREE.PlaneGeometry(100, 200),
  material
);
plane.rotation.x = -Math.PI / 2.0;

scene.add(plane);

/**
 * Lights
 */
scene.add(new THREE.AmbientLight(0xcccccc));

const directionalLight = new THREE.DirectionalLight('#ffffff', 2);
directionalLight.position.set(6.25, 3, 4);
scene.add(directionalLight);

/**
 * Sizes
 */
const sizes = {
  width: window.innerWidth,
  height: window.innerHeight,
  pixelRatio: Math.min(window.devicePixelRatio, 2),
};

// Renderer
const renderer = new THREE.WebGLRenderer({
  canvas: canvas,
  antialias: true
})
renderer.setPixelRatio(sizes.pixelRatio);
renderer.setSize(sizes.width, sizes.height);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
// document.body.appendChild(renderer.domElement);


window.addEventListener('resize', () => {
  sizes.width = window.innerWidth;
  sizes.height = window.innerHeight;
  sizes.pixelRatio = Math.min(window.devicePixelRatio, 2);

  camera.aspect = sizes.width / sizes.height;
  camera.updateProjectionMatrix();

  renderer.setSize(sizes.width, sizes.height);
  renderer.setPixelRatio(sizes.pixelRatio);
});

/**
 * Camera
 */
const camera = new THREE.PerspectiveCamera(30, sizes.width / sizes.height, 0.25, 100);
camera.position.set(0, 1.5, 10); // Start the camera at a positive Z value
scene.add(camera);

/**
 * Camera Movement
 */
let cameraSpeed = 0.1; // Speed at which the camera moves forward
let lastSpawnPosition = camera.position.z; // Track the last Z position where models were spawned
const spawnDistance = 20; // Increase spawn distance to space out models

function moveCamera() {
  camera.position.z -= cameraSpeed; // Move camera forward by decreasing Z position

  plane.position.z -= cameraSpeed; // Move the plane forward in large steps
}

/**
 * Managing spawning and removing objects
 */

function getObjectFromPool() {
  if (objectPool.length > 0) {
    return objectPool.pop(); // Reuse an object from the pool
  } else {
    return null; // Pool is empty, no object to reuse
  }
}

function returnObjectToPool(object) {
  objectPool.push(object);
}

function addOrRemoveInstance(initial = false) {
  const cameraZ = camera.position.z;

  // Add new instances in front of the camera
  if (dynamicInstances < maxDynamicInstances && (adding || initial)) {
    if (initial || lastSpawnPosition - cameraZ >= spawnDistance) {
      for (let i = 0; i < instancesPerFrame; i++) {
        const data = modelData[Math.floor(random() * modelData.length)];
        let modelClone = getObjectFromPool();
        
        if (modelClone === null) {
          gltfLoader.load(
            data.path,
            (gltf) => {
              modelClone = gltf.scene.clone();
              applyTextureToModel(modelClone, data.texture);

              modelClone.scale.set(2, 2, 2); 

              const modelPosition = placeModelInFrontOfCamera(cameraZ, 70, 50, 150);
              modelClone.position.copy(modelPosition);

              scene.add(modelClone);
              instances.push(modelClone);
              dynamicInstances++;
            },
            undefined,
            (error) => {
              console.error(`Error loading model: ${data.path}`, error);
            }
          );
        } else {
          // If a model is available in the pool, reuse it
          const modelPosition = placeModelInFrontOfCamera(cameraZ, 70, 50, 150);
          modelClone.position.copy(modelPosition);
          scene.add(modelClone);
          instances.push(modelClone);
          dynamicInstances++;
        }
      }

      lastSpawnPosition = cameraZ;
    }
  }

  // Remove instances that are sufficiently behind the camera
  for (let i = instances.length - 1; i >= 0; i--) {
    const instance = instances[i];
    if (instance.position.z > cameraZ) { // Remove objects behind the camera
      scene.remove(instance);
      instances.splice(i, 1);
      dynamicInstances--;
      returnObjectToPool(instance);
      // console.log(`Removed and pooled instance, dynamicInstances: ${dynamicInstances}`);
    }
  }
}


// Initialize stats-gl
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

let lastFrameTime = performance.now();

const tick = () => {
  const now = performance.now()
  const frameTime = now - lastFrameTime
  lastFrameTime = now

  // Move the camera forward
  moveCamera();

  // Procedurally add or remove instances based on camera position
  addOrRemoveInstance();

  // stats.begin()
  const cpuStartTime = performance.now();
  renderer.render(scene, camera);
  const cpuEndTime = performance.now();
  const cpuTime = cpuEndTime - cpuStartTime;
  // stats.end()

  stats.update()
  
  fps = 1000 / frameTime;
  modelCount = dynamicInstances;


  // Increase instancesPerFrame if FPS is above the threshold
  if (fps > fpsThreshold && instancesPerFrame < maxInstancesPerFrame && now - lastIncreaseTime > increaseInterval) {
    instancesPerFrame += 1;
    lastIncreaseTime = now;
  }

  window.statsData = {
    fps: fps,
    gpu: stats.totalGpuDuration,
    cpu: cpuTime,
    modelCount: modelCount
  };

  window.renderInfo = {
      drawCalls: renderer.info.render.calls,
      totalFrameTime: frameTime,
  };

  // console.log(statsData.gpu);
  
  requestAnimationFrame(tick);
};

tick();
// document.addEventListener('visibilitychange', function () {
//   if (document.hidden) {
//     renderer.setAnimationLoop(null);
//   } else {
//     renderer.setAnimationLoop(animate);
//   }
// });

/**
 * Preload all textures and then load the models
 */
preloadTextures(modelData, loadInitialModels);
