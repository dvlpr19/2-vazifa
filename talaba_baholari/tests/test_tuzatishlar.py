"""Topilgan muammolar uchun testlar (har biri HISOBOT.md dagi muammoga mos)."""
import os
import sys
import importlib
import unittest
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


if __name__ == "__main__":
    unittest.main()
