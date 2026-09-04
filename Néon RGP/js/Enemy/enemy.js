import { ctx } from "../screen/canvas.js";
import {
    EFFECT_TYPES,
    getEffectShakeOffset,
    hasEffect,
    updateEffects
} from "../game/effects.js";

// ============================================================
// enemy.js — Classe de base pour l'Ennemi
// ============================================================

export class Enemy {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        
        // Stats de base
        this.speed = 2.5;
        this.maxHp = 50;
        this.hp = this.maxHp;
        this.size = 14;
        this.color = "#ff3b6b"; // Couleur rose/rouge issue de l'ancien CSS
        
        // Combat
        this.damage = 10;
        this.hitTimer = 0; // Pour clignoter en blanc quand touché
        this.activeEffects = new Map();
    }

    // L'ennemi suit bêtement une cible (le joueur)
    update(target) {
        if (this.hitTimer > 0) this.hitTimer -= 16.66; // 60fps approx
        updateEffects(this, 16.66);

        if (!target) return;
        if (hasEffect(this, EFFECT_TYPES.STUN)) return;

        const dx = target.x - this.x;
        const dy = target.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 0) {
            this.x += (dx / distance) * this.speed;
            this.y += (dy / distance) * this.speed;
        }
    }

    takeDamage(amount) {
        this.hp -= amount;
        this.hitTimer = 150; // Clignote pendant 150ms
    }

    draw() {
        const shake = getEffectShakeOffset(this);
        const isCriticalHit = hasEffect(this, EFFECT_TYPES.CRITICAL);
        ctx.save();
        ctx.translate(shake.x, shake.y);

        ctx.fillStyle = this.hitTimer > 0 ? "#ffffff" : this.color;
        
        // Effet néon
        ctx.shadowBlur = 20;
        ctx.shadowColor = this.color;
        
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();

        if (isCriticalHit) {
            ctx.strokeStyle = "#ffcf5c";
            ctx.lineWidth = 3;
            ctx.shadowBlur = 14;
            ctx.shadowColor = "#ffcf5c";
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size + 6, 0, Math.PI * 2);
            ctx.stroke();

            ctx.fillStyle = "#fff3b0";
            ctx.font = "900 11px Segoe UI, sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("CRIT !", this.x, this.y - this.size - 22);
        }

        // Dessiner la barre de vie
        this.drawHealthBar();
        ctx.restore();
    }

    drawHealthBar() {
        ctx.shadowBlur = 0; // Pas de néon pour la barre de vie
        
        const barWidth = 30;
        const barHeight = 5;
        const barX = this.x - barWidth / 2;
        const barY = this.y - this.size - 12;

        // Fond gris
        ctx.fillStyle = "#333333";
        ctx.fillRect(barX, barY, barWidth, barHeight);

        // Barre de vie restante
        ctx.fillStyle = this.color;
        const currentWidth = (this.hp / this.maxHp) * barWidth;
        ctx.fillRect(barX, barY, Math.max(0, currentWidth), barHeight);
    }
}
