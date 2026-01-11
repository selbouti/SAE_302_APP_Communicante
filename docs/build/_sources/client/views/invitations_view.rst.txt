Vue des invitations
===================

La vue ``InvitationsView`` permet à l’utilisateur de gérer les invitations
liées aux trajets de covoiturage.

Elle regroupe deux catégories d’invitations :

- les invitations **reçues** (en tant que passager)
- les invitations **envoyées** (en tant que conducteur)

L’interface repose sur un système d’onglets afin de séparer clairement
ces deux cas d’usage.

Organisation de l’interface
----------------------------

L’interface est composée de :

- un ``QTabWidget`` avec deux onglets :
  
  - **Invitations reçues**
  - **Invitations envoyées**

- deux tableaux ``QTableWidget`` affichant les informations suivantes :
  
  - départ
  - arrivée
  - utilisateur concerné
  - statut
  - date de création

- des boutons d’action permettant :
  
  - d’accepter une invitation
  - de refuser une invitation
  - de supprimer une invitation envoyée

Chargement des données
----------------------

La méthode ``load`` permet de recharger simultanément :

- les invitations reçues
- les invitations envoyées

Chaque onglet peut également être rafraîchi indépendamment grâce
à un bouton dédié.

Gestion des actions
-------------------

Les actions possibles sur une invitation sont :

- **Accepter** une invitation reçue
- **Refuser** une invitation reçue
- **Supprimer** une invitation envoyée

Chaque action déclenche un appel au contrôleur
``InvitationController`` et affiche un message de confirmation
ou d’erreur selon le résultat.

Classe InvitationsView
----------------------

.. autoclass:: client.views.invitations_view.InvitationsView
   :members:
   :undoc-members:
   :show-inheritance:
