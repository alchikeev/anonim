from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Демонстрирует настройку reCAPTCHA с тестовыми ключами'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔒 Демонстрация настройки reCAPTCHA')
        )
        self.stdout.write('=' * 40)
        
        # Показываем текущие настройки
        self.show_current_settings()
        
        # Показываем пример настройки
        self.show_setup_example()
        
        # Показываем тестовые ключи
        self.show_test_keys()

    def show_current_settings(self):
        """Показывает текущие настройки reCAPTCHA"""
        self.stdout.write('\n📋 Текущие настройки:')
        
        public_key = getattr(settings, 'RECAPTCHA_PUBLIC_KEY', '')
        private_key = getattr(settings, 'RECAPTCHA_PRIVATE_KEY', '')
        
        if public_key:
            self.stdout.write(f'  ✅ RECAPTCHA_PUBLIC_KEY: {public_key[:20]}...')
        else:
            self.stdout.write('  ⚠️  RECAPTCHA_PUBLIC_KEY: не настроен')
        
        if private_key:
            self.stdout.write(f'  ✅ RECAPTCHA_PRIVATE_KEY: {private_key[:20]}...')
        else:
            self.stdout.write('  ⚠️  RECAPTCHA_PRIVATE_KEY: не настроен')

    def show_setup_example(self):
        """Показывает пример настройки"""
        self.stdout.write('\n🛠️ Пример настройки:')
        self.stdout.write('# 1. Получите ключи на https://www.google.com/recaptcha/admin')
        self.stdout.write('# 2. Настройте для обеих сред:')
        self.stdout.write('python manage.py setup_recaptcha --public-key 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI --private-key 6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
        self.stdout.write('# 3. Проверьте настройки:')
        self.stdout.write('python manage.py test_recaptcha')

    def show_test_keys(self):
        """Показывает тестовые ключи для разработки"""
        self.stdout.write('\n🧪 Тестовые ключи для разработки:')
        self.stdout.write('Эти ключи работают только на localhost и 127.0.0.1:')
        self.stdout.write('')
        self.stdout.write('Публичный ключ:')
        self.stdout.write('6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
        self.stdout.write('')
        self.stdout.write('Приватный ключ:')
        self.stdout.write('6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
        self.stdout.write('')
        self.stdout.write('⚠️  ВАЖНО: Эти ключи только для тестирования!')
        self.stdout.write('Для продакшена получите собственные ключи.')
        
        self.stdout.write('\n🚀 Быстрая настройка для разработки:')
        self.stdout.write('python manage.py setup_recaptcha --env dev --public-key 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI --private-key 6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
