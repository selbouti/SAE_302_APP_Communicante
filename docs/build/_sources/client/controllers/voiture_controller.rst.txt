Contrôleur voiture
==================

.. automodule:: client.controllers.voiture_controller
   :members:
   :undoc-members:
   :show-inheritance:

Présentation
------------

Le ``VoitureController`` est un contrôleur côté client chargé de la
gestion du véhicule associé à un utilisateur.

Il communique exclusivement avec l’API REST du serveur et ne contient
aucune logique métier locale.

Fonctionnalités
---------------

Ce contrôleur permet :

- la récupération de la voiture de l’utilisateur
- l’ajout ou la modification des informations du véhicule
- la suppression du véhicule

Méthodes disponibles
--------------------

- ``get_voiture(user_id)`` : récupère la voiture associée à un utilisateur
- ``save_voiture(user_id, voiture_data)`` : crée ou met à jour une voiture
- ``delete_voiture(user_id)`` : supprime la voiture de l’utilisateur

Validation des données
----------------------

Des assertions sont utilisées pour vérifier :

- le type de l’identifiant utilisateur
- la structure des données du véhicule avant l’envoi à l’API

Position dans l’architecture
----------------------------

Le ``VoitureController`` appartient à la couche **client** :

- Interface graphique PyQt
- Contrôleurs client (API REST)
- Serveur Flask
- Base de données

Cette organisation garantit une séparation claire des responsabilités.
