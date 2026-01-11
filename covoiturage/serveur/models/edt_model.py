# models/edt_model.py

from config.database import get_connection


class EDTModel:
    """
    Model handling user schedules (EDT - Emploi du Temps).

    This class provides methods to retrieve, store, and replace
    a user's schedule, either from a file or a URL.

    Each user can have only one schedule at a time.
    """

    def get_edt(self, user_id):
        """
        Retrieve the current schedule for a given user.

        :param user_id: Identifier of the user
        :type user_id: int
        :return: Schedule data or None if not found
        :rtype: dict or None
        """
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT user_id, source_type, source
            FROM EmploiDuTemps
            WHERE user_id = %s
            LIMIT 1
        """, (user_id,))

        edt = cur.fetchone()

        # IMPORTANT: clear remaining results
        cur.fetchall()

        cur.close()
        conn.close()
        return edt

    # -----------------------------
    #  Save EDT from file
    # -----------------------------
    def save_edt_file(self, user_id, file_path):
        """
        Save a schedule for a user using a local file path.

        :param user_id: Identifier of the user
        :type user_id: int
        :param file_path: Path to the EDT file
        :type file_path: str
        """
        self._replace_edt(user_id, "fichier", file_path)

    # -----------------------------
    #  Save EDT from URL
    # -----------------------------
    def save_edt_url(self, user_id, url):
        """
        Save a schedule for a user using a remote URL.

        :param user_id: Identifier of the user
        :type user_id: int
        :param url: URL pointing to the schedule
        :type url: str
        """
        self._replace_edt(user_id, "url", url)

    # -----------------------------
    #  Replace existing EDT
    # -----------------------------
    def _replace_edt(self, user_id, source_type, source):
        """
        Replace the user's existing schedule.

        This method removes any existing schedule for the user
        and inserts a new one. Only one schedule is allowed
        per user.

        :param user_id: Identifier of the user
        :type user_id: int
        :param source_type: Type of source ("fichier" or "url")
        :type source_type: str
        :param source: File path or URL
        :type source: str
        """
        conn = get_connection()
        cur = conn.cursor()

        # Delete existing EDT
        cur.execute(
            "DELETE FROM EmploiDuTemps WHERE user_id = %s",
            (user_id,)
        )

        # Insert new EDT
        cur.execute("""
            INSERT INTO EmploiDuTemps (user_id, source_type, source)
            VALUES (%s, %s, %s)
        """, (user_id, source_type, source))

        conn.commit()
        cur.close()
        conn.close()
