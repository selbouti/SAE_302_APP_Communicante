import sqlite3
import hashlib

DB_PATH = "covoiturage.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- Créer les tables si elles n'existent pas ---

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

# --- Vider les tables existantes ---
for table in ["invitations", "reservations", "trajets", "voitures", "utilisateurs"]:
    cursor.execute(f"DELETE FROM {table}")
conn.commit()

# --- Créer utilisateurs ---
users = [
    ("jean@test.com", "Dupont", "Jean", "0601020304"),
    ("sophie@test.com", "Martin", "Sophie", "0602030405"),
    ("pierre@test.com", "Durand", "Pierre", "0603040506"),
    ("marie@test.com", "Bernard", "Marie", "0604050607"),
    ("luc@test.com", "Petit", "Luc", "0605060708"),
    ("alice@test.com", "Moreau", "Alice", "0606070809"),
    ("bob@test.com", "Simon", "Bob", "0607080910"),
]

for email, nom, prenom, tel in users:
    cursor.execute("""
        INSERT INTO utilisateurs (email, password, nom, prenom, telephone)
        VALUES (?, ?, ?, ?, ?)
    """, (email, hash_password("password123"), nom, prenom, tel))

cursor.execute("SELECT id FROM utilisateurs ORDER BY id")
user_ids = [row[0] for row in cursor.fetchall()]

# --- Voitures (1 par conducteur) ---
voitures = [
    (user_ids[0], "Peugeot", "3008", "Noir", "AB-123-CD", 4),
    (user_ids[1], "Renault", "Clio", "Blanc", "EF-456-GH", 5),
    (user_ids[4], "Toyota", "Corolla", "Gris", "IJ-789-KL", 5),
    (user_ids[5], "Citroën", "C3", "Bleu", "MN-012-OP", 4),
]

cursor.executemany("""
    INSERT INTO voitures (utilisateur_id, marque, modele, couleur, plaque, places_totales)
    VALUES (?, ?, ?, ?, ?, ?)
""", voitures)

cursor.execute("SELECT id FROM voitures ORDER BY id")
voiture_ids = [row[0] for row in cursor.fetchall()]

# --- Trajets ---
trajets = [
    # Conducteurs
    (user_ids[0], voiture_ids[0], "Poitiers", "Paris", "2024-01-22", "lundi", "08:00", 15.0, "conducteur"), # Jean
    (user_ids[1], voiture_ids[1], "Poitiers", "Paris", "2024-01-23", "mardi", "09:00", 15.0, "conducteur"), # Sophie
    (user_ids[4], voiture_ids[2], "Poitiers", "Lyon", "2024-01-24", "mercredi", "10:00", 10.0, "conducteur"), # Luc
    (user_ids[5], voiture_ids[3], "Poitiers", "Lyon", "2024-01-25", "jeudi", "07:30", 10.0, "conducteur"), # Alice
    # Passagers
    (user_ids[2], None, "Poitiers", "Paris", "2024-01-22", "lundi", "08:00", 0.0, "passager"), # Pierre
    (user_ids[3], None, "Poitiers", "Paris", "2024-01-23", "mardi", "09:00", 0.0, "passager"), # Marie
    (user_ids[6], None, "Poitiers", "Lyon", "2024-01-24", "mercredi", "10:00", 0.0, "passager"), # Bob
]

cursor.executemany("""
    INSERT INTO trajets (utilisateur_id, voiture_id, depart, arrivee, date_depart, jour_semaine, heure_depart, prix_par_place, mode)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", trajets)

cursor.execute("SELECT id FROM trajets ORDER BY id")
trajet_ids = [row[0] for row in cursor.fetchall()]

# --- Réservations ---
reservations = [
    (trajet_ids[0], user_ids[2], 1, "acceptee"),  # Pierre sur trajet Jean
    (trajet_ids[1], user_ids[3], 1, "en_attente"),# Marie sur trajet Sophie
    (trajet_ids[4], user_ids[0], 1, "en_attente"),# Jean sur trajet Pierre
]

cursor.executemany("""
    INSERT INTO reservations (trajet_id, passager_id, places_reservees, statut)
    VALUES (?, ?, ?, ?)
""", reservations)

# --- Invitations ---
invitations = [
    (trajet_ids[0], user_ids[4], "acceptee"),    # Jean invite Luc
    (trajet_ids[2], user_ids[6], "en_attente"),  # Luc invite Bob
]

cursor.executemany("""
    INSERT INTO invitations (trajet_id, passager_id, statut)
    VALUES (?, ?, ?)
""", invitations)

conn.commit()
conn.close()
print("✅ Jeu de données complet pour matching créé !")
