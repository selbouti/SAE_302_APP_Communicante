Vue d’import de l’emploi du temps
=================================

La vue ``EDTImportView`` permet à l’utilisateur de gérer son emploi du temps
(EDT) depuis l’interface graphique.

Elle propose deux méthodes d’import :
- un fichier iCalendar (.ics)
- une URL distante contenant un calendrier compatible

Fonctionnalités principales
----------------------------

- Affichage de l’EDT actuellement enregistré
- Import d’un nouvel EDT depuis un fichier .ics
- Import d’un nouvel EDT depuis une URL
- Mise à jour automatique des disponibilités
- Retour au menu principal

Cycle de fonctionnement
-----------------------

1. L’utilisateur accède à la vue d’import EDT  
2. Le système affiche l’EDT actuellement enregistré (s’il existe)  
3. L’utilisateur choisit :
   - soit un fichier .ics
   - soit une URL de calendrier
4. L’EDT est enregistré côté serveur
5. Les disponibilités sont recalculées automatiquement

Classe EDTImportView
--------------------

.. autoclass:: client.views.edt_import_view.EDTImportView
   :members:
   :undoc-members:
   :show-inheritance:
