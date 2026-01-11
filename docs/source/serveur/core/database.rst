Accès à la base de données
==========================

Ce module fournit une classe utilitaire permettant d’interagir avec
la base de données de l’application.

Il centralise les opérations SQL courantes et simplifie l’accès aux données
en encapsulant la gestion de la connexion.

Fonctionnalités principales
----------------------------

La classe ``Database`` permet notamment :

- d’exécuter des requêtes SQL classiques
- de récupérer un ensemble de résultats
- de récupérer une seule ligne de résultat
- d’insérer des données et de récupérer l’identifiant généré

Ces méthodes sont utilisées par l’ensemble des modèles côté serveur.

---

.. automodule:: serveur.core.database
   :members:
   :undoc-members:
   :show-inheritance:
