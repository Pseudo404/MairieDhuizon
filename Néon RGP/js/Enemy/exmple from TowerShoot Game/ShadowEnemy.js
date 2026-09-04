// ShadowEnemy.js
class ShadowEnemy extends Enemy {
    constructor(x, y) {
        super(x, y, 30, 2.5, 15, 20, "hsl(0, 0%, 30%)", SHAPE.CIRCLE, 0);
        this.dodgeChance = 0.25;
    }
    update(dt) {
        this.updateStatusEffects(dt);
        this.moveTowardPlayer(dt);
    }
}
