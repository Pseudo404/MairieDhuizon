import { clearScreen, ctx } from "../screen/canvas.js";
import { Bullet } from "./bullet.js";
import { Enemy } from "../Enemy/enemy.js";
import { applyEffect, EFFECT_TYPES, hasEffect } from "./effects.js";
import { awardRunCredits } from "./progression.js";
import { ENEMY_TYPES, getWaveConfig, pickRandomEnemyType, createEnemy } from "../Enemy/enemyRegistry.js";

// ============================================================
// gameManager.js — Gestionnaire de l'état du jeu
// ============================================================

export class GameManager {
    constructor(player) {
        this.player = player;
        this.enemies = [];
        this.bullets = [];
        this.meleeEffects = [];
        this.laserEffect = null;
        this.isPlaying = false;
        this.isGameOver = false;
        this.onGameOver = null;
        
        // Système de vagues
        this.waveNumber = 1;
        this.enemiesToSpawn = 0;
        this.spawnTimer = 0;
        this.waveActive = false;

        // Nouveaux systèmes pour les ennemis spéciaux
        this.enemyBullets = [];  // Projectiles tirés par les ennemis
        this.hazards = [];       // Zones de danger au sol (mage)
        this.traps = [];         // Pièges au sol (trapper)
        this.corpses = [];       // Cadavres d'ennemis (nécromancien)
        this.grapples = [];      // Liens de grappin (grapper)
    }

    start() {
        this.isPlaying = true;
        this.isGameOver = false;
        this.enemies = [];
        this.bullets = [];
        this.enemyBullets = [];
        this.hazards = [];
        this.traps = [];
        this.corpses = [];
        this.grapples = [];
        this.meleeEffects = [];
        this.laserEffect = null;
        this.startWave(1);
    }

    startWave(num) {
        this.waveNumber = num;
        this.enemiesToSpawn = 5 + (num * 3); // De plus en plus d'ennemis
        this.waveActive = true;
        
        // Mettre à jour l'UI
        const badge = document.getElementById('waveBadge');
        if (badge) badge.innerText = `VAGUE ${this.waveNumber}`;
    }

    pause() {
        this.isPlaying = false;
    }

    resume() {
        this.isPlaying = true;
    }

    stop() {
        this.isPlaying = false;
    }

    endGame() {
        // Empêche qu'une collision restante déclenche plusieurs fois la défaite.
        if (this.isGameOver) return;

        this.isPlaying = false;
        this.isGameOver = true;
        this.waveActive = false;
        const rewards = awardRunCredits(this.waveNumber, this.player.score);

        if (this.onGameOver) {
            this.onGameOver({
                wave: this.waveNumber,
                score: this.player.score,
                level: this.player.level,
                creditsEarned: rewards.earned,
                totalCredits: rewards.total
            });
        }
    }

    spawnEnemy(enemy) {
        this.enemies.push(enemy);
    }

    // Tire sur l'ennemi le plus proche
    autoShoot() {
        if (this.player.attackStyle === "laser") {
            this.useLaser(16.66);
            return;
        }

        const now = Date.now();
        if (now - this.player.lastAttack < this.player.attackCooldown) return;

        if (this.player.attackStyle === "hammer") {
            this.useHammer(now);
            return;
        }

        // Trouver l'ennemi le plus proche
        let nearest = null;
        let minDist = Infinity;

        for (let enemy of this.enemies) {
            const dx = enemy.x - this.player.x;
            const dy = enemy.y - this.player.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            // Portée infinie ou limite ? Disons max 500px
            if (dist < minDist && dist < this.player.range) {
                minDist = dist;
                nearest = enemy;
            }
        }

        if (nearest) {
            // Tirer vers l'ennemi
            const dx = nearest.x - this.player.x;
            const dy = nearest.y - this.player.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            const dirX = dx / dist;
            const dirY = dy / dist;

            const isCritical = Math.random() < (this.player.critChance || 0);
            const bulletDamage = isCritical ? this.player.damage * 2 : this.player.damage;

            // Les projectiles critiques sont dorés et infligent le double de dégâts.
            const bullet = new Bullet(
                this.player.x, 
                this.player.y, 
                dirX, 
                dirY, 
                10, // speed
                bulletDamage,
                isCritical ? "#ffcf5c" : this.player.color,
                isCritical ? 6 : 4,
                isCritical
            );
            bullet.remainingPierces = this.player.piercing || 0;
            bullet.homingStrength = this.player.followBullet || 0;
            this.bullets.push(bullet);

            this.player.lastAttack = now;
        }
    }

