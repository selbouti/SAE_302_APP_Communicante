MatchingView
============

La classe ``MatchingView`` permet à un utilisateur de rechercher et
d’interagir avec des trajets compatibles avec les siens.

Elle constitue l’interface principale de la fonctionnalité de *matching*
de l’application **Covoiturage Daily**.

---

Fonctionnalités principales
---------------------------

Cette vue permet à l’utilisateur de :

- sélectionner l’un de ses trajets
- afficher les trajets compatibles
- réserver une place sur un trajet compatible
- inviter un autre utilisateur
- effectuer une recherche avancée avec marges horaires

---

Sélection du trajet
-------------------

Un menu déroulant permet de choisir un trajet personnel.
Une fois sélectionné, les informations suivantes sont affichées :

- date du trajet
- heure de départ
- heure de retour

Ces informations servent de base au matching.

---

Affichage des trajets compatibles
---------------------------------

Les trajets compatibles sont affichés dans un tableau contenant :

- le conducteur
- le point de départ
- la destination
- les horaires
- le véhicule
- le prix par place
- le nombre de places disponibles
- une action (réserver ou inviter)

Le type d’action dépend du mode de recherche.

---

Recherche avec marges horaires
------------------------------

Un mode avancé permet de rechercher des conducteurs compatibles
en appliquant des marges horaires sur :

- l’heure de départ
- l’heure de retour

Le système recommande automatiquement le conducteur ayant
le moins de trajets réalisés.

---

Actions utilisateur
-------------------

Selon le contexte, l’utilisateur peut :

- réserver une place sur un trajet
- envoyer une invitation à un autre utilisateur
- confirmer une réservation issue d’une recherche avec marges

Des messages de confirmation ou d’erreur sont affichés
via des boîtes de dialogue.

---

Intégration avec le contrôleur
------------------------------

La vue repose sur le ``MatchingController`` pour :

- charger les trajets personnels
- récupérer les trajets compatibles
- créer des réservations
- envoyer des invitations
- effectuer des recherches avec marges

---

Documentation automatique
-------------------------

.. automodule:: client.views.matching_view
   :members:
   :undoc-members:
   :show-inheritance:
