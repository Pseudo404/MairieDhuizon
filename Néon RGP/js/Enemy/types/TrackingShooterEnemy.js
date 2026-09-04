import { ShooterEnemy } from "./ShooterEnemy.js";

export class TrackingShooterEnemy extends ShooterEnemy {
    constructor(x, y, gameManager = null) {
        super(x, y, gameManager);
        this.color = "#ff9100"; // orange
    }

    shoot(target) {
        const dx = target.x - this.x;
        const dy = target.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist === 0) return;

        this.gameManager.enemyBullets.push({
            x: this.x,
            y: this.y,
            dirX: dx / dist,
            dirY: dy / dist,
            speed: 4,
            radius: 5,
            damage: this.damage,
            color: this.color,
            lifetime: 180,
            tracking: true,
            trackTurnRate: 0.06
        });
    }
}
