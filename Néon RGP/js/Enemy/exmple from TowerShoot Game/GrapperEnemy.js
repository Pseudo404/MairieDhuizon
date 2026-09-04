// GrapperEnemy.js
class GrapperEnemy extends Enemy {
    constructor(x, y) {
        super(x, y, 70, 1.5, 10, 30, "hsl(40, 80%, 50%)", SHAPE.POLYGON, 4);
        this.timer = 0;
    }
    update(dt) {
        this.updateStatusEffects(dt);
        this.moveTowardPlayer(dt);
        this.shapeAngle += 0.02 * (dt / 16.66);
        this.timer += dt;
        if (this.timer > 4000) {
            this.timer = 0;
            if (squaredDistance(this.x, this.y, player.x, player.y) < 90000)
                grapples.push({
                    source: this,
                    target: player,
                    life: 1000,
                    pullSpeed: 0.75,
                });
        }
    }
}
