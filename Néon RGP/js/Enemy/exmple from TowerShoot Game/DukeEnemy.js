// DukeEnemy.js
class DukeEnemy extends Enemy { constructor(x, y) { super(x, y, 200, 1.0, 20, 50, "hsl(45, 90%, 40%)", SHAPE.POLYGON, 6); this.timer = 0; } update(dt) { this.updateStatusEffects(dt); this.moveTowardPlayer(dt); this.timer += dt; this.shapeAngle += 0.01 * (dt / 16.66); } }
