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
Installer Postgres SQL:
- apt-get install postgresql libpq-dev postgresql-client postgresql-client-common
- pip install psycopg2
Creer une base de données 
sudo -u postgres psql
postgres=# CREATE DATABASE dbname;
> CREATE USER username WITH PASSWORD 'password';
ALTER ROLE username SET client_encoding TO 'utf8'; 

https://openclassrooms.com/fr/courses/4425101-deployez-une-application-django/4688553-utilisez-le-serveur-http-nginx

ALTER ROLE username SET default_transaction_isolation TO 'read committed'; 

ALTER ROLE username SET timezone TO 'Asia/Kolkata';
/l lister les bases de données
Installer Django 2.2.13

#Installation
- Cloner le projet sur Github
- Creer votre base de données Postgres et noter les indentifiants de connexion a la base
- Aller dans le fichier de settings de production et au niveau des parametres DB et renseigner les différents parametres de connexion
- Executer la commande pip3 install -r requirements.txt pour installer toutes les app.
- Executer 
python manage.py  makemigrations
python manage.py migrate
python manage.py createsuperuser 

Online
user : zoom  
pwd : n23zoom

pg_ctlcluster 12 main start

Admin django root n23zoom  

source zoomEnv/bin/activate
sudo supervisorctl reread

sudo supervisorctl status 
sudo supervisorctl status
 nano zoom-gunicorn.conf

