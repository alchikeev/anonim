from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import School
import qrcode
import io
import base64
from django.urls import reverse


class Command(BaseCommand):
    help = 'Обновляет QR-коды для всех школ с новым доменом'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            help='Новый домен для QR-кодов (например: example.com)',
        )

    def handle(self, *args, **options):
        domain = options.get('domain')
        if not domain:
            domain = getattr(settings, 'SITE_DOMAIN', '127.0.0.1:8000')
        
        protocol = 'https' if not settings.DEBUG else 'http'
        
        self.stdout.write(f'Обновление QR-кодов для домена: {protocol}://{domain}')
        
        schools = School.objects.all()
        updated_count = 0
        
        for school in schools:
            # Генерируем полную ссылку
            relative_url = reverse('send_message', args=[school.unique_code])
            full_url = f"{protocol}://{domain}{relative_url}"
            
            # Создаем QR-код
            qr = qrcode.make(full_url)
            buf = io.BytesIO()
            qr.save(buf, format='PNG')
            qr_data = buf.getvalue()
            
            self.stdout.write(f'Обновлен QR-код для школы: {school.name}')
            self.stdout.write(f'  Ссылка: {full_url}')
            self.stdout.write(f'  Размер QR-кода: {len(qr_data)} байт')
            
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Успешно обновлено {updated_count} QR-кодов')
        )
        
        # Показываем инструкции
        self.stdout.write('\n' + '='*50)
        self.stdout.write('ИНСТРУКЦИИ ДЛЯ РАЗВЕРТЫВАНИЯ:')
        self.stdout.write('='*50)
        self.stdout.write('1. Установите переменную окружения DJANGO_SITE_DOMAIN')
        self.stdout.write(f'   export DJANGO_SITE_DOMAIN={domain}')
        self.stdout.write('')
        self.stdout.write('2. Перезапустите сервер Django')
        self.stdout.write('')
        self.stdout.write('3. QR-коды будут автоматически обновлены')
        self.stdout.write('')
        self.stdout.write('4. Распечатайте новые QR-коды из админки Django')
        self.stdout.write('   /admin/core/school/')
        self.stdout.write('')
        self.stdout.write('5. Замените старые QR-коды в школах на новые')
