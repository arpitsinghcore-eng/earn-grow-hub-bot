import sqlite3
import json

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database.sqlite", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0,
            state TEXT,
            state_data TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS withdraws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
            amount REAL,
            method TEXT,
            details TEXT,
            status TEXT DEFAULT 'pending',
            admin_reason TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS gmail_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT,
            reward REAL,
            instructions TEXT,
            status TEXT DEFAULT 'available',
            assigned_to INTEGER
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS review_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT,
            place_name TEXT,
            required_stars INTEGER,
            keywords TEXT,
            reward REAL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
            task_type TEXT,
            task_id INTEGER,
            image_hash TEXT,
            status TEXT DEFAULT 'pending'
        )
        """)

        self.conn.commit()

        self.set_default("currency", "₹")
        self.set_default("min_withdraw", "50")
        self.set_default("auto_verify", "1")

    def set_default(self, key, value):
        self.cursor.execute(
            "INSERT OR IGNORE INTO settings (key,value) VALUES (?,?)",
            (key, value)
        )
        self.conn.commit()

    def get_setting(self, key):
        self.cursor.execute(
            "SELECT value FROM settings WHERE key=?",
            (key,)
        )
        row = self.cursor.fetchone()
        return row["value"] if row else ""

    def get_user(self, user_id):
        self.cursor.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )
        user = self.cursor.fetchone()

        if not user:
            self.cursor.execute(
                "INSERT INTO users (user_id) VALUES (?)",
                (user_id,)
            )
            self.conn.commit()

            self.cursor.execute(
                "SELECT * FROM users WHERE user_id=?",
                (user_id,)
            )
            user = self.cursor.fetchone()

        return user

    def update_balance(self, user_id, amount):
        self.cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id=?",
            (amount, user_id)
        )
        self.conn.commit()

    def set_state(self, user_id, state, data=None):
        state_data = json.dumps(data) if data else None
        self.cursor.execute("""
        UPDATE users
        SET state=?, state_data=?
        WHERE user_id=?
        """, (state, state_data, user_id))
        self.conn.commit()


db = Database()