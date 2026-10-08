"""CSV va JSON fayllardan ma'lumot yuklash."""

import csv
import json
from datetime import datetime

import db


SANA_FORMATLARI = ("%d.%m.%Y", "%Y-%m-%d")


def sanani_oqish(matn):
    """Sanani o'qiydi: 'kun.oy.yil' (15.09.2024) yoki ISO 'yil-oy-kun' (2024-09-15)."""
    for fmt in SANA_FORMATLARI:
        try:
            return datetime.strptime(matn.strip(), fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Sana noto'g'ri yoki noma'lum formatda: {matn!r}")


def _talaba_id(conn, ism, manba):
    talaba_id = db.talaba_id_olish(conn, ism)
    if talaba_id is None:
        raise ValueError(f"{manba}: {ism!r} talabalar ro'yxatida yo'q")
    return talaba_id


def csv_dan_yuklash(conn, papka):
    """papka/talabalar.csv va papka/baholar.csv fayllarini bazaga yuklaydi."""
    with open(f"{papka}/talabalar.csv", newline="", encoding="utf-8") as f:
        for qator in csv.DictReader(f):
            db.talaba_qoshish(conn, qator["ism"].strip(), qator["guruh"].strip())

    with open(f"{papka}/baholar.csv", newline="", encoding="utf-8") as f:
        for qator in csv.DictReader(f):
            talaba_id = _talaba_id(conn, qator["ism"], "baholar.csv")
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
    with open(fayl_yoli, encoding="utf-8") as f:
        malumot = json.load(f)

    for yozuv in malumot:
        talaba_id = _talaba_id(conn, yozuv["ism"], fayl_yoli)
        sana = sanani_oqish(yozuv["sana"])
        db.baho_qoshish(conn, talaba_id, yozuv["fan"], int(yozuv["baho"]), sana.isoformat())
