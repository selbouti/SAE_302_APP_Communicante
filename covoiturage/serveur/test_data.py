import sqlite3
import hashlib

DB_PATH = "covoiturage.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Créer les tables si elles n'existent pas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        nom TEXT,
        prenom TEXT,
        telephone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS voitures (
        id INTEGER PRIMARY KEY,
        utilisateur_id INTEGER,
        marque TEXT,
        modele TEXT,
        couleur TEXT,
        plaque TEXT UNIQUE,
        places_totales INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS trajets (
        id INTEGER PRIMARY KEY,
        utilisateur_id INTEGER,
        voiture_id INTEGER,
        depart TEXT,
        arrivee TEXT,
        date_depart TEXT,
        jour_semaine TEXT,
        heure_depart TEXT,
        prix_par_place REAL,
        mode TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id),
        FOREIGN KEY (voiture_id) REFERENCES voitures(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY,
        trajet_id INTEGER,
        passager_id INTEGER,
        places_reservees INTEGER,
        statut TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (trajet_id) REFERENCES trajets(id),
        FOREIGN KEY (passager_id) REFERENCES utilisateurs(id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS invitations (
        id INTEGER PRIMARY KEY,
        trajet_id INTEGER,
        passager_id INTEGER,
        statut TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (trajet_id) REFERENCES trajets(id),
        FOREIGN KEY (passager_id) REFERENCES utilisateurs(id)
    )
""")

conn.commit()

# Vider les données
cursor.execute("DELETE FROM invitations")
cursor.execute("DELETE FROM reservations")
cursor.execute("DELETE FROM trajets")
cursor.execute("DELETE FROM voitures")
cursor.execute("DELETE FROM utilisateurs")

# Créer utilisateurs
users = [
    ("jean@test.com", hash_password("password123"), "Dupont", "Jean", "0601020304"),
    ("sophie@test.com", hash_password("password123"), "Martin", "Sophie", "0602030405"),
    ("pierre@test.com", hash_password("password123"), "Durand", "Pierre", "0603040506"),
    ("marie@test.com", hash_password("password123"), "Bernard", "Marie", "0604050607"),
    ("luc@test.com", hash_password("password123"), "Petit", "Luc", "0605060708"),
    ("alice@test.com", hash_password("password123"), "Moreau", "Alice", "0606070809"),
    ("bob@test.com", hash_password("password123"), "Simon", "Bob", "0607080910"),
]

cursor.executemany("""
    INSERT INTO utilisateurs (email, password, nom, prenom, telephone)
    VALUES (?, ?, ?, ?, ?)
""", users)

# Récupérer les IDs
cursor.execute("SELECT id FROM utilisateurs ORDER BY id")
user_ids = [row[0] for row in cursor.fetchall()]

# Créer voitures
voitures = [
    (user_ids[0], "Peugeot", "3008", "Noir", "AB-123-CD", 4),
    (user_ids[1], "Renault", "Clio", "Blanc", "EF-456-GH", 5),
    (user_ids[4], "Toyota", "Corolla", "Gris", "IJ-789-KL", 5),
    (user_ids[5], "Citroën", "C3", "Bleu", "MN-012-OP", 4),
    (user_ids[1], "Peugeot", "308", "Rouge", "QR-345-ST", 3),
]

cursor.executemany("""
    INSERT INTO voitures (utilisateur_id, marque, modele, couleur, plaque, places_totales)
    VALUES (?, ?, ?, ?, ?, ?)
""", voitures)

# Récupérer les IDs voitures
cursor.execute("SELECT id FROM voitures ORDER BY id")
voiture_ids = [row[0] for row in cursor.fetchall()]

# Créer trajets
trajets = [
    (user_ids[0], voiture_ids[0], "Poitiers", "Paris", "2024-01-22", "lundi", "08:00", 8.0, "conducteur"),
    (user_ids[1], voiture_ids[1], "Poitiers", "Paris", "2024-01-23", "mardi", "09:00", 8.0, "conducteur"),
    (user_ids[2], None, "Poitiers", "Paris", "2024-01-22", "lundi", "08:00", 0.0, "passager"),
    (user_ids[3], None, "Poitiers", "Paris", "2024-01-23", "mardi", "09:00", 0.0, "passager"),
    (user_ids[4], voiture_ids[2], "Poitiers", "Lyon", "2024-01-24", "mercredi", "10:00", 7.0, "conducteur"),
    (user_ids[5], voiture_ids[3], "Poitiers", "Lyon", "2024-01-25", "jeudi", "07:30", 7.0, "conducteur"),
    (user_ids[6], None, "Poitiers", "Lyon", "2024-01-24", "mercredi", "10:00", 0.0, "passager"),
    (user_ids[0], None, "Poitiers", "Lyon", "2024-01-25", "jeudi", "07:30", 0.0, "passager"),
    (user_ids[1], voiture_ids[4], "Poitiers", "Bordeaux", "2024-01-26", "vendredi", "14:00", 6.0, "conducteur"),
    (user_ids[2], None, "Poitiers", "Bordeaux", "2024-01-26", "vendredi", "14:00", 0.0, "passager"),
]

cursor.executemany("""
    INSERT INTO trajets (utilisateur_id, voiture_id, depart, arrivee, date_depart, jour_semaine, heure_depart, prix_par_place, mode)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", trajets)

# Récupérer les IDs des trajets
cursor.execute("SELECT id FROM trajets ORDER BY id")
trajet_ids = [row[0] for row in cursor.fetchall()]

# Créer réservations
reservations = [
    (trajet_ids[0], user_ids[2], 1, "acceptee"),
    (trajet_ids[1], user_ids[3], 1, "en_attente"),
    (trajet_ids[4], user_ids[6], 2, "acceptee"),
    (trajet_ids[5], user_ids[0], 1, "en_attente"),
    (trajet_ids[8], user_ids[2], 1, "acceptee"),
]

cursor.executemany("""
    INSERT INTO reservations (trajet_id, passager_id, places_reservees, statut)
    VALUES (?, ?, ?, ?)
""", reservations)

# Créer invitations
invitations = [
    (trajet_ids[0], user_ids[4], "acceptee"),
    (trajet_ids[4], user_ids[3], "en_attente"),
    (trajet_ids[8], user_ids[5], "refusee"),
]

cursor.executemany("""
    INSERT INTO invitations (trajet_id, passager_id, statut)
    VALUES (?, ?, ?)
""", invitations)

conn.commit()
conn.close()

print("✅ Jeu de données créé!")