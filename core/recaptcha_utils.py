import requests
from django.conf import settings

def verify_recaptcha(token, remote_ip=None):
    """
    Проверяет токен reCAPTCHA v3
    """
    if not settings.RECAPTCHA_PRIVATE_KEY:
        # В режиме разработки без ключей пропускаем проверку
        return True
    
    data = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': token,
    }
    
    if remote_ip:
        data['remoteip'] = remote_ip
    
    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=data,
            timeout=10
        )
        result = response.json()
        return result.get('success', False) and result.get('score', 0) >= 0.5
    except Exception:
        return False
