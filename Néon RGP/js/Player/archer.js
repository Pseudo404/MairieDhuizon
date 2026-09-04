import { Player } from "./player.js";

export class Archer extends Player {
    constructor(x, y) {
        super(x, y);

        this.color = "#00e0ff";
        this.speed = 6;
        this.maxHp = 80;
        this.hp = 80;
        this.damage = 35;
        this.range = 500;
        this.attackCooldown = 350;
        this.critChance = 0.1;
    }
}
