# Open class Room Projet 12
Développez une architecture back-end sécurisée avec Python et SQL.
# Sénario:

Vous travaillez chez Epic Events, une entreprise de conseil et de gestion dans l'événementiel qui répond aux besoins des start-up voulant organiser des « fêtes épiques » . En tant que développeur de logiciels dans le département informatique, vous avez principalement travaillé sur le site Internet vitrine de l'entreprise.L'entreprise souhaite développer un logiciel CRM(Customer Relationship Management) pour améliorer leur travail. Le logiciel CRM permet de collecter et de traiter les données des clients et de leur sévénements, tout en facilitant la communication entre les différents pôles de l'entreprise


<center>

![Logo de Epic Event](img\16903799358611_P12-02.png)


</center>


# Projet : Application CRM Epic Events
1. [Général / Présentation](#Général)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Fonctionnement](#fonctionnement)
5. [License](#licence)


## <a id = Général>Général / Présentation</a>
***
Le logiciel CRM permet de collecter et de traiter les données des clients et de leur sévénements, tout en facilitant la communication entre les différents pôles de l'entreprise. L'application est une application CLI(commande line interace.)



## <a id = technologies>Technologies</a>
***

  ![Python](https://img.shields.io/badge/python_3.10-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 

L'application est developpée sous python et utilise comme moteur de base de donnée PostgreSQL.



* [Python](https://www.python.org/downloads/release/python-31012/) : Version 3.10
* [Type Base de donnée ](https://www.postgresql.org/download//) : PostgeSQL 15.4



## <a id = installation>Installation</a>
***
> **Installation** > Python doit etre instalé sur votre machine.
***
> **Installation** > le moter PostgreSQL, ainsi qu'une base de donnée de donnée (vide) doit etre installé sur votre machine.
***

* [Comment installer une base de donné Postgresql](https://www.postgresql.org/docs/15/tutorial-install.html)

* Lors de l'installation et la création de la base de donné veiller à bien noter les différentes information(type, nom, port mot de passe ,etc) 

### *Telecharger ou cloner les fichiers du repository GITHUB dans le dossier de votre choix, puis deplacer vous dans le dossier "CRM_Epic_Event"*.
***
Toutes les opérations suivantes seront exécutées dans ce répertoire "CRM_Epic_Event".

### _**Création environnement Virtuel**_

Por créer un environnement virtuel, taper dans votre terminal les commandes suivantes : 


> Sous Windows:
> ````commandline
> py -m venv env 
>````

> Sous Unix/Mac:
>````commandline
>python3 -m venv env
>````

### _**Activation environnement Virtuel**_

Pour activer ce dernier, taper les instructions suivantes toujours dans votre terminal :

> Sous Windows:
> ````commandline
> env\scripts\activate
>````

> Sous Unix/Mac:
>````commandline
>source env/bin/activate
>````

Votre terminal affichera la ligne de commande comme ci-dessous, confirmant l'activation de l'environnement virtuel :

````
(venv) PS C:\xxx\xxxx\xxxx\CRM_Epic_Event>
````


###  **_Installation des packages_**

Taper dans votre terminal les commandes suivantes : 

> Sous Windows:
> ````commandline
> py -m pip install -r requirements.txt
>````

> Sous Unix/Mac:
>````commandline
>python3 -m pip install -r requirements.txt
>````


Cette commande permet l'installation de tous les packages nécessaire au fonctionnement de l'application.

### **_Variable d'environnement_**

Ce projet utilise des variables d'environnement afin de stocker notamment les données sensible (mot de passe basse de données , Key sentry , identifiant utilsateur par default, key token).

Vous trouverez dans le dossier CRM_Epic_Event/.env.example_  un exemple de configuration de variables d'environnement utilisée pour ce projet.


## <a id= fonctionnement>Fonctionnement</a>

###  **_1er Lancement_**

Lors du premier lancement une commande specifique doit etre effectuer afin de mettre en place les différentes tables de la bases de données da l'application.
 :

> ````commandline
> alembic uprgade head
>````

Le terminal affichera :

>````commandline
>INFO  [alembic.context] Context class PostgresqlContext.
>INFO  [alembic.context] Will assume transactional DDL.
>INFO  [alembic.context] Running upgrade xxx -> xxxxxx


* Cette commande est seulement à executer lors du premier lancement !!!!

Ensuite taper la commande suivante pour lancer l'aplication CRM:

> ````commandline
> python main.py
>````

le terminal affichera la page de authentification de l' application:
<center>

![Logo de Epic Event](img\authentication.png)

</center>

Aprés vous etre authentifié, vous serrez redirigé vers la home Page de l'aplication. Dés la, il vous suffit de suivre les instructions affichées, afin des réaliser les opérations CRUD sur les différents éléments( Utilisateur, Contract, Clients etc).

***
## <a id = licence>Licence</a>


* [Licence ouverte](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf) : Version 2.0
***
