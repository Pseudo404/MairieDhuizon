import { ENEMY_TYPES, createEnemy } from '../Enemy/enemyRegistry.js';
import { Player } from '../Player/player.js';
import { overrideContext, clearScreen } from './canvas.js';
import { GameManager } from '../game/gameManager.js';

export class BestiaryPreview {
    constructor() {
        this.canvas = document.getElementById('bestiary-preview');
        this.ctx = this.canvas.getContext('2d');
        this.animationId = null;
        this.currentEnemyType = null;
        
        // On utilise un vrai GameManager mais on va surcharger certaines choses
        // pour éviter qu'il n'interagisse avec le jeu principal.
        this.mockPlayer = new Player(this.canvas.width / 2, this.canvas.height / 2);
        this.mockPlayer.updateHUD = () => {};
        
        this.game = new GameManager(this.mockPlayer);
        // On empêche le game manager de spawner des vagues
        this.game.startWave = () => {};
        this.previewPlayerDied = false;
        this.game.endGame = () => { this.previewPlayerDied = true; };
        
        this.sceneTimer = 0;
        this.lastTime = performance.now();
    }

    start(enemyType) {
        this.currentEnemyType = enemyType;
        this.canvas.style.display = 'block';
        
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        this.resetScene();
        this.lastTime = performance.now();
        this.loop();
    }

