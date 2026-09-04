// TrapperEnemy.js
class TrapperEnemy extends Enemy {
    constructor(x, y) { super(x, y, 40, 2.0, 10, 20, "hsl(120, 80%, 50%)", SHAPE.STAR, 5); this.trapTimer = 0; }
    update(dt) { super.update(dt); this.trapTimer += dt; if (this.trapTimer > 5000) { this.trapTimer = 0; traps.push(new Trap(this.x, this.y)); } }
}
