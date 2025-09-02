import logging
import json
from typing import Dict, Any, Optional
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import requests
from .models import School
from dashboard.models import Message

User = get_user_model()
logger = logging.getLogger(__name__)

class TelegramBot:
    """Основной класс Telegram бота"""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.username = settings.TELEGRAM_BOT_USERNAME
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        
    def send_message(self, chat_id: int, text: str, reply_markup: Optional[Dict] = None) -> bool:
        """Отправка сообщения в Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
                
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения в Telegram: {e}")
            return False
    
    def edit_message(self, chat_id: int, message_id: int, text: str, reply_markup: Optional[Dict] = None) -> bool:
        """Редактирование сообщения в Telegram"""
        try:
            url = f"{self.base_url}/editMessageText"
            data = {
                'chat_id': chat_id,
                'message_id': message_id,
                'text': text,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
                
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            return True
            
        except Exception as e:
            logger.error(f"Ошибка редактирования сообщения в Telegram: {e}")
            return False
    
    def answer_callback_query(self, callback_query_id: str, text: str = None, show_alert: bool = False) -> bool:
        """Ответ на callback query"""
        try:
            url = f"{self.base_url}/answerCallbackQuery"
            data = {
                'callback_query_id': callback_query_id,
                'show_alert': show_alert
            }
            
            if text:
                data['text'] = text
                
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            return True
            
        except Exception as e:
            logger.error(f"Ошибка ответа на callback query: {e}")
            return False

class TelegramBotHandler:
    """Обработчик команд и сообщений Telegram бота"""
    
    def __init__(self):
        self.bot = TelegramBot()
        self.user_sessions = {}  # Временное хранение сессий пользователей
        
    def handle_start(self, chat_id: int, user_data: Dict) -> None:
        """Обработка команды /start"""
        welcome_text = """
🤖 <b>Добро пожаловать в Аноним Мектеп!</b>

Этот бот поможет вам управлять обращениями и получать уведомления о новых сообщениях.

Для начала работы необходимо авторизоваться.

Введите ваш <b>логин</b>:
        """
        
        self.bot.send_message(chat_id, welcome_text)
        self.user_sessions[chat_id] = {'state': 'waiting_username'}
        
    def handle_username(self, chat_id: int, username: str) -> None:
        """Обработка ввода логина"""
        if chat_id not in self.user_sessions:
            self.handle_start(chat_id, {})
            return
            
        self.user_sessions[chat_id]['username'] = username
        self.user_sessions[chat_id]['state'] = 'waiting_password'
        
        self.bot.send_message(chat_id, "Теперь введите ваш <b>пароль</b>:")
        
    def handle_password(self, chat_id: int, password: str) -> None:
        """Обработка ввода пароля и авторизация"""
        if chat_id not in self.user_sessions or 'username' not in self.user_sessions[chat_id]:
            self.handle_start(chat_id, {})
            return
            
        username = self.user_sessions[chat_id]['username']
        
        # Попытка авторизации
        user = authenticate(username=username, password=password)
        
        if user and user.role in ['super_admin', 'rayon_otdel', 'teacher']:
            # Успешная авторизация
            user.telegram_chat_id = chat_id
            user.save()
            
            # Удаляем сессию
            del self.user_sessions[chat_id]
            
            # Отправляем главное меню
            self.send_main_menu(chat_id, user)
            
        else:
            # Неудачная авторизация
            self.bot.send_message(chat_id, "❌ Неверный логин или пароль. Попробуйте еще раз.")
            self.user_sessions[chat_id]['state'] = 'waiting_username'
            self.bot.send_message(chat_id, "Введите ваш <b>логин</b>:")
    
    def send_main_menu(self, chat_id: int, user: User) -> None:
        """Отправка главного меню"""
        role_display = user.get_role_display()
        
        if user.role == 'teacher':
            school_name = user.school.name if user.school else "Не назначена"
            menu_text = f"""
👋 <b>Добро пожаловать, {user.get_full_name() or user.username}!</b>

📋 <b>Ваша роль:</b> {role_display}
🏫 <b>Школа:</b> {school_name}

Выберите действие:
            """
        else:
            menu_text = f"""
👋 <b>Добро пожаловать, {user.get_full_name() or user.username}!</b>

📋 <b>Ваша роль:</b> {role_display}

Выберите действие:
            """
        
        keyboard = self.get_main_menu_keyboard(user)
        self.bot.send_message(chat_id, menu_text, keyboard)
    
    def get_main_menu_keyboard(self, user: User) -> Dict:
        """Получение клавиатуры главного меню"""
        keyboard = {
            'inline_keyboard': []
        }
        
        if user.role == 'teacher':
            # Меню для учителя
            keyboard['inline_keyboard'] = [
                [{'text': '📊 Статистика школы', 'callback_data': 'stats_school'}],
                [{'text': '📝 Новые сообщения', 'callback_data': 'new_messages'}],
                [{'text': '⏳ В работе', 'callback_data': 'in_progress_messages'}],
                [{'text': '✅ Решенные', 'callback_data': 'resolved_messages'}],
                [{'text': '🔄 Обновить', 'callback_data': 'refresh'}]
            ]
        elif user.role == 'rayon_otdel':
            # Меню для районного отдела
            keyboard['inline_keyboard'] = [
                [{'text': '📊 Общая статистика', 'callback_data': 'stats_all'}],
                [{'text': '🏢 Сообщения в районный отдел', 'callback_data': 'general_messages'}],
                [{'text': '📝 Новые сообщения', 'callback_data': 'new_messages'}],
                [{'text': '⏳ В работе', 'callback_data': 'in_progress_messages'}],
                [{'text': '✅ Решенные', 'callback_data': 'resolved_messages'}],
                [{'text': '🔄 Обновить', 'callback_data': 'refresh'}]
            ]
        else:
            # Меню для супер-админа
            keyboard['inline_keyboard'] = [
                [{'text': '📊 Общая статистика', 'callback_data': 'stats_all'}],
                [{'text': '🏢 Сообщения в районный отдел', 'callback_data': 'general_messages'}],
                [{'text': '📝 Новые сообщения', 'callback_data': 'new_messages'}],
                [{'text': '⏳ В работе', 'callback_data': 'in_progress_messages'}],
                [{'text': '✅ Решенные', 'callback_data': 'resolved_messages'}],
                [{'text': '🏫 Управление школами', 'callback_data': 'manage_schools'}],
                [{'text': '👥 Управление пользователями', 'callback_data': 'manage_users'}],
                [{'text': '🔄 Обновить', 'callback_data': 'refresh'}]
            ]
        
        return keyboard
    
    def handle_callback_query(self, chat_id: int, callback_data: str, message_id: int) -> None:
        """Обработка callback query"""
        try:
            user = User.objects.get(telegram_chat_id=chat_id)
        except User.DoesNotExist:
            self.bot.send_message(chat_id, "❌ Пользователь не найден. Используйте /start для авторизации.")
            return
        
        if callback_data == 'stats_all':
            self.show_stats_all(chat_id, user, message_id)
        elif callback_data == 'stats_school':
            self.show_stats_school(chat_id, user, message_id)
        elif callback_data == 'general_messages':
            self.show_general_messages(chat_id, user, message_id)
        elif callback_data == 'new_messages':
            self.show_new_messages(chat_id, user, message_id)
        elif callback_data == 'in_progress_messages':
            self.show_in_progress_messages(chat_id, user, message_id)
        elif callback_data == 'resolved_messages':
            self.show_resolved_messages(chat_id, user, message_id)
        elif callback_data == 'refresh':
            self.send_main_menu(chat_id, user)
        elif callback_data.startswith('message_'):
            self.handle_message_action(chat_id, callback_data, user, message_id)
        elif callback_data.startswith('set_status_'):
            self.handle_set_status(chat_id, callback_data, user, message_id)
        elif callback_data.startswith('comment_'):
            self.handle_comment(chat_id, callback_data, user, message_id)
        elif callback_data == 'back_to_menu':
            self.send_main_menu(chat_id, user)
        else:
            self.bot.answer_callback_query(callback_data, "Функция в разработке")
    
    def show_stats_all(self, chat_id: int, user: User, message_id: int) -> None:
        """Показать общую статистику"""
        messages = Message.objects.all()
        
        stats_text = f"""
📊 <b>Общая статистика</b>

🔴 Новых: {messages.filter(status='new').count()}
🟡 В работе: {messages.filter(status='in_progress').count()}
🟢 Решено: {messages.filter(status='resolved').count()}
📈 Всего: {messages.count()}

📋 <b>По типам проблем:</b>
• Буллинг: {messages.filter(problem_type='bullying').count()}
• Вымогательство: {messages.filter(problem_type='extortion').count()}
• Притеснения: {messages.filter(problem_type='harassment').count()}
• Другие: {messages.filter(problem_type='other').count()}
        """
        
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
            ]
        }
        
        self.bot.edit_message(chat_id, message_id, stats_text, keyboard)
    
    def show_stats_school(self, chat_id: int, user: User, message_id: int) -> None:
        """Показать статистику школы"""
        if not user.school:
            self.bot.edit_message(chat_id, message_id, "❌ Школа не назначена")
            return
            
        messages = Message.objects.filter(school=user.school)
        
        stats_text = f"""
📊 <b>Статистика школы: {user.school.name}</b>

🔴 Новых: {messages.filter(status='new').count()}
🟡 В работе: {messages.filter(status='in_progress').count()}
🟢 Решено: {messages.filter(status='resolved').count()}
📈 Всего: {messages.count()}
        """
        
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
            ]
        }
        
        self.bot.edit_message(chat_id, message_id, stats_text, keyboard)
    
    def show_new_messages(self, chat_id: int, user: User, message_id: int) -> None:
        """Показать новые сообщения"""
        if user.role == 'teacher':
            messages = Message.objects.filter(school=user.school, status='new')
        else:
            messages = Message.objects.filter(status='new')
        
        if not messages.exists():
            text = "📝 <b>Новых сообщений нет</b>"
            keyboard = {
                'inline_keyboard': [
                    [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
                ]
            }
        else:
            text = f"📝 <b>Новые сообщения ({messages.count()})</b>\n\n"
            keyboard = {'inline_keyboard': []}
            
            for message in messages[:10]:  # Показываем первые 10
                school_name = message.school.name if message.school else "Районный отдел"
                text += f"• <b>#{message.id}</b> - {school_name}\n"
                text += f"  {message.problem[:50]}...\n"
                text += f"  <i>{message.created_at.strftime('%d.%m.%Y %H:%M')}</i>\n\n"
                
                keyboard['inline_keyboard'].append([
                    {'text': f'📋 #{message.id}', 'callback_data': f'message_{message.id}'}
                ])
            
            keyboard['inline_keyboard'].append([
                {'text': '🔙 Назад', 'callback_data': 'back_to_menu'}
            ])
        
        self.bot.edit_message(chat_id, message_id, text, keyboard)
    
    def handle_message_action(self, chat_id: int, callback_data: str, user: User, message_id: int) -> None:
        """Обработка действий с сообщением"""
        try:
            message_id_from_callback = int(callback_data.split('_')[1])
            message = Message.objects.get(id=message_id_from_callback)
            
            # Проверяем права доступа
            if user.role == 'teacher' and message.school != user.school:
                self.bot.answer_callback_query(callback_data, "Нет доступа к этому сообщению")
                return
            
            self.show_message_details(chat_id, message, user, message_id)
            
        except (ValueError, Message.DoesNotExist):
            self.bot.answer_callback_query(callback_data, "Сообщение не найдено")
    
    def show_message_details(self, chat_id: int, message: Message, user: User, bot_message_id: int) -> None:
        """Показать детали сообщения с кнопками действий"""
        school_name = message.school.name if message.school else "Районный отдел"
        problem_type_display = dict(message.PROBLEM_TYPE_CHOICES).get(message.problem_type, 'Неизвестно')
        status_display = dict(message.STATUS_CHOICES).get(message.status, 'Неизвестно')
        
        text = f"""
📋 <b>Сообщение #{message.id}</b>

🏫 <b>Школа:</b> {school_name}
📝 <b>Тип:</b> {problem_type_display}
📊 <b>Статус:</b> {status_display}
📅 <b>Дата:</b> {message.created_at.strftime('%d.%m.%Y %H:%M')}

📄 <b>Описание:</b>
{message.problem}
        """
        
        keyboard = {
            'inline_keyboard': [
                [
                    {'text': '⏳ В работу', 'callback_data': f'set_status_{message.id}_in_progress'},
                    {'text': '✅ Решено', 'callback_data': f'set_status_{message.id}_resolved'}
                ],
                [{'text': '💬 Комментарий', 'callback_data': f'comment_{message.id}'}],
                [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
            ]
        }
        
        self.bot.edit_message(chat_id, bot_message_id, text, keyboard)
    
    def handle_set_status(self, chat_id: int, callback_data: str, user: User, message_id: int) -> None:
        """Обработка изменения статуса сообщения"""
        try:
            # Парсим callback_data: set_status_{message_id}_{new_status}
            parts = callback_data.split('_')
            message_id_from_callback = int(parts[2])
            new_status = parts[3]
            
            message = Message.objects.get(id=message_id_from_callback)
            
            # Проверяем права доступа
            if user.role == 'teacher' and message.school != user.school:
                self.bot.answer_callback_query(callback_data, "Нет доступа к этому сообщению")
                return
            
            # Изменяем статус
            old_status = message.status
            message.status = new_status
            message.save()
            
            # Отправляем подтверждение
            status_display = dict(message.STATUS_CHOICES).get(new_status, 'Неизвестно')
            self.bot.answer_callback_query(callback_data, f"Статус изменен на: {status_display}")
            
            # Обновляем сообщение
            self.show_message_details(chat_id, message, user, message_id)
            
        except (ValueError, Message.DoesNotExist):
            self.bot.answer_callback_query(callback_data, "Сообщение не найдено")
    
    def handle_comment(self, chat_id: int, callback_data: str, user: User, message_id: int) -> None:
        """Обработка добавления комментария"""
        try:
            message_id_from_callback = int(callback_data.split('_')[1])
            message = Message.objects.get(id=message_id_from_callback)
            
            # Проверяем права доступа
            if user.role == 'teacher' and message.school != user.school:
                self.bot.answer_callback_query(callback_data, "Нет доступа к этому сообщению")
                return
            
            # Сохраняем информацию о том, что пользователь хочет добавить комментарий
            if chat_id not in self.user_sessions:
                self.user_sessions[chat_id] = {}
            
            self.user_sessions[chat_id]['waiting_comment'] = message_id_from_callback
            self.user_sessions[chat_id]['state'] = 'waiting_comment'
            
            self.bot.answer_callback_query(callback_data, "Введите комментарий:")
            self.bot.send_message(chat_id, "💬 <b>Добавление комментария</b>\n\nВведите ваш комментарий:")
            
        except (ValueError, Message.DoesNotExist):
            self.bot.answer_callback_query(callback_data, "Сообщение не найдено")
    
    def handle_comment_text(self, chat_id: int, comment_text: str) -> None:
        """Обработка текста комментария"""
        if chat_id not in self.user_sessions or 'waiting_comment' not in self.user_sessions[chat_id]:
            return
        
        try:
            message_id = self.user_sessions[chat_id]['waiting_comment']
            message = Message.objects.get(id=message_id)
            user = User.objects.get(telegram_chat_id=chat_id)
            
            # Создаем комментарий
            from dashboard.models import InternalComment
            InternalComment.objects.create(
                message=message,
                author=user,
                content=comment_text
            )
            
            # Очищаем сессию
            del self.user_sessions[chat_id]
            
            # Отправляем подтверждение
            self.bot.send_message(chat_id, "✅ <b>Комментарий добавлен успешно!</b>")
            
        except (Message.DoesNotExist, User.DoesNotExist):
            self.bot.send_message(chat_id, "❌ Ошибка добавления комментария")
    
    def process_update(self, update: Dict[str, Any]) -> None:
        """Обработка входящего обновления от Telegram"""
        try:
            if 'message' in update:
                self.process_message(update['message'])
            elif 'callback_query' in update:
                self.process_callback_query(update['callback_query'])
        except Exception as e:
            logger.error(f"Ошибка обработки обновления: {e}")
    
    def process_message(self, message: Dict[str, Any]) -> None:
        """Обработка текстового сообщения"""
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        if text.startswith('/start'):
            self.handle_start(chat_id, message.get('from', {}))
        elif chat_id in self.user_sessions:
            state = self.user_sessions[chat_id]['state']
            if state == 'waiting_username':
                self.handle_username(chat_id, text)
            elif state == 'waiting_password':
                self.handle_password(chat_id, text)
            elif state == 'waiting_comment':
                self.handle_comment_text(chat_id, text)
    
    def process_callback_query(self, callback_query: Dict[str, Any]) -> None:
        """Обработка callback query"""
        chat_id = callback_query['message']['chat']['id']
        callback_data = callback_query['data']
        message_id = callback_query['message']['message_id']
        query_id = callback_query['id']
        
        # Отвечаем на callback query
        self.bot.answer_callback_query(query_id)
        
        # Обрабатываем действие
        self.handle_callback_query(chat_id, callback_data, message_id)

# Глобальный экземпляр обработчика
bot_handler = TelegramBotHandler()
