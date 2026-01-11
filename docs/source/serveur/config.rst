Configuration de l’application
==============================

Ce module définit la configuration globale de l’application serveur Flask
du projet **Covoiturage**.

Il centralise l’ensemble des paramètres nécessaires au bon fonctionnement
du serveur, notamment :

- la configuration de la base de données
- les paramètres réseau (hôte, port)
- le mode debug
- les paramètres de sécurité liés à l’authentification JWT

Classe ``Config``
-----------------

La classe ``Config`` regroupe les constantes de configuration utilisées
par l’application Flask.

Elle permet de modifier facilement le comportement du serveur sans
impacter le reste du code.

Principaux paramètres
---------------------

- **DATABASE_PATH**  
  Chemin vers le fichier de base de données SQLite utilisé par l’application.

- **DEBUG**  
  Active ou désactive le mode debug de Flask (utile en développement).

- **HOST**  
  Adresse réseau sur laquelle le serveur Flask écoute.

- **PORT**  
  Port d’écoute du serveur Flask.

- **JWT_SECRET**  
  Clé secrète utilisée pour signer les JSON Web Tokens (JWT).  
  Elle peut être définie via une variable d’environnement pour plus de sécurité.

- **JWT_EXPIRATION**  
  Durée de validité des tokens JWT (par défaut : 24 heures).

Documentation automatique
-------------------------

La documentation de ce module est générée automatiquement à partir
des **docstrings en anglais** présentes dans le code source.

.. automodule:: serveur.config
   :members:
   :undoc-members:
   :show-inheritance:
