from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Переключает между средами разработки и продакшена'

    def add_arguments(self, parser):
        parser.add_argument(
            'env',
            choices=['dev', 'prod'],
            help='Среда для переключения (dev или prod)'
        )

    def handle(self, *args, **options):
        env = options['env']
        
        # Устанавливаем переменную окружения
        os.environ['DJANGO_ENV'] = env
        
        self.stdout.write(
            self.style.SUCCESS(f'🔄 Переключение на среду: {env.upper()}')
        )
        
        if env == 'dev':
            self.stdout.write('📋 Настройки для разработки:')
            self.stdout.write('  - DEBUG: True')
            self.stdout.write('  - База данных: SQLite')
            self.stdout.write('  - Webhook: https://127.0.0.1:8000/telegram/webhook/')
            self.stdout.write('  - Домен: 127.0.0.1:8000')
        else:
            self.stdout.write('📋 Настройки для продакшена:')
            self.stdout.write('  - DEBUG: False')
            self.stdout.write('  - База данных: PostgreSQL (рекомендуется)')
            self.stdout.write('  - Webhook: https://anonim-m.online/telegram/webhook/')
            self.stdout.write('  - Домен: anonim-m.online')
        
        self.stdout.write(
            self.style.WARNING('\n⚠️  Для применения изменений перезапустите сервер Django')
        )
        
        self.stdout.write('\n🔧 Команды для проверки:')
        self.stdout.write('  python manage.py check_config')
        self.stdout.write('  python manage.py runserver')
        
        # Показываем текущую среду
        current_env = os.environ.get('DJANGO_ENV', 'dev')
        self.stdout.write(f'\n✅ Текущая среда: {current_env.upper()}')
