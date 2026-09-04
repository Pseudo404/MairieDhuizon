import { applyUpgrade, getAvailableUpgrades } from "./upgrade.js";

// ============================================================
// upgradeManager.js — Affichage et sélection des améliorations
// ============================================================

export class UpgradeManager {
    constructor(gameManager, uiManager) {
        this.gameManager = gameManager;
        this.uiManager = uiManager;

    }

    // Affiche l'écran de Level Up
    triggerLevelUp() {
        this.gameManager.pause(); // Mettre le jeu en pause
        this.uiManager.showScreen('screen-levelup');
        
        const container = document.getElementById('perk-container');
        container.innerHTML = '';

        // Obtenir le nom de la classe du héros actuel
        const currentHeroClass = this.gameManager.player.constructor.name;

        // Filtrer la banque
        const availableUpgrades = getAvailableUpgrades(currentHeroClass);

        // Tirer 3 améliorations aléatoires (sans doublon si possible)
        const choices = this.getRandomUpgrades(availableUpgrades, 3);

        choices.forEach(upgrade => {
            const card = document.createElement('div');
            card.className = 'perkCard';
            card.innerHTML = `
                <div class="perkIcon">${upgrade.icon}</div>
                <div>
                    <div class="perkName">${upgrade.name}</div>
                    <div class="perkDesc">${upgrade.desc}</div>
                </div>
            `;
            
            card.addEventListener('click', () => {
                // L'effet est défini et centralisé dans upgrade.js.
                applyUpgrade(upgrade, this.gameManager.player);
                
                // Cacher l'écran et reprendre
                this.uiManager.showScreen('screen-game');
                this.gameManager.resume();
            });

            container.appendChild(card);
        });
    }

    // Fonction utilitaire pour tirer N éléments aléatoires
    getRandomUpgrades(pool, count) {
        const shuffled = [...pool].sort(() => 0.5 - Math.random());
        return shuffled.slice(0, count);
    }
}
