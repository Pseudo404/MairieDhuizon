import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class TrapperEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 2.2;
        this.maxHp = 50;
        this.hp = this.maxHp;
        this.damage = 8;
        this.color = "#00e676"; // green
        this.trapTimer = 0;
        this.trapCooldown = 5000;
    }

    update(target) {
        super.update(target);
        
        this.trapTimer -= 16.66;
        if (this.trapTimer <= 0 && this.gameManager && this.gameManager.traps) {
            this.trapTimer = this.trapCooldown;
            this.gameManager.traps.push({
                x: this.x,
                y: this.y,
                radius: 20,
                life: 8000,
                damage: 8,
                color: '#00e676'
            });
        }
    }

    draw() {
        super.draw();
        
        // Forme d'étoile superposée
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 1.5;
        
        for (let i = 0; i < 4; i++) {
            ctx.beginPath();
            ctx.moveTo(-this.size + 4, 0);
            ctx.lineTo(this.size - 4, 0);
            ctx.stroke();
            ctx.rotate(Math.PI / 4);
        }
        
        ctx.restore();
    }
}
