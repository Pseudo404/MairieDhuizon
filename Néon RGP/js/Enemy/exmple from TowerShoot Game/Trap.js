// Trap.js
class Trap {
    constructor(x, y) { this.x = x; this.y = y; this.radius = 18; this.life = 8000; this.damage = 6; }
    update(dt) { this.life -= dt; }
    draw(ctx) { ctx.fillStyle = "rgba(0, 255, 0, 0.4)"; ctx.strokeStyle = "#0f0"; beginShapePath(ctx, SHAPE.STAR, this.x, this.y, this.radius, this.life / 200, 4); ctx.fill(); ctx.stroke(); }
}
