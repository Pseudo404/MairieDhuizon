import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class NecromancerEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.5;
        this.maxHp = 70;
        this.hp = this.maxHp;
        this.damage = 10;
        this.color = "#7c4dff"; // deep purple
        this.reviveTimer = 0;
        this.reviveCooldown = 4000;
        this.auraRotation = 0;
    }

    update(target) {
        super.update(target);
        
        this.auraRotation -= 0.02;
        this.reviveTimer -= 16.66;
        
        if (this.reviveTimer <= 0 && this.gameManager && this.gameManager.corpses && this.gameManager.corpses.length > 0) {
            this.reviveTimer = this.reviveCooldown;
            // Prend le premier cadavre disponible
            const corpse = this.gameManager.corpses.shift();
            
            // Fait revivre un ennemi basique
            const revivedEnemy = new Enemy(corpse.x, corpse.y);
            revivedEnemy.hp = revivedEnemy.maxHp / 2;
            
            if (this.gameManager.enemies) {
                this.gameManager.enemies.push(revivedEnemy);
            }
        }
    }

    draw() {
        // Aura lumineuse terrifiante
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.auraRotation);
        ctx.fillStyle = this.color;
        ctx.globalAlpha = 0.3;
        ctx.beginPath();
        
        // Aura en étoile
        for (let i = 0; i < 8; i++) {
            ctx.lineTo(0, this.size + (i % 2 === 0 ? 10 : 4));
            ctx.rotate((Math.PI * 2) / 8);
        }
        
        ctx.closePath();
        ctx.fill();
        ctx.restore();
        
        super.draw();
    }
}
