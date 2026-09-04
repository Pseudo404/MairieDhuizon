import { Enemy } from './enemy.js';
import { FastChaser } from './types/FastChaser.js';
import { TankEnemy } from './types/TankEnemy.js';
import { ShooterEnemy } from './types/ShooterEnemy.js';
import { FastShooterEnemy } from './types/FastShooterEnemy.js';
import { TrackingShooterEnemy } from './types/TrackingShooterEnemy.js';
import { ShadowEnemy } from './types/ShadowEnemy.js';
import { ShieldEnemy } from './types/ShieldEnemy.js';
import { HealerEnemy } from './types/HealerEnemy.js';
import { JumperEnemy } from './types/JumperEnemy.js';
import { MageEnemy } from './types/MageEnemy.js';
import { MirageEnemy } from './types/MirageEnemy.js';
import { GrapperEnemy } from './types/GrapperEnemy.js';
import { TrapperEnemy } from './types/TrapperEnemy.js';
import { NecromancerEnemy } from './types/NecromancerEnemy.js';
import { SummonerEnemy } from './types/SummonerEnemy.js';
import { DukeEnemy } from './types/DukeEnemy.js';

export const ENEMY_TYPES = Object.freeze({
    Grunt:           Enemy,
    FastChaser:      FastChaser,
    Tank:            TankEnemy,
    Shooter:         ShooterEnemy,
    FastShooter:     FastShooterEnemy,
    TrackingShooter: TrackingShooterEnemy,
    Shadow:          ShadowEnemy,
    Shield:          ShieldEnemy,
    Healer:          HealerEnemy,
    Jumper:          JumperEnemy,
    Mage:            MageEnemy,
    Mirage:          MirageEnemy,
    Grapper:         GrapperEnemy,
    Trapper:         TrapperEnemy,
    Necromancer:     NecromancerEnemy,
    Summoner:        SummonerEnemy,
    Duke:            DukeEnemy
});

export const WAVE_TABLE = Object.freeze([
    // Vagues 1-2 : seulement des Grunts
    { minWave: 1,  types: [{ type: 'Grunt', weight: 10 }] },
    // Vague 3 : FastChasers apparaissent
    { minWave: 3,  types: [{ type: 'Grunt', weight: 8 }, { type: 'FastChaser', weight: 4 }] },
    // Vague 5 : Tanks et Shooters
    { minWave: 5,  types: [{ type: 'Grunt', weight: 6 }, { type: 'FastChaser', weight: 4 }, { type: 'Tank', weight: 3 }, { type: 'Shooter', weight: 3 }] },
    // Vague 7 : Shadow et Shield
    { minWave: 7,  types: [{ type: 'Grunt', weight: 5 }, { type: 'FastChaser', weight: 4 }, { type: 'Tank', weight: 3 }, { type: 'Shooter', weight: 3 }, { type: 'Shadow', weight: 3 }, { type: 'Shield', weight: 2 }] },
    // Vague 9 : Healer et Trapper
    { minWave: 9,  types: [{ type: 'Grunt', weight: 4 }, { type: 'FastChaser', weight: 3 }, { type: 'Tank', weight: 3 }, { type: 'Shooter', weight: 3 }, { type: 'Shadow', weight: 3 }, { type: 'Shield', weight: 2 }, { type: 'Healer', weight: 2 }, { type: 'Trapper', weight: 2 }] },
    // Vague 11 : Jumper et FastShooter
    { minWave: 11, types: [{ type: 'Grunt', weight: 3 }, { type: 'FastChaser', weight: 3 }, { type: 'Tank', weight: 3 }, { type: 'Shooter', weight: 2 }, { type: 'FastShooter', weight: 3 }, { type: 'Shadow', weight: 3 }, { type: 'Shield', weight: 2 }, { type: 'Healer', weight: 2 }, { type: 'Trapper', weight: 2 }, { type: 'Jumper', weight: 3 }] },
    // Vague 13 : Mage et TrackingShooter
    { minWave: 13, types: [{ type: 'Grunt', weight: 2 }, { type: 'FastChaser', weight: 3 }, { type: 'Tank', weight: 3 }, { type: 'Shooter', weight: 2 }, { type: 'FastShooter', weight: 3 }, { type: 'TrackingShooter', weight: 2 }, { type: 'Shadow', weight: 3 }, { type: 'Shield', weight: 2 }, { type: 'Healer', weight: 2 }, { type: 'Trapper', weight: 2 }, { type: 'Jumper', weight: 3 }, { type: 'Mage', weight: 2 }] },
    // Vague 15 : Mirage et Grapper
    { minWave: 15, types: [{ type: 'Grunt', weight: 2 }, { type: 'FastChaser', weight: 3 }, { type: 'Tank', weight: 3 }, { type: 'Shooter', weight: 2 }, { type: 'FastShooter', weight: 3 }, { type: 'TrackingShooter', weight: 2 }, { type: 'Shadow', weight: 3 }, { type: 'Shield', weight: 2 }, { type: 'Healer', weight: 2 }, { type: 'Trapper', weight: 2 }, { type: 'Jumper', weight: 3 }, { type: 'Mage', weight: 2 }, { type: 'Mirage', weight: 2 }, { type: 'Grapper', weight: 2 }] },
    // Vague 18 : Necromancer
    { minWave: 18, types: [{ type: 'Grunt', weight: 1 }, { type: 'FastChaser', weight: 3 }, { type: 'Tank', weight: 3 }, { type: 'Shooter', weight: 2 }, { type: 'FastShooter', weight: 3 }, { type: 'TrackingShooter', weight: 2 }, { type: 'Shadow', weight: 3 }, { type: 'Shield', weight: 2 }, { type: 'Healer', weight: 2 }, { type: 'Trapper', weight: 2 }, { type: 'Jumper', weight: 3 }, { type: 'Mage', weight: 2 }, { type: 'Mirage', weight: 2 }, { type: 'Grapper', weight: 2 }, { type: 'Necromancer', weight: 1 }] },
    // Vague 20 : Summoner
    { minWave: 20, types: [{ type: 'Grunt', weight: 1 }, { type: 'FastChaser', weight: 3 }, { type: 'Tank', weight: 3 }, { type: 'Shooter', weight: 2 }, { type: 'FastShooter', weight: 3 }, { type: 'TrackingShooter', weight: 2 }, { type: 'Shadow', weight: 3 }, { type: 'Shield', weight: 2 }, { type: 'Healer', weight: 2 }, { type: 'Trapper', weight: 2 }, { type: 'Jumper', weight: 3 }, { type: 'Mage', weight: 2 }, { type: 'Mirage', weight: 2 }, { type: 'Grapper', weight: 2 }, { type: 'Necromancer', weight: 2 }, { type: 'Summoner', weight: 1 }] },
    // Vague 25 : BOSS Duke
    { minWave: 25, types: [{ type: 'FastChaser', weight: 3 }, { type: 'Tank', weight: 3 }, { type: 'Shooter', weight: 2 }, { type: 'FastShooter', weight: 3 }, { type: 'TrackingShooter', weight: 2 }, { type: 'Shadow', weight: 3 }, { type: 'Shield', weight: 2 }, { type: 'Healer', weight: 2 }, { type: 'Trapper', weight: 2 }, { type: 'Jumper', weight: 3 }, { type: 'Mage', weight: 2 }, { type: 'Mirage', weight: 2 }, { type: 'Grapper', weight: 2 }, { type: 'Necromancer', weight: 2 }, { type: 'Summoner', weight: 2 }, { type: 'Duke', weight: 1 }] }
]);

