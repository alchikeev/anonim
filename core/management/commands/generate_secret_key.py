from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = 'Генерирует новый секретный ключ для Django'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            choices=['env', 'python'],
            default='env',
            help='Формат вывода: env (для .env файла) или python (для settings.py)'
        )

    def handle(self, *args, **options):
        secret_key = get_random_secret_key()
        
        if options['format'] == 'env':
            self.stdout.write(
                self.style.SUCCESS('Скопируйте эту строку в ваш .env файл:')
            )
            self.stdout.write(f'DJANGO_SECRET_KEY={secret_key}')
        else:
            self.stdout.write(
                self.style.SUCCESS('Скопируйте эту строку в settings.py:')
            )
            self.stdout.write(f'SECRET_KEY = \'{secret_key}\'')
        
        self.stdout.write(
            self.style.WARNING('\n⚠️  ВАЖНО: Никогда не коммитьте секретный ключ в git!')
        )
