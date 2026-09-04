// MirageEnemy.js
class MirageEnemy extends Enemy {
    constructor(x, y) { super(x, y, 60, 1.2, 15, 35, "hsl(280, 80%, 60%)", SHAPE.POLYGON, 6); this.attackTimer = 0; this.cloneTimer = 0; }
    update(dt) { this.updateStatusEffects(dt); const dx = player.x - this.x, dy = player.y - this.y, distance = Math.sqrt(dx * dx + dy * dy); if (distance > 150) { this.x += dx / distance * this.speed * (dt / 16.66); this.y += dy / distance * this.speed * (dt / 16.66); } this.attackTimer += dt; if (this.attackTimer > 1500) { this.attackTimer = 0; enemyBullets.push({ x: this.x, y: this.y, vx: dx / distance * 4, vy: dy / distance * 4, radius: 6, damage: 10, color: this.color }); } this.cloneTimer += dt; }
}
