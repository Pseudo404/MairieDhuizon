import { Player } from "./player.js";

export class Stealer extends Player {
    constructor(x, y) {
        super(x, y);

        this.color = "#4ee6c8";
        this.speed = 7;
        this.maxHp = 50;
        this.hp = 50;
        this.damage = 25;
        this.range = 400;
        this.attackCooldown = 280;
        this.lifeSteal = 0.1;
    }
}
