import { Client } from 'rpc-websockets';

const ENABLE_WS = true;

let ws: Client | undefined = undefined;
let isWebsocketOpen = false;

if (ENABLE_WS) {
    ws = new Client('ws://192.168.0.103:8080');

    ws.on('open', () => (isWebsocketOpen = true));
}

enum ComparatorType {
    Positive = 'Positive',
    Negative = 'Negative',
    Equal = 'Equal',
}

export interface IBrain {
    fireThreshold: number;
    accumLeft: number;
    accumRight: number;
    tempDiff: number;
    prevTemp: number;

    stimulatePositiveComparator: boolean;
    stimulateNegativeComparator: boolean;

    init: () => void;
    update: (temp: number) => Promise<void>;

    _comparator: (temp: number, fireThreshold: number) => Promise<ComparatorType>;
    _gradientDetector: (
        side: Exclude<ComparatorType, ComparatorType.Equal>,
        lastTemp: number,
        temp: number,
    ) => Promise<boolean>;
}

const deg2rad = (deg: number) => deg * (Math.PI / 180);

const getRandom = (min: number, max: number) => Math.floor(Math.random() * (max - min + 1) + min);

const canUseWs = () => ENABLE_WS && isWebsocketOpen;

export const Brain: IBrain = {
    fireThreshold: 20,

    accumLeft: 0,
    accumRight: 0,

    tempDiff: 0,

    prevTemp: 0,

    stimulateNegativeComparator: false,
    stimulatePositiveComparator: false,

    init: function (): void {
        this.accumLeft += getRandom(deg2rad(-7.5), deg2rad(7.5));
        this.accumRight += getRandom(deg2rad(-7.5), deg2rad(7.5));
    },

    update: async function (temp: number): Promise<void> {
        // console.log('\n');

        switch (await this._comparator(temp, this.fireThreshold)) {
            case ComparatorType.Positive:
                console.log('[-] Activated positive comparator');
                console.log(this.prevTemp);
                console.log(temp);

                this.stimulatePositiveComparator = true;
                this.stimulateNegativeComparator = false;

                if (await this._gradientDetector(ComparatorType.Positive, this.prevTemp, temp)) {
                    console.log('[~] Activated positive gradient');

                    this.accumLeft = deg2rad(25);
                    this.accumRight = 0;
                    break;
                }

                console.log('[*] Random walk');
                this.accumLeft = deg2rad(getRandom(-30, 30));
                this.accumRight = deg2rad(getRandom(-30, 30));
                break;
            case ComparatorType.Negative:
                console.log('[-] Activated negative comparator');

                this.stimulateNegativeComparator = true;
                this.stimulatePositiveComparator = false;

                if (await this._gradientDetector(ComparatorType.Negative, this.prevTemp, temp)) {
                    console.log('[~] Activated negative gradient');

                    this.accumRight = deg2rad(25);
                    this.accumLeft = 0;
                    break;
                }

                console.log('[*] Random walk');
                this.accumLeft = deg2rad(getRandom(-30, 30));
                this.accumRight = deg2rad(getRandom(-30, 30));
                break;
            case ComparatorType.Equal:
                this.stimulateNegativeComparator = false;
                this.stimulatePositiveComparator = false;
                console.log('[±] Ideal temperature');
                this.accumLeft = deg2rad(getRandom(-15, 15));
                this.accumRight = deg2rad(getRandom(-15, 15));
                break;
        }

        console.log('------- Parameter -------');
        console.log('Temp: ' + temp);
        console.log('Accum left: ' + this.accumLeft);
        console.log('Accum right: ' + this.accumRight);
        console.log('=========================');

        this.prevTemp = temp;
    },

    _comparator: async function (temp, fireThreshold) {
        // Check if we can use the WebSocket
        if (canUseWs()) {
            try {
                // Call the comparator RPC method
                const res = await ws.call('comparator', { temp, fireThreshold });
                if (temp < fireThreshold + 0.5 && temp > fireThreshold - 0.5) return ComparatorType.Equal;
                return res as ComparatorType;
            } catch (error) {
                // Log an error if any
                console.error(error);
            }
        }

        // Default to manual comparator implementation
        if (temp > fireThreshold + 0.5) return ComparatorType.Positive;
        else if (temp < fireThreshold - 0.5) return ComparatorType.Negative;
        else return ComparatorType.Equal;
    },

    _gradientDetector: async function (side, prevTemp, temp) {
        // Check if we can use the WebSocket
        if (canUseWs()) {
            // get if checking for positive or negative gradient
            const _side = side as string;
            try {
                // Call the gradient detector RPC method
                const res = await ws.call('gradientDetector', { side: _side, prevTemp, temp });
                return res as boolean;
            } catch (error) {
                // Log an error if any
                console.log(error);
            }
        }

        // Default to manual gradient detector implementation
        return side === 'Positive' ? temp > prevTemp + 0.01 : temp < prevTemp - 0.01;
    },
};
