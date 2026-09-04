import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";
import { EFFECT_TYPES, hasEffect } from "../../game/effects.js";

export class MirageEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.5;
        this.maxHp = 65;
        this.hp = this.maxHp;
        this.damage = 12;
        this.color = "#ea80fc"; // light purple
        this.shootTimer = 0;
        this.cloneTimer = 0;
        this.isClone = false;
    }

    update(target) {
        super.update(null); // Gère les effets

        if (!target) return;
        if (hasEffect(this, EFFECT_TYPES.STUN)) return;

        // Maintient la distance
        const targetDistance = 150;
        const dx = target.x - this.x;
        const dy = target.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const angle = Math.atan2(dy, dx);

        if (distance > targetDistance + 10) {
            this.x += Math.cos(angle) * this.speed;
            this.y += Math.sin(angle) * this.speed;
        } else if (distance < targetDistance - 10) {
            this.x -= Math.cos(angle) * this.speed;
            this.y -= Math.sin(angle) * this.speed;
        }

        // Tir
        this.shootTimer -= 16.66;
        if (this.shootTimer <= 0 && this.gameManager && this.gameManager.enemyBullets) {
            this.shootTimer = 1800;
            this.gameManager.enemyBullets.push({
                x: this.x,
                y: this.y,
                dirX: dx / distance,
                dirY: dy / distance,
                speed: 4,
                radius: 5,
                damage: this.damage,
                color: this.color,
                lifetime: 180
            });
        }

        // Clonage
        if (!this.isClone) {
            this.cloneTimer -= 16.66;
            if (this.cloneTimer <= 0 && this.gameManager && this.gameManager.enemies) {
                this.cloneTimer = 8000;
                const offsetX = (Math.random() - 0.5) * 100;
                const offsetY = (Math.random() - 0.5) * 100;
                const clone = new MirageEnemy(this.x + offsetX, this.y + offsetY, this.gameManager);
                clone.isClone = true;
                clone.hp = this.maxHp / 2;
                clone.maxHp = this.maxHp / 2;
                this.gameManager.enemies.push(clone);
            }
        }
    }

    draw() {
        if (this.isClone) {
            ctx.globalAlpha = 0.6;
        }
        super.draw();
        ctx.globalAlpha = 1.0;
    }
}
