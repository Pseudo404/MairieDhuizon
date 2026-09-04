
const originalCanvas = document.getElementById("game-canvas");
const originalCtx = originalCanvas.getContext("2d");

export let canvas = originalCanvas;
export let ctx = originalCtx;

export function overrideContext(newCanvas, newCtx) {
    canvas = newCanvas || originalCanvas;
    ctx = newCtx || originalCtx;
}

function resize() {
    if (canvas === originalCanvas) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
}

window.addEventListener("resize", resize);
resize(); // Initialisation

export function clearScreen(color = "#111111") {
    ctx.shadowBlur = 0;
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}
