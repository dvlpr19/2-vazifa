# 2-vazifa: Hisobot

**Ism-familiya:**
**AI chat tarixi (link yoki fayl nomi):**

Qator raqamlari **boshlang'ich koddagi** (birinchi commit `Boshlang'ich kod`) holatga ko'ra.
Har bir muammo alohida commitda tuzatilgan. Testlar `talaba_baholari/tests/test_tuzatishlar.py` faylida.
Har bir test tuzatishdan oldin ishga tushirilib, yiqilgani tekshirilgan (xato matni "Tuzatishdan oldin" qatorida).

Barcha testlar:
```bash
cd talaba_baholari
python -m unittest discover -s tests -v
```

---

## Muammo 1 — Telegram bot tokeni kodda ochiq yozilgan

- **Fayl va qator:** `config.py:6-7`
- **Turi:** xavfsizlik
- **Jiddiyligi:** yuqori
- **Nima bo'ladi?** Kodni ko'rgan har kim (GitHub, server, arxiv) botni to'liq boshqara oladi: xabar yuborish, bot nomidan yozish, kelgan xabarlarni o'qish.
- **Nega shunday bo'ladi?** Maxfiy kalit (`TELEGRAM_BOT_TOKEN`) va `ADMIN_CHAT_ID` to'g'ridan-to'g'ri manba kodga yozilgan.
- **Qanday tuzatdingiz?** Qiymatlar `os.environ.get("TELEGRAM_BOT_TOKEN")` / `os.environ.get("ADMIN_CHAT_ID")` orqali muhit o'zgaruvchilaridan olinadi.
  **Muhim:** token allaqachon oshkor bo'lgan (git tarixida ham bor), shuning uchun kodni tuzatish yetarli emas — tokenni @BotFather orqali **bekor qilib (revoke), yangisini olish** kerak.
- **Qaysi test buni tekshiradi?** `MaxfiyTokenTest` (token muhitdan o'qiladi; `config.py` matnida token yo'q).
  Tuzatishdan oldin: `AssertionError: '7412398765:AAH...' != 'env-token'`
- **Buni kim topdi?** AI topdi, testi bilan tasdiqlandi

---

## Muammo 2 — Qidiruvda SQL injection

- **Fayl va qator:** `db.py:58`
- **Turi:** xavfsizlik
- **Jiddiyligi:** yuqori
- **Nima bo'ladi?** `--qidir "' OR '1'='1"` barcha talabalarni qaytaradi; yanada yomon so'rov bilan bazadagi boshqa ma'lumotni ham o'qish mumkin. Oddiy apostrofli ism ham dasturni yiqitadi: `--qidir "O'tkir"` → `sqlite3.OperationalError: near "tkir": syntax error`.
- **Nega shunday bo'ladi?** So'rov f-string bilan yig'ilgan: `f"... LIKE '%{ism}%'"`. Foydalanuvchi kiritgan matn SQL kodining bir qismiga aylanadi.
- **Qanday tuzatdingiz?** Parametrli so'rov: `conn.execute("... WHERE ism LIKE ?", (f"%{ism}%",))`. Endi matn har doim ma'lumot sifatida uzatiladi.
- **Qaysi test buni tekshiradi?** `QidiruvSqlInjectionTest` (injection hamma talabani qaytarmaydi; apostrofli qidiruv ishlaydi).
  Tuzatishdan oldin: `sqlite3.OperationalError: near "tkir": syntax error` va `Lists differ: [<Row>, <Row>] != []`
- **Buni kim topdi?** AI topdi, testi bilan tasdiqlandi

---

## Muammo 3 — Haqiqiy ma'lumotda ikki xil sana formati

- **Fayl va qator:** `importer.py:12`
- **Turi:** ma'lumotga bog'liq
- **Jiddiyligi:** yuqori
- **Nima bo'ladi?** `python main.py haqiqiy_data` darhol yiqiladi: `ValueError: time data '2024-09-20' does not match format '%d.%m.%Y'`. Hech bir buyruq ishlamaydi.
- **Nega shunday bo'ladi?** `haqiqiy_data/baholar.csv` da sanalar ham `15.09.2024`, ham `2024-09-20` (ISO) ko'rinishida. Kod faqat birinchisini qabul qiladi.
- **Qanday tuzatdingiz?** `sanani_oqish` ikkala formatni sinab ko'radi (`SANA_FORMATLARI`). Ikkalasi ham mos kelmasa, qaysi qiymat noto'g'ri ekanini ko'rsatadigan `ValueError` beradi.
- **Qaysi test buni tekshiradi?** `SanaFormatiTest`.
  Tuzatishdan oldin: `ValueError: time data '2024-09-20' does not match format '%d.%m.%Y'`
- **Buni kim topdi?** AI topdi (haqiqiy ma'lumotda ishga tushirib), testi bilan tasdiqlandi

---

## Muammo 4 — Ismlardagi turli apostroflar (Gʻulom / G'ulom)

- **Fayl va qator:** `importer.py:23`, `importer.py:43`, `db.py:33-59` (ism saqlash, `talaba_id_olish`, `talaba_topish`)
- **Turi:** ma'lumotga bog'liq
- **Jiddiyligi:** yuqori
- **Nima bo'ladi?** `talabalar.csv` da `Gʻulom Karimov` (`ʻ`, U+02BB), `baholar.csv` ning bir qatorida esa `G'ulom Karimov` (oddiy `'`). Talaba topilmaydi, `talaba_id = None` va dastur `sqlite3.IntegrityError: NOT NULL constraint failed: baholar.talaba_id` bilan yiqiladi. Shuningdek `--qidir "O'tkir"` (klaviaturadagi oddiy `'` bilan) bazadagi `Oʻtkir Rahimov` ni topmaydi.
- **Nega shunday bo'ladi?** O'zbekcha `oʻ`/`gʻ` turli manbalarda turli belgilar bilan yoziladi (`'`, `ʻ`, `ʼ`, `‘`, `’`, `` ` ``). Kod ismlarni belgima-belgi solishtiradi. Bundan tashqari, talaba topilmaganda kod buni tekshirmaydi va tushunarsiz baza xatosi chiqadi.
- **Qanday tuzatdingiz?** `db.ismni_tozalash()` — bo'sh joylarni olib tashlaydi va barcha apostrof turlarini `'` ga keltiradi. U ism saqlashda, ID qidirishda va `talaba_topish` da qo'llanadi. Importda talaba topilmasa, fayl nomi va ism ko'rsatilgan aniq `ValueError` chiqadi.
  (Natijada ismlar `'` bilan ko'rsatiladi: `G'ulom Karimov`.)
- **Qaysi test buni tekshiradi?** `ApostrofTest` (5 xil apostrof bir talabaga mos keladi; qidiruv apostrofga bog'liq emas; noma'lum talaba aniq xato beradi).
  Tuzatishdan oldin: `AssertionError: None != 1 : G'ulom Karimov`, `sqlite3.IntegrityError: NOT NULL constraint failed`
- **Buni kim topdi?** AI topdi (fayllardagi baytlarni ko'rib), testi bilan tasdiqlandi

---

## Muammo 5 — Bahosi yo'q talaba bo'lsa nolga bo'lish

- **Fayl va qator:** `hisobot.py:10`, `hisobot.py:38-41`, `main.py:39`
- **Turi:** ma'lumotga bog'liq
- **Jiddiyligi:** yuqori
- **Nima bo'ladi?** `python main.py haqiqiy_data` (`--json` siz) → `ZeroDivisionError: division by zero`. `Dilnoza Yusupova` ning baholari faqat `qoshimcha.json` da bor, CSV da yo'q.
- **Nega shunday bo'ladi?** `ortacha_baho` bo'sh ro'yxat uchun `sum([]) / len([])` = `0 / 0` hisoblaydi.
- **Qanday tuzatdingiz?** `hisobot_tuzish` da bahosi yo'q talaba uchun `ortacha = None`, `otdi = False` (o'tgan deb hisoblanmaydi). `main.py` bunday talabani `—  BAHO YO'Q` deb chiqaradi.
- **Qaysi test buni tekshiradi?** `BahosizTalabaTest` (oddiy va vaznli hisobot yiqilmaydi; `main.py` "BAHO YO'Q" chiqaradi).
  Tuzatishdan oldin: `ZeroDivisionError: division by zero`
- **Buni kim topdi?** AI topdi (haqiqiy ma'lumotda ishga tushirib), testi bilan tasdiqlandi

---

## Muammo 6 — `json.loads(..., encoding=...)` eskirgan

- **Fayl va qator:** `importer.py:40`
- **Turi:** eskirgan kod
- **Jiddiyligi:** yuqori
- **Nima bo'ladi?** `--json` bilan har qanday ishga tushirish: `TypeError: JSONDecoder.__init__() got an unexpected keyword argument 'encoding'`.
- **Nega shunday bo'ladi?** `json.loads` ning `encoding` argumenti Python 3.1 dan beri e'tiborsiz qoldirilgan va Python 3.9 da butunlay olib tashlangan.
- **Qanday tuzatdingiz?** Fayl `open(fayl_yoli, encoding="utf-8")` bilan ochiladi va `json.load(f)` ishlatiladi.
- **Qaysi test buni tekshiradi?** `JsonYuklashTest`.
  Tuzatishdan oldin: `TypeError: JSONDecoder.__init__() got an unexpected keyword argument 'encoding'`
- **Buni kim topdi?** AI topdi, testi bilan tasdiqlandi

---

## Muammo 7 — Mavjud bo'lmagan `statistics.weighted_mean`

- **Fayl va qator:** `hisobot.py:16`
- **Turi:** mavjud bo'lmagan funksiya
- **Jiddiyligi:** yuqori
- **Nima bo'ladi?** `--vaznli` hatto test ma'lumotida ham yiqiladi: `AttributeError: module 'statistics' has no attribute 'weighted_mean'`.
- **Nega shunday bo'ladi?** `statistics` modulida bunday funksiya yo'q (AI "to'qib chiqargan"). Python 3.11+ da `statistics.fmean(data, weights)` bor, lekin bu ham eski versiyalarda ishlamaydi.
- **Qanday tuzatdingiz?** Formula to'g'ridan-to'g'ri yozildi: `sum(baho * kredit) / sum(kredit)`. `import statistics` olib tashlandi.
- **Qaysi test buni tekshiradi?** `VaznliOrtachaTest` (kreditlar hisobga olinadi; ro'yxatda yo'q fan 1 kredit).
  Tuzatishdan oldin: `AttributeError: module 'statistics' has no attribute 'weighted_mean'`
- **Buni kim topdi?** AI topdi, testi bilan tasdiqlandi

---

## Muammo 8 — Aynan 55 ball olgan talaba "yiqilgan" chiqadi

- **Fayl va qator:** `hisobot.py:21`
- **Turi:** xato
- **Jiddiyligi:** yuqori (foydalanuvchilar shikoyat qilgan noto'g'ri natija)
- **Nima bo'ladi?** O'rtacha bahosi aynan 55 bo'lgan talaba `YIQILDI` deb chiqadi. Haqiqiy ma'lumotda: `Sardor Toshmatov` (50 va 60, o'rtacha 55.0).
- **Nega shunday bo'ladi?** `config.py` va `otdimi` izohida "55 **va undan yuqori**" deyilgan, lekin kodda `ortacha > OTISH_BALI` yozilgan.
- **Qanday tuzatdingiz?** `>` → `>=`.
- **Qaysi test buni tekshiradi?** `OtishBaliTest` (55 va 55.0 o'tadi, 54.9 o'tmaydi).
  Tuzatishdan oldin: `AssertionError: False is not true`
- **Buni kim topdi?** AI topdi, testi bilan tasdiqlandi

---

## Muammo 9 — `otmaganlar()` dagi o'zgaruvchan standart argument

- **Fayl va qator:** `hisobot.py:24`
- **Turi:** xato
- **Jiddiyligi:** o'rta
- **Nima bo'ladi?** `otmaganlar()` ikkinchi marta chaqirilganda oldingi natijalar ham ro'yxatda qoladi: `['A', 'A']`. Server kabi uzoq ishlaydigan jarayonda har bir hisobotda o'tmaganlar ro'yxati o'sib boradi va boshqa hisobotlardagi ismlar ham chiqadi. Hozirgi `main.py` funksiyani bir marta chaqirgani uchun bu ko'rinmaydi.
- **Nega shunday bo'ladi?** `royxat=[]` funksiya **aniqlanganda** bir marta yaratiladi va barcha chaqiruvlarda o'sha bitta ro'yxat ishlatiladi.
- **Qanday tuzatdingiz?** `royxat=None`, funksiya ichida `if royxat is None: royxat = []`.
- **Qaysi test buni tekshiradi?** `OtmaganlarTest` (ikki marta chaqirilganda ham natija `['A']`).
  Tuzatishdan oldin: `AssertionError: Lists differ: ['A', 'A'] != ['A']`
- **Buni kim topdi?** AI topdi, testi bilan tasdiqlandi

---

## Muammo 10 — CSV fayllar kodlash ko'rsatilmasdan ochiladi

- **Fayl va qator:** `importer.py:17`, `importer.py:21`
- **Turi:** ma'lumotga bog'liq (platformaga bog'liq)
- **Jiddiyligi:** o'rta
- **Nima bo'ladi?** Linux (UTF-8 lokal) da ishlaydi. Lekin Windows'da (cp1251/cp1252) yoki lokali `C`/`POSIX` bo'lgan serverda (Docker konteynerlar, cron) `Oʻtkir` kabi ismlar uchun `UnicodeDecodeError: 'ascii' codec can't decode byte 0xca` yoki buzilgan ismlar chiqadi.
- **Nega shunday bo'ladi?** `encoding` berilmasa, `open()` operatsion tizimning standart kodlashini ishlatadi. Fayllar esa UTF-8 da.
- **Qanday tuzatdingiz?** Ikkala `open()` ga `encoding="utf-8"` qo'shildi.
- **Qaysi test buni tekshiradi?** `CsvKodlashTest` — importni alohida jarayonda `LC_ALL=C` (ASCII standart kodlash) bilan ishga tushiradi.
  Tuzatishdan oldin: `UnicodeDecodeError: 'ascii' codec can't decode byte 0xca in position 11`
- **Buni kim topdi?** AI topdi, testi bilan tasdiqlandi

---

## Muammo 11 — Testlar faqat loyiha papkasidan ishlaydi

- **Fayl va qator:** `tests/test_hisobot.py:5-11`
- **Turi:** boshqa (test infratuzilmasi)
- **Jiddiyligi:** past
- **Nima bo'ladi?** Boshqa papkadan ishga tushirilsa (masalan CI'da `python -m unittest discover -s talaba_baholari/tests`) → `ImportError: Failed to import test module: test_hisobot`.
- **Nega shunday bo'ladi?** `import db` / `hisobot` / `importer` qatorlari `sys.path.insert(0, LOYIHA)` dan **oldin** yozilgan, shuning uchun yo'l qo'shilishi hech narsaga ta'sir qilmaydi. Testlar faqat joriy papka tasodifan `talaba_baholari/` bo'lgani uchun o'tardi.
- **Qanday tuzatdingiz?** Importlar `sys.path.insert` dan keyinga ko'chirildi.
- **Qaysi test buni tekshiradi?** Alohida test yo'q. Tekshirish: `2-vazifa/` papkasidan `python -m unittest discover -s talaba_baholari/tests` — tuzatishdan oldin `ImportError`, keyin `OK`.
- **Buni kim topdi?** AI topdi, ishga tushirib tasdiqlandi

---

## Tuzatishdan keyingi natija

```
$ python main.py haqiqiy_data --json haqiqiy_data/qoshimcha.json
Aliyev Bobur              IT-21      81.5  O'TDI
Dilnoza Yusupova          IT-22      77.0  O'TDI
G'ulom Karimov            IT-22      53.0  YIQILDI
O'tkir Rahimov            IT-21      66.3  O'TDI
Sardor Toshmatov          IT-21      55.0  O'TDI

O'tmaganlar: G'ulom Karimov
```

Qo'lda tekshirildi: Aliyev (85+78)/2 = 81.5; Oʻtkir (62+71+66)/3 = 66.3; vaznli Aliyev (85·4 + 78·3)/7 = 82.0.

---

## Umumiy xulosa

**AI qaysi muammolarni topa olmadi?**

<!-- O'zingiz to'ldiring: kodni o'zingiz ko'rib chiqqaningizda AI e'tibor bermagan narsa topdingizmi? -->

**AI qaysi "muammo"larni noto'g'ri topdi (aslida muammo emas edi)?**

Quyidagilar ko'rib chiqildi, lekin muammo deb **hisoblanmadi**:

- **Ko'rsatilgan o'rtacha yaxlitlangan, `otdi` esa yaxlitlanmagan qiymatdan hisoblanadi** (`hisobot.py:47-48`). Masalan, 54.96 `55.0 YIQILDI` deb chiqadi. Qoida "o'rtacha 55 va undan yuqori" — 54.96 haqiqatan 55 dan kichik, demak natija to'g'ri, faqat ko'rinishi chalkash.
- **Qidiruvda `%` va `_` belgilari** LIKE shabloni sifatida ishlaydi (`--qidir "%"` hammani topadi). Parametrli so'rovdan keyin bu xavfsizlik muammosi emas — faqat qidiruvning xususiyati.
- **Har bir qatordan keyin `conn.commit()`** — sekinroq, lekin xato emas; ma'lumot hajmi kichik.
- **`PRAGMA foreign_keys` yoqilmagan** — `talaba_id` baribir `NOT NULL`, endi esa import talaba borligini oldindan tekshiradi; mavjud bo'lmagan ID kiritiladigan yo'l qolmadi.
