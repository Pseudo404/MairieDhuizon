import {
    getProgression,
    HEROES,
    selectOrUnlockHero
} from "../game/progression.js";
import { ENEMY_CATALOG, HERO_CATALOG } from "../game/catalog.js";

// ============================================================
// uiManager.js — Gestionnaire de l'interface et de la navigation
// ============================================================

export class UIManager {
    constructor(gameManager) {
        this.gameManager = gameManager;
        
        // Tous les écrans (overlays et game)
        this.screens = [
            'screen-main', 
            'screen-heroes', 
            'screen-bestiary', 
            'screen-trophies', 
            'screen-pause', 
            'screen-levelup',
            'screen-gameover',
            'screen-game'
        ];
        
        this.bindEvents();
        this.refreshHeroCards();
        this.showHeroDetails(getProgression().selectedHero);
        this.refreshHomeSummary();
    }

    showScreen(screenId) {
        this.screens.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.classList.add('hidden'); // hidden vient du style.css de base
        });
        
        const target = document.getElementById(screenId);
        if (target) target.classList.remove('hidden');

        // Gérer la preview du bestiaire
        if (this.bestiaryPreview) {
            if (screenId !== 'screen-bestiary') {
                this.bestiaryPreview.stop();
            }
        }
    }

    showGameOver({ wave, score, level, creditsEarned, totalCredits }) {
        const waveText = document.getElementById('gameover-wave');
        const scoreText = document.getElementById('gameover-score');
        const levelText = document.getElementById('gameover-level');
        const earnedCreditsText = document.getElementById('gameover-credits-earned');
        const totalCreditsText = document.getElementById('gameover-credits-total');

        if (waveText) waveText.innerText = `VAGUE ${wave}`;
        if (scoreText) scoreText.innerText = `${score} PTS`;
        if (levelText) levelText.innerText = `NIV ${level}`;
        if (earnedCreditsText) earnedCreditsText.innerText = `+${creditsEarned} ⬡`;
        if (totalCreditsText) totalCreditsText.innerText = `${totalCredits} ⬡`;

        this.refreshHomeSummary();
        this.showScreen('screen-gameover');
    }

    refreshHomeSummary() {
        const progression = getProgression();
        const hero = HERO_CATALOG[progression.selectedHero];
        const creditsText = document.getElementById('home-credits');
        const summary = document.getElementById('home-hero-summary');

        if (creditsText) creditsText.innerText = progression.credits;
        if (!hero || !summary) return;

        summary.innerHTML = `
            <div class="homeHeroLabel">HÉROS SÉLECTIONNÉ</div>
            <div class="homeHeroContent">
                <span class="homeHeroIcon">${hero.icon}</span>
                <div>
                    <div class="homeHeroName">${hero.name}</div>
                    <div class="homeHeroAbility">${hero.ability}</div>
                </div>
            </div>
        `;
    }

    refreshHeroCards(message = '') {
        const progression = getProgression();
        const creditsText = document.getElementById('hero-credits');
        const messageText = document.getElementById('hero-selection-message');

        if (creditsText) creditsText.innerText = `${progression.credits} ⬡`;
        if (messageText) messageText.innerText = message;

        document.querySelectorAll('.hero-select-btn').forEach(card => {
            const heroId = card.getAttribute('data-hero');
            const hero = HEROES[heroId];
            const status = card.querySelector('.heroStatus');
            const unlocked = progression.unlockedHeroes.includes(heroId);
            const selected = progression.selectedHero === heroId;

            card.classList.toggle('lockedHero', !unlocked);
            card.classList.toggle('selectedHero', selected);

            if (!status || !hero) return;
            if (selected) status.innerText = 'SÉLECTIONNÉ';
            else if (unlocked) status.innerText = 'DISPONIBLE';
            else status.innerText = `🔒 DÉBLOQUER — ${hero.price} ⬡`;
        });

        this.showHeroDetails(progression.selectedHero);
        this.refreshHomeSummary();
    }

    showHeroDetails(heroId) {
        const hero = HERO_CATALOG[heroId];
        const container = document.getElementById('hero-detail');
        if (!hero || !container) return;

        container.innerHTML = `
            <div class="detailHeading">${hero.icon} ${hero.name}</div>
            <p class="detailSummary">${hero.summary}</p>
            <div class="detailStats">
                ${hero.stats.map(([label, value]) => `<span><b>${value}</b>${label}</span>`).join('')}
            </div>
            <p class="detailAbility"><b>SPÉCIAL</b> ${hero.ability}</p>
        `;
    }

    showEnemyDetails(enemyId) {
        const enemy = ENEMY_CATALOG[enemyId];
        const container = document.getElementById('bestiary-detail');
        if (!enemy || !container) return;
        
        const previewCanvasHTML = `
            <div class="bestiaryPreviewFrame">
                <span class="bestiaryPreviewLabel">SIMULATION ACTIVE</span>
                <canvas id="bestiary-preview" width="300" height="200"></canvas>
            </div>`;

        container.innerHTML = `
            ${previewCanvasHTML}
            <div class="bestiaryDetailTop">
                <span class="bestiaryEnemyIcon">${enemy.icon}</span>
                <div><div class="detailEyebrow">ENNEMI · VAGUE ${enemy.minWave}</div><div class="detailHeading">${enemy.name}</div></div>
            </div>
            <p class="detailSummary">${enemy.summary}</p>
            <div class="detailStats">
                ${enemy.stats.map(([label, value]) => `<span><b>${value}</b>${label}</span>`).join('')}
            </div>
            <p class="detailAbility"><b>DÉPLACEMENT</b> ${enemy.movement}</p>
            <p class="detailAbility"><b>ATTAQUE</b> ${enemy.specialAttack}</p>
            <p class="detailAbility"><b>FAIBLESSE</b> ${enemy.weakness}</p>
        `;
        
        if (!this.bestiaryPreview) {
            import('./bestiaryPreview.js').then(module => {
                this.bestiaryPreview = new module.BestiaryPreview();
                // Assigner à nouveau le canvas puisque le DOM vient de changer
                this.bestiaryPreview.canvas = document.getElementById('bestiary-preview');
                this.bestiaryPreview.ctx = this.bestiaryPreview.canvas.getContext('2d');
                this.bestiaryPreview.start(enemyId);
            });
        } else {
            this.bestiaryPreview.canvas = document.getElementById('bestiary-preview');
            this.bestiaryPreview.ctx = this.bestiaryPreview.canvas.getContext('2d');
            this.bestiaryPreview.start(enemyId);
        }
    }

    bindEvents() {
        // --- MENU PRINCIPAL ---
        document.getElementById('btn-play').addEventListener('click', () => {
            this.showScreen('screen-game');
            this.gameManager.start();
        });
        
        document.getElementById('btn-heroes').addEventListener('click', () => {
            this.refreshHeroCards();
            this.showScreen('screen-heroes');
        });

        document.querySelectorAll('.hero-select-btn').forEach(card => {
            card.addEventListener('click', () => {
                const result = selectOrUnlockHero(card.getAttribute('data-hero'));
                this.refreshHeroCards(result.message);
            });
        });

        document.querySelectorAll('.bCard[data-enemy]').forEach(card => {
            card.addEventListener('click', () => {
                this.showEnemyDetails(card.getAttribute('data-enemy'));
            });
        });
        
        document.getElementById('btn-bestiary').addEventListener('click', () => {
            this.showScreen('screen-bestiary');
        });
        
        document.getElementById('btn-trophies').addEventListener('click', () => {
            this.showScreen('screen-trophies');
        });

        // --- BOUTONS RETOUR ---
        document.querySelectorAll('.btn-back').forEach(btn => {
            btn.addEventListener('click', () => {
                this.showScreen('screen-main');
            });
        });

        // --- EN JEU (PAUSE) ---
        document.getElementById('btn-pause').addEventListener('click', () => {
            this.showScreen('screen-pause');
            this.gameManager.pause();
        });

        document.getElementById('btn-resume').addEventListener('click', () => {
            this.showScreen('screen-game');
            this.gameManager.resume();
        });

        document.getElementById('btn-quit').addEventListener('click', () => {
            this.showScreen('screen-main');
            this.gameManager.stop();
        });

        // --- FIN DE PARTIE ---
        document.getElementById('btn-restart').addEventListener('click', () => {
            this.showScreen('screen-game');
            this.gameManager.start();
        });

        document.getElementById('btn-gameover-menu').addEventListener('click', () => {
            this.gameManager.stop();
            this.showScreen('screen-main');
        });
    }
}
