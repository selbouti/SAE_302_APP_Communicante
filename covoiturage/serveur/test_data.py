# ============= config_db/database.py =============
import sqlite3

DB_FILE = "covoiturage.db"

def get_db():
    """
    Get a database connection.
    
    Returns:
        sqlite3.Connection: A connection to the database with row factory enabled
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def _column_exists(conn, table, column) -> bool:
    """
    Check if a column exists in a table.
    
    Args:
        conn: Database connection
        table: Table name
        column: Column name
        
    Returns:
        bool: True if column exists, False otherwise
    """
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in c.fetchall()]
    return column in cols

def migrate_db(conn):
    """
    Migrate the database to add missing columns/tables.
    
    Args:
        conn: Database connection
    """
    c = conn.cursor()

    # ===== Table voitures =====
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='voitures'")
    if not c.fetchone():
        print("✓ Création table voitures...")
        c.execute('''CREATE TABLE voitures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur_id INTEGER UNIQUE NOT NULL,
            marque TEXT NOT NULL,
            modele TEXT NOT NULL,
            chevaux_fiscaux INTEGER NOT NULL,
            motorisation TEXT NOT NULL,
            taux_co2 REAL NOT NULL,
            places_max INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
        )''')
    else:
        for col, col_type in [
            ("marque", "TEXT NOT NULL"),
            ("modele", "TEXT NOT NULL"),
            ("chevaux_fiscaux", "INTEGER"),
            ("motorisation", "TEXT"),
            ("taux_co2", "REAL"),
            ("places_max", "INTEGER")
        ]:
            if not _column_exists(conn, "voitures", col):
                print(f"✓ Ajout colonne {col} à voitures...")
                c.execute(f'ALTER TABLE voitures ADD COLUMN {col} {col_type}')

        print("✓ Création index unique (voitures.utilisateur_id)...")
        c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_voitures_user_unique ON voitures(utilisateur_id)')

    # ===== Table emplois_du_temps (EDT) =====
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emplois_du_temps'")
    if not c.fetchone():
        print("✓ Création table emplois_du_temps...")
        c.execute('''CREATE TABLE emplois_du_temps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur_id INTEGER UNIQUE,
            source_type TEXT NOT NULL CHECK (source_type IN ('fichier','url')),
            source TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
        )''')

    # ===== Table trajets - ajouter colonnes manquantes =====
    c.execute("PRAGMA table_info(trajets)")
    columns = [col[1] for col in c.fetchall()]
    
    for col, col_type, default in [
        ("voiture_id", "INTEGER", None),
        ("jour_semaine", "TEXT", None),
        ("heure_depart", "TEXT", None),
        ("heure_retour", "TEXT", None),
        ("mode", "TEXT", '"conducteur"')
    ]:
        if col not in columns:
            print(f"✓ Ajout colonne {col} à trajets...")
            default_sql = f" DEFAULT {default}" if default else ""
            c.execute(f'ALTER TABLE trajets ADD COLUMN {col} {col_type}{default_sql}')

    conn.commit()

def init_db():
    """Initialize the database with all required tables."""
    conn = get_db()
    c = conn.cursor()

    # ===== Table utilisateurs =====
    c.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        nom TEXT,
        prenom TEXT,
        telephone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # ===== Table voitures =====
    c.execute('''CREATE TABLE IF NOT EXISTS voitures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilisateur_id INTEGER UNIQUE NOT NULL,
        marque TEXT NOT NULL,
        modele TEXT NOT NULL,
        chevaux_fiscaux INTEGER NOT NULL,
        motorisation TEXT NOT NULL,
        taux_co2 REAL NOT NULL,
        places_max INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
    )''')

    # ===== Table trajets =====
    c.execute('''CREATE TABLE IF NOT EXISTS trajets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilisateur_id INTEGER,
        voiture_id INTEGER,
        depart TEXT,
        arrivee TEXT,
        date_depart TEXT,
        jour_semaine TEXT,
        heure_depart TEXT,
        heure_retour TEXT,
        prix_par_place REAL,
        mode TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id),
        FOREIGN KEY (voiture_id) REFERENCES voitures(id)
    )''')

    # ===== Table reservations =====
    c.execute('''CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trajet_id INTEGER,
        passager_id INTEGER,
        places_reservees INTEGER,
        statut TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (trajet_id) REFERENCES trajets(id),
        FOREIGN KEY (passager_id) REFERENCES utilisateurs(id)
    )''')

    # ===== Table invitations =====
    c.execute('''CREATE TABLE IF NOT EXISTS invitations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trajet_id INTEGER,
        passager_id INTEGER,
        statut TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (trajet_id) REFERENCES trajets(id),
        FOREIGN KEY (passager_id) REFERENCES utilisateurs(id)
    )''')

    conn.commit()

    # ===== Migration pour colonnes / tables manquantes =====
    migrate_db(conn)
    conn.close()
    print("✓ Base de données initialisée et migrée avec succès")