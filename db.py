# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        time TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_chat(q, a, t):
    with sqlite3.connect("chat.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (question, answer, time) VALUES (?, ?, ?)",
            (q, a, t)
        )
        conn.commit()#存到資料庫裡