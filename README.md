### Projet 3 - Logiciel de gestion de tournoi d'échec
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Status](https://img.shields.io/badge/status-En%20développement-yellow)

> Logiciel en ligne de commande permettant de gérer des tournois d'échecs : joueurs, rondes, résultats et classement final.


---

## À propos du projet

Ce projet est développé dans le cadre d'une formation de développeur Python.
Il s'agit d'une application de gestion de tournois d'échecs, en architecture **MVC** (Modèle - Vue - Contrôleur), avec stockage local au format JSON. L'application fonctionne en **console (CLI)**.

---

##  Fonctionnalités

- Création d'un nouveau tournoi avec nom, lieu, date, nombre de rounds
- Ajout et gestion des joueurs (prénom, nom, date de naissance, ID d'échec)
- Lancement automatique des rondes et génération des appariements suisses
- Saisie des résultats (victoire, nul, défaite)
- Mise à jour du classement des joueurs
- Affichage des classements et historiques

---

##  Technologies utilisées

- Python 3.12
- Architecture MVC
- JSON (sérialisation des données)
- `flake8` pour la qualité du code

---

## Installation

### Prérequis
*python 3.12*
- installation: 
```bash
winget install "Python 3.12"
```
- soit:
https://www.python.org/downloads/release/python-3120/

### 1. Cloner ce dépôt
```bash
git clone git@github.com:C-eorl/Chest_tournament.git
cd Chest_tournament
```
### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # sous Windows : venv\Scripts\activate
```
### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
### 4. Lancer le script
```bash
python main.py
```

### Qualité et linting

Le projet suit les standards de style PEP8 via flake8.
Générer un rapport avec flake8-html :
```bash
flake8 --format=html --htmldir=flake-report
```