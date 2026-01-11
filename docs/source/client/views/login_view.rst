Vue de connexion
================

La vue ``LoginView`` permet à un utilisateur de se connecter à
l’application **Covoiturage Daily**.

Elle constitue le point d’entrée principal de l’application
côté client.

Objectifs de la vue
-------------------

Cette vue a pour rôle de :

- permettre à l’utilisateur de saisir son adresse email
- permettre la saisie sécurisée du mot de passe
- transmettre les identifiants au contrôleur utilisateur
- gérer les erreurs de connexion
- rediriger l’utilisateur après authentification réussie

Structure de l’interface
------------------------

L’interface graphique est composée de :

- un titre principal affichant le nom de l’application
- un formulaire de connexion comprenant :
  
  - un champ ``QLineEdit`` pour l’email
  - un champ ``QLineEdit`` masqué pour le mot de passe

- deux boutons principaux :
  
  - **Se connecter**
  - **Annuler**

- un bouton secondaire permettant d’accéder à la création de compte

L’ensemble est présenté sous forme de carte centrale
afin d’améliorer la lisibilité et l’expérience utilisateur.

Processus de connexion
----------------------

Lorsque l’utilisateur clique sur le bouton *Se connecter* :

1. les identifiants sont envoyés au ``UserController``
2. une requête est effectuée vers l’API serveur
3. en cas de succès :
   
   - l’utilisateur est enregistré comme connecté
   - la vue d’accueil est affichée

4. en cas d’échec :
   
   - un message d’erreur est affiché via une boîte de dialogue

Classe LoginView
----------------

.. autoclass:: client.views.login_view.LoginView
   :members:
   :undoc-members:
   :show-inheritance:
