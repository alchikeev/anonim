from django.conf import settings
from core.models import User, School
from .telegram_bot import TelegramBot

TELEGRAM_BOT_TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)

def send_telegram_message(chat_id, text, reply_markup=None):
    """Отправка сообщения через новый Telegram бот"""
    if not TELEGRAM_BOT_TOKEN:
        return False
    try:
        bot = TelegramBot()
        return bot.send_message(chat_id, text, reply_markup)
    except Exception as e:
        print(f"Ошибка отправки Telegram сообщения: {e}")
        return False

def notify_admins_about_message(message_obj):
    school = message_obj.school
    site_domain = getattr(settings, 'SITE_DOMAIN', '127.0.0.1:8000')
    protocol = 'https' if not settings.DEBUG else 'http'
    
    # Формируем сообщение
    problem_type_display = dict(message_obj.PROBLEM_TYPE_CHOICES).get(message_obj.problem_type, 'Неизвестно')
    
    # Определяем получателя сообщения
    if school:
        recipient = f"🏫 <b>Школа:</b> {school.name}"
    else:
        recipient = "🏢 <b>Районный отдел образования</b>"
    
    message_text = f"""
🚨 <b>Новое сообщение #{message_obj.id}</b>

{recipient}
📋 <b>Тип проблемы:</b> {problem_type_display}
📝 <b>Описание:</b> {message_obj.problem[:200]}{'...' if len(message_obj.problem) > 200 else ''}
⏰ <b>Время:</b> {message_obj.created_at.strftime('%d.%m.%Y %H:%M')}
"""
    
    # Создаем inline кнопки для работы с сообщением
    inline_keyboard = {
        'inline_keyboard': [
            [
                {'text': '⏳ В работу', 'callback_data': f'set_status_{message_obj.id}_in_progress'},
                {'text': '✅ Решено', 'callback_data': f'set_status_{message_obj.id}_resolved'}
            ],
            [{'text': '💬 Комментарий', 'callback_data': f'comment_{message_obj.id}'}],
            [{'text': '📋 Открыть в браузере', 'url': f"{protocol}://{site_domain}/staff/messages/{message_obj.id}/"}]
        ]
    }
    
    # Уведомление учителям по школе (только если сообщение для конкретной школы)
    if school:
        teachers = User.objects.filter(role=User.TEACHER, school=school, is_active=True)
        for teacher in teachers:
            if hasattr(teacher, 'telegram_chat_id') and teacher.telegram_chat_id:
                send_telegram_message(
                    teacher.telegram_chat_id, 
                    message_text,
                    reply_markup=inline_keyboard
                )
    
    # Уведомление районному отделу по всем школам
    rayon_admins = User.objects.filter(role=User.RAYON_OTDEL, is_active=True)
    for admin in rayon_admins:
        if hasattr(admin, 'telegram_chat_id') and admin.telegram_chat_id:
            send_telegram_message(
                admin.telegram_chat_id, 
                message_text,
                reply_markup=inline_keyboard
            )
    
    # Уведомление супер-админов
    super_admins = User.objects.filter(role=User.SUPER_ADMIN, is_active=True)
    for admin in super_admins:
        if hasattr(admin, 'telegram_chat_id') and admin.telegram_chat_id:
            send_telegram_message(
                admin.telegram_chat_id, 
                message_text,
                reply_markup=inline_keyboard
            )
