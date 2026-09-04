import { ShooterEnemy } from "./ShooterEnemy.js";

export class FastShooterEnemy extends ShooterEnemy {
    constructor(x, y, gameManager = null) {
        super(x, y, gameManager);
        this.shootCooldown = 800; // Tire plus vite
        this.color = "#18ffff";
        this.damage = 5;
    }
}
