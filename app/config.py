import os


class Config:
    # Configuration de la base de données
    secret_key = 'pGdSYS0UmTYh3CaKH5dhwAFK1kPx8dsZqcucFZ2HeAbIDys1ff'
    SECRET_KEY = os.environ.get('SECRET_KEY') or secret_key  # clé secrète pour Flask
    database_url = 'mysql+pymysql://adrien:adrien@localhost/bibliotheque_perso_and_family'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://adrien:adrien@localhost/bibliotheque_perso_and_family'  # configuration de la base de données MySQL
    # Configuration de la clé secrète pour les sessions sécurisées
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # désactiver le suivi des modifications de la base de données
