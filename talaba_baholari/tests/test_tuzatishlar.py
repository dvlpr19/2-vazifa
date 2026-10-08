"""Topilgan muammolar uchun testlar (har biri HISOBOT.md dagi muammoga mos)."""
import os
import sys
import unittest

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


if __name__ == "__main__":
    unittest.main()
