UserModel
=========

Le module ``user_model`` gère les utilisateurs de l'application
Covoiturage au niveau de la base de données.

Il permet :

- la création de comptes utilisateurs
- l’authentification via email et mot de passe
- la récupération des informations utilisateur

Les mots de passe sont stockés de manière sécurisée à l’aide
d’un hachage SHA-256.

---

API du modèle utilisateur
-------------------------

.. automodule:: serveur.models.user_model
   :members:
   :undoc-members:
   :show-inheritance:
