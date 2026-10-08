"""Talabalar baholari hisoboti.

Ishlatish:
    python main.py test_data
    python main.py test_data --vaznli
    python main.py test_data --json qoshimcha.json
    python main.py test_data --qidir "Ali"
"""

import argparse

import db
import hisobot
import importer


def main():
    parser = argparse.ArgumentParser(description="Talabalar baholari hisoboti")
    parser.add_argument("papka", help="talabalar.csv va baholar.csv joylashgan papka")
    parser.add_argument("--vaznli", action="store_true", help="fan kreditlari bo'yicha vaznli o'rtacha")
    parser.add_argument("--json", help="qo'shimcha baholar JSON fayli")
    parser.add_argument("--qidir", help="talabani ismi bo'yicha qidirish")
    args = parser.parse_args()

    conn = db.ulanish(":memory:")
    db.jadvallarni_yaratish(conn)
    importer.csv_dan_yuklash(conn, args.papka)
    if args.json:
        importer.json_dan_yuklash(conn, args.json)

    if args.qidir:
        for t in db.talaba_topish(conn, args.qidir):
            print(f"{t['id']:>3}  {t['ism']:<25} {t['guruh']}")
        return

    natijalar = hisobot.hisobot_tuzish(conn, vaznli=args.vaznli)
    for n in natijalar:
        holat = "O'TDI" if n["otdi"] else "YIQILDI"
        print(f"{n['ism']:<25} {n['guruh']:<8} {n['ortacha']:>6}  {holat}")

    print()
    print("O'tmaganlar:", ", ".join(hisobot.otmaganlar(natijalar)) or "yo'q")


if __name__ == "__main__":
    main()
