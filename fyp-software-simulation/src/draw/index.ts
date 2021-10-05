export const circle = (ctx: CanvasRenderingContext2D, x: number, y: number, r: number, c: string): void => {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2, false);
    ctx.closePath();
    if (c) {
        ctx.fillStyle = c;
        ctx.fill();
    } else {
        ctx.strokeStyle = 'rgba(255,255,255,0.1)';
        ctx.stroke();
    }
};

export const line = (ctx: CanvasRenderingContext2D, x1: number, y1: number, x2: number, y2: number): void => {
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = 'rgba(255,255,255,0.5)';
    ctx.stroke();
};
