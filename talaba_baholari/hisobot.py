"""O'rtacha baholar va o'tish natijalarini hisoblash."""

import db
from config import FAN_KREDITLARI, OTISH_BALI


def ortacha_baho(baholar):
    return sum(baholar) / len(baholar)


def vaznli_ortacha(baholar, fanlar):
    """Fan kreditlarini hisobga olgan holda o'rtacha baho."""
    vaznlar = [FAN_KREDITLARI.get(fan, 1) for fan in fanlar]
    return sum(b * v for b, v in zip(baholar, vaznlar)) / sum(vaznlar)


def otdimi(ortacha):
    """O'rtacha baho OTISH_BALI va undan yuqori bo'lsa True qaytaradi."""
    return ortacha >= OTISH_BALI


def otmaganlar(natijalar, royxat=None):
    """Natijalar ichidan o'tmagan talabalarning ismlarini qaytaradi."""
    if royxat is None:
        royxat = []
    for n in natijalar:
        if not n["otdi"]:
            royxat.append(n["ism"])
    return royxat


def hisobot_tuzish(conn, vaznli=False):
    natijalar = []
    for talaba in db.barcha_talabalar(conn):
        qatorlar = db.talaba_baholari(conn, talaba["id"])
        baholar = [q["baho"] for q in qatorlar]

        if vaznli:
            ortacha = vaznli_ortacha(baholar, [q["fan"] for q in qatorlar])
        else:
            ortacha = ortacha_baho(baholar)

        natijalar.append(
            {
                "ism": talaba["ism"],
                "guruh": talaba["guruh"],
                "ortacha": round(ortacha, 1),
                "otdi": otdimi(ortacha),
            }
        )
    return natijalar
