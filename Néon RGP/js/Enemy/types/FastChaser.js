import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class FastChaser extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 4.5;
        this.maxHp = 35;
        this.hp = this.maxHp;
        this.damage = 15;
        this.color = "#e040fb"; // pink-purple
    }

    update(target) {
        super.update(target); // Base movement and effects
    }

    draw() {
        super.draw();
        // Dessine un triangle par-dessus
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, -this.size + 4);
        ctx.lineTo(this.size - 4, this.size - 4);
        ctx.lineTo(-this.size + 4, this.size - 4);
        ctx.closePath();
        ctx.stroke();
        ctx.restore();
    }
}
