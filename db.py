import sqlite3
from sqlite3 import Connection, OperationalError
from pathlib import Path
from typing import Optional

TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pdf_name TEXT NOT NULL,
    page INTEGER,
    subject TEXT,
    question_text TEXT NOT NULL,
    answer_options TEXT,
    chapter TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db(db_path: Path) -> Optional[Connection]:
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path))
        return conn
    except OperationalError as e:
        print(f"SQLite operational error while opening DB {db_path}: {e}")
    except Exception as e:
        print(f"Unexpected error while opening DB {db_path}: {e}")
    return None


def ensure_table(conn: Connection) -> bool:
    try:
        cur = conn.cursor()
        cur.executescript(TABLE_SCHEMA)
        conn.commit()
        # Ensure columns exist (handle upgrades)
        cur.execute("PRAGMA table_info('questions')")
        existing = {row[1] for row in cur.fetchall()}  # name is at index 1
        needed = {"subject", "answer_options", "chapter"}
        to_add = needed - existing
        for col in to_add:
            try:
                cur.execute(f"ALTER TABLE questions ADD COLUMN {col} TEXT")
            except Exception as e:
                print(f"Failed to add column {col}: {e}")
        conn.commit()
        return True
    except OperationalError as e:
        print(f"Failed to create/verify questions table: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error while ensuring table: {e}")
        return False


def insert_question(
    conn: Connection,
    pdf_name: str,
    page: int,
    question_text: str,
    answer_options: str | None = None,
    subject: str | None = None,
    chapter: str | None = None,
) -> bool:
    try:
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO questions (pdf_name, page, subject, question_text, answer_options, chapter) VALUES (?, ?, ?, ?, ?, ?)",
            (pdf_name, page, subject, question_text, answer_options, chapter),
        )
        conn.commit()
        cur.execute('select * from questions')
        row = cur.fetchall()
        for row in row:
            print(row)
        return True
    except Exception as e:
        print(f"Failed to insert question into DB: {e}")
        try:
            conn.rollback()
        except Exception:
            pass
        return False




def close_db(conn: Connection) -> None:
    try:
        conn.close()
    except Exception:
        pass
