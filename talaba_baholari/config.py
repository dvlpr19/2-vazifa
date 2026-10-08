"""Loyiha sozlamalari."""

import os

DB_PATH = "talabalar.db"

# Telegram bot orqali hisobot yuborish uchun.
# Maxfiy ma'lumot kodda saqlanmaydi — muhit o'zgaruvchilaridan olinadi.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

# O'tish bali: o'rtacha baho 55 va undan yuqori bo'lsa, talaba o'tgan hisoblanadi
OTISH_BALI = 55

# Vaznli o'rtacha uchun fan kreditlari. Ro'yxatda yo'q fan 1 kredit hisoblanadi.
FAN_KREDITLARI = {
    "Matematika": 4,
    "Fizika": 3,
    "Ingliz tili": 2,
    "Tarix": 2,
    "Informatika": 3,
}
