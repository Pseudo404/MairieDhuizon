import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";
import { EFFECT_TYPES, hasEffect } from "../../game/effects.js";

export class HealerEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.8;
        this.maxHp = 50;
        this.hp = this.maxHp;
        this.damage = 5;
        this.color = "#69f0ae"; // green
        this.healTimer = 0;
        this.healCooldown = 2500;
        this.healRadius = 200;
        this.healPulseTimer = 0;
    }

    update(target) {
        super.update(null); // Ne chasse pas le joueur

        if (this.healPulseTimer > 0) this.healPulseTimer -= 16.66;
        if (hasEffect(this, EFFECT_TYPES.STUN)) return;

        let mostDamagedAlly = null;
        let lowestHpRatio = 1.0;

        if (this.gameManager && this.gameManager.enemies) {
            // Trouve l'allié le plus blessé à soigner
            for (const enemy of this.gameManager.enemies) {
                if (enemy === this || enemy instanceof HealerEnemy) continue;
                
                const dx = enemy.x - this.x;
                const dy = enemy.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                const hpRatio = enemy.hp / enemy.maxHp;
                if (dist <= this.healRadius && hpRatio < lowestHpRatio) {
                    lowestHpRatio = hpRatio;
                    mostDamagedAlly = enemy;
                }
            }
        }

        // Mouvement : suit l'allié le plus blessé, ou le joueur par défaut
        const moveTarget = mostDamagedAlly || target;
        if (moveTarget) {
            const dx = moveTarget.x - this.x;
            const dy = moveTarget.y - this.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            // Si c'est un allié, on reste à bonne distance
            const targetDist = mostDamagedAlly ? 50 : 250;
            if (dist > targetDist) {
                this.x += (dx / dist) * this.speed;
                this.y += (dy / dist) * this.speed;
            } else if (dist < targetDist - 20) {
                this.x -= (dx / dist) * this.speed;
                this.y -= (dy / dist) * this.speed;
            }
        }

        // Soin
        this.healTimer -= 16.66;
        if (this.healTimer <= 0 && this.gameManager && this.gameManager.enemies) {
            this.healTimer = this.healCooldown;
            let healed = false;
            
            for (const enemy of this.gameManager.enemies) {
                if (enemy === this || enemy instanceof HealerEnemy) continue;
                
                const dx = enemy.x - this.x;
                const dy = enemy.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist <= this.healRadius && enemy.hp < enemy.maxHp) {
                    enemy.hp = Math.min(enemy.maxHp, enemy.hp + 12);
                    healed = true;
                }
            }
            if (healed) {
                this.healPulseTimer = 500; // Animation de soin
            }
        }
    }

    draw() {
        super.draw();
        if (this.healPulseTimer > 0) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.strokeStyle = this.color;
            ctx.globalAlpha = this.healPulseTimer / 500;
            ctx.lineWidth = 2;
            ctx.beginPath();
            const radius = this.size + (500 - this.healPulseTimer) / 10;
            ctx.arc(0, 0, radius, 0, Math.PI * 2);
            ctx.stroke();
            ctx.restore();
        }
    }
}
