import sqlite3
from contextlib import contextmanager
from app.config import DATA_DIR, DATABASE_PATH
from app.database.tables import SCHEMA

class Database:
    def __init__(self, path=DATABASE_PATH):
        self.path = path

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as conn:
            conn.executescript(SCHEMA)

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
