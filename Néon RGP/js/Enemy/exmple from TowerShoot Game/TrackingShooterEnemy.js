// TrackingShooterEnemy.js
class TrackingShooterEnemy extends ShooterEnemy {
    constructor(x, y) {
        super(x, y);
        this.color = "hsl(30, 80%, 50%)";
    }
    update(dt) {
        super.update(dt);
        if (this.timer === 0) {
            const bullet = enemyBullets[enemyBullets.length - 1];
            bullet.tracking = true;
            bullet.trackTurnRate = (Math.PI * 3.5) / 180;
        }
    }
}
