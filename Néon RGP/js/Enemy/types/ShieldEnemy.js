import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class ShieldEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.5;
        this.maxHp = 90;
        this.hp = this.maxHp;
        this.damage = 15;
        this.color = "#42a5f5"; // blue
        this.shieldAngle = 0;
        this.reflectDamageMultiplier = 0.8;
        this.shieldArc = Math.PI / 3;
    }

    update(target) {
        super.update(target);
        if (target) {
            this.shieldAngle = Math.atan2(target.y - this.y, target.x - this.x);
        }
    }

    isShieldHit(hitX, hitY) {
        const hitAngle = Math.atan2(hitY - this.y, hitX - this.x);
        let diff = Math.abs(hitAngle - this.shieldAngle);
        if (diff > Math.PI) diff = 2 * Math.PI - diff;
        return diff <= this.shieldArc;
    }

    reflectBullet(bullet) {
        if (!this.isShieldHit(bullet.x, bullet.y)) return false;

        // The collision point is placed just outside the shield so the returned
        // projectile cannot immediately collide with this enemy again.
        const exitDistance = this.size + bullet.radius + 2;
        bullet.x = this.x + Math.cos(this.shieldAngle) * exitDistance;
        bullet.y = this.y + Math.sin(this.shieldAngle) * exitDistance;
        bullet.dirX *= -1;
        bullet.dirY *= -1;
        bullet.damage *= this.reflectDamageMultiplier;
        bullet.lifetime = Math.max(bullet.lifetime, 90);
        return true;
    }

    draw() {
        super.draw();
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.shieldAngle);
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 4;
        ctx.beginPath();
        // Dessine l'arc du bouclier
        ctx.arc(0, 0, this.size + 4, -this.shieldArc, this.shieldArc);
        ctx.stroke();
        ctx.restore();
    }
}
