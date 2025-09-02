from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Проверяет конфигурацию проекта'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔍 Проверка конфигурации проекта "Аноним Мектеп"')
        )
        self.stdout.write('=' * 50)
        
        # Проверка основных настроек
        self.check_django_settings()
        self.check_telegram_settings()
        self.check_recaptcha_settings()
        self.check_database_settings()
        
        self.stdout.write('=' * 50)
        self.stdout.write(
            self.style.SUCCESS('✅ Проверка завершена!')
        )

    def check_django_settings(self):
        """Проверка основных настроек Django"""
        self.stdout.write('\n📋 Django настройки:')
        
        # SECRET_KEY
        if settings.SECRET_KEY and settings.SECRET_KEY != 'django-insecure-gta5n-@b68%0u&3^6w!az)v+2t#%x3o)g=e!@_o$hl)ph928ec':
            self.stdout.write('  ✅ SECRET_KEY: настроен')
        else:
            self.stdout.write(
                self.style.WARNING('  ⚠️  SECRET_KEY: использует значение по умолчанию')
            )
        
        # DEBUG
        if settings.DEBUG:
            self.stdout.write('  ⚠️  DEBUG: включен (только для разработки)')
        else:
            self.stdout.write('  ✅ DEBUG: отключен (продакшен)')
        
        # ALLOWED_HOSTS
        if settings.ALLOWED_HOSTS:
            self.stdout.write(f'  ✅ ALLOWED_HOSTS: {", ".join(settings.ALLOWED_HOSTS)}')
        else:
            self.stdout.write(
                self.style.ERROR('  ❌ ALLOWED_HOSTS: не настроен')
            )

    def check_telegram_settings(self):
        """Проверка настроек Telegram бота"""
        self.stdout.write('\n🤖 Telegram Bot настройки:')
        
        # TELEGRAM_BOT_TOKEN
        if hasattr(settings, 'TELEGRAM_BOT_TOKEN') and settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write('  ✅ TELEGRAM_BOT_TOKEN: настроен')
        else:
            self.stdout.write(
                self.style.ERROR('  ❌ TELEGRAM_BOT_TOKEN: не настроен')
            )
        
        # TELEGRAM_BOT_USERNAME
        if hasattr(settings, 'TELEGRAM_BOT_USERNAME') and settings.TELEGRAM_BOT_USERNAME:
            self.stdout.write(f'  ✅ TELEGRAM_BOT_USERNAME: {settings.TELEGRAM_BOT_USERNAME}')
        else:
            self.stdout.write(
                self.style.WARNING('  ⚠️  TELEGRAM_BOT_USERNAME: не настроен')
            )
        
        # TELEGRAM_WEBHOOK_URL
        if hasattr(settings, 'TELEGRAM_WEBHOOK_URL') and settings.TELEGRAM_WEBHOOK_URL:
            self.stdout.write(f'  ✅ TELEGRAM_WEBHOOK_URL: {settings.TELEGRAM_WEBHOOK_URL}')
        else:
            self.stdout.write(
                self.style.WARNING('  ⚠️  TELEGRAM_WEBHOOK_URL: не настроен')
            )

    def check_recaptcha_settings(self):
        """Проверка настроек reCAPTCHA"""
        self.stdout.write('\n🔒 reCAPTCHA настройки:')
        
        # RECAPTCHA_PUBLIC_KEY
        if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY') and settings.RECAPTCHA_PUBLIC_KEY:
            self.stdout.write('  ✅ RECAPTCHA_PUBLIC_KEY: настроен')
        else:
            self.stdout.write(
                self.style.WARNING('  ⚠️  RECAPTCHA_PUBLIC_KEY: не настроен')
            )
        
        # RECAPTCHA_PRIVATE_KEY
        if hasattr(settings, 'RECAPTCHA_PRIVATE_KEY') and settings.RECAPTCHA_PRIVATE_KEY:
            self.stdout.write('  ✅ RECAPTCHA_PRIVATE_KEY: настроен')
        else:
            self.stdout.write(
                self.style.WARNING('  ⚠️  RECAPTCHA_PRIVATE_KEY: не настроен')
            )

    def check_database_settings(self):
        """Проверка настроек базы данных"""
        self.stdout.write('\n🗄️  База данных:')
        
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'sqlite' in db_engine:
            if settings.DEBUG:
                self.stdout.write('  ⚠️  База данных: SQLite (разработка)')
            else:
                self.stdout.write('  ✅ База данных: SQLite (продакшен)')
        elif 'postgresql' in db_engine:
            self.stdout.write('  ✅ База данных: PostgreSQL (продакшен)')
        else:
            self.stdout.write(f'  ℹ️  База данных: {db_engine}')
        
        # SITE_DOMAIN
        if hasattr(settings, 'SITE_DOMAIN') and settings.SITE_DOMAIN:
            self.stdout.write(f'  ✅ SITE_DOMAIN: {settings.SITE_DOMAIN}')
        else:
            self.stdout.write(
                self.style.WARNING('  ⚠️  SITE_DOMAIN: не настроен')
            )
