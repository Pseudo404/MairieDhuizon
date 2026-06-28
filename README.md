# Mairie de Dhuizon — Site web municipal

> **Projet de fin d'année B1 — Projet 0 : Application libre**  
> Application web full-stack développée individuellement sur **6 semaines**, dans le cadre de la validation des acquis en développement web et déploiement.

---

## Table des matières

1. [Contexte et objectifs](#contexte-et-objectifs)
2. [Pourquoi ce projet ?](#pourquoi-ce-projet-)
3. [Public cible et enjeux](#public-cible-et-enjeux)
4. [Fonctionnalités principales](#fonctionnalités-principales)
5. [Conformité au cahier des charges](#conformité-au-cahier-des-charges)
6. [Stack technique et justifications](#stack-technique-et-justifications)
7. [Architecture du projet](#architecture-du-projet)
8. [Sécurité et modération](#sécurité-et-modération)
9. [Installation et lancement en local](#installation-et-lancement-en-local)
10. [Déploiement](#déploiement)
11. [Livrables](#livrables)
12. [Méthodologie de développement](#méthodologie-de-développement)
13. [Difficultés rencontrées](#difficultés-rencontrées)
14. [Liens utiles](#liens-utiles)

---

## Contexte et objectifs

### Contexte pédagogique

Ce projet constitue l'évaluation finale de l'année B1. Il vise à **combiner l'ensemble des compétences acquises** au cours de l'année :

- Gestion de projet et organisation du travail
- Programmation orientée objet (POO)
- Développement front-end (HTML, CSS, JavaScript)
- Développement back-end et gestion de base de données
- UI/UX et accessibilité
- Sécurité web et déploiement

J'ai choisi le **Projet 0 — Application libre**, qui me laisse la liberté de sélectionner un sujet personnel tout en respectant les contraintes fonctionnelles imposées (authentification, gestion de données, tableau de bord, sécurité, etc.).

### Objectif du projet

Concevoir et déployer un **site web officiel pour la commune de Dhuizon** (Loir-et-Cher, Centre-Val de Loire), permettant :

- aux **habitants et visiteurs** de consulter les informations municipales, les services locaux et les actualités ;
- aux **agents et élus de la mairie** de gérer le contenu du site via un panneau d'administration sécurisé.

Le site remplace et modernise une présence web statique ou obsolète, en centralisant l'information communale dans une interface claire, responsive et facilement maintenable.

---

## Pourquoi ce projet ?

La commune de Dhuizon (~1195 habitants) dispose de nombreuses informations dispersées (horaires, associations, commerces, démarches administratives, tourisme local…). Un site municipal structuré répond à un **besoin réel** :

| Problème identifié | Solution apportée |
|---|---|
| Informations difficiles à trouver | Navigation thématique + moteur de recherche global |
| Actualités peu visibles | Section actualités avec publication modérée |
| Horaires souvent obsolètes | Gestion dynamique des horaires (mairie, commerces, services) avec badges ouvert/fermé |
| Contact mairie peu accessible | Formulaire de contact avec envoi d'e-mail et confirmation automatique |
| Mise à jour du site complexe pour les agents | Panneau d'administration CRUD sans compétences techniques |

Ce choix de sujet est **pertinent, concret et ancré dans le territoire**, tout en offrant une complexité technique suffisante pour démontrer la maîtrise des compétences attendues.

---

## Public cible et enjeux

| Public | Besoins |
|---|---|
| **Habitants** | Horaires, démarches, collecte des déchets, école, santé, associations |
| **Visiteurs / touristes** | Patrimoine, hébergements, randonnées, lieux à visiter (Chambord, Sologne…) |
| **Commerçants et entreprises** | Visibilité dans l'annuaire local |
| **Agents municipaux** | Mise à jour autonome du contenu, statistiques de fréquentation |
| **Élus** | Consultation des comptes-rendus de conseil municipal |

**Enjeux principaux :** accessibilité multi-appareils, fiabilité des informations, sécurité des accès administrateurs, et simplicité d'utilisation pour des utilisateurs non techniques.

---

## Fonctionnalités principales

### Partie publique (visiteurs)

- **Page d'accueil** : actualités récentes, liens rapides, présentation de la commune
- **Découvrir Dhuizon** : histoire, patrimoine, galerie photos
- **Vie pratique** : école, santé, pharmacie, crèche, médiathèque, transports, déchets, démarches administratives
- **Loisirs** : équipements sportifs, centre de loisirs, chemins de randonnée
- **Tourisme** : lieux à visiter, cabanes Coocou, hébergements, gîtes
- **Entreprises & commerces** : annuaires avec horaires d'ouverture
- **Conseil municipal** : élus, conseil des jeunes, comptes-rendus, prochaine séance
- **Vie associative** : liste et fiches détaillées des associations
- **Actualités** : articles avec système de publication
- **Contact** : formulaire avec notification e-mail (Brevo) et accusé de réception
- **Recherche globale** : recherche intelligente sur l'ensemble du contenu du site
- **Pages légales** : politique de confidentialité, bandeau cookies (RGPD)

### Partie administration (`/control-panel/`)

- **Authentification sécurisée** des comptes agents (sessions Django)
- **Tableau de bord** : statistiques de visites (jour, mois, visiteurs uniques, temps passé)
- **Gestion CRUD** de plus de 40 entités (actualités, horaires, associations, commerces…)
- **Modération** : publication / dépublication des actualités
- **Journal d'audit** : traçabilité des modifications (qui, quoi, quand)
- **Gestion des comptes administrateurs** (Super Admin)
- **Restriction par IP** pour l'accès au panneau d'administration
- **Export CSV** des statistiques de fréquentation

---

## Conformité au cahier des charges

Le cahier des charges du Projet 0 impose plusieurs exigences fonctionnelles. Voici comment elles sont couvertes :

| Exigence | Implémentation |
|---|---|
| **Authentification** | Connexion des agents municipaux via `/login-admin/`. Gestion des comptes administrateurs (création, suppression, rôles Super Admin / Admin) |
| **Gestion des données** | CRUD complet sur toutes les entités métier (actualités, commerces, associations, horaires…) via le panneau d'administration |
| **Interaction utilisateur** | Formulaire de contact, moteur de recherche, navigation thématique, badges horaires dynamiques |
| **Notifications et alertes** | Messages flash Django (`messages framework`), e-mails de confirmation au contact, retours visuels après actions CRUD |
| **Modération et sécurité** | Publication modérée des actualités, rate limiting, restriction IP admin, chiffrement des mots de passe (PBKDF2 Django), protection CSRF |
| **Tableau de bord** | `/control-panel/stats/` avec graphiques et export (csv) |

> **Note :** Contrairement à un site communautaire ou e-commerce, un site municipal ne nécessite pas d'inscription publique. L'authentification est réservée aux agents de la mairie, ce qui est cohérent avec le cas d'usage réel.

---

## Stack technique et justifications

| Couche | Technologie | Version | Justification |
|---|---|---|---|
| **Back-end** | Python / Django | 6.0.5 | Framework mature, architecture MVT (équivalent MVC), ORM puissant, sécurité intégrée (CSRF, sessions, hashage mots de passe) |
| **Base de données** | SQLite (dev) / PostgreSQL (prod) | — | SQLite pour le développement local ; PostgreSQL prévu en production pour la robustesse et la scalabilité |
| **Front-end** | HTML5 + Django Templates | — | Rendu côté serveur (SSR) : SEO favorable, cohérence avec l'architecture Django |
| **CSS** | Tailwind CSS (django-tailwind) | 4.x | Utility-first, responsive natif, cohérence visuelle, compilation intégrée au projet Django |
| **JavaScript** | Vanilla JS | — | Interactivité légère (statistiques temps réel, tracking, cookies) sans sur-ingénierie |
| **E-mails** | Brevo (API) | — | Envoi transactionnel fiable pour le formulaire de contact |
| **Serveur WSGI** | Gunicorn | 26.0.0 | Serveur de production standard pour Django |
| **Sécurité** | django-ratelimit | 4.1.0 | Protection contre le spam et les abus (formulaire contact, login admin) |
| **Images** | Pillow | 12.2.0 | Traitement et validation des uploads d'images |
| **Config** | python-dotenv | 1.2.2 | Gestion sécurisée des variables d'environnement (.env) |

### Pourquoi Django plutôt que PHP ?

Le cahier des charges cite PHP comme exemple, mais autorise explicitement le **Projet 0** à utiliser le framework de son choix. Django a été retenu car :

- Il respecte une **architecture MVC/MVT cohérente** (modèles, vues, templates, URLs)
- L'**ORM** facilite la modélisation des ~40 entités du site municipal
- La **POO** est au cœur du framework (modèles, middlewares, formulaires)
- Le **système d'authentification** et de sessions est natif et sécurisé
- L'écosystème Python est adapté au déploiement sur serveur Linux (Gunicorn + Nginx)

---

## Architecture du projet

```
mairieDhuizon/
├── core/                    # Application principale Django
│   ├── models.py            # ~40 modèles ORM (BaseModel, horaires, contenus…)
│   ├── views.py             # Vues publiques + panneau admin + API JSON
│   ├── forms.py             # Formulaires (contact, login, CRUD)
│   ├── panel.py             # Configuration du menu d'administration
│   ├── security.py          # Restriction IP, utilitaires sécurité
│   ├── middleware.py        # Tracking visites, protection /admin/
│   ├── permissions.py       # Rôles Super Admin / Admin
│   ├── recherche.py         # Moteur de recherche multi-modèles
│   ├── opening_hours.py     # Logique horaires ouvert/fermé
│   ├── email_service.py     # Envoi e-mails via Brevo
│   ├── uploads.py           # Service de fichiers (PDF, images)
│   └── migrations/          # Migrations base de données
├── mairieDhuizon/           # Configuration Django
│   ├── settings.py          # Paramètres (sécurité prod, BDD, e-mails)
│   ├── urls.py              # Routes de l'application
│   └── wsgi.py              # Point d'entrée WSGI
├── templates/               # Templates HTML (pages publiques + panel admin)
├── theme/                   # Application Tailwind CSS
├── assets/                  # Fichiers statiques (images, logos)
├── media/                   # Fichiers uploadés (PDF, photos)
├── manage.py
├── .env                     # Variables d'environnement (non versionné)
└── db.sqlite3               # Base de données locale
```

### Schéma simplifié

```
┌─────────────┐    HTTP      ┌──────────────────┐     ORM      ┌────────────┐
│  Navigateur │ ◄──────────► │  Django (views)  │ ◄──────────► │  SQLite /  │
│  (HTML/CSS/ │              │  + Middlewares   │              │ PostgreSQL │
│   JS)       │              │  + Templates     │              └────────────┘
└─────────────┘              └────────┬─────────┘
                                      │
                             ┌────────▼─────────┐
                             │ Services externes│
                             │ (Brevo e-mails)  │
                             └──────────────────┘
```

### Modèles de données principaux

Le fichier `core/models.py` contient une architecture normalisée avec :

- **`BaseModel`** : champs `created_at` / `updated_at` partagés
- **`BaseSchedule`** : gestion réutilisable des horaires hebdomadaires
- **Entités métier** : `News`, `Association`, `Commerce`, `Entreprise`, `School`, `Pharmacy`, `Randonnee`, etc.
- **Administration** : `AdminAccount`, `AdminAllowedIP`, `AuditLog`, `PageView`

---

## Sécurité et modération

| Mesure | Détail |
|---|---|
| **Mots de passe** | Hashage PBKDF2 via le système d'auth Django |
| **Sessions** | Cookies HttpOnly, SameSite=Lax, expiration 2 h en production |
| **HTTPS** | Redirection forcée, HSTS, cookies Secure en production |
| **CSRF** | Token sur tous les formulaires POST |
| **Rate limiting** | Limitation par IP (contact : 5/min, login : 4/min, pages : 30/min) |
| **Restriction IP admin** | Whitelist d'adresses IP pour `/control-panel/` et `/login-admin/` |
| **Uploads** | Validation type/taille des fichiers (images, PDF) |
| **XSS** | Échappement HTML dans les e-mails, templates Django auto-escape |
| **Audit** | Journal des actions CRUD avec utilisateur, modèle et changements |
| **Modération contenu** | Flag `is_published` sur les actualités |

---

## Installation et lancement en local

### Prérequis

- Python 3.11+
- Git

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/Pseudo404/MairieDhuizon.git
cd MairieDhuizon

# 2. Créer et activer l'environnement virtuel
python -m venv venv
# Windows :
venv\Scripts\activate

# 3. Installer les dépendances
pip install Django django-tailwind django-ratelimit python-dotenv pillow gunicorn sib-api-v3-sdk

# 4. Configurer les variables d'environnement
# Copier .env et adapter les valeurs (voir section ci-dessous)

# 5. Appliquer les migrations
python manage.py migrate

# 6. Créer un super-utilisateur (accès admin)
python manage.py createsuperuser

# 7. Compiler Tailwind CSS
python manage.py tailwind install
python manage.py tailwind build

# 8. Lancer le serveur de développement
python manage.py runserver
```

Le site est accessible sur [http://127.0.0.1:8000](http://127.0.0.1:8000).  
Le panneau d'administration : [http://127.0.0.1:8000/login-admin/](http://127.0.0.1:8000/login-admin/)

### Variables d'environnement (.env)

| Variable | Description |
|---|---|
| `DJANGO_DEBUG` | `True` en dev, `False` en production |
| `DJANGO_SECRET_KEY` | Clé secrète Django (obligatoire en prod) |
| `DJANGO_ALLOWED_HOSTS` | Domaines autorisés (ex : `localhost,127.0.0.1`) |
| `ADMIN_IP_RESTRICTION_ENABLED` | Active la restriction IP pour l'admin |
| `ADMIN_FALLBACK_IPS` | IPs autorisées (séparées par des virgules) |
| `BREVO_API_KEY` | Clé API Brevo pour l'envoi d'e-mails |
| `BREVO_SENDER_EMAIL` | Adresse expéditeur |
| `BREVO_RECIPIENT_EMAIL` | Adresse de réception (mairie) |

---

## Déploiement

Le site est déployé en production sur le domaine **[dhuizon.fr](https://www.dhuizon.fr)**.

Configuration production (`.env.prod`) :

- `DJANGO_DEBUG=False`
- HTTPS forcé (HSTS, cookies sécurisés)
- Restriction IP active pour le panneau admin
- Serveur WSGI Gunicorn derrière un reverse proxy (Nginx)

---

## Livrables

Conformément au cahier des charges du Projet 0 :

| Livrable | Emplacement |
|---|---|
| Code source complet | [GitHub — MairieDhuizon](https://github.com/Pseudo404/MairieDhuizon.git) |
| Export base de données (.sqlite3) | Fichier `db.sqlite3` fourni |
| Documentation utilisateur | Guide d'utilisation fourni avec les livrables |
| Documentation technique | Ce README + commentaires dans le code source |
| Support de soutenance | Support de présentation (slides) fourni + démonstration live |

---

## Méthodologie de développement

Le projet s'est déroulé sur **6 semaines** avec une approche itérative :

| Semaine | Travail réalisé |
|---|---|
| **S1** | Analyse du besoin, réflexions UI/UX, modélisation de la base de données |
| **S2** | Mise en place Django, modèles ORM, pages publiques principales |
| **S3** | Panneau d'administration CRUD, gestion des horaires, uploads |
| **S4** | Recherche, statistiques, e-mails, sécurité (IP, rate limiting, audit) |
| **S5** | Ajouts mineurs, corrections, Tests |
| **S6** | Tests, corrections, présentation à la mairie, préparation soutenance |

**Organisation :**

- Dépôt Git centralisé
- Séparation claire back-end (`core/`) / front-end (`templates/`, `theme/`)
- Variables sensibles externalisées dans `.env`
- Itérations fonctionnelles : chaque page testée avant passage à la suivante

---

## Difficultés rencontrées

| Difficulté | Solution adoptée |
|---|---|
| Gestion complexe des horaires (plusieurs entités, saisons) | Création d'un modèle abstrait `BaseSchedule` + module `opening_hours.py` |
| Sécurisation de l'accès admin sans bloquer les agents en mairie | Système de whitelist IP configurable (BDD + `.env`) avec fallback localhost en dev |
| Panneau admin générique pour ~40 modèles | CRUD dynamique basé sur `modelform_factory` et menu configuré dans `panel.py` |
| Recherche pertinente | Moteur de recherche avec mots-clés par modèle dans `recherche.py` |
| Responsive design cohérent | Tailwind CSS avec approche mobile-first |

---

## Liens utiles

- **Dépôt GitHub :** [https://github.com/Pseudo404/MairieDhuizon](https://github.com/Pseudo404/MairieDhuizon)
- **Site en production (futur) :** [https://www.dhuizon.fr](https://www.dhuizon.fr)
- **Documentation Django :** [https://docs.djangoproject.com](https://docs.djangoproject.com)
- **Documentation Tailwind CSS :** [https://tailwindcss.com/docs](https://tailwindcss.com/docs)

---

## Auteur

Projet réalisé par **Tom CIZEAU** — B1 Développement Web  
École : **CODA_**  
Année scolaire : **2025–2026**

---

*Ce README sert de documentation technique et de support pour la soutenance de 30 minutes (présentation 15 min + questions 10 min + débriefing 5 min).*


> ⚠️ Note de sécurité :
>
> La base de données publiée sur GitHub est uniquement destinée à la démonstration.
> Les comptes utilisateurs présents dans cette version seront remplacés avant la mise en production (identifiants, e-mails et mots de passe).
>
> Aucun compte de production ne sera issu de cette base.