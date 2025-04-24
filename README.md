# TriXel

## Description

Ce projet vise à développer un agent d'apprentissage par renforcement pour le tri des déchets. En utilisant des techniques d'apprentissage par renforcement, nous entraînons un agent à reconnaître et à trier différents types de déchets de manière efficace.

## Fonctionnalités

- Apprentissage par renforcement : Utilisation d'algorithmes de renforcement pour entraîner l'agent.
- Tri des déchets : Capacité à identifier et à trier différents types de déchets.
- Environnement de simulation : Environnement pour tester et améliorer les performances de l'agent.

## Installation

Pour installer et exécuter ce projet localement, suivez ces étapes :

1. Cloner le dépôt :
```
git clone https://github.com/Redart71/trash_sort_rl.git
cd trash_sort_rl
```

2. Configurer l'environnement :
Assurez-vous d'avoir Python 3.x installé. Vous pouvez créer un environnement virtuel pour isoler les dépendances du projet :

```
python -m venv env
# Sur MacOS et Linux
source env/bin/activate  
# Sur Windows
env\Scripts\activate
```

3. Installer les dépendances :

```
pip install -r requirements.txt
```

## Utilisation

* Entraîner l'agent :
```
python train_q_learning.py
```

* Jouer avec l'agent entraîné :
```
python play_with_agent.py
```

* Entraîner un agent aléatoire :
```
python train_random_agent.py
```

## Structure du projet

* assets/ : Contient les ressources nécessaires pour le projet.
* env/ : Environnement virtuel pour les dépendances Python.
* .gitignore : Fichier pour ignorer certains fichiers et dossiers dans le dépôt Git.
* main.py : Script principal pour exécuter le projet.
* play_with_agent.py : Script pour interagir avec l'agent entraîné.
* q_table.npy : Fichier contenant la table Q utilisée par l'agent.
* train_q_learning.py : Script pour entraîner l'agent avec l'algorithme Q-learning.
* train_random_agent.py : Script pour entraîner un agent aléatoire.