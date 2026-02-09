#  Système de Gestion de Stock & Traçabilité

!Version
!Python
!MySQL
!License

Une solution backend robuste conçue pour les structures solidaires, permettant une gestion rigoureuse du matériel informatique, une catégorisation dynamique et une traçabilité complète des mouvements de stock.

---

## Contexte du Projet

Dans un environnement où la gestion des ressources matérielles est critique (type structure solidaire Simplon), ce projet répond à un besoin double : **optimiser la visibilité du stock en temps réel** et **sécuriser les actifs** via un historique immuable des transactions.

L'application implémente une logique métier relationnelle multi-tables pour lier produits, catégories et utilisateurs, assurant ainsi l'intégrité des données et la responsabilité des actions (entrées/sorties).

## Fonctionnalités Clés

- **Gestion Centralisée des Catégories** : Création, listage et suppression de catégories (ex: Informatique, Mobilier, Papeterie).
- **Catalogue Produits Structuré** : Enregistrement des produits avec association obligatoire à une catégorie pour une organisation optimale.
- **Mouvements de Stock Intelligents** :
  - Gestion des Entrées/Sorties.
  - Mise à jour atomique des quantités en stock.
  - Historisation automatique de chaque opération (Date, Utilisateur, Type de mouvement).
- **Reporting & Traçabilité** :
  - Visualisation des produits par catégorie.
  - Historique détaillé des transactions (Audit log).
- **Système d'Alerte** : Détection proactive des ruptures de stock (seuil critique < 5 unités).

## Architecture Technique

Le projet repose sur une architecture MVC simplifiée (Modèle-Vue-Contrôleur) au sein d'un script CLI, interagissant avec une base de données relationnelle MySQL.

### Modèles de Données
L'application s'appuie sur 4 entités principales :
1.  **CATEGORIES** : Nomenclature des types de produits.
2.  **PRODUITS** : Inventaire physique avec état du stock.
3.  **UTILISATEURS** : Acteurs effectuant les mouvements.
4.  **TRANSACTIONS** : Table de liaison historisant les flux.  

Cette section présente les différentes étapes de la modélisation de la base de données. les etape sont dans le dossier `/images/`.

#### Modèle Conceptuel de Données (MCD)
Le MCD représente les entités principales du système et leurs relations.

!Modèle Conceptuel de Données

#### Modèle Logique de Données (MLD)
Le MLD traduit le MCD en un schéma relationnel, définissant les tables et les clés étrangères.

!Modèle Logique de Données

#### Modèle Physique de Données (MPD)
Le MPD est l'implémentation concrète du MLD pour le SGBD MySQL. Le script de création est disponible dans la section Initialisation de la Base de Données.

!Modèle Physique de Données

## Installation et Configuration

### Prérequis

*   Python 3.x
*   Serveur MySQL (local ou distant)
*   Pip (Gestionnaire de paquets Python)

### 1. Clonage du dépôt

```bash
git clone https://github.com/votre-username/gestion-stock-solidaire.git
cd gestion-stock-solidaire
```

### 2. Installation des dépendances

```bash
pip install mysql-connector-python
```

### 3. Initialisation de la Base de Données

Exécutez le script SQL suivant dans votre client MySQL pour générer la structure nécessaire :

```sql
CREATE DATABASE IF NOT EXISTS GESTION_BOUTIQUE;
USE GESTION_BOUTIQUE;

CREATE TABLE IF NOT EXISTS CATEGORIES (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS PRODUITS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    designation VARCHAR(255) NOT NULL,
    prix DECIMAL(10, 2) NOT NULL,
    stock_actuel INT DEFAULT 0,
    id_categorie INT,
    FOREIGN KEY (id_categorie) REFERENCES CATEGORIES(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS UTILISATEURS (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS TRANSACTIONS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_produit INT,
    id_utilisateur INT,
    quantite INT,
    type_mouvement ENUM('ENTREE', 'SORTIE'),
    date_mouvement DATE,
    FOREIGN KEY (id_produit) REFERENCES PRODUITS(id) ON DELETE CASCADE,
    FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEURS(id_utilisateur)
);  
```

### 4. Configuration

Assurez-vous que les identifiants de connexion dans `main.py` correspondent à votre configuration MySQL locale.

## 👤 Auteur

**Alphonse Desire Haba** - *Développeur Back-end*
