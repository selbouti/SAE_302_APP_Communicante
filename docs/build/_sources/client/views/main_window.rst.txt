MainWindow
==========

La classe ``MainWindow`` représente la fenêtre principale de l’application
*Covoiturage Daily*.  
Elle constitue le point central de l’interface graphique côté client.

Cette fenêtre est responsable de la gestion globale de l’interface :
navigation entre les vues, affichage des menus, barre d’outils et état
de l’utilisateur connecté.

---

Rôle principal
---------------

La fenêtre principale assure les fonctions suivantes :

- affichage des différentes vues grâce à un ``QStackedWidget``
- gestion de la barre de menu (MenuBar)
- gestion de la barre d’outils (ToolBar)
- navigation entre les écrans de l’application
- stockage de l’utilisateur actuellement connecté

---

Architecture générale
---------------------

La navigation repose sur un widget empilé contenant toutes les vues
de l’application.  
Chaque vue est identifiée par une clé (ex. ``login``, ``home``, ``profile``)
et peut être affichée dynamiquement.

La visibilité de la barre de menu et de la barre d’outils dépend
de la vue affichée :

- **login / register** : menu et toolbar masqués
- **home** : menu visible, toolbar masquée
- **autres vues** : menu et toolbar visibles

---

Menu principal
--------------

La barre de menu contient plusieurs sections :

- **Compte**
  - Mon profil
  - Ma voiture
  - Déconnexion
- **Trajets**
  - Mes trajets
  - Matching
- **Réservations**
  - Mes réservations
- **Aide**
  - À propos

Chaque action déclenche un changement de vue ou une action spécifique
comme la déconnexion.

---

Barre d’outils (ToolBar)
------------------------

La barre d’outils permet une navigation rapide entre les fonctionnalités
principales de l’application :

- accès au profil utilisateur
- gestion de la voiture
- gestion des trajets
- matching
- réservations
- déconnexion
- accès à la fenêtre *À propos*

Elle est affichée verticalement sur le côté gauche de la fenêtre.

---

Gestion de la navigation
------------------------

La méthode de navigation centrale permet :

- de changer la vue affichée
- d’adapter l’interface (menu / toolbar)
- de recharger automatiquement une vue si elle expose une méthode
  ``load`` ou ``refresh``

Cela garantit que les données affichées sont toujours à jour.

---

Gestion de l’utilisateur connecté
---------------------------------

La classe conserve les informations de l’utilisateur connecté afin de :

- personnaliser l’interface (message de bienvenue)
- autoriser l’accès aux vues protégées
- transmettre l’identifiant utilisateur aux contrôleurs

---

Dialogue « À propos »
---------------------

Une boîte de dialogue informative permet d’afficher :

- le nom de l’application
- le type d’architecture (client/serveur)
- le contexte pédagogique du projet (SAE)

---

Documentation automatique
-------------------------

.. automodule:: client.views.main_window
   :members:
   :undoc-members:
   :show-inheritance:
