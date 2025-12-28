# ============= config/database.py =============
import sqlite3

DB_FILE = "covoiturage.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def migrate_db(conn):
    """Migrer la DB pour ajouter les colonnes manquantes"""
    c = conn.cursor()
    
    # Vérifier si la table voitures existe
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='voitures'")
    if not c.fetchone():
        print("✓ Création table voitures...")
        c.execute('''CREATE TABLE voitures (
            id INTEGER PRIMARY KEY,
            utilisateur_id INTEGER,
            marque TEXT,
            modele TEXT,
            couleur TEXT,
            plaque TEXT UNIQUE,
            places_totales INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
        )''')
    
    # Vérifier si la colonne voiture_id existe dans trajets
    c.execute("PRAGMA table_info(trajets)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'voiture_id' not in columns:
        print("✓ Ajout colonne voiture_id à trajets...")
        c.execute('ALTER TABLE trajets ADD COLUMN voiture_id INTEGER')
    
    if 'jour_semaine' not in columns:
        print("✓ Ajout colonne jour_semaine à trajets...")
        c.execute('ALTER TABLE trajets ADD COLUMN jour_semaine TEXT')
    
    if 'heure_depart' not in columns:
        print("✓ Ajout colonne heure_depart à trajets...")
        c.execute('ALTER TABLE trajets ADD COLUMN heure_depart TEXT')
    
    if 'mode' not in columns:
        print("✓ Ajout colonne mode à trajets...")
        c.execute('ALTER TABLE trajets ADD COLUMN mode TEXT DEFAULT "conducteur"')
    
    # Supprimer les colonnes obsolètes si elles existent
    if 'places_totales' in columns:
        print("✓ Suppression colonne places_totales (obsolète)...")
        # SQLite ne supporte pas bien ALTER TABLE DROP COLUMN, on va recréer la table
        pass
    
    conn.commit()

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Créer les tables si elles n'existent pas
    c.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        nom TEXT,
        prenom TEXT,
        telephone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS voitures (
        id INTEGER PRIMARY KEY,
        utilisateur_id INTEGER,
        marque TEXT,
        modele TEXT,
        couleur TEXT,
        plaque TEXT UNIQUE,
        places_totales INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS trajets (
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
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY,
        trajet_id INTEGER,
        passager_id INTEGER,
        places_reservees INTEGER,
        statut TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (trajet_id) REFERENCES trajets(id),
        FOREIGN KEY (passager_id) REFERENCES utilisateurs(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS invitations (
        id INTEGER PRIMARY KEY,
        trajet_id INTEGER,
        passager_id INTEGER,
        statut TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (trajet_id) REFERENCES trajets(id),
        FOREIGN KEY (passager_id) REFERENCES utilisateurs(id)
    )''')
    
    conn.commit()
    
    # Appliquer les migrations
    migrate_db(conn)
    
    conn.close()
    print("✓ Base de données initialisée")