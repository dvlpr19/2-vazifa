"""Topilgan muammolar uchun testlar (har biri HISOBOT.md dagi muammoga mos)."""
import os
import sys
import importlib
import json
import subprocess
import tempfile
import unittest
from datetime import date
from unittest import mock

LOYIHA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LOYIHA)

import db  # noqa: E402
import hisobot  # noqa: E402
import importer  # noqa: E402

HAQIQIY_DATA = os.path.join(LOYIHA, "haqiqiy_data")


def bosh_baza():
    conn = db.ulanish(":memory:")
    db.jadvallarni_yaratish(conn)
    return conn


class OtishBaliTest(unittest.TestCase):
    """Muammo: otdimi() da > ishlatilgan, 55 ham o'tish bali."""

    def test_aynan_otish_bali_otadi(self):
        self.assertTrue(hisobot.otdimi(55))
        self.assertTrue(hisobot.otdimi(55.0))
        self.assertFalse(hisobot.otdimi(54.9))


class OtmaganlarTest(unittest.TestCase):
    """Muammo: otmaganlar() ning royxat=[] standart qiymati chaqiruvlar orasida umumiy."""

    def test_ikki_marta_chaqirilsa_royxat_toplanmaydi(self):
        natijalar = [{"ism": "A", "otdi": False}, {"ism": "B", "otdi": True}]
        self.assertEqual(hisobot.otmaganlar(natijalar), ["A"])
        self.assertEqual(hisobot.otmaganlar(natijalar), ["A"])


class VaznliOrtachaTest(unittest.TestCase):
    """Muammo: statistics.weighted_mean degan funksiya mavjud emas."""

    def test_kreditlar_hisobga_olinadi(self):
        # Matematika 4 kredit, Ingliz tili 2 kredit: (50*4 + 60*2) / 6
        self.assertAlmostEqual(
            hisobot.vaznli_ortacha([50, 60], ["Matematika", "Ingliz tili"]), 320 / 6
        )

    def test_royxatda_yoq_fan_1_kredit(self):
        # Matematika 4, "Kimyo" ro'yxatda yo'q -> 1: (80*4 + 30*1) / 5
        self.assertAlmostEqual(hisobot.vaznli_ortacha([80, 30], ["Matematika", "Kimyo"]), 70)


class QidiruvSqlInjectionTest(unittest.TestCase):
    """Muammo: talaba_topish() so'rovni f-string bilan yig'adi (SQL injection)."""

    def setUp(self):
        self.conn = bosh_baza()
        db.talaba_qoshish(self.conn, "Aliyev Bobur", "IT-21")
        db.talaba_qoshish(self.conn, "Karimova Madina", "IT-21")

    def test_injection_hamma_talabani_qaytarmaydi(self):
        self.assertEqual(db.talaba_topish(self.conn, "' OR '1'='1"), [])

    def test_apostrofli_qidiruv_xato_bermaydi(self):
        db.talaba_qoshish(self.conn, "O'tkir Rahimov", "IT-21")
        topildi = db.talaba_topish(self.conn, "O'tkir")
        self.assertEqual([t["ism"] for t in topildi], ["O'tkir Rahimov"])


class MaxfiyTokenTest(unittest.TestCase):
    """Muammo: Telegram bot tokeni kodning ichida ochiq yozilgan."""

    def tearDown(self):
        import config
        importlib.reload(config)

    def test_token_muhit_ozgaruvchisidan_olinadi(self):
        import config
        with mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "env-token",
                                          "ADMIN_CHAT_ID": "42"}):
            importlib.reload(config)
            self.assertEqual(config.TELEGRAM_BOT_TOKEN, "env-token")
            self.assertEqual(config.ADMIN_CHAT_ID, "42")

    def test_kodda_token_yoq(self):
        with open(os.path.join(LOYIHA, "config.py"), encoding="utf-8") as f:
            self.assertNotIn("AAH3kLmP9xQ2vR8sT1uW4yZ6bC0dE5fG7hJ", f.read())


class JsonYuklashTest(unittest.TestCase):
    """Muammo: json.loads(..., encoding=...) Python 3.9 dan beri TypeError beradi."""

    def test_json_dan_baho_yuklanadi(self):
        conn = bosh_baza()
        talaba_id = db.talaba_qoshish(conn, "Dilnoza Yusupova", "IT-22")
        with tempfile.TemporaryDirectory() as papka:
            yol = os.path.join(papka, "q.json")
            with open(yol, "w", encoding="utf-8") as f:
                json.dump([{"ism": "Dilnoza Yusupova", "fan": "Tarix",
                            "baho": 77, "sana": "20.09.2024"}], f)
            importer.json_dan_yuklash(conn, yol)
        baholar = db.talaba_baholari(conn, talaba_id)
        self.assertEqual([(b["fan"], b["baho"], b["sana"]) for b in baholar],
                         [("Tarix", 77, "2024-09-20")])


class CsvKodlashTest(unittest.TestCase):
    """Muammo: CSV fayllar encoding ko'rsatilmasdan ochiladi — tizim kodlashiga bog'liq."""

    def test_utf8_bolmagan_tizimda_ham_oqiladi(self):
        with tempfile.TemporaryDirectory() as papka:
            with open(os.path.join(papka, "talabalar.csv"), "w", encoding="utf-8") as f:
                f.write("ism,guruh\nO\u02bbtkir Rahimov,IT-21\n")
            with open(os.path.join(papka, "baholar.csv"), "w", encoding="utf-8") as f:
                f.write("ism,fan,baho,sana\nO\u02bbtkir Rahimov,Fizika,70,15.09.2024\n")
            kod = (
                "import db, importer\n"
                "c = db.ulanish(':memory:'); db.jadvallarni_yaratish(c)\n"
                f"importer.csv_dan_yuklash(c, {papka!r})\n"
                "print(len(db.barcha_talabalar(c)))\n"
            )
            # Windows yoki C/POSIX lokalli serverni taqlid qilamiz: standart kodlash ASCII
            muhit = {**os.environ, "LC_ALL": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"}
            natija = subprocess.run([sys.executable, "-c", kod], cwd=LOYIHA, env=muhit,
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(natija.returncode, 0, natija.stderr)
            self.assertEqual(natija.stdout.strip(), "1")


class SanaFormatiTest(unittest.TestCase):
    """Muammo: haqiqiy ma'lumotda sanalar ikki xil formatda (15.09.2024 va 2024-09-20)."""

    def test_ikkala_format_oqiladi(self):
        self.assertEqual(importer.sanani_oqish("15.09.2024"), date(2024, 9, 15))
        self.assertEqual(importer.sanani_oqish("2024-09-20"), date(2024, 9, 20))

    def test_notogri_sana_tushunarli_xato_beradi(self):
        with self.assertRaisesRegex(ValueError, "31.02.2024"):
            importer.sanani_oqish("31.02.2024")


if __name__ == "__main__":
    unittest.main()
