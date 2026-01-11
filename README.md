# SAE 302 – Application Communicante  
## Application de covoiturage (Client / Serveur)

Ce projet a été réalisé dans le cadre de la SAE 302 – Application communicante.  
Il s’agit d’une application de covoiturage permettant de mettre en relation des utilisateurs ayant des trajets quotidiens similaires.

L’application repose sur une architecture **client / serveur** :
- Serveur : API REST développée avec Flask
- Client : interface graphique développée en Python avec PyQt
- Base de données : SQLite

---

## Fonctionnalités principales

- Authentification et inscription des utilisateurs
- Importation des trajets via fichier iCalendar
- Gestion des trajets (conducteur / passager)
- Recherche de trajets compatibles avec marges horaires
- Système de réservation et d’invitation
- Calcul du prix du trajet et estimation carburant

---

## Architecture du projet

- Client graphique (PyQt)
- Serveur Flask (API REST)
- Base de données SQLite locale
- Communication via requêtes HTTP (GET, POST, PUT)

---

## Installation

Voir le fichier :  
📄 **GUIDE_INSTALLATION.md**

---

## Lancement rapide (résumé)

### Serveur
```bash
terminal 1 :
cd covoiturage/server
python3 app.py
---
### Serveur
```bash
terminal 1 :
cd covoiturage/client
python3 main.py


