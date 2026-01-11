Profil utilisateur
==================

.. module:: client.views.profile_view

Cette vue permet à l’utilisateur de consulter et modifier
ses informations personnelles depuis l’interface graphique.


Classe ProfileView
------------------

.. autoclass:: ProfileView
   :members:
   :undoc-members:
   :show-inheritance:


Fonctionnalités principales
---------------------------

La vue Profil offre les fonctionnalités suivantes :

- affichage des informations personnelles de l’utilisateur
- activation d’un mode édition
- sauvegarde des modifications via l’API serveur
- navigation vers la gestion de la voiture associée au compte


Chargement des données
----------------------

Les données du profil sont chargées depuis le serveur via
le contrôleur client ``ProfileController``.

La méthode ``load`` est appelée automatiquement lorsque la vue
est affichée.


Mode édition
------------

Par défaut, les champs du profil sont en lecture seule.
Le bouton *Modifier* active le mode édition, permettant
à l’utilisateur de mettre à jour ses informations.


Sauvegarde
----------

Les modifications sont envoyées au serveur à l’aide de la méthode
``update_profile`` du contrôleur.

Un message de confirmation ou d’erreur est affiché selon
la réponse du serveur.


Navigation
----------

La vue permet également :

- l’accès à la gestion de la voiture
- le retour à l’écran d’accueil
