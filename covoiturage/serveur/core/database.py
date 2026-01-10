from config_db.database import get_db

class Database:
    """
    A utility class for interacting with the database.

    This class provides static methods to execute SQL queries, retrieve data, 
    and insert new records into the database. It uses a connection obtained 
    from the `get_db` function to interact with the database.

    Methods:
        execute(query, params=()): Executes a SQL query and returns all results.
        execute_one(query, params=()): Executes a SQL query and returns a single result.
        insert(query, params=()): Executes an INSERT query and returns the last inserted ID.
    """

    @staticmethod
    def execute(query, params=()):
        """
        Execute a SQL query and return all results.

        Args:
            query (str): The SQL query to execute.
            params (tuple): The parameters to bind to the query (default is an empty tuple).

        Returns:
            list: A list of rows returned by the query.
        """
        conn = get_db()
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        result = c.fetchall()
        conn.close()
        return result
    
    @staticmethod
    def execute_one(query, params=()):
        """
        Execute a SQL query and return a single result.

        Args:
            query (str): The SQL query to execute.
            params (tuple): The parameters to bind to the query (default is an empty tuple).

        Returns:
            tuple: A single row returned by the query, or None if no result is found.
        """
        conn = get_db()
        c = conn.cursor()
        c.execute(query, params)
        result = c.fetchone()
        conn.close()
        return result
    
    @staticmethod
    def insert(query, params=()):
        """
        Execute an INSERT SQL query and return the last inserted ID.

        Args:
            query (str): The SQL query to execute.
            params (tuple): The parameters to bind to the query (default is an empty tuple).

        Returns:
            int: The ID of the last inserted row.
        """
        conn = get_db()
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        last_id = c.lastrowid
        conn.close()
        return last_id