// ShieldEnemy.js
class ShieldEnemy extends Enemy {
    constructor(x, y) {
        super(x, y, 80, 1.2, 15, 20, "hsl(200, 80%, 50%)", SHAPE.POLYGON, 3);
        this.rotateSpeed = 0.001;
    }
    update(dt) {
        this.updateStatusEffects(dt);
        this.moveTowardPlayer(dt);
        const targetAngle = Math.atan2(player.y - this.y, player.x - this.x);
        let angleDelta = targetAngle - this.shapeAngle;
        while (angleDelta > Math.PI) angleDelta -= Math.PI * 2;
        while (angleDelta < -Math.PI) angleDelta += Math.PI * 2;
        const maxTurn = this.rotateSpeed * dt;
        this.shapeAngle += Math.max(-maxTurn, Math.min(maxTurn, angleDelta));
    }
    draw(ctx) {
        super.draw(ctx);
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(
            this.x,
            this.y,
            this.radius + 5,
            this.shapeAngle - Math.PI / 9,
            this.shapeAngle + Math.PI / 9,
        );
        ctx.stroke();
    }
}
