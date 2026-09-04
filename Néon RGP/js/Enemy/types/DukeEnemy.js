import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class DukeEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.0;
        this.maxHp = 250;
        this.hp = this.maxHp;
        this.damage = 25;
        this.size = 22;
        this.color = "#ffd740"; // gold
        this.slamTimer = 0;
        this.slamCooldown = 5000;
        this.rotation = 0;
        this.shockwaveRadius = 0;
    }

    update(target) {
        super.update(target);
        
        this.rotation += 0.01;
        this.slamTimer -= 16.66;
        
        // Animation d'onde de choc
        if (this.shockwaveRadius > 0) {
            this.shockwaveRadius += 4;
            if (this.shockwaveRadius > 100) {
                this.shockwaveRadius = 0;
            }
        }
        
        // Attaque de zone (slam)
        if (this.slamTimer <= 0) {
            this.slamTimer = this.slamCooldown;
            this.shockwaveRadius = this.size; // Démarre l'animation
            
            if (target) {
                const dx = target.x - this.x;
                const dy = target.y - this.y;
                if (Math.sqrt(dx * dx + dy * dy) <= 80) {
                    if (target.takeDamage) target.takeDamage(this.damage);
                }
            }
        }
    }

    draw() {
        // Onde de choc
        if (this.shockwaveRadius > 0) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.strokeStyle = this.color;
            ctx.globalAlpha = 1 - (this.shockwaveRadius / 100);
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.arc(0, 0, this.shockwaveRadius, 0, Math.PI * 2);
            ctx.stroke();
            ctx.restore();
        }

        super.draw();

        // Accent de couronne et double anneau
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 1;
        
        // Double anneau
        ctx.beginPath();
        ctx.arc(0, 0, this.size + 4, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(0, 0, this.size + 8, 0, Math.PI * 2);
        ctx.stroke();
        
        // Couronne (petits triangles)
        ctx.fillStyle = "#ffffff";
        for (let i = 0; i < 3; i++) {
            ctx.beginPath();
            ctx.moveTo(-4, -this.size - 2);
            ctx.lineTo(4, -this.size - 2);
            ctx.lineTo(0, -this.size - 10);
            ctx.fill();
            ctx.rotate((Math.PI * 2) / 3);
        }
        
        ctx.restore();
    }
}
