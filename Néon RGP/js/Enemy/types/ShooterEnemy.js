import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";
import { EFFECT_TYPES, hasEffect } from "../../game/effects.js";

export class ShooterEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.8;
        this.maxHp = 40;
        this.hp = this.maxHp;
        this.damage = 8;
        this.color = "#00e5ff"; // cyan
        this.shootTimer = 0;
        this.shootCooldown = 2000;
        this.targetDistance = 210;
        this.targetAngle = 0;
    }

    update(target) {
        super.update(null); // Gère les effets et le hitTimer sans le mouvement de base

        if (!target) return;
        if (hasEffect(this, EFFECT_TYPES.STUN)) return;

        const dx = target.x - this.x;
        const dy = target.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        this.targetAngle = Math.atan2(dy, dx);

        // Maintient la distance
        if (distance > this.targetDistance + 10) {
            this.x += Math.cos(this.targetAngle) * this.speed;
            this.y += Math.sin(this.targetAngle) * this.speed;
        } else if (distance < this.targetDistance - 10) {
            this.x -= Math.cos(this.targetAngle) * this.speed;
            this.y -= Math.sin(this.targetAngle) * this.speed;
        }

        // Tir
        this.shootTimer -= 16.66;
        if (this.shootTimer <= 0 && this.gameManager && this.gameManager.enemyBullets) {
            this.shootTimer = this.shootCooldown;
            this.shoot(target);
        }
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
            lifetime: 180
        });
    }

    draw() {
        super.draw();
        // Ligne de visée
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.targetAngle);
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(this.size, 0);
        ctx.lineTo(this.size + 8, 0);
        ctx.stroke();
        ctx.restore();
    }
}
