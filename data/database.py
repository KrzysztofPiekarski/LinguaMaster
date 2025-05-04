import sqlite3
import threading
from typing import List, Tuple

DB_PATH = "translations.db"

class DatabaseManager:
    _instance = None
    _local = threading.local()

    def __new__(cls, db_file: str = DB_PATH):
        """Singleton: Tylko jedna instancja klasy."""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.db_file = db_file
        return cls._instance

    def connect(self):
        """Zwraca bezpieczne połączenie z bazą danych."""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        return self._local.conn

    def close(self):
        """Zamyka połączenie z bazą danych."""
        if hasattr(self._local, 'conn') and self._local.conn:
            self._local.conn.close()
            self._local.conn = None

    def create_tables(self):
        """Tworzy tabele w bazie danych."""
        try:
            conn = self.connect()
            conn.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY,
                    original_text TEXT,
                    translated_text TEXT,
                    src_lang TEXT,
                    dest_lang TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vocabulary (
                    id INTEGER PRIMARY KEY,
                    word TEXT,
                    translation TEXT,
                    lang TEXT
                )
            """)
        except sqlite3.Error as e:
            print(f"[ERROR] {e}")

    def insert_translation(self, original_text: str, translated_text: str, src_lang: str, dest_lang: str):
        try:
            conn = self.connect()
            conn.execute("""
                INSERT INTO history (original_text, translated_text, src_lang, dest_lang)
                VALUES (?, ?, ?, ?)
            """, (original_text, translated_text, src_lang, dest_lang))
            conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] {e}")

    def insert_vocabulary(self, word: str, translation: str, lang: str):
        try:
            conn = self.connect()
            conn.execute("""
                INSERT INTO vocabulary (word, translation, lang)
                VALUES (?, ?, ?)
            """, (word, translation, lang))
            conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] {e}")

    def get_translation_history(self, limit: int = None) -> List[Tuple[int, str, str, str, str]]:
        try:
            conn = self.connect()
            query = """
                SELECT id, original_text, translated_text, src_lang, dest_lang
                FROM history
                ORDER BY id DESC
            """
            if limit is not None:
                query += f" LIMIT {limit}"
            return conn.execute(query).fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] {e}")
            return []

    def get_vocabulary(self) -> List[Tuple[int, str, str, str]]:
        try:
            conn = self.connect()
            return conn.execute("""
                SELECT id, word, translation, lang
                FROM vocabulary
            """).fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] {e}")
            return []

    def search_vocabulary(self, query: str) -> List[Tuple[int, str, str, str]]:
        try:
            conn = self.connect()
            return conn.execute("""
                SELECT id, word, translation, lang
                FROM vocabulary
                WHERE word LIKE ? OR translation LIKE ?
            """, (f'%{query}%', f'%{query}%')).fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] {e}")
            return []

    def delete_translation(self, translation_id: int):
        try:
            conn = self.connect()
            conn.execute("DELETE FROM history WHERE id = ?", (translation_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] {e}")

    def delete_vocabulary(self, vocabulary_id: int):
        try:
            conn = self.connect()
            conn.execute("DELETE FROM vocabulary WHERE id = ?", (vocabulary_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] {e}")
