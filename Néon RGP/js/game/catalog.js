export const HERO_CATALOG = Object.freeze({
    Player: {
        name: 'Héros Classique',
        icon: '🔵',
        summary: 'Combattant équilibré, idéal pour débuter.',
        stats: [
            ['PV', '100'],
            ['Dégâts', '25'],
            ['Vitesse', '5'],
            ['Attaque', 'Projectile']
        ],
        ability: 'Tir automatique sur l\'ennemi le plus proche.'
    },
    Archer: {
        name: 'Archère',
        icon: '🏹',
        summary: 'Rapide et meurtrière, mais plus fragile.',
        stats: [
            ['PV', '80'],
            ['Dégâts', '35'],
            ['Vitesse', '6'],
            ['Attaque', '0,35 s']
        ],
        ability: '10 % de chance critique. Tire plus vite que les autres héros.'
    },
    Tank: {
        name: 'Tank',
        icon: '🛡️',
        summary: 'Résistant, il tient la ligne au cœur des ennemis.',
        stats: [
            ['PV', '120'],
            ['Dégâts', '30'],
            ['Vitesse', '4'],
            ['Portée', '90 px']
        ],
        ability: 'Marteau de zone à courte portée. Impact Sismique ajoute l\'immobilisation.'
    },
    Sniper: {
        name: 'Sniper',
        icon: '🔭',
        summary: 'Tireur lourd capable de traverser plusieurs ennemis.',
        stats: [
            ['PV', '80'],
            ['Dégâts', '45'],
            ['Vitesse', '4'],
            ['Perforation', '1']
        ],
        ability: 'Ses tirs traversent un ennemi. Les améliorations ajoutent guidage et perforation.'
    },
    Mage: {
        name: 'Mage',
        icon: '🔮',
        summary: 'Canalise un rayon de feu de plus en plus dangereux.',
        stats: [
            ['PV', '85'],
            ['Dégâts', '5–50/s'],
            ['Vitesse', '4'],
            ['Portée', '500 px']
        ],
        ability: 'Le laser chauffe sur une même cible : il devient plus rouge, plus large et plus puissant.'
    },
    Stealer: {
        name: 'Stealer',
        icon: '🩸',
        summary: 'Assassin très mobile, fragile mais difficile à achever.',
        stats: [
            ['PV', '50'],
            ['Dégâts', '25'],
            ['Vitesse', '7'],
            ['Vol de vie', '10 %']
        ],
        ability: 'Récupère 10 % des dégâts infligés. Son vol de vie est plafonné à 35 %.'
    }
});

