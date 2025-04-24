# TriXel

## Description

Ce projet vise à développer un agent d'apprentissage par renforcement pour le tri des déchets. En utilisant des techniques d'apprentissage par renforcement, nous entraînons un agent à reconnaître et à trier différents types de déchets de manière efficace.

<br>

<p align="center">
  <img src="assets/demo.gif" width="700" alt="Démo du projet"/>
</p>

<br>


## Objectifs


* Développer un agent capable de trier efficacement des déchets simulés.
* Comparer les performances de différentes méthodes d'apprentissage par renforcement.
* Fournir un environnement visuel et interactif pour tester et améliorer les algorithmes.

## Environnement de Simulation

### États

Chaque état dans TriXel correspond à un objet TrashObject placé sur une ligne de tri. Cet objet est caractérisé par :

* **name** : nom spécifique de l’objet (ex. : bouteille plastique, journal, verre, etc.).
* **category** : catégorie attendue pour le tri (ex. : Plastique, Papier, Verre, Non recyclable).

L’état est donc défini par l’identité de l’objet courant à trier.

### Objets

Les objets aléatoires générés par TrashObject.generate_random() sont issus de cette liste :

|Nom de l'objet|Catégorie|
|:--------------|:----------|
|bouteille plastique|Plastique|
|carton pizza|Papier|
|journal|Papier|
|papier froissé|Papier|
|verre brisé|Verre|
|canette alu|Non recyclable|
|bouteille de champagne|Verre|
|thé vert|Non recyclable|
|chaussure|Non recyclable|
|livre|Papier|

Chaque objet est accompagné d'une image affichée dans l'interface avec pygame.

### Actions

L’agent peut choisir parmi 5 actions discrètes, correspondant à la poubelle où envoyer le déchet courant :

* Plastique
* Papier
* Verre
* Non recyclable
* Ne rien faire

### Récompenses

Le système de récompense est défini comme suit :

* +1 : si le déchet est placé dans la bonne poubelle.
* -1 : si le déchet est mal trié.
* -0.5 : pour toute autre action ou si aucune action n'est prise.

Ce mécanisme incite l'agent à apprendre des politiques de tri efficaces en maximisant les récompenses cumulées.

## Algorithmes d'Apprentissage

### Q-Learning

Q-learning est un algorithme basé sur une table Q Q(s, a) qui enregistre les récompenses attendues pour chaque couple état/action.

**Formule de mise à jour :**
```
Q(s, a) ← Q(s, a) + α [r + γ max Q(s', a') - Q(s, a)]
```

* **α** : taux d’apprentissage
* **γ** : facteur de discount
* **r** : récompense
* **s'** : état suivant
* **a'** : meilleure action suivante

Idéal pour des environnements simples avec un nombre limité d'états.

### Deep Q-Network (DQN)

Le DQN est une extension du Q-learning qui utilise un réseau de neurones profond pour approximer la fonction Q, permettant de gérer des espaces d'états plus complexes et continus.

Fonctionnement :

1. Utilisation d'un réseau de neurones pour approximer Q(s, a; θ), où θ représente les poids du réseau.

2. Stockage des expériences (s, a, r, s') dans une mémoire tampon (replay buffer).

3. Échantillonnage aléatoire de mini-lots d'expériences pour entraîner le réseau, réduisant la corrélation entre les données.

4. Mise à jour des poids du réseau en minimisant la perte entre les prédictions Q actuelles et les cibles calculées.

## Installation

Pour installer et exécuter ce projet localement, suivez ces étapes :

**1. Cloner le dépôt :**
```
git clone https://github.com/Redart71/trash_sort_rl.git
cd trash_sort_rl
```

**2. Configurer l'environnement :**

Assurez-vous d'avoir Python 3.12.3 installé. Vous pouvez créer un environnement virtuel pour isoler les dépendances du projet :

```
python -m venv env
# Activation sur Unix ou MacOS
source env/bin/activate
# Activation sur Windows
env\Scripts\activate
```

**3. Installer les dépendances :**
```
pip install -r requirements.txt
```

## Utilisation

* **Entraîner l'agent :**
```
python train_q_learning.py
```

* **Jouer avec l'agent entraîné :**
```
python play_with_agent.py
```

* **Entraîner l'agent de manière aléatoire :**
```
python train_random_agent.py
```

## Structure du projet

| Fichier/Dossier | Description |
|:--------------|:-------------|
|assets/ | Ressources graphiques pour les objets|
|env/ | Environnement virtuel (local)|
|.gitignore | Fichiers/dossiers ignorés par Git|
|main.py | Script principal de lancement|
|play_with_agent.py | Interagir avec l’agent entraîné|
|q_table.npy | Table Q sauvegardée pour l’agent Q-learning|
|train_q_learning.py | Entraînement de l’agent avec Q-learning|
|train_random_agent.py | Entraînement d’un agent aléatoire (baseline)|