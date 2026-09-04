// SummonerEnemy.js
class SummonerEnemy extends Enemy {
	constructor(x, y) {
		super(x, y, 100, 1.2, 10, 50, "hsl(320, 80%, 40%)", SHAPE.STAR, 7);
		this.timer = 0;
		this.summonStep = 0;
	}
	update(dt) {
		this.updateStatusEffects(dt);
		const dx = player.x - this.x;
		const dy = player.y - this.y;
		const distance = Math.sqrt(dx * dx + dy * dy);
		if (distance > 0 && distance < 400) {
			this.x -= (dx / distance) * this.speed * (dt / 16.66);
			this.y -= (dy / distance) * this.speed * (dt / 16.66);
		}
		this.x = Math.max(this.radius, Math.min(canvas.width - this.radius, this.x));
		this.y = Math.max(this.radius, Math.min(canvas.height - this.radius, this.y));
		this.shapeAngle += 0.03 * (dt / 16.66);
		this.timer += dt;
		if (this.timer > 4000) {
			this.timer = 0;
			const types = [TankEnemy, TrackingShooterEnemy, MirageEnemy, GrapperEnemy, HealerEnemy];
			const Type = types[this.summonStep % types.length];
			this.summonStep++;
			const ally = new Type(this.x + rand(-50, 50), this.y + rand(-50, 50));
			enemies.push(ally);
			spawnParticleBurst(ally.x, ally.y, this.color);
		}
	}
}
