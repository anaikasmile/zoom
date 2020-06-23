# Description du pojet
Cette plateforme web est une application d'envoi et de suivi de colis

# Versions
Version de l'app: 2.0
Langage: Django 1.10.7
Database: Postgres SQL
Python: 3.6

#Prérequis:
Installer Python 3.6
Installer VirtualEnv =>Creer un environnement virtuel
Installer Django 2.2.13

#Installation
- Cloner le projet sur Github
- Creer votre base de données Postgres et noter les indentifiants de connexion a la base
- Aller dans le fichier de settings de production et au niveau des parametres DB et renseigner les différents parametres de connexion
- Executer la commande pip freeze >> requirements.txt pour installer toutes les app.
- Executer 
python manage.py  makemigrations
python manage.py migrate
python manage.py createsuperuser 


