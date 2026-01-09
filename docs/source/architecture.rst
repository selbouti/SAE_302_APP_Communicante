Architecture
============

L’architecture repose sur deux parties distinctes :

- **Client PyQt5**
  - Interface graphique
  - Appels API REST
  - Gestion locale des vues

- **Serveur Flask**
  - API REST
  - Accès base de données SQLite
  - Logique métier centralisée

Le client communique exclusivement via HTTP avec l’API.
