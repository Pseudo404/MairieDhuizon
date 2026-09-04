import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class TankEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.5;
        this.maxHp = 120;
        this.hp = this.maxHp;
        this.damage = 20;
        this.size = 18;
        this.color = "#b388ff"; // lavender
    }

    update(target) {
        super.update(target);
    }

    draw() {
        super.draw();
        // Double anneau pour le tank
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(0, 0, this.size + 3, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(0, 0, this.size + 6, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }
}
