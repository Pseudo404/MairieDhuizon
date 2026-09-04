import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class ShadowEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 2.8;
        this.maxHp = 35;
        this.hp = this.maxHp;
        this.damage = 15;
        this.color = "#616161"; // dark grey
        this.dodgeChance = 0.25;
        this.dodgeFlash = 0;
    }

    update(target) {
        super.update(target); // Base movement and effects
        if (this.dodgeFlash > 0) this.dodgeFlash -= 16.66;
    }

    takeDamage(amount) {
        if (Math.random() < this.dodgeChance) {
            this.dodgeFlash = 100;
            return;
        }
        super.takeDamage(amount);
    }

    draw() {
        if (this.dodgeFlash > 0) {
            ctx.globalAlpha = 0.3;
        }
        super.draw();
        ctx.globalAlpha = 1.0;
    }
}
