=======================================================================
Application graphique de co-voiturage
=======================================================================

-------------------------
Cadre et objectif général
-------------------------

Le projet vise à développer une application graphique PyQt client/serveur de co-voiturage entre personnes partant de la même ville et travaillant dans une autre ville avec des emplois du temps généralement différents.
L'application devra permettre à chaque utilisateur :

 * de s'inscrire en renseignant un certain nombre d'informations ainsi que leur emploi du temps sous forme de fichier au format i-calendar
 * d'indiquer pour un jour donné :

    * la liste des voyageurs dont l'horaire de départ et l'heure de retour sont compatibles à 15 min, 30 min, 1h, 2h près
    * la liste des voyageurs dont l'horaire de départ est compatible à 15 min, 30 min, 1h, 2h près
    * le conducteur parmis les voyageurs dont les horaires sont compatibles de manière à ce que le nombre de trajet soit le plus équitable possibles
 * de choisir, s'il y en a une, une solution dans la liste proposée
 * d'afficher une page bilan qui récapitule pour chaque personne le nombre de trajets, les coûts, distances parcourues avec sa voiture et le bilan carbonne


Lors de la création/modification de son compte, chaque utilisateur pourra indiquer les éléments suivants :

* nom, prénom
* login/passwd
* adresse 
* coordonnées GPS
* téléphone
* un fichier d'Emploi Du Temps (EDT) au format ical à charger ou à récupérer suivant un lien indiqué
* nombre de places dans la voiture
* nombre de CV fiscaux
* jours d'indisponibilité de la voiture
* réfléchir à l'architecture de l'application
* coût cumulé estimé des trajets (cf règle de calcul frais réels impôts)
* bilan carbonne



Les étapes principales du projet consistent à :

* réfléchir aux données qui devront transiter du serveur vers les clients et vice-versa

* concevoir et créer une base de données qui permet gérer les données 

* proposer une architecture pour l'application client/serveur

* concevoir un serveur qui aura les fonctionnalités suivantes :

	* création, suppression, modification des comptes des utilisateurs,

	* authentification des utilisateurs,

	* d'effectuer les calculs permettant de proposer les listes de solutions et de mettre à jour les coûts et bilans carbonne

        * de communiquer avec les clients des utilisateurs

* convevoir et programmer le client des utilisateurs

* dessiner les interfaces graphiques client accessibles aux utilisateurs concernant :
 
        * l'authentification
        * la création/modification/suppression de compte
        * le paramétrage du calcul
        * l'affichage des liste de solutions

* programmer l'interface graphique



--------------------------------------------
Environnement de développement et dépôt GIT
--------------------------------------------
Le projet doit :

* utiliser l'outil de gestion de version Git et un IDE de développement Python ;

* être structuré suivant l'arborescence indiquée ci-après

* pouvoir s'exécuter sur le système Linux de la Machine Virtuelle deb12-lxqt du datacenter lors de la démonstration finale ;

* être documenté :

        * description du projet au format restructuredText,
	* commentaires pertinents dans le code (si utile à la compréhension),
	* commentaires des fonctions développées


* comporter un répertoire de test où toutes les fonctions Python développées auront un code de test unitaire


Le projet est rattaché à un dépôt GIT que vous aurez créé sur GitHub et à la livraison de vos codes informatiques. 
Le dépôt **devra absolument** être remis lors de la livraison finale du projet.
Le versionnement étant tracé et daté, il servira pour l'évaluation du travail du groupe et de chaque étudiant.


-----------------------------------
Langages de scripting/programmation
-----------------------------------

Le projet doit utiliser :

* le langage de programmation **Python** (version > 3.10) pour les **codes sources** et **PyQt** pour les projets d'interface graphique




----------------------
Arborescence du projet
----------------------


Votre projet doit :

* être exécuté par le biais d'un script ``nom_projet.py``. Ce script reprendra la structure classique des programmes vue en **R1.07-Fondamentaux de la programmation** et décrite dans le formulaire Python. Il prendra d'éventuels paramètres en arguments. 

* respecter l'arborescence suivante (``PROJETGitHUB`` désigne le répertoire auquel est rattaché votre projet et constitue la base du dépôt local Git) :

   .. code-block:: bash

      PROJETGitHUB
      ├── .git/
      ├── data/
      │   └── ...
      ├── docs/
      │     ├── build/
      │     │    └── html/
      │     └── source/ 
      │    	 ├── index.rst 
      │    	 ├── conf.py 
      │    	 ├── content/ 
      │    	 ├── _static/ 
      │          └── _templates/    
      ├── html/
      │   └── ...
      ├── __init__.py
      ├── nomprojet/
      |    ├── nom_projet.py
      │    └── nom_module_projet.py
      ├── tests/
      │   ├── __init__.py
      │   └── test_nom_module_projet.py  
      ├── .gitignore
      ├── AUTHORS
      │ 
      └── requirements.txt


      
   * ``.git`` le répertoire dédié à Git.
  
   * ``data`` le répertoire dédié à stocker différents fichiers de données récupérées et générées pour les besoin du projet.

   * ``docs`` le répertoire dédié à stocker la documentation du projet au format retructuredText (répertoire généré automatiquement par sphinx-build).

   * ``html`` répertoire contenant le site web statique de présentation des résultats

   * ``__init__.py`` fichier indiquant la version du projet :
	.. code-block:: python
			
		__version__ = '0.1.0'

   * ``nomprojet`` le répertoire dédié aux fichiers source Python développés lors du projet

   * ``tests`` le répertoire dédié aux tests unitaires des fonctions développées dans le projet

   * ``tests/__init__.py`` fichier vide

   * ``.gitignore`` le fichier permettant de configurer Git pour ne pas envoyer sur le dépôt distant les fichiers temporaires 

   * ``AUTHORS`` le fichier indiquant le nom des auteurs et de leurs coordonnées 
          
   * ``requirements.txt`` fichier texte décrivant la version de Python  utilisée et les dépendances du programme python (modules et version des modules Python)
   

.. warning::

   * Les fichiers : ``.gitignore`` commence avec un point.

.. note:: Vous pouvez ajouter au besoin autant de modules que nécessaires, pour structurer votre code, en les stockant à la racine du répertoire ``nomprojet``.

.. note:: 
  Un modèle Modèle Vue Contrôleur (MVC) :doc:`MVC_help` pour structurer le code de l'application est à privilégier

--------------------------------------------
Documentation
--------------------------------------------  
* La documentation générale du projet devra être écrite au format restructuredText. Vous pourrez pour cela vous appuyer sur le logiciel `Sphinx <https://www.sphinx-doc.org/en/master/tutorial/getting-started.html>`_ ;

* Il conviendra d'ajouter des commentaires *doctrings* en début de fonction afin de :

     * préciser ce que fait la fonction,
     * d'indiquer son auteur, ses dates de création et de dernière modification,
     * décrire ses paramètres et le cas échéant leurs types,
     * décrire les bornes d'utilisation de paramètres pour un bon fonctionnement de la fonction et exceptions qui sont suceptibles d'être levées,
     * ce qu'elle retourne
     * donner un exemple d'utilisation

--------------------
Tests unitaires
--------------------

En vous inspirant du TP sur les fonctions de la ressource **R1.07-Fondamentaux de la programmation**, vous devrez écrire un code de test de chaque fonction développée dans le projet.
Celui-ci sera placé dans un programme Python du répertoire ``tests``.