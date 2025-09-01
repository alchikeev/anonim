from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Report
from telegram_bot.bot import send_message


@receiver(post_save, sender=Report)
def report_created(sender, instance: Report, created, **kwargs):
    if not created:
        return

    base_url = getattr(settings, "DASHBOARD_BASE_URL", "")
    link = f"{base_url}{instance.id}/"
    message = (
        f"School: {instance.school.name}\n"
        f"Problem: {instance.problem_type.name}\n"
        f"{link}"
    )

    recipients = list(instance.school.teachers.values_list("chat_id", flat=True))
    recipients += list(instance.school.district.admins.values_list("chat_id", flat=True))
    for chat_id in recipients:
        send_message(chat_id, message)
