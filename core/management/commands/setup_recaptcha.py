from django.core.management.base import BaseCommand
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Настраивает reCAPTCHA ключи в .env файлах'

    def add_arguments(self, parser):
        parser.add_argument(
            '--env',
            choices=['dev', 'prod', 'both'],
            default='both',
            help='Какой .env файл обновить (dev, prod или both)'
        )
        parser.add_argument(
            '--public-key',
            type=str,
            help='Публичный ключ reCAPTCHA'
        )
        parser.add_argument(
            '--private-key',
            type=str,
            help='Приватный ключ reCAPTCHA'
        )

    def handle(self, *args, **options):
        env_type = options['env']
        public_key = options.get('public_key')
        private_key = options.get('private_key')
        
        if not public_key or not private_key:
            self.show_instructions()
            return
        
        if env_type in ['dev', 'both']:
            self.update_env_file('.env.dev', public_key, private_key)
        
        if env_type in ['prod', 'both']:
            self.update_env_file('.env.prod', public_key, private_key)
        
        self.stdout.write(
            self.style.SUCCESS('✅ reCAPTCHA ключи настроены!')
        )
        
        # Проверяем конфигурацию
        self.stdout.write('\n🔍 Проверка конфигурации:')
        os.system('python manage.py check_config')

    def show_instructions(self):
        """Показывает инструкции по получению reCAPTCHA ключей"""
        self.stdout.write(
            self.style.SUCCESS('🔒 Настройка reCAPTCHA для "Аноним Мектеп"')
        )
        self.stdout.write('=' * 50)
        
        self.stdout.write('\n📋 Инструкции по получению ключей:')
        self.stdout.write('1. Перейдите на https://www.google.com/recaptcha/admin')
        self.stdout.write('2. Нажмите "+" для создания нового сайта')
        self.stdout.write('3. Заполните форму:')
        self.stdout.write('   - Label: Аноним Мектеп')
        self.stdout.write('   - reCAPTCHA type: reCAPTCHA v3')
        self.stdout.write('   - Domains:')
        self.stdout.write('     * 127.0.0.1 (для разработки)')
        self.stdout.write('     * localhost (для разработки)')
        self.stdout.write('     * anonim-m.online (для продакшена)')
        self.stdout.write('4. Примите условия использования')
        self.stdout.write('5. Нажмите "Submit"')
        self.stdout.write('6. Скопируйте Site Key (публичный) и Secret Key (приватный)')
        
        self.stdout.write('\n🛠️ Команды для настройки:')
        self.stdout.write('# Для разработки:')
        self.stdout.write('python manage.py setup_recaptcha --env dev --public-key YOUR_PUBLIC_KEY --private-key YOUR_PRIVATE_KEY')
        self.stdout.write('\n# Для продакшена:')
        self.stdout.write('python manage.py setup_recaptcha --env prod --public-key YOUR_PUBLIC_KEY --private-key YOUR_PRIVATE_KEY')
        self.stdout.write('\n# Для обеих сред:')
        self.stdout.write('python manage.py setup_recaptcha --public-key YOUR_PUBLIC_KEY --private-key YOUR_PRIVATE_KEY')
        
        self.stdout.write('\n⚠️  Важно:')
        self.stdout.write('- Используйте reCAPTCHA v3 для лучшей защиты')
        self.stdout.write('- Добавьте все домены (dev и prod) в один сайт')
        self.stdout.write('- Храните ключи в безопасности')

    def update_env_file(self, env_file, public_key, private_key):
        """Обновляет .env файл с reCAPTCHA ключами"""
        env_path = Path(env_file)
        
        if not env_path.exists():
            self.stdout.write(
                self.style.ERROR(f'❌ Файл {env_file} не найден!')
            )
            return
        
        # Читаем файл
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Обновляем или добавляем ключи
        lines = content.split('\n')
        updated_lines = []
        public_key_found = False
        private_key_found = False
        
        for line in lines:
            if line.startswith('RECAPTCHA_PUBLIC_KEY='):
                updated_lines.append(f'RECAPTCHA_PUBLIC_KEY={public_key}')
                public_key_found = True
            elif line.startswith('RECAPTCHA_PRIVATE_KEY='):
                updated_lines.append(f'RECAPTCHA_PRIVATE_KEY={private_key}')
                private_key_found = True
            else:
                updated_lines.append(line)
        
        # Добавляем недостающие ключи
        if not public_key_found:
            updated_lines.append(f'RECAPTCHA_PUBLIC_KEY={public_key}')
        if not private_key_found:
            updated_lines.append(f'RECAPTCHA_PRIVATE_KEY={private_key}')
        
        # Записываем обновленный файл
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ {env_file} обновлен с reCAPTCHA ключами')
        )
