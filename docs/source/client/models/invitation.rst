Invitation
==========

Présentation
------------

Le modèle ``Invitation`` représente une invitation envoyée ou reçue
par un utilisateur pour rejoindre un trajet.

Il est utilisé côté client après réception des données depuis l’API
et permet d’afficher les informations essentielles liées à une invitation.

Classe Invitation
-----------------

.. automodule:: client.models.invitation
   :members:
   :undoc-members:
   :show-inheritance:

Fonctionnalités principales
---------------------------

- Stockage des informations du trajet (départ, arrivée)
- Identification du passager invité
- Suivi du statut de l’invitation (en attente, acceptée, refusée)
- Méthode d’affichage formatée pour l’interface graphique
