import sqlite3


class ContextManager:
    def __init__(self, db_path="./src/db/context.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # create the table
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS context (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            content TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
        )

    def insert_context(self, user: str, content: str, role: str):
        """Insert a new row into the context table."""
        self.cursor.execute(
            "INSERT INTO context (user, content, role) VALUES (?, ?, ?)",
            (user, content, role),
        )
        self.conn.commit()

        print(f"✅ Added context: user={user}, role={role}")

    def get_contexts_by_user(self, user: str):
        """Fetch all context rows for a given user."""

        self.cursor.execute(
            "SELECT id, user, content, role FROM context WHERE user = ?", (user,)
        )
        rows = self.cursor.fetchall()

        self.conn.close()
        return rows


db = ContextManager()
