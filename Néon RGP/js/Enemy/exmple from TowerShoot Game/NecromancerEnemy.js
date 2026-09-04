// NecromancerEnemy.js
class NecromancerEnemy extends Enemy {
    constructor(x, y) { super(x, y, 60, 1.5, 10, 30, "hsl(280, 80%, 30%)", SHAPE.STAR, 6); this.timer = 0; }
    update(dt) { this.updateStatusEffects(dt); this.moveTowardPlayer(dt); this.shapeAngle += 0.02 * (dt / 16.66); this.timer += dt; if (this.timer > 3000 && corpses.length) { this.timer = 0; const corpse = corpses.shift(); spawnParticleBurst(corpse.x, corpse.y, "#a855f7"); const Type = ENEMY_FACTORY[corpse.type] || ChaserEnemy; const enemy = new Type(corpse.x, corpse.y); enemy.health = enemy.maxHealth / 2; enemies.push(enemy); } }
}
