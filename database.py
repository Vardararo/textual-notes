'''App DB'''

import pathlib
import sqlite3

DATABASE_PATH = pathlib.Path().home() / "notes.db"

class Database:
    def __init__(self, db_path=DATABASE_PATH):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self._create_table()

    def _create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS contacts(
                id INTEGER PRIMARY KEY,
                subject TEXT,
                text TEXT
            );
        """
        self._run_query(query)

    def _run_query(self, query, *query_args):
        result = self.cursor.execute(query, [*query_args])
        self.db.commit()
        return result
# End-of-file (EOF)
