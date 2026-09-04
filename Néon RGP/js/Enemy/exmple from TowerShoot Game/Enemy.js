// Enemy.js
class Enemy {
    constructor(x, y, health, speed, damage, xpValue, color, shape, sides) {
        this.x = x; this.y = y; this.radius = 14; this.maxHealth = health; this.health = health;
        this.speed = speed; this.damage = damage; this.xpValue = xpValue; this.color = color;
        this.shape = shape; this.sides = sides; this.shapeAngle = 0; this.dodgeChance = 0;
        this.statusEffects = []; this.hitTimer = 0;
    }
    _lighterHsl() {
        const match = this.color.match(/hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)/);
        return match ? `hsl(${match[1]}, ${match[2]}%, ${Math.min(100, parseInt(match[3]) + 20)}%)` : this.color;
    }
    applyStatus(EffectClass) {
        const current = this.statusEffects.find(effect => effect instanceof EffectClass);
        if (current) current.timeLeft = current.duration;
        else this.statusEffects.push(new EffectClass());
    }
    updateStatusEffects(dt) {
        if (this.hitTimer > 0) this.hitTimer -= dt;
        this.statusEffects = this.statusEffects.filter(effect => effect.update(dt, this));
        if (this.statusEffects.some(effect => effect instanceof BurnEffect) && Math.random() < 0.2) {
            particles.push({ x: this.x + rand(-8, 8), y: this.y + rand(-8, 8), vx: rand(-0.5, 0.5), vy: rand(-2, -0.5), life: 450, color: Math.random() < 0.5 ? "#f97316" : "#fbbf24", size: rand(4, 8) });
        }
        if (this.statusEffects.some(effect => effect instanceof PoisonEffect) && Math.random() < 0.18) {
            particles.push({ x: this.x + rand(-6, 6), y: this.y + rand(-4, 4), vx: rand(-0.3, 0.3), vy: rand(-1.8, -0.6), life: 500, color: "#22c55e", size: rand(4, 7) });
        }
        if (this.statusEffects.some(effect => effect instanceof ElectricEffect) && Math.random() < 0.35) {
            const angle = Math.random() * Math.PI * 2, length = rand(12, 30);
            particles.push({ isArc: true, x1: this.x, y1: this.y, x2: this.x + Math.cos(angle) * length, y2: this.y + Math.sin(angle) * length, life: rand(80, 180), color: "#00ffff" });
        }
    }
    moveTowardPlayer(dt) {
        const dx = player.x - this.x, dy = player.y - this.y, distance = Math.sqrt(dx * dx + dy * dy);
        if (distance > 0) { this.x += dx / distance * this.speed * (dt / 16.66); this.y += dy / distance * this.speed * (dt / 16.66); }
    }
    update(dt) { this.updateStatusEffects(dt); this.moveTowardPlayer(dt); this.shapeAngle += 0.05 * (dt / 16.66); }
    draw(ctx) {
        ctx.fillStyle = this.hitTimer > 0 ? "#ffffff" : this.color;
        ctx.strokeStyle = this.hitTimer > 0 ? "#ffffff" : this._lighterHsl();
        ctx.lineWidth = 2; beginShapePath(ctx, this.shape, this.x, this.y, this.radius, this.shapeAngle, this.sides); ctx.fill(); ctx.stroke();
    }
}
