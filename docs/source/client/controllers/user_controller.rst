Contrôleur utilisateur
======================

.. automodule:: client.controllers.user_controller
   :members:
   :undoc-members:
   :show-inheritance:

Présentation
------------

Le ``UserController`` est un contrôleur côté client chargé de toutes les
interactions liées aux utilisateurs avec l’API REST du serveur.

Il permet notamment :

- l’inscription d’un utilisateur
- la connexion
- la récupération du profil
- l’envoi d’un fichier iCalendar
- la mise à jour du calendrier utilisateur

Fonctionnement
--------------

Chaque méthode effectue une requête HTTP via la bibliothèque ``requests``.
Les données sont transmises au serveur au format JSON ou multipart selon
le type de requête.

Des assertions sont utilisées afin de vérifier les types et la validité
des paramètres avant l’envoi des requêtes.

Méthodes principales
--------------------

- ``register(...)`` : inscription d’un utilisateur
- ``login(...)`` : authentification
- ``get_profile(user_id)`` : récupération du profil
- ``upload_icalendar(user_id, file_path)`` : import d’un calendrier
- ``update_calendar(user_id, file_path)`` : mise à jour du calendrier

Place dans l’architecture
-------------------------

Le ``UserController`` fait partie de la couche **contrôleur client** :

- Interface graphique (PyQt)
- Contrôleurs client (API)
- Serveur Flask (logique métier)
- Base de données

Cette séparation garantit une architecture claire et maintenable.
