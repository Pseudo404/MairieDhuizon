import { initInput } from "./js/game/input.js";
import { canvas } from "./js/screen/canvas.js";
import { Player } from "./js/Player/player.js";
import { Archer } from "./js/Player/archer.js";
import { Tank } from "./js/Player/tank.js";
import { Sniper } from "./js/Player/sniper.js";
import { Mage } from "./js/Player/heros/mage.js";
import { Stealer } from "./js/Player/stealer.js";
import { Enemy } from "./js/Enemy/enemy.js";
import { GameManager } from "./js/game/gameManager.js";
import { UIManager } from "./js/screen/uiManager.js";
import { UpgradeManager } from "./js/game/upgradeManager.js";
import { getSelectedHero } from "./js/game/progression.js";

// ============================================================
// main.js — Point d'entrée principal du jeu
// ============================================================

// 1. Initialiser les contrôles
initInput();

// Variables globales de l'état
let game = null;
let ui = null;
let upgradeManager = null;

// Fonction pour démarrer/redémarrer une vraie partie
function startGame() {
    const selectedHeroClass = getSelectedHero();

    // Choisir la classe selon la sélection
    let player;
    if (selectedHeroClass === "Archer") {
        player = new Archer(canvas.width / 2, canvas.height / 2);
    } else if (selectedHeroClass === "Tank") {
        player = new Tank(canvas.width / 2, canvas.height / 2);
    } else if (selectedHeroClass === "Sniper") {
        player = new Sniper(canvas.width / 2, canvas.height / 2);
    } else if (selectedHeroClass === "Mage") {
        player = new Mage(canvas.width / 2, canvas.height / 2);
    } else if (selectedHeroClass === "Stealer") {
        player = new Stealer(canvas.width / 2, canvas.height / 2);
    } else {
        player = new Player(canvas.width / 2, canvas.height / 2);
    }

    // Créer ou remplacer le GameManager
    game = new GameManager(player);

    // Initialiser le système d'amélioration
    upgradeManager = new UpgradeManager(game, ui);
    
    // Connecter l'événement de Level Up
    player.onLevelUp = () => {
        upgradeManager.triggerLevelUp();
    };

    // Connecter la fin de partie au nouvel écran de défaite.
    game.onGameOver = (stats) => {
        ui.showGameOver(stats);
    };

    // Lancer la première vague
    game.start();
}

// Initialiser l'interface utilisateur
ui = new UIManager({ start: startGame, pause: () => game?.pause(), resume: () => game?.resume(), stop: () => game?.stop() });

// ============================================================
// BOUCLE PRINCIPALE (GAME LOOP)
// ============================================================
function loop() {
    if (game) {
        // Mettre à jour la logique du jeu
        game.update();
        
        // Dessiner
        game.draw();
    }
    
    requestAnimationFrame(loop);
}

// Lancer la boucle d'affichage (même si on est dans le menu)
loop();
