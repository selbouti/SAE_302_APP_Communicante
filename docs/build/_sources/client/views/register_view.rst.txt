Inscription utilisateur
=======================

La vue *RegisterView* permet à un nouvel utilisateur de créer un compte
dans l'application Covoiturage Daily.

Fonctionnalités principales
----------------------------

Cette vue propose :

- la saisie des informations personnelles de l'utilisateur
- l'ajout optionnel d'un véhicule personnel
- l'import optionnel d'un fichier iCalendar (.ics)
- la création du compte via l'API serveur

Gestion du véhicule
-------------------

Si l'utilisateur coche l'option **« J'ai une voiture »**, des champs
supplémentaires apparaissent afin de saisir les informations du véhicule :

- marque et modèle
- chevaux fiscaux
- motorisation
- taux de CO₂
- nombre de places disponibles

Import iCalendar
----------------

L'utilisateur peut sélectionner un fichier **.ics** afin d'importer
automatiquement ses trajets depuis un emploi du temps.

Documentation technique
-----------------------

.. automodule:: client.views.register_view
   :members:
   :undoc-members:
   :show-inheritance:
