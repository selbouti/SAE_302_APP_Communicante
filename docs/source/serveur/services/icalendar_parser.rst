ICalendarParser
===============

Le module ``icalendar_parser`` fournit des outils permettant d’analyser
des fichiers **iCalendar (.ics)** afin d’en extraire des événements
exploitables par l’application de covoiturage.

Il est principalement utilisé pour :

- importer un emploi du temps utilisateur
- extraire des événements depuis un fichier `.ics`
- convertir ces événements en structures de données compatibles
  avec la création automatique de trajets

---

Description générale
--------------------

Le module repose sur la bibliothèque externe ``icalendar`` pour lire
et parcourir le contenu des fichiers iCalendar.

Chaque événement de type ``VEVENT`` est transformé en un dictionnaire
contenant des informations essentielles telles que :

- le résumé (summary)
- la description
- la date et l’heure de début
- le lieu

Ces données sont ensuite utilisées par les services métier
pour générer des trajets ou des disponibilités.

---

Documentation de l’API
----------------------

.. automodule:: serveur.services.icalendar_parser
   :members:
   :undoc-members:
   :show-inheritance:

---

