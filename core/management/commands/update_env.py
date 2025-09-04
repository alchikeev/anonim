from django.core.management.base import BaseCommand
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Обновляет .env файлы с настройками Telegram бота'

    def add_arguments(self, parser):
        parser.add_argument(
            '--env',
            choices=['dev', 'prod'],
            default='dev',
            help='Какой .env файл обновить (dev или prod)'
        )

    def handle(self, *args, **options):
        env_type = options['env']
        env_file = f'.env.{env_type}'
        env_path = Path(env_file)
        
        # Telegram Bot настройки
        telegram_settings = {
            'TELEGRAM_BOT_TOKEN': 'your_telegram_bot_token_here',
            'TELEGRAM_BOT_USERNAME': 'anonim_mektep_bot',
        }
        
        if env_type == 'dev':
            telegram_settings['TELEGRAM_WEBHOOK_URL'] = 'http://127.0.0.1:8009/telegram/webhook/'
        else:
            telegram_settings['TELEGRAM_WEBHOOK_URL'] = 'https://anonim-m.online/telegram/webhook/'
        
        self.stdout.write(
            self.style.SUCCESS(f'Обновление файла {env_file}...')
        )
        
        # Читаем существующий файл
        existing_lines = []
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                existing_lines = f.readlines()
        
        # Обновляем или добавляем настройки Telegram
        updated_lines = []
        telegram_keys_found = set()
        
        for line in existing_lines:
            line_stripped = line.strip()
            if line_stripped and not line_stripped.startswith('#'):
                key = line_stripped.split('=')[0]
                if key in telegram_settings:
                    telegram_keys_found.add(key)
                    updated_lines.append(f'{key}={telegram_settings[key]}\n')
                    continue
            updated_lines.append(line)
        
        # Добавляем недостающие настройки
        for key, value in telegram_settings.items():
            if key not in telegram_keys_found:
                updated_lines.append(f'{key}={value}\n')
        
        # Записываем обновленный файл
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Файл {env_file} обновлен!')
        )
        
        # Показываем добавленные настройки
        self.stdout.write('\n📋 Добавленные настройки Telegram:')
        for key, value in telegram_settings.items():
            self.stdout.write(f'  {key}={value}')
        
        self.stdout.write(
            self.style.WARNING(f'\n⚠️  Для применения изменений перезапустите сервер Django')
        )
        
        # Показываем, как переключаться между средами
        self.stdout.write('\n🔄 Переключение между средами:')
        self.stdout.write('  Для разработки: export DJANGO_ENV=dev')
        self.stdout.write('  Для продакшена: export DJANGO_ENV=prod')
        self.stdout.write('  Проверить текущую среду: echo $DJANGO_ENV')
