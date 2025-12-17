#!/bin/bash

echo "========================================"
echo " 🚀 SCRIPT D’INTÉGRATION — ETAPE A "
echo " Gestion utilisateur / voiture / indisponibilités "
echo "========================================"

# ----------------------------
# 1) Création des dossiers MVC
# ----------------------------
echo "➡ Création des dossiers..."

mkdir -p models
mkdir -p controllers
mkdir -p views

echo "   ✔ Dossiers OK"

# ----------------------------
# 2) Installation du modèle utilisateur
# ----------------------------
echo "➡ Installation de models/user_model.py ..."

cat > models/user_model.py << 'EOF'
from config.database import get_connection

class UserModel:

    def authenticate(self, login, password):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT * FROM Utilisateur
            WHERE login=%s AND mot_de_passe=%s
        """, (login, password))

        user = cur.fetchone()
        cur.close()
        conn.close()
        return user

    def create_user(self, data):
        conn = get_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO Utilisateur
        (login, mot_de_passe, nom, prenom, email, telephone, adresse, ville, cp)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cur.execute(sql, (
            data["login"], data["mot_de_passe"], data["nom"], data["prenom"],
            data["email"], data["telephone"], data["adresse"], data["ville"], data["cp"]
        ))

        conn.commit()
        uid = cur.lastrowid
        cur.close()
        conn.close()
        return uid

    def update_user(self, user_id, data):
        conn = get_connection()
        cur = conn.cursor()

        sql = """
        UPDATE Utilisateur
        SET nom=%s, prenom=%s, email=%s, telephone=%s,
            adresse=%s, ville=%s, cp=%s
        WHERE id_user=%s
        """

        cur.execute(sql, (
            data["nom"], data["prenom"], data["email"], data["telephone"],
            data["adresse"], data["ville"], data["cp"], user_id
        ))

        conn.commit()
        cur.close()
        conn.close()

    def get_user(self, user_id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM Utilisateur WHERE id_user=%s", (user_id,))
        user = cur.fetchone()

        cur.close()
        conn.close()
        return user
EOF

echo "   ✔ user_model.py installé"


# ----------------------------
# 3) Installation modèle voiture
# ----------------------------
echo "➡ Installation de models/voiture_model.py ..."

cat > models/voiture_model.py << 'EOF'
from config.database import get_connection

class VoitureModel:

    def get_voiture_by_user(self, user_id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM Voiture WHERE user_id=%s", (user_id,))
        car = cur.fetchone()

        cur.close()
        conn.close()
        return car

    def add_voiture(self, user_id, data):
        conn = get_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO Voiture (user_id, marque, modele, chevaux_fiscaux,
                             motorisation, taux_co2, places_max)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        cur.execute(sql, (
            user_id, data["marque"], data["modele"], data["chevaux_fiscaux"],
            data["motorisation"], data["taux_co2"], data["places_max"]
        ))

        conn.commit()
        cur.close()
        conn.close()

    def delete_voiture(self, voiture_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Voiture WHERE id_voiture=%s", (voiture_id,))
        conn.commit()

        cur.close()
        conn.close()
EOF

echo "   ✔ voiture_model.py installé"


# ----------------------------
# 4) Installation modèle indisponibilité
# ----------------------------
echo "➡ Installation de models/disponibilite_model.py ..."

cat > models/disponibilite_model.py << 'EOF'
from config.database import get_connection

class DisponibiliteModel:

    def get_indispo(self, user_id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM Disponibilite WHERE user_id=%s", (user_id,))
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows

    def add_indispo(self, user_id, data):
        conn = get_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO Disponibilite (user_id, date_dispo, heure_debut, heure_fin)
        VALUES (%s,%s,%s,%s)
        """

        cur.execute(sql, (
            user_id, data["date_dispo"], data["heure_debut"], data["heure_fin"]
        ))

        conn.commit()
        cur.close()
        conn.close()

    def delete_indispo(self, dispo_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Disponibilite WHERE id_dispo=%s", (dispo_id,))
        conn.commit()

        cur.close()
        conn.close()
EOF

echo "   ✔ disponibilite_model.py installé"


# ----------------------------
# 5) Installation du contrôleur
# ----------------------------
echo "➡ Installation de controllers/user_controller.py ..."

cat > controllers/user_controller.py << 'EOF'
from models.user_model import UserModel
from models.voiture_model import VoitureModel
from models.disponibilite_model import DisponibiliteModel

class UserController:

    def __init__(self, main_window):
        self.main = main_window
        self.user_model = UserModel()
        self.voiture_model = VoitureModel()
        self.dispo_model = DisponibiliteModel()
        self.current_user = None

    def login(self, login, password):
        user = self.user_model.authenticate(login, password)
        if user:
            self.current_user = user
            self.main.show_home_page()
        else:
            self.main.show_error("Identifiants incorrects")

    def update_profile(self, data):
        self.user_model.update_user(self.current_user["id_user"], data)
        self.main.show_message("Profil mis à jour.")

    def add_voiture(self, data):
        self.voiture_model.add_voiture(self.current_user["id_user"], data)
        self.main.show_message("Voiture ajoutée.")

    def delete_voiture(self, voiture_id):
        self.voiture_model.delete_voiture(voiture_id)
        self.main.show_message("Voiture supprimée.")

    def add_indispo(self, data):
        self.dispo_model.add_indispo(self.current_user["id_user"], data)
        self.main.show_message("Indisponibilité ajoutée.")

    def delete_indispo(self, dispo_id):
        self.dispo_model.delete_indispo(dispo_id)
        self.main.show_message("Indisponibilité supprimée.")
EOF

echo "   ✔ user_controller.py installé"


# ----------------------------
# 6) Installation vue profil
# ----------------------------
echo "➡ Installation de views/user_profile_view.py ..."

cat > views/user_profile_view.py << 'EOF'
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class UserProfileView(QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Page de gestion du profil"))
        layout.addWidget(QLabel("(Formulaires à compléter par la suite)"))

        self.setLayout(layout)
EOF

echo "   ✔ user_profile_view.py installé"

echo "========================================"
echo " 🎉 ETAPE A INSTALLÉE AVEC SUCCÈS !"
echo "========================================"
