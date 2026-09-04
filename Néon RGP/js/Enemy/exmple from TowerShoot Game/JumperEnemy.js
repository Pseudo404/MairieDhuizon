// JumperEnemy.js
class JumperEnemy extends Enemy {
    constructor(x, y) {
        super(x, y, 50, 0, 25, 25, "hsl(20, 80%, 50%)", SHAPE.POLYGON, 5);
        this.jumpState = "idle";
        this.timer = 0;
        this.warningTimer = 0;
    }
    update(dt) {
        this.updateStatusEffects(dt);
        if (this.jumpState === "idle") {
            this.timer += dt;
            if (this.timer > 2000) {
                this.jumpState = "warning";
                this.timer = 0;
                this.jumpTargetX = player.x;
                this.jumpTargetY = player.y;
            }
        } else if (this.jumpState === "warning") {
            this.warningTimer += dt;
            if (this.warningTimer > 1000) {
                this.jumpState = "jumping";
                this.warningTimer = 0;
                this.startX = this.x;
                this.startY = this.y;
                this.jumpProgress = 0;
            }
        } else if (this.jumpState === "jumping") {
            this.jumpProgress += dt * 0.002;
            if (this.jumpProgress >= 1) {
            this.jumpState = "idle";
            this.jumpProgress = 0;
                this.x = this.jumpTargetX;
                this.y = this.jumpTargetY;
                spawnParticleBurst(this.x, this.y, this.color);
                if (
                    squaredDistance(this.x, this.y, player.x, player.y) <
                    (this.radius + 30 + player.radius) ** 2
                )
                    damagePlayer(this.damage);
            } else {
                this.x =
                    this.startX +
                    (this.jumpTargetX - this.startX) * this.jumpProgress;
                this.y =
                    this.startY +
                    (this.jumpTargetY - this.startY) * this.jumpProgress;
            }
        }
        this.shapeAngle += 0.05 * (dt / 16.66);
    }
}
