// ============================================================
// upgrade.js — Catalogue et effets des améliorations
// ============================================================

export function increaseMaxHealth(player) {
    player.maxHp += 20;
    player.hp += 20;
}

export function increaseSpeed(player) {
    player.speed += 1;
}

export function increaseDamage(player) {
    player.damage += 10;
}

export function healPlayer(player) {
    player.hp = Math.min(player.maxHp, player.hp + 20);
}

export function reduceAttackCooldown(player) {
    player.attackCooldown = Math.max(100, player.attackCooldown - 50);
}

export function increaseCriticalChance(player) {
    player.critChance = (player.critChance || 0) + 0.1;
}

export function increaseCriticalDamage(player) {
    player.critDamage = (player.critDamage || 0) + 5;
}

export function increaseDamageReduction(player) {
    // 80 % est une limite de sécurité : le Tank doit toujours pouvoir mourir.
    player.damageReduction = Math.min(0.8, (player.damageReduction || 0) + 0.05);
}

export function increaseHammerStunDuration(player) {
    player.hammerStunDuration = (player.hammerStunDuration || 0) + 250;
}

export function increaseBulletGuidance(player) {
    player.followBullet = Math.min(0.5, (player.followBullet || 0) + 0.08);
}

export function increaseBulletPiercing(player) {
    player.piercing = (player.piercing || 0) + 1;
}

export function increaseLaserHeatRate(player) {
    player.laserHeatRate = Math.min(1, (player.laserHeatRate || 0) + 0.08);
}

export function increaseLaserMinDamage(player) {
    player.damage += 5;
}

export function increaseLaserMaxDamage(player) {
    player.maxDamage += 15;
}

export function increaseStealerSpeed(player) {
    player.speed += 1;
}

export function increaseLifeSteal(player) {
    // Plafond à 35 % pour garder le héros vulnérable.
    player.lifeSteal = Math.min(0.35, (player.lifeSteal || 0) + 0.05);
}

export function increaseStealerAttackSpeed(player) {
    player.attackCooldown = Math.max(100, player.attackCooldown - 40);
}

// Toutes les informations présentées au joueur vivent ici, avec leur effet.
export const UPGRADES = [
    {
        id: 'heal_up',
        name: 'Soin',
        desc: '+20 PV',
        icon: '🩹',
        heroes: ['All'],
        effect: healPlayer
    },
    {
        id: 'hp_up',
        name: 'Santé Max',
        desc: '+20 PV Max',
        icon: '❤️',
        heroes: ['All'],
        effect: increaseMaxHealth
    },
    {
        id: 'speed_up',
        name: 'Bottes de Vent',
        desc: '+1 Vitesse',
        icon: '👟',
        heroes: ['All'],
        effect: increaseSpeed
    },
    {
        id: 'damage_up',
        name: 'Force Brute',
        desc: '+10 Dégâts',
        icon: '⚔️',
        heroes: ['Archer', 'Tank', 'Sniper'],
        effect: increaseDamage
    },
    {
        id: 'attack_speed_up',
        name: 'Corde Tendue',
        desc: 'Tire plus vite (-50 ms de délai)',
        icon: '🏹',
        heroes: ['Archer'],
        effect: reduceAttackCooldown
    },
    {
        id: 'crit_chance_up',
        name: 'Œil de Faucon',
        desc: '+10 % Chance de Critique',
        icon: '👁️',
        heroes: ['Archer'],
        effect: increaseCriticalChance
    },
    {
        id: 'damage_reduction_up',
        name: 'Armure Renforcée',
        desc: '-5 % Dégâts reçus',
        icon: '🛡️',
        heroes: ['Tank'],
        effect: increaseDamageReduction
    },
    {
        id: 'hammer_stun_up',
        name: 'Impact Sismique',
        desc: '+0,25 s d’immobilisation',
        icon: '🔨',
        heroes: ['Tank'],
        effect: increaseHammerStunDuration
    },
    {
        id: 'bullet_guidance_up',
        name: 'Guidage Balistique',
        desc: '+8 % de guidage du projectile',
        icon: '🎯',
        heroes: ['Sniper'],
        effect: increaseBulletGuidance
    },
    {
        id: 'bullet_piercing_up',
        name: 'Munitions Perforantes',
        desc: '+1 ennemi traversé',
        icon: '🪡',
        heroes: ['Sniper'],
        effect: increaseBulletPiercing
    },
    {
        id: 'laser_heat_rate_up',
        name: 'Surchauffe Accélérée',
        desc: '+8 % de vitesse de chauffe',
        icon: '🔥',
        heroes: ['Mage'],
        effect: increaseLaserHeatRate
    },
    {
        id: 'laser_min_damage_up',
        name: 'Rayon Initial',
        desc: '+5 dégâts minimum',
        icon: '🔴',
        heroes: ['Mage'],
        effect: increaseLaserMinDamage
    },
    {
        id: 'laser_max_damage_up',
        name: 'Cœur Incandescent',
        desc: '+15 dégâts maximum',
        icon: '☀️',
        heroes: ['Mage'],
        effect: increaseLaserMaxDamage
    },
    {
        id: 'stealer_speed_up',
        name: 'Pas Fantôme',
        desc: '+1 vitesse de déplacement',
        icon: '💨',
        heroes: ['Stealer'],
        effect: increaseStealerSpeed
    },
    {
        id: 'life_steal_up',
        name: 'Soif de Sang',
        desc: '+5 % de vol de vie (max 35 %)',
        icon: '🩸',
        heroes: ['Stealer'],
        effect: increaseLifeSteal
    },
    {
        id: 'stealer_attack_speed_up',
        name: 'Lames Frénétiques',
        desc: 'Tire plus vite (-40 ms)',
        icon: '⚡',
        heroes: ['Stealer'],
        effect: increaseStealerAttackSpeed
    }
];

export function getAvailableUpgrades(heroName) {
    return UPGRADES.filter(upgrade =>
        upgrade.heroes.includes('All') || upgrade.heroes.includes(heroName)
    );
}

export function applyUpgrade(upgrade, player) {
    upgrade.effect(player);
}
