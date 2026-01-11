# Guide d'installation – SAE 302 Covoiturage

---

## 1. Prérequis système

- **Système** : Linux
- **Python** : version 3.8 ou supérieure
- **Outils requis** :
  - `git`
  - `sqlite3`
  - `python3-venv`
  - `python3-pip`

---

## 2. Récupération du projet
```bash
git clone https://github.com/selbouti/SAE_302_APP_Communicante.git
cd SAE_302_APP_Communicante
```

---

## 3. Installation des dépendances système
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip sqlite3 git
```

---

## 4. Environnement virtuel Python
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 5. Installation des dépendances Python
```bash
pip install -r requirements.txt
```

---

## 6. Base de données

### 6.1 Base de données fournie

Une base de données SQLite contenant un jeu de test est déjà présente dans le projet.  
Il est possible de lancer directement l'application sans aucune manipulation supplémentaire.

### 6.2 Génération manuelle du jeu de test
```bash
cd covoiturage/serveur
python3 test_data.py
```

Le script génère une base nommée `covoiturage_db`.  
Si nécessaire, déplacer la base dans : `covoiturage/serveur/`

### 6.3 Création automatique d'une base vide

Si aucune base n'est présente, le fichier `covoiturage/config/database.py` crée automatiquement une base vide avec les tables nécessaires au démarrage de l'application.

---

## 7. Lancement de l'application

Deux terminaux sont nécessaires.

### Terminal 1 – Serveur Flask
```bash
cd covoiturage/serveur
source ../../venv/bin/activate
python3 app.py
```

Le serveur est accessible sur : **http://127.0.0.1:5000**

### Terminal 2 – Client graphique
```bash
cd SAE_302_APP_Communicante
source venv/bin/activate
python3 main.py
```

---

## 8. Fichier iCalendar de test

Un fichier iCalendar (`.ics`) est disponible dans : `SAE_302_APP_Communicante/data/`

Il permet de tester l'importation des trajets dans l'application.

---

## 9. Exécution des tests
```bash
pip install pytest
pytest
```

---

## 📄 Contenu du fichier `requirements.txt`
```txt
Flask>=2.2
flask-cors>=3.0
requests>=2.28
```

---

**Fin du guide d'installation**