    stop() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        this.canvas.style.display = 'none';
        overrideContext(null, null);
    }

    resetScene() {
        this.sceneTimer = 0;
        this.previewPlayerDied = false;
        this.game.start(); // Reset les tableaux du GameManager
        this.game.isPlaying = true;
        this.game.waveActive = false; // Pas de vagues
        
        this.mockPlayer.x = 50;
        this.mockPlayer.y = this.canvas.height / 2;
        this.mockPlayer.hp = this.mockPlayer.maxHp;
        this.mockPlayer.hitTimer = 0;
        this.mockPlayer.hitCooldown = 0;
        this.mockPlayer.lastAttack = Infinity; // Ne tire pas
        
        const enemyX = this.canvas.width - 50;
        const enemyY = this.canvas.height / 2;

        let enemy = createEnemy(this.currentEnemyType, enemyX, enemyY, this.game);
        this.game.enemies.push(enemy);

        // Mises en scène spécifiques
        if (this.currentEnemyType === 'Necromancer') {
            // Le cadavre est relevé dès le début : le héros le prend alors
            // pour cible, ce qui rend la résurrection lisible dans l'aperçu.
            this.game.corpses.push({ x: this.canvas.width / 2, y: this.canvas.height / 2, type: 'Grunt' });
            this.mockPlayer.lastAttack = 0;
            this.mockPlayer.attackCooldown = 350;
        } else if (this.currentEnemyType === 'Shield') {
            // Le joueur est placé face au bouclier et tire : chaque impact
            // frontal doit revenir vers lui pour illustrer le renvoi.
            this.mockPlayer.lastAttack = 0;
            this.mockPlayer.attackCooldown = 650;
        } else if (this.currentEnemyType === 'Shadow') {
            // Réglages limités à la prévisualisation : l'Ombre avance assez
            // lentement pour que ses esquives soient visibles avant de gagner.
            enemy.speed = 0.65;
            enemy.maxHp = 220;
            enemy.hp = enemy.maxHp;
            this.mockPlayer.lastAttack = 0;
            this.mockPlayer.attackCooldown = 420;

            // Une esquive sur les deux premiers tirs de chaque série de trois
            // rend la capacité compréhensible sans modifier les probabilités
            // de l'Ombre durant une vraie partie.
            let previewShots = 0;
            const receiveDamage = enemy.takeDamage.bind(enemy);
            enemy.dodgeChance = 0;
            enemy.takeDamage = (amount) => {
                previewShots++;
                if (previewShots % 3 !== 0) {
                    enemy.dodgeFlash = 180;
                    return;
                }
                receiveDamage(amount);
            };
        } else if (this.currentEnemyType === 'Healer') {
            // Le Tireur reste immobile afin que le soin et ses tirs soient
            // faciles à lire dans la petite scène.
            const shooter = createEnemy('Shooter', enemyX - 50, enemyY + 20, this.game);
            shooter.hp = 8;
            shooter.speed = 0;
            shooter.damage = 20;
            shooter.shootCooldown = 700;
            this.game.enemies.push(shooter);
        } else if (['Shooter', 'FastShooter', 'TrackingShooter', 'Mirage'].includes(this.currentEnemyType)) {
            this.mockPlayer.x = 40;
        } else if (this.currentEnemyType === 'Summoner') {
            this.mockPlayer.x = this.canvas.width / 2;
            enemy.x = this.canvas.width - 30;
        } else if (this.currentEnemyType === 'Trapper') {
            this.mockPlayer.x = 20;
        }
    }

    loop() {
        const now = performance.now();
        const dt = now - this.lastTime;
        this.lastTime = now;

        this.sceneTimer += dt;

        this.updateAI();

        // 1. Définir le contexte de rendu sur notre canvas de preview
        overrideContext(this.canvas, this.ctx);

        // 2. Mettre à jour la logique avec un faux appel au joueur
        // On sauvegarde temporairement la vraie update du joueur
        const originalPlayerUpdate = this.mockPlayer.update;
        // Le héros reste immobile, mais ses compteurs de dégâts doivent
        // continuer à avancer : sinon son délai d'impact reste figé après
        // le premier coup et il devient involontairement invincible.
        this.mockPlayer.update = () => {
            if (this.mockPlayer.hitTimer > 0) this.mockPlayer.hitTimer -= 16.66;
            if (this.mockPlayer.hitCooldown > 0) this.mockPlayer.hitCooldown -= 16.66;
        };
        
        this.game.update();
        
        this.mockPlayer.update = originalPlayerUpdate;

        // Unlike the main game, a death in this isolated scene simply starts
        // the demonstration again and never awards progression credits.
        if (this.previewPlayerDied || this.mockPlayer.hp <= 0) {
            this.resetScene();
            overrideContext(null, null);
            this.animationId = requestAnimationFrame(() => this.loop());
            return;
        }

        // Limiter tout le monde aux bords du petit canvas
        this.mockPlayer.x = Math.max(this.mockPlayer.size, Math.min(this.canvas.width - this.mockPlayer.size, this.mockPlayer.x));
        this.mockPlayer.y = Math.max(this.mockPlayer.size, Math.min(this.canvas.height - this.mockPlayer.size, this.mockPlayer.y));
        for (const e of this.game.enemies) {
            e.x = Math.max(e.size, Math.min(this.canvas.width - e.size, e.x));
            e.y = Math.max(e.size, Math.min(this.canvas.height - e.size, e.y));
        }

        // 3. Dessiner
        this.game.draw();
        this.drawPlayerHealthBar();

        // 4. Restaurer le contexte normal
        overrideContext(null, null);

        this.animationId = requestAnimationFrame(() => this.loop());
    }

    drawPlayerHealthBar() {
        const p = this.mockPlayer;
        const width = 34;
        const height = 5;
        const x = p.x - width / 2;
        const y = Math.max(6, p.y - p.size - 13);
        const healthRatio = Math.max(0, Math.min(1, p.hp / p.maxHp));

        this.ctx.save();
        this.ctx.shadowBlur = 0;
        this.ctx.fillStyle = 'rgba(4, 8, 20, 0.85)';
        this.ctx.fillRect(x - 1, y - 1, width + 2, height + 2);
        this.ctx.fillStyle = '#29334f';
        this.ctx.fillRect(x, y, width, height);
        this.ctx.fillStyle = healthRatio > 0.35 ? '#4ee6c8' : '#ff3b6b';
        this.ctx.fillRect(x, y, width * healthRatio, height);
        this.ctx.restore();
    }

    updateAI() {
        const type = this.currentEnemyType;
        const p = this.mockPlayer;
        const h = this.canvas.height;
        const w = this.canvas.width;

        if (type === 'TrackingShooter') {
            // Mouvement de bas en haut pour montrer le suivi
            p.y = h / 2 + Math.sin(this.sceneTimer / 300) * 60;
        } else if (type === 'Trapper') {
            // Se jette dans les pièges
            if (this.game.traps.length > 0) {
                const target = this.game.traps[0];
                const dx = target.x - p.x;
                const dy = target.y - p.y;
                const dist = Math.hypot(dx, dy);
                if (dist > 5) {
                    p.x += (dx / dist) * 1.5;
                    p.y += (dy / dist) * 1.5;
                }
            } else {
                p.x = 30; p.y = h / 2;
            }
        } else if (['Mage', 'Jumper', 'Duke'].includes(type)) {
            // Esquive de bas en haut
            if (this.sceneTimer > 1500 && this.sceneTimer < 3500) {
                p.y -= 1;
            } else if (this.sceneTimer > 4000) {
                p.y += 1;
            }
        } else if (type === 'Grapper') {
            // Essaie de fuir
            if (p.x > 30) p.x -= 0.5;
        } else if (type === 'Summoner') {
            // S'approche
            p.x += 0.5;
        }
    }
}
