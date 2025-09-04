from django.core.management.base import BaseCommand
from django.conf import settings
from core.telegram_bot import bot_handler
import requests
import json
import time
import signal
import sys


class Command(BaseCommand):
    help = 'Запуск Telegram бота в режиме polling (для разработки)'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = True
        self.last_update_id = 0
        
        # Обработчик сигнала для корректного завершения
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        self.stdout.write(self.style.WARNING('\n🛑 Получен сигнал завершения. Останавливаем polling...'))
        self.running = False
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='Таймаут для long polling (по умолчанию 30 секунд)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Максимальное количество обновлений за раз (по умолчанию 100)'
        )
    
    def handle(self, *args, **options):
        timeout = options['timeout']
        limit = options['limit']
        
        if not settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write(
                self.style.ERROR('❌ TELEGRAM_BOT_TOKEN не настроен в settings.py')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('🤖 Запуск Telegram бота в режиме polling...')
        )
        self.stdout.write(f'📡 Таймаут: {timeout} секунд')
        self.stdout.write(f'📊 Лимит обновлений: {limit}')
        self.stdout.write('⏹️  Для остановки нажмите Ctrl+C\n')
        
        try:
            while self.running:
                try:
                    # Получаем обновления
                    updates = self.get_updates(timeout, limit)
                    
                    if updates:
                        self.stdout.write(
                            self.style.SUCCESS(f'📨 Получено {len(updates)} обновлений')
                        )
                        
                        for update in updates:
                            try:
                                # Обрабатываем каждое обновление
                                bot_handler.process_update(update)
                                self.stdout.write(f'✅ Обработано обновление {update.get("update_id", "?")}')
                            except Exception as e:
                                self.stdout.write(
                                    self.style.ERROR(f'❌ Ошибка обработки обновления: {e}')
                                )
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Ошибка получения обновлений: {e}')
                    )
                    time.sleep(5)  # Пауза перед повтором
                    
        except KeyboardInterrupt:
            pass
        
        self.stdout.write(self.style.SUCCESS('👋 Polling остановлен'))
    
    def get_updates(self, timeout, limit):
        """Получение обновлений от Telegram"""
        try:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates"
            params = {
                'offset': self.last_update_id + 1,
                'limit': limit,
                'timeout': timeout,
                'allowed_updates': ['message', 'callback_query']
            }
            
            response = requests.get(url, params=params, timeout=timeout + 10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ok'):
                updates = result.get('result', [])
                
                # Обновляем last_update_id
                if updates:
                    self.last_update_id = max(update['update_id'] for update in updates)
                
                return updates
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Ошибка API: {result.get("description")}')
                )
                return []
                
        except requests.exceptions.Timeout:
            # Таймаут - это нормально для long polling
            return []
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка запроса: {e}')
            )
            return []
