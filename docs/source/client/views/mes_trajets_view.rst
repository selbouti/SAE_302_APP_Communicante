Mes trajets
===========

.. module:: client.views.mes_trajets_view

Cette vue permet à l’utilisateur de consulter et gérer les trajets
qu’il a créés dans l’application.

Elle offre les fonctionnalités suivantes :

- affichage de la liste des trajets de l’utilisateur
- distinction entre les trajets en mode conducteur et passager
- basculement du mode d’un trajet
- suppression d’un trajet existant


Classe MesTrajetsView
---------------------

.. autoclass:: MesTrajetsView
   :members:
   :undoc-members:
   :show-inheritance:


Fonctionnement général
----------------------

Lors de l’affichage de la vue, la méthode ``showEvent`` est déclenchée
automatiquement afin de charger les trajets depuis l’API serveur.

Les trajets sont affichés sous forme de tableau avec les informations
suivantes :

- lieu de départ
- lieu d’arrivée
- date et heure du trajet
- informations sur le véhicule (si conducteur)
- mode du trajet (conducteur ou passager)
- prix par place
- actions disponibles (changement de mode, suppression)

Les actions sont effectuées via le contrôleur client ``TrajetController``,
qui communique avec l’API REST du serveur.


Actions disponibles
-------------------

**Changer de mode**
    Permet de basculer un trajet entre le mode *conducteur* et *passager*.

**Supprimer**
    Supprime définitivement le trajet sélectionné côté serveur.


Interactions avec le contrôleur
-------------------------------

Cette vue utilise les méthodes suivantes du contrôleur :

- ``TrajetController.lister_trajets``
- ``TrajetController.supprimer_trajet``
- ``TrajetController.basculer_mode``

Ces appels assurent la synchronisation entre l’interface graphique
et les données stockées côté serveur.
