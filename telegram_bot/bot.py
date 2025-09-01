from telegram import Bot
from django.conf import settings


_bot = None


def get_bot() -> Bot:
    global _bot
    if _bot is None and getattr(settings, "TELEGRAM_BOT_TOKEN", None):
        _bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    return _bot


def send_message(chat_id: str, text: str) -> None:
    bot = get_bot()
    if bot is None:
        return
    bot.send_message(chat_id=chat_id, text=text)
