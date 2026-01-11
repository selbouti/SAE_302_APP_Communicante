Gestion des emplois du temps (EDT)
==================================

Ce module gère les emplois du temps des utilisateurs côté serveur.

Il permet :
- de récupérer l’emploi du temps associé à un utilisateur
- d’enregistrer un emploi du temps à partir d’un fichier
- d’enregistrer un emploi du temps à partir d’une URL
- de remplacer automatiquement un emploi du temps existant

Chaque utilisateur ne peut posséder qu’un seul emploi du temps à la fois.

---

Classe EDTModel
---------------

La classe ``EDTModel`` encapsule toutes les opérations liées à la table
``EmploiDuTemps`` de la base de données.

Elle utilise une connexion fournie par le module de configuration
de la base de données et effectue directement les requêtes SQL nécessaires.

---

Méthodes principales
--------------------

- ``get_edt(user_id)``  
  Récupère l’emploi du temps enregistré pour un utilisateur donné.

- ``save_edt_file(user_id, file_path)``  
  Enregistre un emploi du temps à partir d’un fichier (format ICS).

- ``save_edt_url(user_id, url)``  
  Enregistre un emploi du temps à partir d’une URL distante.

- ``_replace_edt(user_id, source_type, source)``  
  Supprime l’ancien emploi du temps et insère le nouveau.
  Cette méthode interne garantit qu’un seul EDT est stocké par utilisateur.

---

Documentation automatique
-------------------------

.. automodule:: serveur.models.edt_model
   :members:
   :undoc-members:
   :show-inheritance:
