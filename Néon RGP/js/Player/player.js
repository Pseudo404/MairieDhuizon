import { ctx, canvas } from "../screen/canvas.js";
import { getInput } from "../game/input.js";

export class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        
        this.speed = 5;
        this.maxHp = 100;
        this.hp = 100;
        this.size = 12;
        this.color = "#38bdf8";

        this.damage = 25;
        this.range = 500;
        this.attackCooldown = 500;
        this.lastAttack = 0;
        this.damageReduction = 0;
        
        this.hitTimer = 0;
        this.hitCooldown = 0;

        this.level = 1;
        this.maxLevel = 50;
        this.xp = 0;
        this.xpNeeded = 100;
        this.score = 0;
        
        this.onLevelUp = null;
    }

    update() {
        if (this.hitTimer > 0) this.hitTimer -= 16.66;
        if (this.hitCooldown > 0) this.hitCooldown -= 16.66;

        const input = getInput();
        
        this.x += input.dx * this.speed;
        this.y += input.dy * this.speed;

        this.x = Math.max(this.size, Math.min(canvas.width - this.size, this.x));
        this.y = Math.max(this.size, Math.min(canvas.height - this.size, this.y));

        this.updateHUD();
    }

    takeDamage(amount) {
        if (this.hitCooldown > 0) return false;
        
        const reducedDamage = amount * (1 - this.damageReduction);
        this.hp -= reducedDamage;
        if (this.hp < 0) this.hp = 0;
        
        this.hitTimer = 200; // Clignotement très rapide et court (200ms)
        this.hitCooldown = 70; // On peut se refaire toucher très vite (70ms)

        return true;
    }

    draw() {
        // Clignotement blanc très rapide si touché
        if (this.hitTimer > 0 && Math.floor(this.hitTimer / 50) % 2 === 0) {
            ctx.fillStyle = "#ffffff";
        } else {
            ctx.fillStyle = this.color;
        }
        
        // Effet néon
        ctx.shadowBlur = 20;
        ctx.shadowColor = this.color;
        
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }

    updateHUD() {
        const hpBar = document.getElementById('hpBar');
        const hpText = document.getElementById('hpText');
        const xpBar = document.getElementById('xpBar');
        const lvlText = document.getElementById('lvlText');
        const scoreText = document.getElementById('scoreText');
        
        if (hpBar) {
            const percent = Math.max(0, (this.hp / this.maxHp) * 100);
            hpBar.style.width = `${percent}%`;
        }
        if (hpText) {
            hpText.innerText = `${Math.floor(this.hp)} / ${this.maxHp}`;
        }
        if (xpBar) {
            const xpPercent = Math.min(100, (this.xp / this.xpNeeded) * 100);
            xpBar.style.width = `${xpPercent}%`;
        }
        if (lvlText) {
            lvlText.innerText = `NIV ${this.level}`;
        }
        if (scoreText) {
            scoreText.innerText = `${this.score} PTS`;
        }
    }

    gainXp(amount) {
        if (this.level >= this.maxLevel) return; // Plus d'XP au niveau max

        this.xp += amount;
        this.score += amount;
        
        // Level up (peut monter de plusieurs niveaux d'un coup si beaucoup d'XP)
        while (this.xp >= this.xpNeeded && this.level < this.maxLevel) {
            this.xp -= this.xpNeeded;
            this.level++;
            this.xpNeeded = Math.floor(this.xpNeeded * 1.5); // Augmente la difficulté
            
            // Soin au level up
            // this.maxHp += 5;
            // this.hp = this.maxHp;
            
            // Appeler le callback pour afficher l'écran d'amélioration
            if (this.onLevelUp) {
                this.onLevelUp();
            }
        }
        
        // Si on a atteint le niveau max pendant la boucle, on vide l'XP restante
        if (this.level >= this.maxLevel) {
            this.xp = this.xpNeeded; 
        }
    }

    // Gardé par rétrocompatibilité avec notre gameManager, mais ne fait rien
    // puisque le HUD est géré en HTML maintenant
    drawHUD() {
        // Ne rien faire
    }
}
