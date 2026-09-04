import { ctx } from "../screen/canvas.js";

export class Bullet {
    constructor(x, y, dirX, dirY, speed, damage, color, radius, isCritical = false) {
        this.x = x;
        this.y = y;
        this.dirX = dirX;
        this.dirY = dirY;
        this.speed = speed;
        this.damage = damage;
        this.color = color;
        this.radius = radius;
        this.isCritical = isCritical;
        this.remainingPierces = 0;
        this.homingStrength = 0;
        this.hitEnemies = new Set();

        this.lifetime = 120;
    }

    update() {
        this.x += this.dirX * this.speed;
        this.y += this.dirY * this.speed;
        this.lifetime--;
    }

    draw() {
        ctx.fillStyle = this.color;
        
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();

        if (this.isCritical) {
            ctx.strokeStyle = "#fff3b0";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius + 3, 0, Math.PI * 2);
            ctx.stroke();
        }
        
        ctx.shadowBlur = 0; // Reset
    }
}
