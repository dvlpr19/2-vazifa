# 2-vazifa: "AI yozgan" kodni tekshirish

**Taxminiy vaqt:** 3–4 soat
**AI:** ruxsat etiladi.

## Vaziyat

Oldingi stajyor AI yordamida **talabalar baholari bo'yicha hisobot tizimini** yozgan (`talaba_baholari/` papkasi). Tizim:

- CSV fayllardan talabalar va baholarni yuklaydi;
- har bir talabaning o'rtacha bahosini hisoblaydi va o'tgan-o'tmaganini aniqlaydi;
- talabani ismi bo'yicha qidiradi.

Test ma'lumotlarida (`test_data/`) hammasi ishlaydi va testlar o'tadi:

```bash
cd talaba_baholari
python -m unittest discover -s tests -v
python main.py test_data
```

**Lekin:**
- haqiqiy ma'lumotda (`haqiqiy_data/`) dastur ishlamayapti;
- xavfsizlik bo'limi kodni ko'rib, "bu holida serverga chiqarib bo'lmaydi" dedi;
- foydalanuvchilar ba'zi talabalarning natijasi noto'g'ri chiqayotganidan shikoyat qilishdi.

Rahbariyat ertaga shu kodni ishga tushirmoqchi. Sizning vazifangiz uni **tekshirish va tuzatish**.

## Topshiriq

1. Koddagi **barcha** muammolarni toping: xatolar, xavfsizlik teshiklari, eskirgan yoki mavjud bo'lmagan funksiyalar, haqiqiy ma'lumotda buziladigan joylar. Muammolar soni oldindan aytilmaydi.
2. Har bir muammo bo'yicha `HISOBOT.md` faylini to'ldiring (shablon shu papkada).
3. Har bir muammoni tuzating.
4. Har bir tuzatilgan muammo uchun **test** yozing. Test tuzatishdan oldin yiqilib, tuzatishdan keyin o'tishi kerak.
5. Tuzatishdan keyin quyidagi buyruqlar xatosiz ishlashi kerak:
   ```bash
   python main.py haqiqiy_data
   python main.py haqiqiy_data --vaznli
   python main.py haqiqiy_data --json haqiqiy_data/qoshimcha.json
   python main.py haqiqiy_data --qidir "O'tkir"
   ```

## Qoidalar va maslahatlar

- **Kodni noldan qayta yozmang.** Faqat muammoli joylarni tuzating. Hamma narsa qayta yozilgan bo'lsa, vazifa qabul qilinmaydi.
- AI'dan "kodni tekshirib ber" deb so'rashingiz mumkin. Lekin AI'ning hamma javobiga ishonmang, har bir topilmani o'zingiz tekshiring.
- Hisobotda faqat **haqiqatan mavjud** muammolarni yozing. AI to'qib chiqargan "muammo"lar uchun ball ayiriladi.
- Ma'lumot to'g'risidagi qoidalar (masalan, o'tish bali) `config.py` va funksiyalarning izohlarida yozilgan.
