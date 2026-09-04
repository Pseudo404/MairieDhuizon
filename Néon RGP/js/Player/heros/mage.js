import { Player } from "../player.js";

export class Mage extends Player {
    constructor(x, y) {
        super(x, y);

        this.color = "#ff4d6d";
        this.speed = 4;
        this.maxHp = 85;
        this.hp = 85;
        this.damage = 15;
        this.maxDamage = 100;
        this.range = 500;
        this.attackStyle = "laser";
        this.laserHeatRate = 0.15;
        this.laserHeat = 0;
        this.laserTarget = null;
    }
}
