Contrôleur d’authentification
=============================

.. module:: serveur.controllers.auth_controller
   :synopsis: Gestion de l’authentification utilisateur

Ce module expose les routes liées à l’**authentification des utilisateurs**
côté serveur.

Il permet :

- la réception des identifiants utilisateur
- la vérification des informations via le modèle utilisateur
- la gestion des erreurs d’authentification
- le retour des données utilisateur en cas de succès

Route de connexion
------------------

.. autofunction:: login
