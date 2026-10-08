"""SQLite ma'lumotlar bazasi bilan ishlash."""

import sqlite3

from config import DB_PATH


def ulanish(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def jadvallarni_yaratish(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS talabalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ism TEXT NOT NULL UNIQUE,
            guruh TEXT
        );
        CREATE TABLE IF NOT EXISTS baholar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            talaba_id INTEGER NOT NULL REFERENCES talabalar(id),
            fan TEXT NOT NULL,
            baho INTEGER NOT NULL,
            sana TEXT NOT NULL
        );
        """
    )


def talaba_qoshish(conn, ism, guruh):
    cur = conn.execute(
        "INSERT INTO talabalar (ism, guruh) VALUES (?, ?)", (ism, guruh)
    )
    conn.commit()
    return cur.lastrowid


def baho_qoshish(conn, talaba_id, fan, baho, sana):
    conn.execute(
        "INSERT INTO baholar (talaba_id, fan, baho, sana) VALUES (?, ?, ?, ?)",
        (talaba_id, fan, baho, sana),
    )
    conn.commit()


def talaba_id_olish(conn, ism):
    qator = conn.execute(
        "SELECT id FROM talabalar WHERE ism = ?", (ism,)
    ).fetchone()
    return qator["id"] if qator else None


def talaba_topish(conn, ism):
    """Ismida berilgan matn qatnashgan talabalarni qaytaradi."""
    return conn.execute(
        "SELECT * FROM talabalar WHERE ism LIKE ?", (f"%{ism}%",)
    ).fetchall()


def barcha_talabalar(conn):
    return conn.execute("SELECT * FROM talabalar ORDER BY ism").fetchall()


def talaba_baholari(conn, talaba_id):
    return conn.execute(
        "SELECT fan, baho, sana FROM baholar WHERE talaba_id = ?", (talaba_id,)
    ).fetchall()
