
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class EditablePage(models.Model):
    """Модель для редактируемых страниц сайта с поддержкой многоязычности"""
    
    PAGE_CHOICES = [
        ('about', 'О проекте'),
        ('faq', 'FAQ'),
        ('contacts', 'Полезные контакты'),
        ('what_to_do', 'Что делать, если...'),
        ('instructions', 'Инструкции'),
        ('knowledge_base', 'База знаний'),
    ]
    
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('ky', 'Кыргызский'),
    ]
    
    page = models.CharField(max_length=32, choices=PAGE_CHOICES, verbose_name='Страница')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ru', verbose_name='Язык')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')

    class Meta:
        unique_together = ['page', 'language']
        verbose_name = 'Редактируемая страница'
        verbose_name_plural = 'Редактируемые страницы'

    def __str__(self):
        return f"{self.get_page_display()} ({self.get_language_display()})"

def generate_unique_code():
    """Генерация уникального 12-символьного кода для школы"""
    return uuid.uuid4().hex[:12]


class School(models.Model):
    """Модель школы с уникальным кодом для QR-ссылок"""
    
    name = models.CharField(max_length=255, unique=True, verbose_name='Название школы')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    unique_code = models.CharField(
        max_length=32,
        unique=True,
        default=generate_unique_code,
        editable=False,
        blank=True,
        verbose_name='Уникальный код'
    )

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'

    def save(self, *args, **kwargs):
        """Генерируем код, если он отсутствует"""
        if not self.unique_code:
            self.unique_code = generate_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class User(AbstractUser):
    """Кастомная модель пользователя с ролями и привязкой к школе"""
    
    SUPER_ADMIN = 'super_admin'
    RAYON_OTDEL = 'rayon_otdel'
    TEACHER = 'teacher'

    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Супер-админ'),
        (RAYON_OTDEL, 'Районный отдел'),
        (TEACHER, 'Учитель'),
    ]

    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default=TEACHER,
        verbose_name='Роль'
    )
    school = models.ForeignKey(
        School, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='users',
        verbose_name='Школа'
    )
    telegram_chat_id = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        help_text='Telegram chat ID для уведомлений',
        verbose_name='Telegram Chat ID'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
