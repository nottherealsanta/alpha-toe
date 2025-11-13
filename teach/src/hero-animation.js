/**
 * Hero Animation
 * Displays a background animation of X and O shapes.
 */
import * as THREE from 'three';
import { SVGLoader } from 'three/examples/jsm/loaders/SVGLoader.js';

export function initHeroAnimation() {
    const container = document.getElementById('hero-bg');
    if (!container) {
        console.error('hero-bg container not found');
        return;
    }

    let scene, camera, renderer;
    const objects = [];
    const NUM_OBJECTS = 150; // Fixed number of objects

    function init() {
        // Scene
        scene = new THREE.Scene();

        // Camera
        camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 50;

        // Renderer
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        // Load SVGs and create objects
        loadSVG('/assets/x.svg', 0);
        loadSVG('/assets/o.svg', 1);

        // Event Listeners
        window.addEventListener('resize', onWindowResize);

        animate();
    }

    function loadSVG(url, type) {
        const loader = new SVGLoader();
        loader.load(url, (data) => {
            const paths = data.paths;
            const group = new THREE.Group();
            group.scale.multiplyScalar(0.1);
            group.scale.y *= -1;

            for (let i = 0; i < paths.length; i++) {
                const path = paths[i];
                const material = new THREE.MeshBasicMaterial({
                    color: path.color,
                    side: THREE.DoubleSide,
                    depthWrite: false
                });
                const shapes = SVGLoader.createShapes(path);
                for (let j = 0; j < shapes.length; j++) {
                    const shape = shapes[j];
                    const geometry = new THREE.ShapeGeometry(shape);
                    const mesh = new THREE.Mesh(geometry, material);
                    group.add(mesh);
                }
            }
            
            // Distribute objects
            for (let i = 0; i < NUM_OBJECTS / 2; i++) {
                const object = group.clone();
                object.position.x = Math.random() * 100 - 50;
                object.position.y = Math.random() * 100 - 50;
                object.position.z = Math.random() * 100 - 50;
                object.rotation.x = Math.random() * 2 * Math.PI;
                object.rotation.y = Math.random() * 2 * Math.PI;
                object.rotation.z = Math.random() * 2 * Math.PI;
                object.userData.type = type;
                objects.push(object);
                scene.add(object);
            }
        });
    }

    function onWindowResize() {
        if (!container) return;
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }

    function animate() {
        requestAnimationFrame(animate);

        objects.forEach(object => {
            if (object.userData.type === 0) { // X
                object.rotation.x += 0.001;
                object.rotation.y += 0.001;
            } else { // O
                object.rotation.x -= 0.001;
                object.rotation.y -= 0.001;
            }
        });

        renderer.render(scene, camera);
    }

    init();
}
