Contrôleur des trajets
======================

.. automodule:: client.controllers.trajet_controller
   :members:
   :undoc-members:
   :show-inheritance:

Présentation
------------

Le ``TrajetController`` est un contrôleur côté client chargé de la gestion
des trajets (trajets personnels et trajets proposés) dans l’application
de covoiturage.

Il sert d’intermédiaire entre les vues PyQt et l’API REST du serveur,
en centralisant toutes les requêtes liées aux trajets.

Rôle du contrôleur
------------------

Ce contrôleur permet de :

- récupérer les trajets d’un utilisateur
- créer ou mettre à jour un trajet
- supprimer un trajet existant
- changer le mode d’un trajet (conducteur ↔ passager)
- lister l’ensemble des trajets personnels

Les méthodes exposées sont statiques et reposent sur le service
``APIService`` pour communiquer avec le serveur.

Fonctionnement général
----------------------

Chaque méthode :

- construit la requête HTTP appropriée (GET, POST, PUT, DELETE)
- transmet les données nécessaires à l’API
- retourne la réponse du serveur ainsi que le code de statut HTTP

Le contrôleur ne contient aucune logique métier complexe, celle-ci étant
entièrement gérée côté serveur.

Méthodes disponibles
--------------------

- ``get_my_trajet(user_id)``
- ``save_trajet(user_id, data)``
- ``lister_trajets(user_id)``
- ``supprimer_trajet(trajet_id)``
- ``basculer_mode(trajet_id, mode_actuel)``

Changement de mode d’un trajet
-------------------------------

La méthode ``basculer_mode`` permet d’alterner dynamiquement le mode
d’un trajet entre :

- **conducteur**
- **passager**

Ce changement est immédiatement transmis au serveur afin de mettre à jour
l’état du trajet dans la base de données.

Place dans l’architecture
-------------------------

Le ``TrajetController`` fait partie de la couche **contrôleur client**
de l’architecture globale de l’application :

- Interface graphique : vues PyQt
- Contrôleurs : communication API
- Serveur : logique métier et persistance des données

Cette séparation améliore la lisibilité, la maintenance et l’évolutivité
du projet.
