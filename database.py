'''App DB'''

import pathlib
import sqlite3

DATABASE_PATH = pathlib.Path().home() / "notes.db"

class Database:
    '''Database for the Notes application'''

    def __init__(self, db_path=DATABASE_PATH):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self._create_table()

    def _create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS notes(
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

    def get_all_notes(self):
        result = self._run_query("SELECT * FROM notes;")
        return result.fetchall()

    def get_last_note(self):
        result = self._run_query(
            "SELECT * FROM notes ORDER BY id DESC LIMIT 1;"
        )
        return result.fetchone()

    def add_new_note(self, note):
        self._run_query(
            "INSERT INTO notes VALUES (NULL, ?, ?);", *note,
        )

    def delete_note(self, note_id):
        self._run_query(
            "DELETE FROM notes WHERE id=(?);", note_id,
        )

    def clear_all_notes(self):
        self._run_query("DELETE FROM notes;")
# End-of-file (EOF)