/**
 * Trouve la configuration de la vague pour le niveau actuel
 * @param {number} waveNumber - Le numéro de la vague
 * @returns {Object} La configuration de la vague avec les types et leurs probabilités
 */
export function getWaveConfig(waveNumber) {
    let currentConfig = WAVE_TABLE[0];
    
    for (const config of WAVE_TABLE) {
        if (waveNumber >= config.minWave) {
            currentConfig = config;
        } else {
            // Puisque la table est triée par minWave, on peut s'arrêter dès qu'on dépasse
            break;
        }
    }
    
    return currentConfig;
}

/**
 * Choisit un type d'ennemi aléatoire selon les probabilités de la vague
 * @param {number} waveNumber - Le numéro de la vague
 * @returns {Function} La classe (constructeur) de l'ennemi
 */
export function pickRandomEnemyType(waveNumber) {
    const waveConfig = getWaveConfig(waveNumber);
    
    // Calcul de la somme totale des poids
    const totalWeight = waveConfig.types.reduce((sum, item) => sum + item.weight, 0);
    
    // Sélection aléatoire basée sur le poids
    let randomValue = Math.random() * totalWeight;
    
    for (const item of waveConfig.types) {
        if (randomValue < item.weight) {
            return ENEMY_TYPES[item.type];
        }
        randomValue -= item.weight;
    }
    
    // Fallback de sécurité, retourne l'ennemi de base
    return ENEMY_TYPES.Grunt;
}

/**
 * Crée une instance d'un ennemi spécifique
 * @param {string} typeKey - La clé de l'ennemi (ex: 'Tank', 'Shooter')
 * @param {number} x - Position X
 * @param {number} y - Position Y
 * @param {Object} gameManager - Référence au game manager
 * @returns {Object} Une instance de l'ennemi demandé
 */
export function createEnemy(typeKey, x, y, gameManager) {
    const EnemyClass = ENEMY_TYPES[typeKey];
    
    if (!EnemyClass) {
        console.warn(`Type d'ennemi "${typeKey}" introuvable, création d'un Grunt par défaut.`);
        return new ENEMY_TYPES.Grunt(x, y, gameManager);
    }
    
    return new EnemyClass(x, y, gameManager);
}