export const ENEMY_CATALOG = Object.freeze({
    Grunt: {
        name: 'Grunt',
        icon: '🔴',
        color: '#ff3b6b',
        summary: 'L\'ennemi de base. Il devient plus dangereux à chaque vague.',
        stats: [
            ['PV', '50'],
            ['Dégâts', '10'],
            ['Vitesse', '2,5'],
            ['Portée', 'Contact']
        ],
        movement: 'Poursuit directement le héros le plus proche.',
        specialAttack: 'Aucune capacité spéciale : il inflige des dégâts au contact.',
        weakness: 'Sensible à l\'étourdissement du marteau du Tank.',
        minWave: 1
    },
    FastChaser: {
        name: 'Chasseur Rapide',
        icon: '⚡',
        color: '#e040fb',
        summary: 'Extrêmement rapide mais très fragile. Il fonce droit sur le joueur.',
        stats: [
            ['PV', '35'],
            ['Dégâts', '15'],
            ['Vitesse', '4,5'],
            ['Portée', 'Contact']
        ],
        movement: 'Sprint en ligne droite vers le héros.',
        specialAttack: 'Aucune — sa vitesse est son arme.',
        weakness: 'Peu de PV : un ou deux tirs suffisent.',
        minWave: 3
    },
    Tank: {
        name: 'Tank',
        icon: '🟣',
        color: '#b388ff',
        summary: 'Ennemi massif et résistant. Lent mais dévastateur au contact.',
        stats: [
            ['PV', '120'],
            ['Dégâts', '20'],
            ['Vitesse', '1,5'],
            ['Taille', 'Grande']
        ],
        movement: 'Avance lentement vers le héros.',
        specialAttack: 'Inflige de gros dégâts au contact.',
        weakness: 'Sa lenteur le rend vulnérable aux tirs à distance.',
        minWave: 5
    },
    Shooter: {
        name: 'Tireur',
        icon: '🔫',
        color: '#00e5ff',
        summary: 'Reste à distance et tire des projectiles sur le héros.',
        stats: [
            ['PV', '40'],
            ['Dégâts', '8'],
            ['Vitesse', '1,8'],
            ['Portée', '210 px']
        ],
        movement: 'S\'approche puis maintient sa distance.',
        specialAttack: 'Tire un projectile toutes les 2 secondes.',
        weakness: 'Fragile au corps à corps.',
        minWave: 5
    },
    FastShooter: {
        name: 'Tireur Rapide',
        icon: '💨',
        color: '#18ffff',
        summary: 'Variante du Tireur avec une cadence de tir accrue.',
        stats: [
            ['PV', '40'],
            ['Dégâts', '5'],
            ['Vitesse', '1,8'],
            ['Cadence', '0,8 s']
        ],
        movement: 'Garde ses distances comme le Tireur.',
        specialAttack: 'Tire un projectile toutes les 0,8 secondes.',
        weakness: 'Dégâts individuels faibles, mais dangereux en groupe.',
        minWave: 11
    },
    TrackingShooter: {
        name: 'Tireur Guidé',
        icon: '🎯',
        color: '#ff9100',
        summary: 'Ses projectiles suivent le joueur en courbe.',
        stats: [
            ['PV', '40'],
            ['Dégâts', '8'],
            ['Vitesse', '1,8'],
            ['Guidage', 'Oui']
        ],
        movement: 'Garde ses distances.',
        specialAttack: 'Projectiles à tête chercheuse.',
        weakness: 'Esquiver ses tirs en faisant des virages serrés.',
        minWave: 13
    },
    Shadow: {
        name: 'Ombre',
        icon: '👤',
        color: '#616161',
        summary: 'Ennemi furtif capable d\'esquiver 25 % des attaques.',
        stats: [
            ['PV', '35'],
            ['Dégâts', '15'],
            ['Vitesse', '2,8'],
            ['Esquive', '25 %']
        ],
        movement: 'Poursuit le héros.',
        specialAttack: '25 % de chance d\'esquiver chaque attaque.',
        weakness: 'Les attaques de zone sont impossibles à esquiver.',
        minWave: 7
    },
    Shield: {
        name: 'Bouclier',
        icon: '🛡️',
        color: '#42a5f5',
        summary: 'Porte un bouclier directionnel qui renvoie les tirs frontaux vers le héros.',
        stats: [
            ['PV', '90'],
            ['Dégâts', '15'],
            ['Vitesse', '1,5'],
            ['Bouclier', 'Renvoi']
        ],
        movement: 'S\'oriente vers le héros en avançant.',
        specialAttack: 'Renvoie les projectiles qui heurtent la face avant du bouclier.',
        weakness: 'Le contourner pour attaquer par derrière.',
        minWave: 7
    },
    Healer: {
        name: 'Soigneur',
        icon: '💚',
        color: '#69f0ae',
        summary: 'Soigne les alliés proches toutes les 2,5 secondes.',
        stats: [
            ['PV', '50'],
            ['Dégâts', '5'],
            ['Vitesse', '1,8'],
            ['Soin', '12 PV']
        ],
        movement: 'Suit l\'allié le plus blessé.',
        specialAttack: 'Pulse de soin de zone (200 px).',
        weakness: 'Le cibler en priorité pour empêcher la régénération.',
        minWave: 9
    },
    Jumper: {
        name: 'Sauteur',
        icon: '🦘',
        color: '#ff6e40',
        summary: 'Reste immobile puis bondit sur la position du héros.',
        stats: [
            ['PV', '60'],
            ['Dégâts', '25'],
            ['Vitesse', 'Saut'],
            ['Rayon', '45 px']
        ],
        movement: 'Immobile → Avertissement → Bond.',
        specialAttack: 'Impact de zone à l\'atterrissage.',
        weakness: 'Se déplacer pendant la phase d\'avertissement.',
        minWave: 11
    },
    Mage: {
        name: 'Mage',
        icon: '🔮',
        color: '#536dfe',
        summary: 'Crée des zones de danger sur la position du héros.',
        stats: [
            ['PV', '90'],
            ['Dégâts', '15/s'],
            ['Vitesse', '1,5'],
            ['Portée', 'Zone']
        ],
        movement: 'S\'approche lentement du héros.',
        specialAttack: 'Invoque une zone magique au sol toutes les 3,5 s.',
        weakness: 'Bouger constamment pour éviter les zones.',
        minWave: 13
    },
    Mirage: {
        name: 'Mirage',
        icon: '🪞',
        color: '#ea80fc',
        summary: 'Tire à distance et peut créer un clone de lui-même.',
        stats: [
            ['PV', '65'],
            ['Dégâts', '12'],
            ['Vitesse', '1,5'],
            ['Clone', 'Après 8 s']
        ],
        movement: 'Garde ses distances (150 px).',
        specialAttack: 'Tire et se clone avec la moitié de ses PV.',
        weakness: 'Détruire le Mirage original avant qu\'il ne se clone.',
        minWave: 15
    },
    Grapper: {
        name: 'Grappeur',
        icon: '🪝',
        color: '#ffab40',
        summary: 'Attire le héros vers lui avec un grappin énergétique.',
        stats: [
            ['PV', '80'],
            ['Dégâts', '10'],
            ['Vitesse', '1,8'],
            ['Portée', '300 px']
        ],
        movement: 'S\'approche du héros.',
        specialAttack: 'Grappin qui tire le héros vers lui (toutes les 4,5 s).',
        weakness: 'Rester hors de portée ou le tuer rapidement.',
        minWave: 15
    },
    Trapper: {
        name: 'Piégeur',
        icon: '🕸️',
        color: '#00e676',
        summary: 'Dépose des pièges au sol qui infligent des dégâts.',
        stats: [
            ['PV', '50'],
            ['Dégâts', '8'],
            ['Vitesse', '2,2'],
            ['Piège', 'Toutes les 5 s']
        ],
        movement: 'Poursuit le héros en semant des pièges.',
        specialAttack: 'Piège au sol qui dure 8 secondes.',
        weakness: 'Éviter ses traces et le tuer à distance.',
        minWave: 9
    },
    Necromancer: {
        name: 'Nécromancien',
        icon: '💀',
        color: '#7c4dff',
        summary: 'Ressuscite les ennemis tombés au combat.',
        stats: [
            ['PV', '70'],
            ['Dégâts', '10'],
            ['Vitesse', '1,5'],
            ['Résurrection', 'Toutes les 4 s']
        ],
        movement: 'Suit le héros lentement.',
        specialAttack: 'Ressuscite un ennemi mort avec 50 % de ses PV.',
        weakness: 'Le tuer en priorité absolue.',
        minWave: 18
    },
    Summoner: {
        name: 'Invocateur',
        icon: '⭐',
        color: '#f50057',
        summary: 'Fuit le héros et invoque des renforts.',
        stats: [
            ['PV', '110'],
            ['Dégâts', '10'],
            ['Vitesse', '1,5'],
            ['Invocation', 'Toutes les 5 s']
        ],
        movement: 'Fuit le héros et reste aux bords.',
        specialAttack: 'Invoque un ennemi aléatoire près de lui.',
        weakness: 'Le poursuivre et l\'éliminer avant qu\'il n\'inonde le terrain.',
        minWave: 20
    },
    Duke: {
        name: 'Duc',
        icon: '👑',
        color: '#ffd740',
        summary: 'Mini-boss imposant. Frappe au sol pour créer des ondes de choc.',
        stats: [
            ['PV', '250'],
            ['Dégâts', '25'],
            ['Vitesse', '1,0'],
            ['Zone', '80 px']
        ],
        movement: 'Avance lentement, tourne sur lui-même.',
        specialAttack: 'Frappe de zone (onde de choc) toutes les 5 s.',
        weakness: 'Rester à distance et tirer sans relâche.',
        minWave: 25
    }
});