    useLaser(elapsedMs) {
        let target = null;
        let closestDistance = Infinity;
        for (const enemy of this.enemies) {
            const distance = Math.hypot(enemy.x - this.player.x, enemy.y - this.player.y);
            if (distance < closestDistance && distance <= this.player.range) {
                target = enemy;
                closestDistance = distance;
            }
        }

        // Le rayon suit toujours l'ennemi le plus proche. Changer de cible
        // interrompt la chauffe : les dégâts repartent alors de leur minimum.
        if (target !== this.player.laserTarget) {
            this.player.laserHeat = 0;
            this.player.laserTarget = target;
        }

        if (!target) {
            this.laserEffect = null;
            return;
        }

        this.player.laserHeat = Math.min(
            1,
            this.player.laserHeat + this.player.laserHeatRate * (elapsedMs / 1000)
        );
        const minDamage = Math.min(this.player.damage, this.player.maxDamage);
        const damagePerSecond = minDamage
            + (this.player.maxDamage - minDamage) * this.player.laserHeat;
        target.takeDamage(damagePerSecond * (elapsedMs / 1000));
        this.laserEffect = { target, heat: this.player.laserHeat };

        if (target.hp <= 0) {
            this.handleEnemyDeath(target, this.enemies.indexOf(target));
            this.player.laserTarget = null;
            this.player.laserHeat = 0;
            this.laserEffect = null;
        }
    }

    applyLifeSteal(damage) {
        if (!this.player.lifeSteal || this.player.hp >= this.player.maxHp) return;
        const heal = damage * this.player.lifeSteal;
        this.player.hp = Math.min(this.player.maxHp, this.player.hp + heal);
    }

    guideBullet(bullet) {
        if (bullet.homingStrength <= 0) return;

        let nearest = null;
        let shortestDistance = Infinity;
        for (const enemy of this.enemies) {
            if (bullet.hitEnemies.has(enemy)) continue;
            const dx = enemy.x - bullet.x;
            const dy = enemy.y - bullet.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < shortestDistance) {
                nearest = enemy;
                shortestDistance = distance;
            }
        }
        if (!nearest || shortestDistance <= 0) return;

        const targetX = (nearest.x - bullet.x) / shortestDistance;
        const targetY = (nearest.y - bullet.y) / shortestDistance;
        bullet.dirX += (targetX - bullet.dirX) * bullet.homingStrength;
        bullet.dirY += (targetY - bullet.dirY) * bullet.homingStrength;

