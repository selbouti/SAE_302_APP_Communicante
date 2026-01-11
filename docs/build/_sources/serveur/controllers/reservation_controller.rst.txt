Contrôleur des réservations
===========================

Ce module définit l’ensemble des points d’entrée de l’API REST
liés à la gestion des **réservations de trajets** dans l’application
de covoiturage.

Il permet notamment :

- de créer une réservation pour un trajet
- de consulter les réservations reçues par un conducteur
- de consulter les réservations effectuées par un passager
- d’accepter ou refuser une réservation
- d’annuler une réservation existante

Les données sont échangées au format **JSON** et les opérations
reposent sur le modèle ``ReservationModel``.

---

.. automodule:: serveur.controllers.reservation_controller
   :members:
   :undoc-members:
   :show-inheritance:
