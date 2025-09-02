from django.core.management.base import BaseCommand
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Исправляет домены в .env файлах'

    def add_arguments(self, parser):
        parser.add_argument(
            '--env',
            choices=['dev', 'prod', 'both'],
            default='both',
            help='Какой .env файл исправить (dev, prod или both)'
        )

    def handle(self, *args, **options):
        env_type = options['env']
        
        if env_type in ['dev', 'both']:
            self.fix_dev_env()
        
        if env_type in ['prod', 'both']:
            self.fix_prod_env()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Домены в .env файлах исправлены!')
        )

    def fix_dev_env(self):
        """Исправляет .env.dev файл"""
        env_path = Path('.env.dev')
        
        if not env_path.exists():
            self.stdout.write(
                self.style.ERROR('❌ Файл .env.dev не найден!')
            )
            return
        
        # Читаем файл
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Исправляем домен
        content = content.replace('DJANGO_SITE_DOMAIN=localhost:8000', 'DJANGO_SITE_DOMAIN=127.0.0.1:8000')
        
        # Записываем обратно
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stdout.write(
            self.style.SUCCESS('✅ .env.dev исправлен: домен изменен на 127.0.0.1:8000')
        )

    def fix_prod_env(self):
        """Исправляет .env.prod файл"""
        env_path = Path('.env.prod')
        
        if not env_path.exists():
            self.stdout.write(
                self.style.ERROR('❌ Файл .env.prod не найден!')
            )
            return
        
        # Читаем файл
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Исправляем домен и ALLOWED_HOSTS
        content = content.replace('DJANGO_SITE_DOMAIN=yourdomain.kz', 'DJANGO_SITE_DOMAIN=anonim-m.online')
        content = content.replace('DJANGO_ALLOWED_HOSTS=yourdomain.kz,www.yourdomain.kz,127.0.0.1,localhost', 
                                'DJANGO_ALLOWED_HOSTS=anonim-m.online,www.anonim-m.online,127.0.0.1,localhost')
        
        # Записываем обратно
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stdout.write(
            self.style.SUCCESS('✅ .env.prod исправлен: домен изменен на anonim-m.online')
        )
        
        # Показываем исправленные настройки
        self.stdout.write('\n📋 Исправленные настройки для продакшена:')
        self.stdout.write('  DJANGO_SITE_DOMAIN=anonim-m.online')
        self.stdout.write('  DJANGO_ALLOWED_HOSTS=anonim-m.online,www.anonim-m.online,127.0.0.1,localhost')
        self.stdout.write('  TELEGRAM_WEBHOOK_URL=https://anonim-m.online/telegram/webhook/')
