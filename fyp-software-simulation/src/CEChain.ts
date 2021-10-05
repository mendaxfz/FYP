import { CESeg } from './CESeg';
import { NULL_LOC } from './constants';
import { Loc } from './constants';

interface Props {
    size: number;
    interval: number;
}

export const CEChain = function ({ size, interval }: Props): void {
    // Array of all worm 'segments'
    this.links = new Array<typeof CESeg>(size);

    this.update = function (target: Loc) {
        const link = this.links[0];

        link.head.x = target.x;
        link.head.y = target.y;

        for (let i = 0, n = this.links.length; i < n; ++i) {
            this.links[i].update();
        }
    };

    let point = NULL_LOC;

    for (let i = 0, n = this.links.length; i < n; ++i) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const link = (this.links[i] = new (CESeg as any)({ size: interval, head: point }));
        link.head.x = Math.random() * 500;
        link.head.y = Math.random() * 500;
        link.tail.x = Math.random() * 500;
        link.tail.y = Math.random() * 500;
        point = link.tail;
    }
};
