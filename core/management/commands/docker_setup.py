from django.core.management.base import BaseCommand
import os
import subprocess


class Command(BaseCommand):
    help = 'Настройка проекта для Docker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--env',
            choices=['dev', 'prod'],
            default='prod',
            help='Среда для настройки (dev или prod)'
        )

    def handle(self, *args, **options):
        env = options['env']
        
        self.stdout.write(
            self.style.SUCCESS('🐳 Настройка Docker для "Аноним Мектеп"')
        )
        self.stdout.write('=' * 50)
        
        # Проверяем наличие Docker
        if not self.check_docker():
            self.stdout.write(
                self.style.ERROR('❌ Docker не установлен!')
            )
            return
        
        # Проверяем наличие .env файлов
        self.check_env_files(env)
        
        # Показываем инструкции
        self.show_instructions(env)

    def check_docker(self):
        """Проверяет наличие Docker"""
        try:
            subprocess.run(['docker', '--version'], 
                         capture_output=True, check=True)
            self.stdout.write('✅ Docker установлен')
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def check_env_files(self, env):
        """Проверяет наличие .env файлов"""
        env_file = f'.env.{env}'
        
        if os.path.exists(env_file):
            self.stdout.write(f'✅ Файл {env_file} найден')
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️  Файл {env_file} не найден!')
            )
            self.stdout.write(f'Создайте файл {env_file} на основе env.example')

    def show_instructions(self, env):
        """Показывает инструкции по запуску"""
        self.stdout.write(f'\n📋 Инструкции для {env.upper()} среды:')
        
        if env == 'dev':
            self.stdout.write('\n🛠️ Разработка:')
            self.stdout.write('1. Создайте .env.dev файл:')
            self.stdout.write('   cp env.example .env.dev')
            self.stdout.write('2. Отредактируйте .env.dev с вашими настройками')
            self.stdout.write('3. Запустите контейнеры:')
            self.stdout.write('   ./docker-build.sh dev')
            self.stdout.write('4. Сайт будет доступен по адресу: http://127.0.0.1:8000')
            
        else:
            self.stdout.write('\n🚀 Продакшен:')
            self.stdout.write('1. Создайте .env.prod файл:')
            self.stdout.write('   cp env.example .env.prod')
            self.stdout.write('2. Отредактируйте .env.prod с продакшен настройками')
            self.stdout.write('3. Настройте SSL сертификаты в директории ssl/')
            self.stdout.write('4. Запустите контейнеры:')
            self.stdout.write('   ./docker-build.sh prod')
            self.stdout.write('5. Сайт будет доступен по адресу: https://anonim-m.online')
        
        self.stdout.write('\n🔧 Полезные команды:')
        self.stdout.write('  ./docker-build.sh logs     - Показать логи')
        self.stdout.write('  ./docker-build.sh status   - Статус контейнеров')
        self.stdout.write('  ./docker-build.sh shell    - Войти в контейнер')
        self.stdout.write('  ./docker-build.sh stop     - Остановить контейнеры')
        self.stdout.write('  ./docker-build.sh clean    - Очистить все')
        
        self.stdout.write('\n📊 Мониторинг:')
        self.stdout.write('  docker-compose ps          - Статус контейнеров')
        self.stdout.write('  docker-compose logs -f     - Логи в реальном времени')
        self.stdout.write('  docker stats               - Использование ресурсов')
        
        self.stdout.write('\n⚠️  Важно:')
        self.stdout.write('- Убедитесь, что порты 80 и 443 свободны')
        self.stdout.write('- Настройте SSL сертификаты для продакшена')
        self.stdout.write('- Проверьте настройки reCAPTCHA и Telegram бота')
