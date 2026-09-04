import { Player } from "./player.js";

export class Sniper extends Player {
    constructor(x, y) {
        super(x, y);

        this.color = "#a78bfa";
        this.speed = 4;
        this.maxHp = 80;
        this.hp = 80;
        this.damage = 45;
        this.range = 1000;
        this.attackCooldown = 1000;
        // Ces statistiques sont améliorables via Guidage et Munitions perforantes.
        this.followBullet = 0;
        this.piercing = 1;
    }
}
