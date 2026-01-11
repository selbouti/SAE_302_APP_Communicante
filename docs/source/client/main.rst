Point d’entrée de l’application cliente
=======================================

.. module:: client.main
   :synopsis: Lancement de l’application PyQt cliente

Ce module constitue le **point d’entrée principal** de l’application cliente
PyQt *Covoiturage Daily*.

Il est responsable de :

- l’initialisation de l’application PyQt
- la création de la fenêtre principale
- l’instanciation de toutes les vues
- l’injection des vues dans le `QStackedWidget`
- la sélection de la vue initiale (connexion)
- le démarrage de la boucle événementielle

Fonction principale
-------------------

.. autofunction:: client.main
