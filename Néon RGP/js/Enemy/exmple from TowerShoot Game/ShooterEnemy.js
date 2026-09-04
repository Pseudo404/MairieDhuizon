// ShooterEnemy.js
class ShooterEnemy extends Enemy {
    constructor(x, y) { super(x, y, 25, 1.5, 10, 15, "hsl(190, 80%, 50%)", SHAPE.POLYGON, 4); this.cooldown = 2000; this.timer = 0; }
    update(dt) {
        this.updateStatusEffects(dt); const dx = player.x - this.x, dy = player.y - this.y, distance = Math.sqrt(dx * dx + dy * dy);
        if (distance > 210) { this.x += dx / distance * this.speed * (dt / 16.66); this.y += dy / distance * this.speed * (dt / 16.66); }
        this.shapeAngle += 0.05; this.timer += dt;
        if (this.timer > this.cooldown) { this.timer = 0; enemyBullets.push({ x: this.x, y: this.y, vx: dx / distance * 3, vy: dy / distance * 3, radius: 6, damage: this.damage, color: this.color }); }
    }
}
