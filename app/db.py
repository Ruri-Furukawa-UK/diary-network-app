# app/db.py
import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "diary.db")

def init_db():
    """テーブルがなければ作成"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            content TEXT,
            topics TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(content, topics):
    """日記を追加"""
    date = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO diary (date, content, topics) VALUES (?, ?, ?)",
        (date, content, ", ".join(topics))
    )
    conn.commit()
    conn.close()

def delete_entry(entry_id):
    """日記を削除"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM diary WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def load_entries():
    """日記一覧を取得"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, date, content, topics FROM diary ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data
