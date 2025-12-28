from config_db.database import get_db

class Database:
    @staticmethod
    def execute(query, params=()):
        conn = get_db()
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        result = c.fetchall()
        conn.close()
        return result
    
    @staticmethod
    def execute_one(query, params=()):
        conn = get_db()
        c = conn.cursor()
        c.execute(query, params)
        result = c.fetchone()
        conn.close()
        return result
    
    @staticmethod
    def insert(query, params=()):
        conn = get_db()
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        last_id = c.lastrowid
        conn.close()
        return last_id