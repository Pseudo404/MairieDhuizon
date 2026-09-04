// MageEnemy.js
class MageEnemy extends Enemy {
    constructor(x, y) { super(x, y, 80, 1.5, 30, 40, "hsl(220, 80%, 50%)", SHAPE.POLYGON, 4); this.timer = 0; }
    update(dt) { this.updateStatusEffects(dt); this.moveTowardPlayer(dt); this.shapeAngle += 0.02 * (dt / 16.66); this.timer += dt; if (this.timer > 3000) { this.timer = 0; hazards.push({ x: player.x, y: player.y, radius: 0, maxRadius: 60, timer: 0, duration: 1500, damage: this.damage }); } }
}
