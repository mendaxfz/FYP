import { CEChain } from './CEChain';
import { Loc } from './constants';
import { circle } from './draw';
import * as h337 from 'heatmap.js';
import { Brain } from './brain';

import { GPU } from 'gpu.js';

const canvas: HTMLCanvasElement = document.getElementById('canvas') as HTMLCanvasElement;
const ctx: CanvasRenderingContext2D = canvas.getContext('2d');

let facingDir = 0;
let targetDir = 0;
let speed = 0;

const getRandom = (min: number, max: number) => Math.floor(Math.random() * (max - min + 1) + min);

const heatMapInstance = h337.create({
    radius: 2,
    container: document.getElementById('container'),
});

const gpu = new GPU();

// now generate some random data
const points: { x: number; y: number; value: number }[] = [];
const max = 27;
const min = 16;
const width = 1500;
const height = 1000;

const HEAT_SOURCES = [
    { x: 50, y: 100, i: 3 },
    { x: 500, y: 500, i: 3 },

    { x: 500, y: 540, i: 3 },

    { x: 520, y: 450, i: 3 },

    { x: 520, y: 450, i: 3 },
    { x: 520, y: 300, i: 3 },

    { x: 400, y: 250, i: 3 },

    { x: 800, y: 450, i: 3 },
    { x: 600, y: 700, i: 2 },
    { x: 1000, y: 400, i: 2 },
    { x: 700, y: 100, i: 2 },
    { x: 650, y: 100, i: 2 },

    { x: 200, y: 200, i: -3 },
    { x: 200, y: 400, i: -3 },
    { x: 700, y: 500, i: -3 },
    { x: 650, y: 400, i: -3 },

    { x: 700, y: 200, i: 3 },
    { x: 650, y: 300, i: 3 },

    { x: 700, y: 550, i: -3 },

    { x: 450, y: 100, i: 3 },

    { x: 500, y: 700, i: 3 },
];

// map array objects to GPU vector form
const xs = HEAT_SOURCES.map((h) => h.x);
const ys = HEAT_SOURCES.map((h) => h.y);
const vs = HEAT_SOURCES.map((h) => h.i);

console.time('gpu');
const multip = gpu
    .createKernel(function (xs: number[], ys: number[], vs: number[]) {
        let sum = 0;
        // sum up all the heat sources to get temperature at a point
        for (let i = 0; i < this.constants.points; i++) {
            sum +=
                vs[i] *
                Math.pow(
                    Math.E,
                    (-1 / 40) * Math.sqrt(Math.pow(this.thread.x - xs[i], 2) + Math.pow(this.thread.y - ys[i], 2)),
                );
        }
        // add the sum to the mean value for the map (19 degrees)
        return 19 + sum;
    })
    .setConstants({ points: vs.length })
    .setOutput([height, width]);
console.timeEnd('gpu');

const result: number[][] = multip(xs, ys, vs) as number[][];

for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
        points.push({ x, y, value: result[y][x] });
    }
}

// // heatmap data format
const data = {
    max: max,
    min: min,
    data: points,
};

heatMapInstance.setData(data);

const target: Loc = {
    x: window.innerWidth / 2.8,
    y: window.innerHeight / 1.8,
};
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const chain = new (CEChain as any)({ size: 20, interval: 1 });

// Initialize the worm brain
// NOTE: This Brain object lives in an external file
Brain.init();

console.time('timeToEnd');

/**
 * This function is called when we want to pass the data about
 * the current environment to the brain and in return
 * get the new left/right accumulator from which we decide
 * the new turning direction of the worm
 */
async function updateBrain() {
    const { x, y } = target;
    // send the environment data to the brain
    await Brain.update(result[Math.floor(y)][Math.floor(x)]);

    // update target direction
    targetDir = facingDir + (Brain.accumLeft - Brain.accumRight);

    // if in a comparator state, boost speed up, otherwise decay speed
    if (Brain.stimulatePositiveComparator || Brain.stimulateNegativeComparator) {
        speed += 0.007;
    } else {
        speed -= 0.2;
        console.timeEnd('timeToEnd');
    }
}
// Call for a brain update every 100 ms
setInterval(updateBrain, 100);

const update = () => {
    // Reset speed if it goes above minimum
    // or maximum
    if (speed < 0.1) speed = 0.1;
    if (speed > 0.65) speed = 0.65;

    // Get angle difference
    const facingMinusTarget = facingDir - targetDir;
    let angleDiff = facingMinusTarget;

    if (Math.abs(facingMinusTarget) > Math.PI) {
        if (facingDir > targetDir) {
            angleDiff = -(2 * Math.PI - facingDir + targetDir);
        } else {
            angleDiff = 2 * Math.PI - targetDir + facingDir;
        }
    }

    // Smooth out facing direction changes
    // we only rotate by 0.2 radians per frame
    if (angleDiff > 0) {
        facingDir -= 0.2;
    } else if (angleDiff < 0) {
        facingDir += 0.2;
    }

    // Move in x/y direction at a set speed
    target.x += Math.cos(facingDir) * speed;
    target.y -= Math.sin(facingDir) * speed;

    // Update the worm's chain
    chain.update(target);
};

// Worm's trail
const trail: Array<Loc> = [];

const draw = (): void => {
    // Clear the currently shown context
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // draw a circle at the head's position
    circle(ctx, target.x, target.y, 5, 'rgba(255,255,255,0.1)');

    let link = chain.links[0];
    let p1 = link.head,
        p2 = link.tail;

    // set context parameters for worm trail's drawing
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 20;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';

    trail.push({ ...target });

    // --- Draw trail elements ---
    trail.forEach((t) => {
        circle(ctx, t.x, t.y, 1, 'rgba(255,255,255,0.5)');
    });

    for (let i = 0, n = chain.links.length; i < n; ++i) {
        link = chain.links[i];
        p1 = link.head;
        p2 = link.tail;
        ctx.lineTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
    }

    ctx.stroke();
    // ===========================
};

(function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    window.onresize = resize;
})();

setInterval(function () {
    update();
    draw();
}, 1e3 / 60);
