import os


class Config:
    # Configuration de la base de données
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key' # clé secrète pour Flask
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://username:password@localhost/bibliotheque_personnelle' # configuration de la base de données MySQL
    # Configuration de la clé secrète pour les sessions sécurisées
    SQLALCHEMY_TRACK_MODIFICATIONS = False # désactiver le suivi des modifications de la base de données
