import os

import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contact
import environ
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
BOT_TOKEN =env('Token')
CHAT_ID = env('CHAT_ID')

@receiver(post_save, sender=Contact)
def send_telegram_notification(sender, instance, created, **kwargs):
    if created:
        text = (
            f"📩 <b>Yangi kontakt xabari!</b>\n\n"
            f"👤 <b>Ism:</b> {instance.fullname}\n"
            f"📧 <b>Email:</b> {instance.gmail}\n"
            f"💬 <b>Xabar:</b>\n{instance.message}"
        )
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"  # bu formatlash uchun
        }
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"Telegramga yuborishda xatolik: {e}")
