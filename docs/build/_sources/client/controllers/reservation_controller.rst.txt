Contrôleur des réservations
===========================

.. automodule:: client.controllers.reservation_controller
   :members:
   :undoc-members:
   :show-inheritance:

Présentation
------------

Le ``ReservationController`` est un contrôleur côté client chargé de la
gestion des réservations de trajets dans l’application de covoiturage.

Il assure la communication entre l’interface graphique PyQt et l’API REST
du serveur pour toutes les opérations liées aux réservations.



Responsabilités du contrôleur
-----------------------------

Le contrôleur permet notamment de :

- créer une réservation pour un trajet donné
- récupérer les réservations reçues par un conducteur
- récupérer les réservations effectuées par un passager
- accepter ou refuser une réservation
- annuler une réservation existante

Fonctionnement général
----------------------

Les méthodes du contrôleur :

- envoient des requêtes HTTP à l’API via ``APIService``
- interprètent les réponses du serveur
- transforment les données reçues en objets ``Reservation`` lorsque nécessaire
- renvoient des messages de succès ou d’erreur exploitables par la vue

Méthodes disponibles
--------------------

- ``creer_reservation(trajet_id, passager_id, places)``
- ``get_reservations_recues(user_id)``
- ``get_reservations_faites(user_id)``
- ``accepter_reservation(reservation_id)``
- ``refuser_reservation(reservation_id)``
- ``annuler_reservation(reservation_id)``

Gestion des erreurs
-------------------

Les erreurs de communication avec l’API ou les réponses inattendues
sont signalées par :

- un code de statut HTTP
- un message d’erreur explicite renvoyé au client

Cela permet à l’interface graphique d’informer clairement l’utilisateur
en cas d’échec d’une opération.

Place dans l’architecture
-------------------------

Le ``ReservationController`` s’inscrit dans une architecture
**client / serveur** :

- côté client : contrôleur léger sans logique métier lourde
- côté serveur : validation, persistance et règles métier

Cette séparation garantit une meilleure maintenabilité et évolutivité
de l’application.
