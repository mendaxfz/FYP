import { NULL_LOC } from './constants';
import { Loc } from './constants';

interface Props {
    size: number;
    head?: Loc;
    tail?: Loc;
}

const SPRINGINESS = 0.998;
const FORCE_M = 0.99;

export const CESeg = function ({ size, head, tail }: Props): void {
    this.size = size;
    /**
     * NOTE: NULL_LOC represents the {x: 0, y: 0} position
     */
    // get head and tail position or fallback
    this.head = head ?? NULL_LOC;
    this.tail = tail ?? {
        x: this.head.x + size,
        y: this.head.y + size,
    };

    this.update = function (): void {
        // Position derivitives
        const dx = this.head.x - this.tail.x;
        const dy = this.head.y - this.tail.y;

        const dist = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));
        // FORCE_M = 0.99
        const force = FORCE_M * (0.5 - (this.size / dist) * 0.5);
        // SPRINGINESS = 0.998
        const strength = SPRINGINESS; // The higher the number the less springiness (almost none in our case)

        const fx = force * dx;
        const fy = force * dy;

        // Re-calculate the tail and head positions
        this.tail.x += fx * strength * 2.0;
        this.tail.y += fy * strength * 2.0;
        this.head.x -= fx * (1.0 - strength) * 2.0;
        this.head.y -= fy * (1.0 - strength) * 2.0;
    };
};
