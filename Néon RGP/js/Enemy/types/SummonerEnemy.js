import { Enemy } from "../enemy.js";
import { ctx } from "../../screen/canvas.js";

export class SummonerEnemy extends Enemy {
    constructor(x, y, gameManager = null) {
        super(x, y);
        this.gameManager = gameManager;
        this.speed = 1.5;
        this.maxHp = 110;
        this.hp = this.maxHp;
        this.damage = 10;
        this.color = "#f50057"; // hot pink
        this.summonTimer = 0;
        this.summonCooldown = 5000;
        this.pulsePhase = 0;
    }

    update(target) {
        super.update(null); // Gère les effets

        this.pulsePhase += 0.05;

        if (target) {
            const dx = target.x - this.x;
            const dy = target.y - this.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            // Fuit le joueur si trop proche
            if (dist < 350) {
                this.x -= (dx / dist) * this.speed;
                this.y -= (dy / dist) * this.speed;
            }
            
            // Garde l'ennemi dans l'écran (basé sur une taille typique)
            this.x = Math.max(30, Math.min(this.x, window.innerWidth - 30));
            this.y = Math.max(30, Math.min(this.y, window.innerHeight - 30));
        }

        // Invocation
        this.summonTimer -= 16.66;
        if (this.summonTimer <= 0 && this.gameManager && this.gameManager.enemies) {
            this.summonTimer = this.summonCooldown;
            
            const offsetX = (Math.random() - 0.5) * 60;
            const offsetY = (Math.random() - 0.5) * 60;
            const summoned = new Enemy(this.x + offsetX, this.y + offsetY);
            this.gameManager.enemies.push(summoned);
        }
    }

    draw() {
        // Aura pulsante
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.strokeStyle = this.color;
        ctx.globalAlpha = 0.4 + Math.sin(this.pulsePhase) * 0.2;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(0, 0, this.size + 8 + Math.sin(this.pulsePhase) * 4, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();

        super.draw();
    }
}
