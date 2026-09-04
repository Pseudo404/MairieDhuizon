import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class GrapperEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.8;
        this.maxHp = 80;
        this.hp = this.maxHp;
        this.damage = 10;
        this.color = "#ffab40"; // amber
        this.grappleTimer = 0;
        this.isGrappling = false;
        this.grappleTarget = null;
    }

    update(target) {
        super.update(target);
        
        this.grappleTimer -= 16.66;
        this.isGrappling = false;
        
        if (target && this.gameManager && this.gameManager.grapples) {
            const dx = target.x - this.x;
            const dy = target.y - this.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            // Vérifie s'il y a déjà un grappin actif depuis cet ennemi
            const hasActiveGrapple = this.gameManager.grapples.some(g => g.source === this);
            
            if (hasActiveGrapple) {
                this.isGrappling = true;
                this.grappleTarget = target;
            } else if (this.grappleTimer <= 0 && dist < 300) {
                this.grappleTimer = 4500;
                this.gameManager.grapples.push({
                    source: this,
                    targetPlayer: true,
                    life: 800,
                    pullSpeed: 1.0
                });
                this.isGrappling = true;
                this.grappleTarget = target;
            }
        }
    }

    draw() {
        if (this.isGrappling && this.grappleTarget) {
            ctx.save();
            ctx.strokeStyle = this.color;
            ctx.lineWidth = 2;
            ctx.globalAlpha = 0.6;
            ctx.beginPath();
            ctx.moveTo(this.x, this.y);
            ctx.lineTo(this.grappleTarget.x, this.grappleTarget.y);
            ctx.stroke();
            ctx.restore();
        }
        super.draw();
    }
}
