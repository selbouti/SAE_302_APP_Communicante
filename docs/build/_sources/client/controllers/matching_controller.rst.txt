MatchingController
==================

Le module ``MatchingController`` gère la logique de *matching* côté client.
Il permet à un utilisateur de :

- consulter ses propres trajets,
- rechercher des trajets compatibles,
- effectuer des réservations,
- envoyer des invitations,
- rechercher des conducteurs à l’aide de marges horaires.

Il s’appuie sur les contrôleurs ``ReservationController`` et
``InvitationController`` ainsi que sur le service ``APIService``.

---

Classe MatchingController
-------------------------

.. automodule:: client.controllers.matching_controller
   :members:
   :undoc-members:
   :show-inheritance:
