"""SQLite ma'lumotlar bazasi bilan ishlash."""

import sqlite3

from config import DB_PATH

# O'zbek tilidagi o' va g' turli manbalarda turlicha yoziladi:
# ' (U+0027), ʻ (U+02BB), ʼ (U+02BC), ‘ (U+2018), ’ (U+2019), ` (U+0060).
# Ismlarni solishtirish uchun hammasini bitta ' ga keltiramiz.
APOSTROFLAR = str.maketrans({c: "'" for c in "\u02bb\u02bc\u2018\u2019`"})


def ismni_tozalash(ism):
    return ism.strip().translate(APOSTROFLAR)


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
        "INSERT INTO talabalar (ism, guruh) VALUES (?, ?)", (ismni_tozalash(ism), guruh)
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
        "SELECT id FROM talabalar WHERE ism = ?", (ismni_tozalash(ism),)
    ).fetchone()
    return qator["id"] if qator else None


def talaba_topish(conn, ism):
    """Ismida berilgan matn qatnashgan talabalarni qaytaradi."""
    return conn.execute(
        "SELECT * FROM talabalar WHERE ism LIKE ?", (f"%{ismni_tozalash(ism)}%",)
    ).fetchall()


def barcha_talabalar(conn):
    return conn.execute("SELECT * FROM talabalar ORDER BY ism").fetchall()


def talaba_baholari(conn, talaba_id):
    return conn.execute(
        "SELECT fan, baho, sana FROM baholar WHERE talaba_id = ?", (talaba_id,)
    ).fetchall()
