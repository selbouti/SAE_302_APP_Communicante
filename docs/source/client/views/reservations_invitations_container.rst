Conteneur Réservations et Invitations
=====================================

La vue ``ReservationsInvitationsContainer`` regroupe dans une seule interface
les fonctionnalités liées aux réservations et aux invitations.

Elle s’appuie sur un système d’onglets afin de séparer clairement les deux
types d’informations tout en conservant une navigation fluide.

Organisation de l’interface
----------------------------

L’interface est composée de :

- Un composant ``QTabWidget`` contenant deux onglets
- Un onglet **Réservations** affichant les réservations de l’utilisateur
- Un onglet **Invitations** affichant les invitations reçues ou envoyées
- Un bouton **Retour** permettant de revenir à la vue d’accueil

Chargement des données
----------------------

La méthode ``load`` permet de rafraîchir simultanément :

- la vue des réservations
- la vue des invitations

Cela garantit que les données affichées sont à jour à chaque affichage
de la page.

Classe ReservationsInvitationsContainer
---------------------------------------

.. autoclass:: client.views.reservations_invitations_container.ReservationsInvitationsContainer
   :members:
   :undoc-members:
   :show-inheritance:
