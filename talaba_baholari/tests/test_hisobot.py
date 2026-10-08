import os
import sys
import unittest
from datetime import date
import db# noqa: E402
import hisobot  # noqa: E402
import importer  # noqa: E402


LOYIHA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LOYIHA)


TEST_DATA = os.path.join(LOYIHA, "test_data")


class HisobotTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.ulanish(":memory:")
        db.jadvallarni_yaratish(self.conn)
        importer.csv_dan_yuklash(self.conn, TEST_DATA)

    def tearDown(self):
        self.conn.close()

    def natija(self, ism):
        for n in hisobot.hisobot_tuzish(self.conn):
            if n["ism"] == ism:
                return n
        self.fail(f"{ism} topilmadi")

    def test_talabalar_soni(self):
        self.assertEqual(len(db.barcha_talabalar(self.conn)), 4)

    def test_ortacha_baho(self):
        self.assertEqual(self.natija("Aliyev Bobur")["ortacha"], 85.0)
        self.assertEqual(self.natija("Saidova Nilufar")["ortacha"], 88.3)

    def test_otgan_talaba(self):
        self.assertTrue(self.natija("Karimova Madina")["otdi"])

    def test_yiqilgan_talaba(self):
        self.assertFalse(self.natija("Rashidov Jasur")["otdi"])

    def test_otmaganlar_royxati(self):
        natijalar = hisobot.hisobot_tuzish(self.conn)
        self.assertEqual(hisobot.otmaganlar(natijalar), ["Rashidov Jasur"])

    def test_qidiruv(self):
        topilganlar = db.talaba_topish(self.conn, "Ali")
        self.assertEqual([t["ism"] for t in topilganlar], ["Aliyev Bobur"])

    def test_sanani_oqish(self):
        self.assertEqual(importer.sanani_oqish("02.09.2024"), date(2024, 9, 2))


if __name__ == "__main__":
    unittest.main()
