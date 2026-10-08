"""CSV va JSON fayllardan ma'lumot yuklash."""

import csv
import json
from datetime import datetime

import db


def sanani_oqish(matn):
    """Sanani 'kun.oy.yil' formatidan o'qiydi, masalan 15.09.2024."""
    return datetime.strptime(matn.strip(), "%d.%m.%Y").date()


def csv_dan_yuklash(conn, papka):
    """papka/talabalar.csv va papka/baholar.csv fayllarini bazaga yuklaydi."""
    with open(f"{papka}/talabalar.csv", newline="") as f:
        for qator in csv.DictReader(f):
            db.talaba_qoshish(conn, qator["ism"].strip(), qator["guruh"].strip())

    with open(f"{papka}/baholar.csv", newline="") as f:
        for qator in csv.DictReader(f):
            talaba_id = db.talaba_id_olish(conn, qator["ism"].strip())
            sana = sanani_oqish(qator["sana"])
            db.baho_qoshish(
                conn,
                talaba_id,
                qator["fan"].strip(),
                int(qator["baho"]),
                sana.isoformat(),
            )


def json_dan_yuklash(conn, fayl_yoli):
    """Qo'shimcha baholarni JSON fayldan yuklaydi.

    Format: [{"ism": "...", "fan": "...", "baho": 80, "sana": "15.09.2024"}, ...]
    """
    with open(fayl_yoli, "rb") as f:
        malumot = json.loads(f.read(), encoding="utf-8")

    for yozuv in malumot:
        talaba_id = db.talaba_id_olish(conn, yozuv["ism"])
        sana = sanani_oqish(yozuv["sana"])
        db.baho_qoshish(conn, talaba_id, yozuv["fan"], int(yozuv["baho"]), sana.isoformat())
