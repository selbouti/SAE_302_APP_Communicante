Contrôleur Profil
=================

.. automodule:: client.controllers.profile_controller
   :members:
   :undoc-members:
   :show-inheritance:

Présentation
------------

Le ``ProfileController`` est un contrôleur côté client chargé de la
gestion du profil utilisateur. Il agit comme une couche intermédiaire
entre l’interface graphique et l’API REST du serveur.



Fonctionnalités principales
---------------------------

- Récupération des informations du profil utilisateur
- Mise à jour des données personnelles
- Validation des paramètres avant communication avec l’API

Méthodes disponibles
--------------------

- ``get_profile(user_id)``
- ``update_profile(user_id, profile_data)``

Gestion de la robustesse
------------------------

Des assertions sont utilisées dans le contrôleur afin de :

- vérifier la validité des paramètres fournis
- éviter les appels API incorrects
- améliorer la fiabilité du client
