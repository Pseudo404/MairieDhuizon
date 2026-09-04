// ============================================================
// progression.js — Sauvegarde locale des héros et des crédits
// ============================================================

const STORAGE_KEY = 'neon-rpg-progression-v1';

export const HEROES = Object.freeze({
    Player: { name: 'Héros Classique', price: 0 },
    Archer: { name: 'Archère', price: 150 },
    Tank: { name: 'Tank', price: 300 },
    Sniper: { name: 'Sniper', price: 450 },
    Mage: { name: 'Mage', price: 550 },
    Stealer: { name: 'Stealer', price: 600 }
});

const DEFAULT_PROGRESSION = {
    credits: 0,
    unlockedHeroes: ['Player'],
    selectedHero: 'Player'
};

function readProgression() {
    try {
        const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
        if (!saved) return { ...DEFAULT_PROGRESSION };

        const unlockedHeroes = Array.isArray(saved.unlockedHeroes)
            ? saved.unlockedHeroes.filter(hero => HEROES[hero])
            : ['Player'];
        if (!unlockedHeroes.includes('Player')) unlockedHeroes.push('Player');

        const selectedHero = unlockedHeroes.includes(saved.selectedHero)
            ? saved.selectedHero
            : 'Player';

        return {
            credits: Math.max(0, Number(saved.credits) || 0),
            unlockedHeroes,
            selectedHero
        };
    } catch {
        return { ...DEFAULT_PROGRESSION };
    }
}

function writeProgression(progression) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progression));
}

export function getProgression() {
    return readProgression();
}

export function getSelectedHero() {
    return readProgression().selectedHero;
}

export function selectOrUnlockHero(heroId) {
    const hero = HEROES[heroId];
    if (!hero) return { success: false, message: 'Héros introuvable.' };

    const progression = readProgression();

    if (progression.unlockedHeroes.includes(heroId)) {
        progression.selectedHero = heroId;
        writeProgression(progression);
        return { success: true, message: `${hero.name} sélectionné.` };
    }

    if (progression.credits < hero.price) {
        const missingCredits = hero.price - progression.credits;
        return {
            success: false,
            message: `Il te manque ${missingCredits} crédits pour débloquer ${hero.name}.`
        };
    }

    progression.credits -= hero.price;
    progression.unlockedHeroes.push(heroId);
    progression.selectedHero = heroId;
    writeProgression(progression);

    return { success: true, message: `${hero.name} débloqué et sélectionné !` };
}

export function awardRunCredits(wave, score) {
    // La vague est la principale source de récompense ; le score la complète.
    const earned = 25 + Math.max(0, wave - 1) * 25 + Math.floor(score / 20);
    const progression = readProgression();
    progression.credits += earned;
    writeProgression(progression);

    return { earned, total: progression.credits };
}
