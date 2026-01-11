Application Flask – Serveur Covoiturage
=======================================

Ce module constitue le **point d’entrée principal** de l’API serveur
du projet *Covoiturage*.

Il initialise l’application Flask, configure les extensions nécessaires
et enregistre l’ensemble des **blueprints** correspondant aux différentes
fonctionnalités de l’API.

Initialisation
--------------

Au démarrage, l’application :

- crée une instance Flask
- active le support **CORS** pour permettre les appels depuis le client
- initialise la base de données
- enregistre tous les contrôleurs de l’API

Blueprints enregistrés
----------------------

Les modules suivants sont chargés sous forme de blueprints Flask :

- ``user_controller`` : gestion des utilisateurs (inscription, connexion)
- ``voiture_controller`` : gestion des véhicules
- ``trajet_controller`` : création et gestion des trajets
- ``matching_controller`` : matching conducteur / passager
- ``reservation_controller`` : gestion des réservations
- ``invitation_controller`` : gestion des invitations
- ``profile_controller_api`` : consultation et modification du profil

Configuration serveur
---------------------

- Adresse : ``127.0.0.1``
- Port : ``5000``
- Mode debug : activé (développement)

Génération de la documentation
-------------------------------

La documentation est générée automatiquement à partir des **docstrings
en anglais** présentes dans le code Python, à l’aide de **Sphinx**.

.. automodule:: serveur.app
   :members:
   :undoc-members:
   :show-inheritance:
