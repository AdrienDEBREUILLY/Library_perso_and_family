#!/bin/bash

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
export FLASK_APP=run.py
flask db init
flask db migrate
flask db upgrade

# Lancer l'application
flask run