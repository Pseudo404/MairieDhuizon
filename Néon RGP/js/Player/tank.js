import { Player } from "./player.js";

export class Tank extends Player {
    constructor(x, y) {
        super(x, y);

        this.color = "#005763ff";
        this.speed = 4;
        this.maxHp = 120;
        this.hp = 120;
        this.damage = 30;
        this.attackCooldown = 700;
        this.attackStyle = "hammer";
        this.range = 90;
        this.hammerStunDuration = 0;
    }
}
