Disponibilités utilisateur
==========================

Présentation
------------

La vue ``DisponibiliteView`` permet à un utilisateur de consulter et de
générer ses disponibilités quotidiennes.

Elle s’appuie sur l’emploi du temps (EDT) de l’utilisateur afin de calculer
automatiquement les plages horaires disponibles pour une date donnée.

Cette vue est accessible depuis l’interface principale de l’application
client.

Classe DisponibiliteView
------------------------

.. automodule:: client.views.disponibilite_view
   :members:
   :undoc-members:
   :show-inheritance:

Fonctionnalités principales
---------------------------

- Sélection d’une date via un calendrier
- Génération automatique des disponibilités depuis l’EDT
- Affichage des plages horaires disponibles
- Navigation vers la page d’accueil

Comportement de la vue
----------------------

Lorsqu’une date est sélectionnée et que l’utilisateur clique sur
le bouton *Générer depuis l’EDT*, la vue :

1. Récupère la date sélectionnée
2. Déclenche la génération des disponibilités via le contrôleur
3. Rafraîchit la liste affichée

Les disponibilités sont affichées sous la forme :

::

   AAAA-MM-JJ : HH:MM → HH:MM
