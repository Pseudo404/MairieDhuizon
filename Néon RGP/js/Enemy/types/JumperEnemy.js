import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";
import { EFFECT_TYPES, hasEffect } from "../../game/effects.js";

export class JumperEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 0; // Se déplace uniquement en sautant
        this.maxHp = 60;
        this.hp = this.maxHp;
        this.damage = 25;
        this.color = "#ff6e40"; // orange-red
        
        this.state = "idle"; // idle, warning, jumping
        this.stateTimer = 2500;
        
        this.targetX = 0;
        this.targetY = 0;
        this.startX = 0;
        this.startY = 0;
    }

    update(target) {
        super.update(null); // Gère les effets mais pas le mouvement

        if (hasEffect(this, EFFECT_TYPES.STUN)) return;
        
        this.stateTimer -= 16.66;
        
        if (this.state === "idle") {
            if (this.stateTimer <= 0 && target) {
                this.state = "warning";
                this.stateTimer = 1000;
                this.targetX = target.x;
                this.targetY = target.y;
            }
        } else if (this.state === "warning") {
            if (this.stateTimer <= 0) {
                this.state = "jumping";
                this.stateTimer = 500;
                this.startX = this.x;
                this.startY = this.y;
            }
        } else if (this.state === "jumping") {
            const progress = 1 - (this.stateTimer / 500);
            if (this.stateTimer <= 0) {
                // Atterrissage
                this.x = this.targetX;
                this.y = this.targetY;
                this.state = "idle";
                this.stateTimer = 2500;
                
                // Dégâts de zone
                if (target) {
                    const dx = target.x - this.x;
                    const dy = target.y - this.y;
                    if (Math.sqrt(dx * dx + dy * dy) <= 45) {
                        if (target.takeDamage) target.takeDamage(this.damage);
                    }
                }
            } else {
                // Lerp
                this.x = this.startX + (this.targetX - this.startX) * progress;
                this.y = this.startY + (this.targetY - this.startY) * progress;
            }
        }
    }

    draw() {
        if (this.state === "warning") {
            // Dessine la zone de danger
            ctx.save();
            ctx.translate(this.targetX, this.targetY);
            ctx.strokeStyle = this.color;
            ctx.globalAlpha = 0.5 + Math.sin(this.stateTimer / 50) * 0.5;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(0, 0, 45, 0, Math.PI * 2);
            ctx.stroke();
            ctx.restore();
        }

        super.draw();
        
        if (this.state === "jumping") {
            // Étirement pendant le saut
            ctx.save();
            ctx.translate(this.x, this.y);
            const angle = Math.atan2(this.targetY - this.startY, this.targetX - this.startX);
            ctx.rotate(angle);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = 0.5;
            ctx.beginPath();
            ctx.ellipse(0, 0, this.size * 2, this.size * 0.5, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }
}
