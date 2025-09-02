from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json


class Command(BaseCommand):
    help = 'Управление Telegram ботом'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['set-webhook', 'delete-webhook', 'get-info', 'test'],
            help='Действие для выполнения с ботом'
        )
        parser.add_argument(
            '--url',
            type=str,
            help='URL для webhook (для set-webhook)'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        if not settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write(
                self.style.ERROR('TELEGRAM_BOT_TOKEN не настроен в settings.py')
            )
            return
        
        if action == 'set-webhook':
            self.set_webhook(options.get('url'))
        elif action == 'delete-webhook':
            self.delete_webhook()
        elif action == 'get-info':
            self.get_bot_info()
        elif action == 'test':
            self.test_bot()

    def set_webhook(self, url=None):
        """Установка webhook"""
        if not url:
            url = settings.TELEGRAM_WEBHOOK_URL
        
        if not url:
            self.stdout.write(
                self.style.ERROR('URL не указан. Используйте --url или настройте TELEGRAM_WEBHOOK_URL')
            )
            return
        
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook",
                data={'url': url, 'allowed_updates': ['message', 'callback_query']},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('ok'):
                self.stdout.write(
                    self.style.SUCCESS(f'Webhook установлен: {url}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка: {result.get("description")}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка установки webhook: {e}')
            )

    def delete_webhook(self):
        """Удаление webhook"""
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/deleteWebhook",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('ok'):
                self.stdout.write(
                    self.style.SUCCESS('Webhook удален')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка: {result.get("description")}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка удаления webhook: {e}')
            )

    def get_bot_info(self):
        """Получение информации о боте"""
        try:
            # Информация о боте
            response = requests.get(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getMe",
                timeout=10
            )
            response.raise_for_status()
            bot_info = response.json()
            
            if bot_info.get('ok'):
                bot_data = bot_info['result']
                self.stdout.write(
                    self.style.SUCCESS('Информация о боте:')
                )
                self.stdout.write(f'  Имя: {bot_data.get("first_name")}')
                self.stdout.write(f'  Username: @{bot_data.get("username")}')
                self.stdout.write(f'  ID: {bot_data.get("id")}')
                self.stdout.write(f'  Может присоединяться к группам: {bot_data.get("can_join_groups", False)}')
                self.stdout.write(f'  Может читать сообщения группы: {bot_data.get("can_read_all_group_messages", False)}')
                self.stdout.write(f'  Поддерживает inline запросы: {bot_data.get("supports_inline_queries", False)}')
            
            # Информация о webhook
            response = requests.get(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getWebhookInfo",
                timeout=10
            )
            response.raise_for_status()
            webhook_info = response.json()
            
            if webhook_info.get('ok'):
                webhook_data = webhook_info['result']
                self.stdout.write('\nИнформация о webhook:')
                self.stdout.write(f'  URL: {webhook_data.get("url", "Не установлен")}')
                self.stdout.write(f'  Ожидает сертификат: {webhook_data.get("has_custom_certificate", False)}')
                self.stdout.write(f'  Ожидающие обновления: {webhook_data.get("pending_update_count", 0)}')
                
                if webhook_data.get('last_error_date'):
                    self.stdout.write(f'  Последняя ошибка: {webhook_data.get("last_error_message")}')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка получения информации: {e}')
            )

    def test_bot(self):
        """Тестирование бота"""
        try:
            # Проверяем, что бот отвечает
            response = requests.get(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getMe",
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('ok'):
                bot_data = result['result']
                self.stdout.write(
                    self.style.SUCCESS('✅ Бот работает корректно!')
                )
                self.stdout.write(f'  Имя: {bot_data.get("first_name")}')
                self.stdout.write(f'  Username: @{bot_data.get("username")}')
                
                # Проверяем webhook
                response = requests.get(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getWebhookInfo",
                    timeout=10
                )
                response.raise_for_status()
                webhook_result = response.json()
                
                if webhook_result.get('ok'):
                    webhook_data = webhook_result['result']
                    if webhook_data.get('url'):
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Webhook установлен: {webhook_data["url"]}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING('⚠️  Webhook не установлен')
                        )
                
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Ошибка бота: {result.get("description")}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка тестирования: {e}')
            )
