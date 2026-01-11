Vue d’accueil
=============

La vue ``HomeView`` correspond à l’écran principal affiché après la connexion
de l’utilisateur.

Elle joue le rôle de tableau de bord et permet d’accéder rapidement aux
fonctionnalités clés de l’application de covoiturage.

Fonctionnalités principales
----------------------------

- Affichage d’un message de bienvenue personnalisé
- Accès rapide au profil utilisateur
- Accès aux trajets personnels
- Accès au matching de trajets
- Accès aux réservations et invitations
- Déconnexion de l’utilisateur

Navigation utilisateur
----------------------

Chaque bouton déclenche un changement de vue via le
``QStackedWidget`` géré par la fenêtre principale :

- **Mon profil** → vue profil
- **Matching** → vue de matching
- **Mes trajets** → gestion des trajets
- **Mes réservations et invitations** → réservations
- **Déconnexion** → retour à l’écran de connexion

Classe HomeView
---------------

.. autoclass:: views.home_view.HomeView
   :members:
   :undoc-members:
   :show-inheritance:
