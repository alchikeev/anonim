import logging
import json
from typing import Dict, Any, Optional, List, Tuple
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q, Count, QuerySet
import requests
from .models import School
from dashboard.models import Message

User = get_user_model()
logger = logging.getLogger(__name__)

# Константы
PAGINATION_SIZE = 5
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

# Роли пользователей
ROLES = {
    'SUPER_ADMIN': 'super_admin',
    'RAYON_OTDEL': 'rayon_otdel', 
    'TEACHER': 'teacher'
}

# Состояния пользователей
USER_STATES = {
    'WAITING_USERNAME': 'waiting_username',
    'WAITING_PASSWORD': 'waiting_password',
    'WAITING_COMMENT': 'waiting_comment'
}

# Статусы сообщений
MESSAGE_STATUSES = {
    'NEW': 'new',
    'IN_PROGRESS': 'in_progress',
    'RESOLVED': 'resolved'
}

class TelegramBot:
    """Оптимизированный класс Telegram бота"""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.username = settings.TELEGRAM_BOT_USERNAME
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AnonimMektepBot/1.0'
        })
        
    def _make_request(self, method: str, data: Dict[str, Any]) -> Optional[Dict]:
        """Универсальный метод для выполнения запросов к Telegram API"""
        url = f"{self.base_url}/{method}"
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.post(url, json=data, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Попытка {attempt + 1} не удалась: {e}")
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"Все попытки исчерпаны для {method}: {e}")
                    return None
                    
        return None
        
    def send_message(self, chat_id: int, text: str, reply_markup: Optional[Dict] = None) -> bool:
        """Отправка сообщения в Telegram"""
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        if reply_markup:
            data['reply_markup'] = reply_markup
            
        result = self._make_request('sendMessage', data)
        return result is not None and result.get('ok', False)
    
    def edit_message(self, chat_id: int, message_id: int, text: str, reply_markup: Optional[Dict] = None) -> bool:
        """Редактирование сообщения в Telegram"""
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        if reply_markup:
            data['reply_markup'] = reply_markup
            
        result = self._make_request('editMessageText', data)
        return result is not None and result.get('ok', False)
    
    def answer_callback_query(self, callback_query_id: str, text: str = None, show_alert: bool = False) -> bool:
        """Ответ на callback query"""
        data = {
            'callback_query_id': callback_query_id,
            'show_alert': show_alert
        }
        
        if text:
            data['text'] = text
            
        result = self._make_request('answerCallbackQuery', data)
        return result is not None and result.get('ok', False)


class KeyboardBuilder:
    """Класс для создания клавиатур"""
    
    @staticmethod
    def create_reply_keyboard(buttons: List[List[str]]) -> Dict[str, Any]:
        """Создание reply клавиатуры"""
        return {
            'keyboard': buttons,
            'resize_keyboard': True,
            'one_time_keyboard': False,
            'selective': False
        }
    
    @staticmethod
    def create_inline_keyboard(buttons: List[List[Dict[str, str]]]) -> Dict[str, Any]:
        """Создание inline клавиатуры"""
        return {
            'inline_keyboard': buttons
        }
    
    @staticmethod
    def create_navigation_buttons(page: int, total_pages: int, callback_prefix: str) -> List[Dict[str, str]]:
        """Создание кнопок навигации"""
        buttons = []
        
        # Кнопка "Назад"
        if page > 1:
            buttons.append({'text': '⬅️ Назад', 'callback_data': f'{callback_prefix}_page_{page-1}'})
        else:
            buttons.append({'text': '⬅️ Назад', 'callback_data': 'disabled'})
        
        # Кнопка "На главную"
        buttons.append({'text': '🏠 На главную', 'callback_data': 'back_to_menu'})
        
        # Кнопка "Вперед"
        if page < total_pages:
            buttons.append({'text': 'Вперед ➡️', 'callback_data': f'{callback_prefix}_page_{page+1}'})
        else:
            buttons.append({'text': 'Вперед ➡️', 'callback_data': 'disabled'})
        
        return buttons


class MessageFormatter:
    """Класс для форматирования сообщений"""
    
    @staticmethod
    def format_message(message: Message) -> str:
        """Форматирование сообщения для отображения"""
        school_name = message.school.name if message.school else "Районный отдел"
        text = f"• <b>#{message.id}</b> - {school_name}\n"
        text += f"  {message.problem[:50]}...\n"
        text += f"  <i>{message.created_at.strftime('%d.%m.%Y %H:%M')}</i>"
        return text
    
    @staticmethod
    def format_school(school: School, base_url: str) -> str:
        """Форматирование школы для отображения"""
        from dashboard.models import Message
        messages_count = Message.objects.filter(school=school).count()
        
        school_url = f"{base_url}/send/{school.unique_code}/"
        text = f"• <b>{school.name}</b>\n"
        text += f"  Ссылка: {school_url}\n"
        text += f"  Учителей: {school.users.filter(role=ROLES['TEACHER']).count()}\n"
        text += f"  Сообщений: {messages_count}"
        return text


class DatabaseOptimizer:
    """Класс для оптимизации запросов к базе данных"""
    
    @staticmethod
    def get_user_with_relations(telegram_chat_id: int) -> Optional[User]:
        """Получение пользователя с предзагруженными связями"""
        return User.objects.select_related('school').filter(
            telegram_chat_id=telegram_chat_id
        ).first()
    
    @staticmethod
    def get_messages_with_relations(status: str = None, school: School = None) -> QuerySet:
        """Получение сообщений с предзагруженными связями"""
        queryset = Message.objects.select_related('school', 'user').prefetch_related('comments')
        
        if status:
            queryset = queryset.filter(status=status)
        if school:
            queryset = queryset.filter(school=school)
            
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_schools_with_stats() -> QuerySet:
        """Получение школ со статистикой"""
        return School.objects.annotate(
            teachers_count=Count('users', filter=Q(users__role=ROLES['TEACHER'])),
            messages_count=Count('message')
        ).order_by('name')


class TelegramBotHandler:
    """Обработчик команд и сообщений Telegram бота"""
    
    def __init__(self):
        self.bot = TelegramBot()
        self.user_sessions = {}  # Временное хранение сессий пользователей
        self.cleanup_duplicate_users()  # Очищаем дублирующихся пользователей при запуске
    
    def cleanup_duplicate_users(self) -> None:
        """Очистка дублирующихся пользователей с одинаковым telegram_chat_id"""
        try:
            from django.db.models import Count
            from core.models import User
            
            # Находим пользователей с дублирующимися telegram_chat_id
            duplicates = User.objects.values('telegram_chat_id').annotate(
                count=Count('telegram_chat_id')
            ).filter(count__gt=1, telegram_chat_id__isnull=False)
            
            for duplicate in duplicates:
                chat_id = duplicate['telegram_chat_id']
                users = User.objects.filter(telegram_chat_id=chat_id).order_by('id')
                
                # Оставляем первого пользователя, остальным убираем telegram_chat_id
                for i, user in enumerate(users):
                    if i > 0:  # Все кроме первого
                        user.telegram_chat_id = None
                        user.save()
                        print(f"Очищен дублирующийся telegram_chat_id у пользователя {user.username} (ID: {user.id})")
            
            if duplicates:
                print(f"Очищено {len(duplicates)} дублирующихся telegram_chat_id")
                
        except Exception as e:
            print(f"Ошибка при очистке дублирующихся пользователей: {e}")
        
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
            # Проверяем, есть ли уже пользователь с этим telegram_chat_id
            existing_user = User.objects.filter(telegram_chat_id=chat_id).first()
            
            if existing_user and existing_user.id != user.id:
                # Если есть другой пользователь с этим chat_id, обновляем его
                existing_user.telegram_chat_id = None
                existing_user.save()
            
            # Обновляем текущего пользователя
            user.telegram_chat_id = chat_id
            user.save()
            
            # Удаляем сессию
            del self.user_sessions[chat_id]
            
            # Отправляем главное меню
            self.send_main_menu(chat_id, user)
            
        else:
            # Неудачная авторизация
            self.bot.send_message(chat_id, "❌ Неверный логин или пароль. Обратитесь в администрацию школы и/или в районный отдел образования.")
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

Перезагрузить бота можно командой /start
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
        # Определяем кнопки в зависимости от роли
        if user.role == ROLES['TEACHER']:
            buttons = [
                ['📝 Все сообщения'],
                ['📝 Новые', '⏳ В работе', '✅ Решено'],
                ['📊 Статистика', '🔗 Ссылка школы']
            ]
        else:  # super_admin или rayon_otdel
            buttons = [
                ['📊 Общая статистика'],
                ['🏢 РайОО', '🏫 Школы'],
                ['📝 Новые', '⏳ В работе', '✅ Решено'],
                ['👥 Учителя', '👨‍💼 Сотрудники']
            ]
        
        return KeyboardBuilder.create_reply_keyboard(buttons)
    
    def handle_text_message(self, chat_id: int, text: str) -> None:
        """Обработка текстовых сообщений"""
        user = DatabaseOptimizer.get_user_with_relations(chat_id)
        if not user:
            self.bot.send_message(chat_id, "❌ Пользователь не найден. Используйте /start для авторизации.")
            return
        
        # Обработка команд по тексту
        if text == '📊 Общая статистика':
            self.show_stats_all(chat_id, user)
        elif text == '📊 Статистика':
            if user.role == 'teacher':
                self.show_stats_school(chat_id, user)
            else:
                self.show_stats_all(chat_id, user)
        elif text == '🏢 РайОО':
            self.show_general_messages(chat_id, user)
        elif text == '🏫 Школы':
            if user.role in ['super_admin', 'rayon_otdel']:
                self.show_schools(chat_id, user)
            else:
                self.show_school_messages(chat_id, user)
        elif text == '📝 Все сообщения':
            self.show_all_messages(chat_id, user)
        elif text == '📝 Новые':
            self.show_new_messages(chat_id, user)
        elif text == '⏳ В работе':
            self.show_in_progress_messages(chat_id, user)
        elif text == '✅ Решено':
            self.show_resolved_messages(chat_id, user)
        elif text == '🔄 Обновить':
            self.send_main_menu(chat_id, user)
        elif text == '🔗 Ссылка школы':
            self.show_school_link(chat_id, user)
        elif text == '👥 Учителя':
            self.manage_teachers(chat_id, user)
        elif text == '👨‍💼 Сотрудники':
            self.manage_staff(chat_id, user)
        else:
            # Если это не команда, проверяем состояние пользователя
            if chat_id in self.user_sessions:
                state = self.user_sessions[chat_id]['state']
                if state == USER_STATES['WAITING_USERNAME']:
                    self.handle_username(chat_id, text)
                elif state == USER_STATES['WAITING_PASSWORD']:
                    self.handle_password(chat_id, text)
                elif state == USER_STATES['WAITING_COMMENT']:
                    self.handle_comment_text(chat_id, text)
                else:
                    # Если пользователь в неизвестном состоянии, возвращаем главное меню
                    self.send_main_menu(chat_id, user)
            else:
                # Если пользователь не в сессии, возвращаем главное меню
                self.send_main_menu(chat_id, user)
    
    def handle_callback_query(self, chat_id: int, callback_data: str, message_id: int, query_id: str = None) -> None:
        """Обработка callback query (для inline кнопок в сообщениях)"""
        user = DatabaseOptimizer.get_user_with_relations(chat_id)
        if not user:
            self.bot.send_message(chat_id, "❌ Пользователь не найден. Используйте /start для авторизации.")
            return
        
        if callback_data.startswith('message_'):
            self.handle_message_action(chat_id, callback_data, user, message_id, query_id)
        elif callback_data.startswith('set_status_'):
            self.handle_set_status(chat_id, callback_data, user, message_id, query_id)
        elif callback_data.startswith('comment_'):
            self.handle_comment(chat_id, callback_data, user, message_id, query_id)
        elif callback_data == 'back_to_menu':
            self.send_main_menu(chat_id, user)
        elif callback_data == 'disabled':
            self.bot.answer_callback_query(query_id, "Эта кнопка недоступна")
        elif callback_data.startswith('general_page_'):
            page = int(callback_data.split('_')[2])
            self.show_general_messages(chat_id, user, page)
        elif callback_data.startswith('in_progress_page_'):
            page = int(callback_data.split('_')[2])
            self.show_in_progress_messages(chat_id, user, page)
        elif callback_data.startswith('resolved_page_'):
            page = int(callback_data.split('_')[2])
            self.show_resolved_messages(chat_id, user, page)
        elif callback_data.startswith('new_page_'):
            page = int(callback_data.split('_')[2])
            self.show_new_messages(chat_id, user, page)
        elif callback_data.startswith('schools_page_'):
            page = int(callback_data.split('_')[2])
            self.show_schools(chat_id, user, page)
        elif callback_data.startswith('teachers_page_'):
            page = int(callback_data.split('_')[2])
            self.show_teachers(chat_id, user, page)
        elif callback_data.startswith('staff_page_'):
            page = int(callback_data.split('_')[2])
            self.show_staff(chat_id, user, page)
        elif callback_data.startswith('school_stats_'):
            school_id = int(callback_data.split('_')[2])
            self.show_school_statistics(chat_id, user, school_id)
        elif callback_data.startswith('school_teachers_'):
            school_id = int(callback_data.split('_')[2])
            self.show_school_teachers(chat_id, user, school_id)
        elif callback_data.startswith('school_messages_'):
            school_id = int(callback_data.split('_')[2])
            self.show_school_messages_by_id(chat_id, user, school_id)
        elif callback_data == 'back_to_schools':
            self.show_schools(chat_id, user)
        else:
            self.bot.answer_callback_query(query_id, "Функция в разработке")
    
    def show_stats_all(self, chat_id: int, user: User, message_id: int = None) -> None:
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
        
        self.bot.send_message(chat_id, stats_text, keyboard)
    
    def show_stats_school(self, chat_id: int, user: User, message_id: int = None) -> None:
        """Показать статистику школы"""
        if not user.school:
            self.bot.send_message(chat_id, "❌ Школа не назначена")
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
        
        self.bot.send_message(chat_id, stats_text, keyboard)
    
    def show_general_messages(self, chat_id: int, user: User, page: int = 1) -> None:
        """Показать сообщения в районный отдел с пагинацией"""
        messages = Message.objects.filter(school__isnull=True).order_by('-created_at')
        self.show_messages_with_pagination(chat_id, user, messages, "Сообщения в районный отдел", page, "general")
    
    def show_messages_with_pagination(self, chat_id: int, user: User, messages, title: str, page: int = 1, callback_prefix: str = 'messages') -> None:
        """Универсальный метод для показа сообщений с пагинацией"""
        if not messages.exists():
            text = f"📝 <b>{title} нет</b>"
            keyboard = KeyboardBuilder.create_inline_keyboard([
                [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
            ])
            self.bot.send_message(chat_id, text, keyboard)
        else:
            # Пагинация
            total_pages = (messages.count() + PAGINATION_SIZE - 1) // PAGINATION_SIZE
            start_idx = (page - 1) * PAGINATION_SIZE
            end_idx = start_idx + PAGINATION_SIZE
            
            page_messages = messages[start_idx:end_idx]
            
            # Отправляем заголовок с пагинацией
            header_text = f"📝 <b>{title} (стр. {page}/{total_pages})</b>"
            self.bot.send_message(chat_id, header_text)
            
            # Отправляем каждое сообщение отдельно
            for message in page_messages:
                text = MessageFormatter.format_message(message)
                keyboard = KeyboardBuilder.create_inline_keyboard([
                    [{'text': f'📋 Подробнее #{message.id}', 'callback_data': f'message_{message.id}'}]
                ])
                self.bot.send_message(chat_id, text, keyboard)
            
            # Создаем кнопки навигации
            navigation_buttons = KeyboardBuilder.create_navigation_buttons(page, total_pages, callback_prefix)
            
            # Отправляем навигацию
            navigation_text = f"📄 Навигация ({page} страница из {total_pages})"
            navigation_keyboard = KeyboardBuilder.create_inline_keyboard([navigation_buttons])
            self.bot.send_message(chat_id, navigation_text, navigation_keyboard)
    
    def show_in_progress_messages(self, chat_id: int, user: User, page: int = 1) -> None:
        """Показать сообщения в работе"""
        if user.role == ROLES['TEACHER']:
            messages = DatabaseOptimizer.get_messages_with_relations(MESSAGE_STATUSES['IN_PROGRESS'], user.school)
        else:
            messages = DatabaseOptimizer.get_messages_with_relations(MESSAGE_STATUSES['IN_PROGRESS'])
        
        self.show_messages_with_pagination(chat_id, user, messages, "⏳ Сообщения в работе", page, "in_progress")
    
    def show_resolved_messages(self, chat_id: int, user: User, page: int = 1) -> None:
        """Показать решенные сообщения"""
        if user.role == 'teacher':
            messages = Message.objects.filter(school=user.school, status='resolved').order_by('-created_at')
        else:
            messages = Message.objects.filter(status='resolved').order_by('-created_at')
        
        self.show_messages_with_pagination(chat_id, user, messages, "✅ Решенные сообщения", page, "resolved")
    
    def show_new_messages(self, chat_id: int, user: User, page: int = 1) -> None:
        """Показать новые сообщения"""
        if user.role == 'teacher':
            messages = Message.objects.filter(school=user.school, status='new').order_by('-created_at')
        else:
            messages = Message.objects.filter(status='new').order_by('-created_at')
        
        self.show_messages_with_pagination(chat_id, user, messages, "📝 Новые сообщения", page, "new")
    
    def show_all_messages(self, chat_id: int, user: User) -> None:
        """Показать все сообщения (для учителей - все сообщения школы, сначала новые)"""
        if user.role == 'teacher':
            # Для учителей показываем все сообщения школы, сначала новые
            messages = Message.objects.filter(school=user.school).order_by('-created_at')
            self.show_messages_with_pagination(chat_id, user, messages, "Все сообщения школы", 1, "all")
        else:
            # Для админов показываем все сообщения
            messages = Message.objects.all().order_by('-created_at')
            self.show_messages_with_pagination(chat_id, user, messages, "Все сообщения", 1, "all")
    
    def show_school_messages(self, chat_id: int, user: User) -> None:
        """Показать сообщения по школам"""
        messages = Message.objects.filter(school__isnull=False).order_by('-created_at')
        
        if not messages.exists():
            text = "📝 <b>Сообщений в школы нет</b>"
        else:
            text = f"📝 <b>Сообщения в школы ({messages.count()})</b>\n\n"
            for message in messages[:10]:  # Показываем первые 10
                text += f"• <b>#{message.id}</b> - {message.school.name}\n"
                text += f"  {message.problem[:50]}...\n"
                text += f"  Статус: {message.get_status_display()}\n\n"
        
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
            ]
        }
        
        self.bot.send_message(chat_id, text, keyboard)
    
    def show_schools(self, chat_id: int, user: User, page: int = 1) -> None:
        """Показать школы с пагинацией"""
        if user.role not in ['super_admin', 'rayon_otdel']:
            self.bot.send_message(chat_id, "❌ У вас нет прав для просмотра школ")
            return
        
        schools = School.objects.all().order_by('name')
        
        if not schools.exists():
            text = "🏫 <b>Школы не найдены</b>"
            keyboard = {
                'inline_keyboard': [
                    [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
                ]
            }
            self.bot.send_message(chat_id, text, keyboard)
        else:
            # Пагинация
            per_page = 5
            total_pages = (schools.count() + per_page - 1) // per_page
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            
            page_schools = schools[start_idx:end_idx]
            
            # Отправляем заголовок с пагинацией
            header_text = f"🏫 <b>Школы (стр. {page}/{total_pages})</b>"
            self.bot.send_message(chat_id, header_text)
            
            # Отправляем каждую школу отдельно
            for school in page_schools:
                # Получаем базовый URL из настроек
                from django.conf import settings
                base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
                school_url = f"{base_url}/send/{school.unique_code}/"
                
                # Подсчитываем сообщения для школы
                from dashboard.models import Message
                messages_count = Message.objects.filter(school=school).count()
                
                text = f"• <b>{school.name}</b>\n"
                text += f"  Ссылка: {school_url}\n"
                text += f"  Учителей: {school.users.filter(role='teacher').count()}\n"
                text += f"  Сообщений: {messages_count}"
                
                keyboard = {
                    'inline_keyboard': [
                        [
                            {'text': f'📊 Статистика', 'callback_data': f'school_stats_{school.id}'},
                            {'text': f'👥 Учителя', 'callback_data': f'school_teachers_{school.id}'},
                            {'text': f'📝 Сообщения', 'callback_data': f'school_messages_{school.id}'}
                        ]
                    ]
                }
                
                self.bot.send_message(chat_id, text, keyboard)
            
            # Создаем кнопки навигации
            navigation_buttons = []
            
            # Кнопка "Назад" (предыдущая страница)
            if page > 1:
                navigation_buttons.append({'text': '⬅️ Назад', 'callback_data': f'schools_page_{page-1}'})
            else:
                navigation_buttons.append({'text': '⬅️ Назад', 'callback_data': 'disabled'})
            
            # Кнопка "На главную"
            navigation_buttons.append({'text': '🏠 На главную', 'callback_data': 'back_to_menu'})
            
            # Кнопка "Вперед" (следующая страница)
            if page < total_pages:
                navigation_buttons.append({'text': 'Вперед ➡️', 'callback_data': f'schools_page_{page+1}'})
            else:
                navigation_buttons.append({'text': 'Вперед ➡️', 'callback_data': 'disabled'})
            
            # Отправляем навигацию
            navigation_text = f"📄 Навигация ({page} страница из {total_pages})"
            navigation_keyboard = {
                'inline_keyboard': [navigation_buttons]
            }
            self.bot.send_message(chat_id, navigation_text, navigation_keyboard)
    
    def show_teachers(self, chat_id: int, user: User, page: int = 1) -> None:
        """Показать учителей с пагинацией"""
        if user.role not in ['super_admin', 'rayon_otdel']:
            self.bot.send_message(chat_id, "❌ У вас нет прав для просмотра учителей")
            return
        
        teachers = User.objects.filter(role='teacher').select_related('school').order_by('school__name', 'username')
        
        if not teachers.exists():
            text = "👥 <b>Учителя не найдены</b>"
            keyboard = {
                'inline_keyboard': [
                    [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
                ]
            }
            self.bot.send_message(chat_id, text, keyboard)
        else:
            # Пагинация
            per_page = 5
            total_pages = (teachers.count() + per_page - 1) // per_page
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            
            page_teachers = teachers[start_idx:end_idx]
            
            # Отправляем заголовок с пагинацией
            header_text = f"👥 <b>Учителя (стр. {page}/{total_pages})</b>"
            self.bot.send_message(chat_id, header_text)
            
            # Отправляем каждого учителя отдельно
            for teacher in page_teachers:
                school_name = teacher.school.name if teacher.school else "Не назначена"
                text = f"• <b>{teacher.get_full_name() or teacher.username}</b>\n"
                text += f"  Школа: {school_name}\n"
                text += f"  Активен: {'✅' if teacher.is_active else '❌'}"
                
                self.bot.send_message(chat_id, text)
            
            # Создаем кнопки навигации
            navigation_buttons = []
            
            # Кнопка "Назад" (предыдущая страница)
            if page > 1:
                navigation_buttons.append({'text': '⬅️ Назад', 'callback_data': f'teachers_page_{page-1}'})
            else:
                navigation_buttons.append({'text': '⬅️ Назад', 'callback_data': 'disabled'})
            
            # Кнопка "На главную"
            navigation_buttons.append({'text': '🏠 На главную', 'callback_data': 'back_to_menu'})
            
            # Кнопка "Вперед" (следующая страница)
            if page < total_pages:
                navigation_buttons.append({'text': 'Вперед ➡️', 'callback_data': f'teachers_page_{page+1}'})
            else:
                navigation_buttons.append({'text': 'Вперед ➡️', 'callback_data': 'disabled'})
            
            # Отправляем навигацию
            navigation_text = f"📄 Навигация ({page} страница из {total_pages})"
            navigation_keyboard = {
                'inline_keyboard': [navigation_buttons]
            }
            self.bot.send_message(chat_id, navigation_text, navigation_keyboard)
    
    def manage_teachers(self, chat_id: int, user: User) -> None:
        """Управление учителями - перенаправляем на show_teachers"""
        self.show_teachers(chat_id, user)
    
    def show_staff(self, chat_id: int, user: User, page: int = 1) -> None:
        """Показать сотрудников районного отдела с пагинацией"""
        if user.role not in ['super_admin', 'rayon_otdel']:
            self.bot.send_message(chat_id, "❌ У вас нет прав для просмотра сотрудников")
            return
        
        staff = User.objects.filter(role='rayon_otdel').order_by('username')
        
        if not staff.exists():
            text = "👨‍💼 <b>Сотрудники не найдены</b>"
            keyboard = {
                'inline_keyboard': [
                    [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
                ]
            }
            self.bot.send_message(chat_id, text, keyboard)
        else:
            # Пагинация
            per_page = 5
            total_pages = (staff.count() + per_page - 1) // per_page
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            
            page_staff = staff[start_idx:end_idx]
            
            # Отправляем заголовок с пагинацией
            header_text = f"👨‍💼 <b>Сотрудники РайОО (стр. {page}/{total_pages})</b>"
            self.bot.send_message(chat_id, header_text)
            
            # Отправляем каждого сотрудника отдельно
            for person in page_staff:
                text = f"• <b>{person.get_full_name() or person.username}</b>\n"
                text += f"  Активен: {'✅' if person.is_active else '❌'}"
                
                self.bot.send_message(chat_id, text)
            
            # Создаем кнопки навигации
            navigation_buttons = []
            
            # Кнопка "Назад" (предыдущая страница)
            if page > 1:
                navigation_buttons.append({'text': '⬅️ Назад', 'callback_data': f'staff_page_{page-1}'})
            else:
                navigation_buttons.append({'text': '⬅️ Назад', 'callback_data': 'disabled'})
            
            # Кнопка "На главную"
            navigation_buttons.append({'text': '🏠 На главную', 'callback_data': 'back_to_menu'})
            
            # Кнопка "Вперед" (следующая страница)
            if page < total_pages:
                navigation_buttons.append({'text': 'Вперед ➡️', 'callback_data': f'staff_page_{page+1}'})
            else:
                navigation_buttons.append({'text': 'Вперед ➡️', 'callback_data': 'disabled'})
            
            # Отправляем навигацию
            navigation_text = f"📄 Навигация ({page} страница из {total_pages})"
            navigation_keyboard = {
                'inline_keyboard': [navigation_buttons]
            }
            self.bot.send_message(chat_id, navigation_text, navigation_keyboard)
    
    def manage_staff(self, chat_id: int, user: User) -> None:
        """Управление сотрудниками - перенаправляем на show_staff"""
        self.show_staff(chat_id, user)
    
    def show_school_link(self, chat_id: int, user: User) -> None:
        """Показать ссылку школы для учителя"""
        if user.role != 'teacher' or not user.school:
            self.bot.send_message(chat_id, "❌ Эта функция доступна только учителям с назначенной школой.")
            return
        
        from django.conf import settings
        base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
        school_url = f"{base_url}/send/{user.school.unique_code}/"
        
        # Получаем общую ссылку на сайт
        general_url = f"{base_url}/"
        
        text = f"""
📝 <b>Салам! 👋</b>

Если у вас есть проблемы или вопросы, связанные с образованием, вы можете анонимно сообщить о них через нашу систему Аноним Мектеп:

Вот ссылка для отправки сообщения:
{school_url}

Также вы можете посетить наш общий сайт:
{general_url}

Ваше сообщение будет рассмотрено и на него ответят в кратчайшие сроки.

С уважением,
{user.school.name}
        """
        
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад', 'callback_data': 'back_to_menu'}]
            ]
        }
        
        self.bot.send_message(chat_id, text, keyboard)
    
    def handle_message_action(self, chat_id: int, callback_data: str, user: User, message_id: int, query_id: str = None) -> None:
        """Обработка действий с сообщением"""
        try:
            message_id_from_callback = int(callback_data.split('_')[1])
            message = Message.objects.get(id=message_id_from_callback)
            
            # Проверяем права доступа
            if user.role == 'teacher' and message.school != user.school:
                self.bot.answer_callback_query(query_id, "Нет доступа к этому сообщению")
                return
            
            self.show_message_details(chat_id, message, user, message_id)
            
        except (ValueError, Message.DoesNotExist):
            self.bot.answer_callback_query(query_id, "Сообщение не найдено")
    
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

📄 <b>Проблема:</b>
{message.problem}
        """
        
        # Добавляем ожидаемую помощь, если есть
        if message.help:
            text += f"\n\n🤝 <b>Ожидаемая помощь:</b>\n{message.help}"
        
        # Добавляем контакты, если есть
        if message.contact:
            text += f"\n\n📞 <b>Контакты:</b>\n{message.contact}"
        
        # Добавляем комментарии, если есть
        comments = message.comments.all().order_by('created_at')
        if comments.exists():
            text += f"\n\n💬 <b>Комментарии ({comments.count()}):</b>"
            for comment in comments:
                author_name = comment.author.username if comment.author else "Неизвестно"
                text += f"\n\n👤 <b>{author_name}</b> ({comment.created_at.strftime('%d.%m.%Y %H:%M')}):"
                text += f"\n{comment.text}"
        
        keyboard = {
            'inline_keyboard': [
                [
                    {'text': '⏳ В работу', 'callback_data': f'set_status_{message.id}_in_progress'},
                    {'text': '✅ Решено', 'callback_data': f'set_status_{message.id}_resolved'}
                ],
                [{'text': '💬 Комментарий', 'callback_data': f'comment_{message.id}'}]
            ]
        }
        
        self.bot.edit_message(chat_id, bot_message_id, text, keyboard)
    
    def handle_set_status(self, chat_id: int, callback_data: str, user: User, message_id: int, query_id: str = None) -> None:
        """Обработка изменения статуса сообщения"""
        try:
            # Парсим callback_data: set_status_{message_id}_{new_status}
            parts = callback_data.split('_')
            message_id_from_callback = int(parts[2])
            new_status = parts[3]
            
            message = Message.objects.get(id=message_id_from_callback)
            
            # Проверяем права доступа
            if user.role == 'teacher' and message.school != user.school:
                self.bot.answer_callback_query(query_id, "Нет доступа к этому сообщению")
                return
            
            # Изменяем статус
            old_status = message.status
            message.status = new_status
            message.save()
            
            # Отправляем подтверждение
            status_display = dict(message.STATUS_CHOICES).get(new_status, 'Неизвестно')
            self.bot.answer_callback_query(query_id, f"Статус изменен на: {status_display}")
            
            # Обновляем сообщение
            self.show_message_details(chat_id, message, user, message_id)
            
        except (ValueError, Message.DoesNotExist):
            self.bot.answer_callback_query(query_id, "Сообщение не найдено")
    
    def handle_comment(self, chat_id: int, callback_data: str, user: User, message_id: int, query_id: str = None) -> None:
        """Обработка добавления комментария"""
        try:
            message_id_from_callback = int(callback_data.split('_')[1])
            message = Message.objects.get(id=message_id_from_callback)
            
            # Проверяем права доступа
            if user.role == 'teacher' and message.school != user.school:
                self.bot.answer_callback_query(query_id, "Нет доступа к этому сообщению")
                return
            
            # Сохраняем информацию о том, что пользователь хочет добавить комментарий
            if chat_id not in self.user_sessions:
                self.user_sessions[chat_id] = {}
            
            self.user_sessions[chat_id]['waiting_comment'] = message_id_from_callback
            self.user_sessions[chat_id]['state'] = 'waiting_comment'
            
            self.bot.answer_callback_query(query_id, "Введите комментарий:")
            self.bot.send_message(chat_id, "💬 <b>Добавление комментария</b>\n\nВведите ваш комментарий:")
            
        except (ValueError, Message.DoesNotExist):
            self.bot.answer_callback_query(query_id, "Сообщение не найдено")
    
    def handle_comment_text(self, chat_id: int, comment_text: str) -> None:
        """Обработка текста комментария"""
        if chat_id not in self.user_sessions or 'waiting_comment' not in self.user_sessions[chat_id]:
            return
        
        try:
            message_id = self.user_sessions[chat_id]['waiting_comment']
            message = Message.objects.get(id=message_id)
            user = User.objects.filter(telegram_chat_id=chat_id).first()
            
            # Создаем комментарий
            from dashboard.models import InternalComment
            InternalComment.objects.create(
                message=message,
                author=user,
                text=comment_text
            )
            
            # Очищаем сессию
            del self.user_sessions[chat_id]
            
            # Отправляем подтверждение и главное меню
            self.bot.send_message(chat_id, "✅ <b>Комментарий добавлен успешно!</b>")
            self.send_main_menu(chat_id, user)
            
        except (Message.DoesNotExist, User.DoesNotExist):
            self.bot.send_message(chat_id, "❌ Ошибка добавления комментария")
    
    def show_school_statistics(self, chat_id: int, user: User, school_id: int) -> None:
        """Показать статистику конкретной школы"""
        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            self.bot.send_message(chat_id, "❌ Школа не найдена")
            return
        
        # Статистика сообщений по школе
        messages = Message.objects.filter(school=school)
        new_count = messages.filter(status='new').count()
        in_progress_count = messages.filter(status='in_progress').count()
        resolved_count = messages.filter(status='resolved').count()
        total_count = messages.count()
        
        # Статистика учителей
        teachers_count = school.users.filter(role='teacher', is_active=True).count()
        
        text = f"📊 <b>Статистика школы: {school.name}</b>\n\n"
        text += f"📝 <b>Сообщения:</b>\n"
        text += f"  • Всего: {total_count}\n"
        text += f"  • Новые: {new_count}\n"
        text += f"  • В работе: {in_progress_count}\n"
        text += f"  • Решено: {resolved_count}\n\n"
        text += f"👥 <b>Учителя:</b> {teachers_count}"
        
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад к школам', 'callback_data': 'back_to_schools'}]
            ]
        }
        
        self.bot.send_message(chat_id, text, keyboard)
    
    def show_school_teachers(self, chat_id: int, user: User, school_id: int) -> None:
        """Показать учителей конкретной школы"""
        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            self.bot.send_message(chat_id, "❌ Школа не найдена")
            return
        
        teachers = school.users.filter(role='teacher').order_by('username')
        
        if not teachers.exists():
            text = f"👥 <b>Учителя школы: {school.name}</b>\n\n❌ Учителя не найдены"
        else:
            text = f"👥 <b>Учителя школы: {school.name}</b>\n\n"
            for teacher in teachers:
                text += f"• <b>{teacher.get_full_name() or teacher.username}</b>\n"
                text += f"  Активен: {'✅' if teacher.is_active else '❌'}\n\n"
        
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад к школам', 'callback_data': 'back_to_schools'}]
            ]
        }
        
        self.bot.send_message(chat_id, text, keyboard)
    
    def show_school_messages_by_id(self, chat_id: int, user: User, school_id: int) -> None:
        """Показать сообщения конкретной школы"""
        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            self.bot.send_message(chat_id, "❌ Школа не найдена")
            return
        
        messages = Message.objects.filter(school=school).order_by('-created_at')
        
        if not messages.exists():
            self.bot.send_message(chat_id, f"📝 <b>Сообщения школы {school.name}</b>\n\nНет сообщений.")
            # Кнопка "Назад"
            back_keyboard = {'inline_keyboard': [[{'text': '🔙 Назад к школам', 'callback_data': f'schools_page_1'}]]}
            self.bot.send_message(chat_id, "🔙 Вернуться к школам:", back_keyboard)
            return
        
        # Отправляем заголовок
        header_text = f"📝 <b>Сообщения школы {school.name}</b>"
        self.bot.send_message(chat_id, header_text)
        
        # Отправляем каждое сообщение отдельно
        for message in messages:
            text = f"• <b>#{message.id}</b>\n"
            text += f"  <b>Проблема:</b> {message.problem[:100]}{'...' if len(message.problem) > 100 else ''}\n"
            
            if message.help:
                text += f"  <b>Ожидаемая помощь:</b> {message.help[:100]}{'...' if len(message.help) > 100 else ''}\n"
            
            if message.contact:
                text += f"  <b>Контакты:</b> {message.contact[:100]}{'...' if len(message.contact) > 100 else ''}\n"
            
            text += f"  <b>Статус:</b> {message.get_status_display()}\n"
            text += f"  <i>{message.created_at.strftime('%d.%m.%Y %H:%M')}</i>"
            
            keyboard = {
                'inline_keyboard': [
                    [{'text': f'📋 Подробнее #{message.id}', 'callback_data': f'message_{message.id}'}]
                ]
            }
            self.bot.send_message(chat_id, text, keyboard)
        
        # Кнопка "Назад"
        back_keyboard = {'inline_keyboard': [[{'text': '🔙 Назад к школам', 'callback_data': f'schools_page_1'}]]}
        self.bot.send_message(chat_id, "🔙 Вернуться к школам:", back_keyboard)
    
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
        else:
            # Обработка команд через кнопки
            self.handle_text_message(chat_id, text)
    
    def process_callback_query(self, callback_query: Dict[str, Any]) -> None:
        """Обработка callback query"""
        chat_id = callback_query['message']['chat']['id']
        callback_data = callback_query['data']
        message_id = callback_query['message']['message_id']
        query_id = callback_query['id']
        
        # Обрабатываем действие
        self.handle_callback_query(chat_id, callback_data, message_id, query_id)
        
        # Отвечаем на callback query
        self.bot.answer_callback_query(query_id)

# Глобальный экземпляр обработчика
bot_handler = TelegramBotHandler()
