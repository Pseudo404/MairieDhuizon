import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class MageEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.5;
        this.maxHp = 90;
        this.hp = this.maxHp;
        this.damage = 20;
        this.color = "#536dfe"; // indigo-blue
        this.castTimer = 0;
        this.castCooldown = 3500;
        this.orbRotation = 0;
    }

    update(target) {
        super.update(target);
        
        this.orbRotation += 0.05;
        this.castTimer -= 16.66;
        
        if (this.castTimer <= 0 && target && this.gameManager && this.gameManager.hazards) {
            this.castTimer = this.castCooldown;
            this.gameManager.hazards.push({
                x: target.x,
                y: target.y,
                radius: 0,
                maxRadius: 55,
                timer: 0,
                duration: 2000,
                damage: 15,
                color: '#536dfe'
            });
        }
    }

    draw() {
        super.draw();
        
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.orbRotation);
        ctx.fillStyle = "#ffffff";
        
        for (let i = 0; i < 4; i++) {
            ctx.beginPath();
            ctx.arc(this.size + 6, 0, 2, 0, Math.PI * 2);
            ctx.fill();
            ctx.rotate(Math.PI / 2);
        }
        
        ctx.restore();
    }
}
