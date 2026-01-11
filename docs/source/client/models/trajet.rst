Trajet
======

Présentation
------------

Le modèle ``Trajet`` représente un trajet côté client, principalement
utilisé dans le cadre du matching des trajets.

Il est construit à partir des données retournées par l’API serveur.

Classe Trajet
-------------

.. automodule:: client.models.trajet
   :members:
   :undoc-members:
   :show-inheritance:

Fonctionnalités principales
---------------------------

- Stockage des informations du conducteur
- Gestion des horaires de départ et de retour
- Affichage de la voiture associée
- Calcul et vérification des places disponibles

Règles métier
-------------

La méthode ``est_complet`` permet de vérifier si un trajet
dispose encore de places disponibles pour de nouveaux passagers.
