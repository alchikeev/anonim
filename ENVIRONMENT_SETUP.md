# Настройка окружений DEV и PROD

## 🎯 **Цель**
Автоматическое переключение между DEV и PROD окружениями без необходимости изменения настроек вручную.

## 🔧 **Как это работает**

### 1. **Автоматическое определение окружения**
Система автоматически определяет окружение по переменной `DJANGO_ENV`:
- `DJANGO_ENV=dev` → DEV режим (локальный сервер)
- `DJANGO_ENV=prod` → PROD режим (продакшен)

### 2. **Настройки окружений**

#### **DEV режим** (`DJANGO_ENV=dev`)
```python
BASE_URL = 'http://127.0.0.1:8000'
TELEGRAM_BOT_TOKEN = из .env.dev
TELEGRAM_BOT_USERNAME = из .env.dev
TELEGRAM_WEBHOOK_URL = из .env.dev
RECAPTCHA_PUBLIC_KEY = из .env.dev
RECAPTCHA_PRIVATE_KEY = из .env.dev
```

#### **PROD режим** (`DJANGO_ENV=prod`)
```python
BASE_URL = 'https://anonim-m.online'
TELEGRAM_BOT_TOKEN = из .env.prod
TELEGRAM_BOT_USERNAME = из .env.prod
TELEGRAM_WEBHOOK_URL = из .env.prod
RECAPTCHA_PUBLIC_KEY = из .env.prod
RECAPTCHA_PRIVATE_KEY = из .env.prod
```

## 🚀 **Скрипты для запуска**

### **DEV режим**
```bash
# Запуск веб-сервера
./start_dev.sh

# Запуск Telegram бота
./telegram_dev.sh
```

### **PROD режим**
```bash
# Запуск веб-сервера
./start_prod.sh

# Запуск Telegram бота
./telegram_prod.sh
```

## 📁 **Файлы конфигурации**

### **`.env.dev`** (уже существует)
```env
DJANGO_ENV=dev
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_BOT_USERNAME=anon_mektep_bot
TELEGRAM_WEBHOOK_URL=
RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
```

### **`.env.prod`** (нужно создать)
```env
DJANGO_ENV=prod
TELEGRAM_BOT_TOKEN=your-prod-bot-token
TELEGRAM_BOT_USERNAME=anonim_mektep_bot
TELEGRAM_WEBHOOK_URL=https://anonim-m.online/telegram/webhook/
RECAPTCHA_PUBLIC_KEY=your-prod-recaptcha-public-key
RECAPTCHA_PRIVATE_KEY=your-prod-recaptcha-private-key
```

## 🏫 **Отображение школ**

Теперь в Telegram боте школы отображаются с полной информацией:

```
🏫 Школы (стр. 1/2)

• Школа №3 Ч.Айтматова
  Ссылка: http://127.0.0.1:8000/send/abc123def456/
  Учителей: 15
  Сообщений: 12
[📊 Статистика] [👥 Учителя] [📝 Сообщения]

• Школа №5 им. Ленина
  Ссылка: http://127.0.0.1:8000/send/def456ghi789/
  Учителей: 8
  Сообщений: 5
[📊 Статистика] [👥 Учителя] [📝 Сообщения]
```

## 🔄 **Переключение между режимами**

### **Для разработки (DEV)**
```bash
export DJANGO_ENV=dev
./start_dev.sh
./telegram_dev.sh
```

### **Для продакшена (PROD)**
```bash
export DJANGO_ENV=prod
./start_prod.sh
./telegram_prod.sh
```

## ✅ **Преимущества**

1. **Автоматическое переключение** - не нужно менять настройки вручную
2. **Правильные ссылки** - в DEV локальные, в PROD реальные
3. **Разные боты** - DEV и PROD используют разных ботов
4. **Удобные скрипты** - простой запуск одной командой
5. **Безопасность** - настройки не смешиваются

## 🎉 **Готово к использованию!**

Теперь вы можете легко переключаться между DEV и PROD режимами без изменения настроек! 🚀
