// HealerEnemy.js
class HealerEnemy extends Enemy {
    constructor(x, y) {
        super(x, y, 40, 1.8, 5, 20, "hsl(150, 80%, 50%)", SHAPE.CIRCLE, 0);
        this.timer = 0;
    }
    update(dt) {
        this.updateStatusEffects(dt);
        this.x = Math.max(this.radius, Math.min(canvas.width - this.radius, this.x));
        this.y = Math.max(this.radius, Math.min(canvas.height - this.radius, this.y));
        let target = null;
        let nearestDistance = Infinity;
        enemies.forEach((ally) => {
            if (ally !== this && !(ally instanceof HealerEnemy) && ally.health > 0 && ally.health < ally.maxHealth) {
                const distance = squaredDistance(this.x, this.y, ally.x, ally.y);
                if (distance < nearestDistance) {
                    nearestDistance = distance;
                    target = ally;
                }
            }
        });

        if (target) {
            const dx = target.x - this.x;
            const dy = target.y - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance > 70) {
                this.x += (dx / distance) * this.speed * (dt / 16.66);
                this.y += (dy / distance) * this.speed * (dt / 16.66);
            }
        }

        this.x = Math.max(this.radius, Math.min(canvas.width - this.radius, this.x));
        this.y = Math.max(this.radius, Math.min(canvas.height - this.radius, this.y));
        this.timer += dt;
        if (this.timer > 2000) {
            this.timer = 0;
            enemies.forEach((enemy) => {
                if (
                    enemy !== this &&
                    !(enemy instanceof HealerEnemy) &&
                    enemy.health > 0 &&
                    enemy.health < enemy.maxHealth &&
                    squaredDistance(this.x, this.y, enemy.x, enemy.y) < 90000
                ) {
                    enemy.health = Math.min(enemy.maxHealth, enemy.health + 15);
                    spawnParticleBurst(enemy.x, enemy.y, "#4ade80");
                }
            });
            spawnParticleBurst(this.x, this.y, "#4ade80");
        }
    }
}