        const directionLength = Math.hypot(bullet.dirX, bullet.dirY);
        bullet.dirX /= directionLength;
        bullet.dirY /= directionLength;
    }

    // Attaque de zone du Tank : frappe et immobilise les ennemis proches.
    useHammer(now) {
        let hitAtLeastOneEnemy = false;

        for (let index = this.enemies.length - 1; index >= 0; index--) {
            const enemy = this.enemies[index];
            const dx = enemy.x - this.player.x;
            const dy = enemy.y - this.player.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance > this.player.range + enemy.size) continue;

            hitAtLeastOneEnemy = true;
            enemy.takeDamage(this.player.damage);

            if (enemy.hp <= 0) {
                this.handleEnemyDeath(enemy, index);
            } else if (this.player.hammerStunDuration > 0) {
                applyEffect(enemy, EFFECT_TYPES.STUN, this.player.hammerStunDuration);
            }
        }

        if (hitAtLeastOneEnemy) {
            this.player.lastAttack = now;
            this.meleeEffects.push({
                x: this.player.x,
                y: this.player.y,
                maxRadius: this.player.range,
                duration: 180,
                remaining: 180
            });
        }
    }

    // Gestion centralisée de la mort d'un ennemi
    handleEnemyDeath(enemy, index) {
        // Stocker le cadavre pour le nécromancien
        this.corpses.push({ x: enemy.x, y: enemy.y, type: enemy.constructor.name });
        // Limiter les cadavres en mémoire
        if (this.corpses.length > 20) this.corpses.shift();

        this.enemies.splice(index, 1);
        this.player.gainXp(20);
    }

    updateMeleeEffects() {
        for (let index = this.meleeEffects.length - 1; index >= 0; index--) {
            const effect = this.meleeEffects[index];
            effect.remaining -= 16.66;
            if (effect.remaining <= 0) this.meleeEffects.splice(index, 1);
        }
    }

    // ============================================================
    // Mise à jour des projectiles ennemis
    // ============================================================
    updateEnemyBullets() {
        for (let i = this.enemyBullets.length - 1; i >= 0; i--) {
            const b = this.enemyBullets[i];

            // Guidage (tracking bullets)
            if (b.tracking && this.player) {
                const dx = this.player.x - b.x;
                const dy = this.player.y - b.y;
                const dist = Math.hypot(dx, dy);
                if (dist > 0) {
                    const targetDirX = dx / dist;
                    const targetDirY = dy / dist;
                    b.dirX += (targetDirX - b.dirX) * (b.trackTurnRate || 0.04);
                    b.dirY += (targetDirY - b.dirY) * (b.trackTurnRate || 0.04);
                    const len = Math.hypot(b.dirX, b.dirY);
                    b.dirX /= len;
                    b.dirY /= len;
                }
            }

            b.x += b.dirX * b.speed;
            b.y += b.dirY * b.speed;
            b.lifetime--;

            // Collision avec le joueur
            const dx = b.x - this.player.x;
            const dy = b.y - this.player.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < b.radius + this.player.size) {
                const wasHit = this.player.takeDamage(b.damage);
                this.enemyBullets.splice(i, 1);

                if (wasHit && this.player.hp <= 0) {
                    this.endGame();
                    return;
                }
                continue;
            }

            // Hors écran ou durée expirée
            if (b.lifetime <= 0 || b.x < -50 || b.x > window.innerWidth + 50 ||
                b.y < -50 || b.y > window.innerHeight + 50) {
                this.enemyBullets.splice(i, 1);
            }
        }
    }

    // ============================================================
    // Mise à jour des zones de danger (mage)
    // ============================================================
    updateHazards() {
        for (let i = this.hazards.length - 1; i >= 0; i--) {
            const h = this.hazards[i];
            h.timer += 16.66;

            // Expansion du rayon
            const progress = Math.min(1, h.timer / 300);
            h.radius = h.maxRadius * progress;

            // Dégâts au joueur dans la zone
            const dx = this.player.x - h.x;
            const dy = this.player.y - h.y;
            if (Math.sqrt(dx * dx + dy * dy) < h.radius + this.player.size) {
                // Dégâts par tick (framerate ~60fps)
                const wasHit = this.player.takeDamage(h.damage * (16.66 / 1000));
                if (wasHit && this.player.hp <= 0) {
                    this.endGame();
                    return;
                }
            }

            if (h.timer >= h.duration) {
                this.hazards.splice(i, 1);
            }
        }
    }

    // ============================================================
    // Mise à jour des pièges (trapper)
    // ============================================================
    updateTraps() {
        for (let i = this.traps.length - 1; i >= 0; i--) {
            const t = this.traps[i];
            t.life -= 16.66;

            // Collision joueur
            const dx = this.player.x - t.x;
            const dy = this.player.y - t.y;
            if (Math.sqrt(dx * dx + dy * dy) < t.radius + this.player.size) {
                const wasHit = this.player.takeDamage(t.damage * (16.66 / 1000));
                if (wasHit && this.player.hp <= 0) {
                    this.endGame();
                    return;
                }
            }

            if (t.life <= 0) {
                this.traps.splice(i, 1);
            }
        }
    }

    // ============================================================
    // Mise à jour des grappins
    // ============================================================
    updateGrapples() {
        for (let i = this.grapples.length - 1; i >= 0; i--) {
            const g = this.grapples[i];
            g.life -= 16.66;

            if (g.life <= 0 || !g.source || g.source.hp <= 0) {
                this.grapples.splice(i, 1);
                continue;
            }

            // Tirer le joueur vers la source
            if (g.targetPlayer) {
                const dx = g.source.x - this.player.x;
                const dy = g.source.y - this.player.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist > 0) {
                    this.player.x += (dx / dist) * g.pullSpeed;
                    this.player.y += (dy / dist) * g.pullSpeed;
                }
            }
        }
    }

    update() {
        if (!this.isPlaying) return;

        this.updateMeleeEffects();

        // Gestion du spawn progressif des ennemis
        if (this.waveActive) {
            this.spawnTimer -= 16.66;
            if (this.spawnTimer <= 0 && this.enemiesToSpawn > 0) {
                // Spawn sur les bords de l'écran
                let x = Math.random() > 0.5 ? -20 : window.innerWidth + 20;
                let y = Math.random() * window.innerHeight;
                
                // Choisir le type d'ennemi selon la vague via le registre
                const EnemyClass = pickRandomEnemyType(this.waveNumber);
                const newEnemy = new EnemyClass(x, y, this);

                // Scaling des stats selon la vague
                const waveScale = 1 + (this.waveNumber - 1) * 0.12;
                newEnemy.maxHp = Math.floor(newEnemy.maxHp * waveScale);
                newEnemy.hp = newEnemy.maxHp;
                newEnemy.speed = newEnemy.speed + (this.waveNumber * 0.08);
                
                this.enemies.push(newEnemy);

                this.enemiesToSpawn--;
                this.spawnTimer = Math.max(200, 1000 - (this.waveNumber * 50)); // De plus en plus rapide
            }

            // Vérifier si la vague est terminée
            if (this.enemiesToSpawn <= 0 && this.enemies.length === 0) {
                this.startWave(this.waveNumber + 1);
            }
        }

        // 1. Mise à jour du joueur
        this.player.update();

        // 2. Tir automatique
        this.autoShoot();

        // 3. Mise à jour des projectiles du joueur
        for (let i = this.bullets.length - 1; i >= 0; i--) {
            let b = this.bullets[i];
            this.guideBullet(b);
            b.update();

            // Vérifier la collision avec les ennemis
            let removeBullet = false;
            for (let j = this.enemies.length - 1; j >= 0; j--) {
                let e = this.enemies[j];
                if (b.hitEnemies.has(e)) continue;
                const dx = b.x - e.x;
                const dy = b.y - e.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < b.radius + e.size) {
                    // Le Bouclier renvoie les tirs qui frappent sa face avant.
                    // Le projectile change alors d'équipe et peut blesser le joueur.
                    if (typeof e.reflectBullet === 'function' && e.reflectBullet(b)) {
                        this.bullets.splice(i, 1);
                        this.enemyBullets.push({
                            x: b.x,
                            y: b.y,
                            dirX: b.dirX,
                            dirY: b.dirY,
                            speed: b.speed,
                            damage: b.damage,
                            radius: b.radius,
                            color: '#8fe9ff',
                            lifetime: b.lifetime,
                            reflected: true
                        });
                        removeBullet = true;
                        break;
                    }

                    // Touché !
                    e.takeDamage(b.damage);
                    this.applyLifeSteal(b.damage);
                    if (b.isCritical) {
                        applyEffect(e, EFFECT_TYPES.CRITICAL, 220);
                    }
                    b.hitEnemies.add(e);

                    // Si l'ennemi meurt
                    if (e.hp <= 0) {
                        this.handleEnemyDeath(e, j);
                    }

                    if (b.remainingPierces > 0) {
                        b.remainingPierces--;
                    } else {
                        removeBullet = true;
                        break;
                    }
                }
            }

            // Supprimer le projectile s'il a touché ou s'il est mort (lifetime)
            if ((removeBullet || b.lifetime <= 0) && this.bullets[i] === b) {
                this.bullets.splice(i, 1);
            }
        }

        // 4. Mise à jour des ennemis & collision joueur
        for (let i = this.enemies.length - 1; i >= 0; i--) {
            const enemy = this.enemies[i];
            enemy.update(this.player);

            // Un ennemi étourdi reste sur place et ne peut pas attaquer.
            if (hasEffect(enemy, EFFECT_TYPES.STUN)) continue;

            // Vérifier la collision joueur/ennemi
            const dx = enemy.x - this.player.x;
            const dy = enemy.y - this.player.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            // Si collision, le joueur prend des dégâts
            if (dist < enemy.size + this.player.size) {
                const wasHit = this.player.takeDamage(enemy.damage);

                // Les dégâts ont bien été appliqués : terminer immédiatement la partie
                // lorsque les PV atteignent zéro.
                if (wasHit && this.player.hp <= 0) {
                    this.endGame();
                    return;
                }
                
                // Petit recul (Knockback) basique du joueur
                if (this.player.invincibleTimer === 1000) { // Juste au moment de l'impact
                    this.player.x += (dx / dist) * -20;
                    this.player.y += (dy / dist) * -20;
                }
            }
        }

        // 5. Mise à jour des systèmes spéciaux
        this.updateEnemyBullets();
        this.updateHazards();
        this.updateTraps();
        this.updateGrapples();
    }

    draw() {
        clearScreen();
        
        if (!this.isPlaying && this.enemies.length === 0) return;

        // Dessiner les pièges au sol
        this.drawTraps();

        // Dessiner les zones de danger
        this.drawHazards();

        for (let b of this.bullets) {
            b.draw();
        }

        // Dessiner les projectiles ennemis
        this.drawEnemyBullets();

        for (let enemy of this.enemies) {
            enemy.draw();
        }

        // Dessiner les grappins
        this.drawGrapples();

        this.drawLaser();
        this.drawMeleeEffects();
        
        this.player.draw();
    }

    // ============================================================
    // Rendu des projectiles ennemis
    // ============================================================
    drawEnemyBullets() {
        for (const b of this.enemyBullets) {
            ctx.save();
            ctx.fillStyle = b.color || '#ff3b6b';
            ctx.shadowBlur = 12;
            ctx.shadowColor = b.color || '#ff3b6b';
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
            ctx.fill();

            // Indicateur de tracking
            if (b.tracking) {
                ctx.strokeStyle = b.color || '#ff9100';
                ctx.lineWidth = 1;
                ctx.globalAlpha = 0.4;
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.radius + 4, 0, Math.PI * 2);
                ctx.stroke();
            }

            ctx.restore();
        }
    }

    // ============================================================
    // Rendu des zones de danger
    // ============================================================
    drawHazards() {
        for (const h of this.hazards) {
            const alpha = Math.max(0, 1 - h.timer / h.duration);
            const color = h.color || '#536dfe';

            ctx.save();
            ctx.globalAlpha = alpha * 0.25;
            ctx.fillStyle = color;
            ctx.shadowBlur = 20;
            ctx.shadowColor = color;
            ctx.beginPath();
            ctx.arc(h.x, h.y, h.radius, 0, Math.PI * 2);
            ctx.fill();

            // Contour
            ctx.globalAlpha = alpha * 0.6;
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.restore();
        }
    }

    // ============================================================
    // Rendu des pièges
    // ============================================================
    drawTraps() {
        for (const t of this.traps) {
            const alpha = Math.max(0.15, t.life / 8000);
            const color = t.color || '#00e676';

            ctx.save();
            ctx.globalAlpha = alpha * 0.35;
            ctx.fillStyle = color;
            ctx.shadowBlur = 10;
            ctx.shadowColor = color;
            ctx.beginPath();

            // Forme étoilée
            const spikes = 4;
            for (let s = 0; s < spikes * 2; s++) {
                const angle = (s * Math.PI) / spikes + (t.life / 200);
                const r = s % 2 === 0 ? t.radius : t.radius * 0.5;
                const px = t.x + Math.cos(angle) * r;
                const py = t.y + Math.sin(angle) * r;
                if (s === 0) ctx.moveTo(px, py);
                else ctx.lineTo(px, py);
            }
            ctx.closePath();
            ctx.fill();

            ctx.globalAlpha = alpha * 0.7;
            ctx.strokeStyle = color;
            ctx.lineWidth = 1.5;
            ctx.stroke();
            ctx.restore();
        }
    }

    // ============================================================
    // Rendu des grappins
    // ============================================================
    drawGrapples() {
        for (const g of this.grapples) {
            if (!g.source || g.source.hp <= 0) continue;

            const target = g.targetPlayer ? this.player : null;
            if (!target) continue;

            const alpha = Math.max(0, g.life / 800);

            ctx.save();
            ctx.globalAlpha = alpha;
            ctx.strokeStyle = g.source.color || '#ffab40';
            ctx.lineWidth = 2;
            ctx.shadowBlur = 8;
            ctx.shadowColor = g.source.color || '#ffab40';
            ctx.setLineDash([8, 6]);
            ctx.beginPath();
            ctx.moveTo(g.source.x, g.source.y);
            ctx.lineTo(target.x, target.y);
            ctx.stroke();
            ctx.setLineDash([]);
            ctx.restore();
        }
    }

    drawLaser() {
        if (!this.laserEffect) return;

        const { target, heat } = this.laserEffect;
        const width = 2 + heat * 9;
        const green = Math.round(80 * (1 - heat));
        const blue = Math.round(105 * (1 - heat));
        const color = `rgb(255, ${green}, ${blue})`;

        ctx.save();
        ctx.strokeStyle = color;
        ctx.lineWidth = width;
        ctx.shadowBlur = 12 + heat * 26;
        ctx.shadowColor = color;
        ctx.beginPath();
        ctx.moveTo(this.player.x, this.player.y);
        ctx.lineTo(target.x, target.y);
        ctx.stroke();

        ctx.fillStyle = "#fff0f0";
        ctx.beginPath();
        ctx.arc(target.x, target.y, 3 + heat * 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    drawMeleeEffects() {
        for (const effect of this.meleeEffects) {
            const progress = 1 - effect.remaining / effect.duration;
            const radius = 16 + (effect.maxRadius - 16) * progress;
            const opacity = Math.max(0, 1 - progress);

            ctx.save();
            ctx.strokeStyle = `rgba(56, 214, 200, ${opacity})`;
            ctx.fillStyle = `rgba(56, 214, 200, ${opacity * 0.12})`;
            ctx.lineWidth = 3 - progress * 2;
            ctx.shadowBlur = 18;
            ctx.shadowColor = "#38d6c8";
            ctx.beginPath();
            ctx.arc(effect.x, effect.y, radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
            ctx.restore();
        }
    }
}
