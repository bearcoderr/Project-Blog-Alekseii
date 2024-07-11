# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .telegram_utils import send_telegram_message

@receiver(post_save, sender=News)
def send_news_to_telegram(sender, instance, created, **kwargs):
    if created:
        message = f"New news: {instance.titleNews}\n\n{instance.contentNews}"
        send_telegram_message(message)
