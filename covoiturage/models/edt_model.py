# models/edt_model.py

from config.database import get_connection

class EDTModel:

    def get_edt(self, user_id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT * FROM EmploiDuTemps WHERE user_id=%s
        """, (user_id,))

        edt = cur.fetchone()
        cur.close()
        conn.close()
        return edt

    def save_edt_file(self, user_id, file_path):
        """Sauvegarde un EDT provenant d’un fichier local."""
        conn = get_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO EmploiDuTemps (user_id, source_type, source)
        VALUES (%s, 'fichier', %s)
        ON DUPLICATE KEY UPDATE source=%s, source_type='fichier'
        """

        cur.execute(sql, (user_id, file_path, file_path))
        conn.commit()

        cur.close()
        conn.close()

    def save_edt_url(self, user_id, url):
        """Sauvegarde un EDT provenant d’une URL."""
        conn = get_connection()
        cur = conn.cursor()

        sql = """
        INSERT INTO EmploiDuTemps (user_id, source_type, source)
        VALUES (%s, 'lien', %s)
        ON DUPLICATE KEY UPDATE source=%s, source_type='lien'
        """

        cur.execute(sql, (user_id, url, url))
        conn.commit()

        cur.close()
        conn.close()
