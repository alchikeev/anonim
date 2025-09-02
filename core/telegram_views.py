import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from .telegram_bot import bot_handler

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(View):
    """View для обработки webhook от Telegram"""
    
    def post(self, request):
        """Обработка POST запроса от Telegram"""
        try:
            # Проверяем, что запрос от Telegram
            if not self.verify_telegram_request(request):
                logger.warning("Неверный запрос от Telegram")
                return JsonResponse({'status': 'error'}, status=403)
            
            # Парсим JSON
            update = json.loads(request.body.decode('utf-8'))
            logger.info(f"Получено обновление от Telegram: {update}")
            
            # Обрабатываем обновление
            bot_handler.process_update(update)
            
            return JsonResponse({'status': 'ok'})
            
        except json.JSONDecodeError:
            logger.error("Ошибка парсинга JSON от Telegram")
            return JsonResponse({'status': 'error'}, status=400)
        except Exception as e:
            logger.error(f"Ошибка обработки webhook: {e}")
            return JsonResponse({'status': 'error'}, status=500)
    
    def verify_telegram_request(self, request) -> bool:
        """Проверка, что запрос действительно от Telegram"""
        # В продакшене здесь должна быть проверка подписи
        # Для разработки просто проверяем наличие токена
        return bool(settings.TELEGRAM_BOT_TOKEN)
    
    def get(self, request):
        """GET запрос для проверки webhook"""
        return JsonResponse({
            'status': 'ok',
            'message': 'Telegram webhook is working',
            'bot_username': settings.TELEGRAM_BOT_USERNAME
        })

@csrf_exempt
@require_http_methods(["POST"])
def set_webhook(request):
    """Установка webhook для Telegram бота"""
    try:
        import requests
        
        webhook_url = settings.TELEGRAM_WEBHOOK_URL
        if not webhook_url:
            return JsonResponse({
                'status': 'error',
                'message': 'TELEGRAM_WEBHOOK_URL не настроен'
            }, status=400)
        
        bot_token = settings.TELEGRAM_BOT_TOKEN
        if not bot_token:
            return JsonResponse({
                'status': 'error',
                'message': 'TELEGRAM_BOT_TOKEN не настроен'
            }, status=400)
        
        # Устанавливаем webhook
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        data = {
            'url': webhook_url,
            'allowed_updates': ['message', 'callback_query']
        }
        
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('ok'):
            return JsonResponse({
                'status': 'success',
                'message': 'Webhook установлен успешно',
                'webhook_url': webhook_url
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Ошибка установки webhook: {result.get('description', 'Неизвестная ошибка')}"
            }, status=400)
            
    except Exception as e:
        logger.error(f"Ошибка установки webhook: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Ошибка: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_webhook_info(request):
    """Получение информации о webhook"""
    try:
        import requests
        
        bot_token = settings.TELEGRAM_BOT_TOKEN
        if not bot_token:
            return JsonResponse({
                'status': 'error',
                'message': 'TELEGRAM_BOT_TOKEN не настроен'
            }, status=400)
        
        # Получаем информацию о webhook
        url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('ok'):
            webhook_info = result.get('result', {})
            return JsonResponse({
                'status': 'success',
                'webhook_info': webhook_info
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f"Ошибка получения информации: {result.get('description', 'Неизвестная ошибка')}"
            }, status=400)
            
    except Exception as e:
        logger.error(f"Ошибка получения информации о webhook: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Ошибка: {str(e)}'
        }, status=500)
