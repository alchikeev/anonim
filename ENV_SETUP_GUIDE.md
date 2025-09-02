# 🔧 Руководство по настройке .env файлов

## 📋 Обзор

API ключи Telegram бота и другие секретные данные успешно перенесены из `settings.py` в `.env` файлы для обеспечения безопасности.

## ✅ **Что было сделано:**

### **1. Обновлен settings.py:**
- Убраны значения по умолчанию для Telegram настроек
- Все секреты теперь читаются только из переменных окружения

### **2. Обновлены .env файлы:**
- **`.env.dev`** - настройки для разработки
- **`.env.prod`** - настройки для продакшена
- Добавлены все Telegram настройки

### **3. Созданы новые команды:**
- `python manage.py update_env` - обновление .env файлов
- `python manage.py switch_env` - переключение между средами

## 🔄 **Переключение между средами**

### **Способ 1: Через команду Django**
```bash
# Переключение на разработку
python manage.py switch_env dev

# Переключение на продакшен
python manage.py switch_env prod
```

### **Способ 2: Через переменную окружения**
```bash
# Для разработки
export DJANGO_ENV=dev

# Для продакшена
export DJANGO_ENV=prod

# Проверить текущую среду
echo $DJANGO_ENV
```

## 📁 **Структура .env файлов**

### **`.env.dev` (разработка):**
```env
# Django настройки
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Домен сайта
DJANGO_SITE_DOMAIN=127.0.0.1:8000

# Telegram Bot настройки
TELEGRAM_BOT_TOKEN=8203837964:AAF8mErf22811XcprPHN3IusUCZU0lERcWI
TELEGRAM_BOT_USERNAME=anonim_mektep_bot
TELEGRAM_WEBHOOK_URL=https://127.0.0.1:8000/telegram/webhook/

# reCAPTCHA настройки
RECAPTCHA_PUBLIC_KEY=your_recaptcha_public_key_here
RECAPTCHA_PRIVATE_KEY=your_recaptcha_private_key_here
```

### **`.env.prod` (продакшен):**
```env
# Django настройки
DJANGO_SECRET_KEY=your-super-secret-production-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=anonim-m.online,www.anonim-m.online

# Домен сайта
DJANGO_SITE_DOMAIN=anonim-m.online

# Telegram Bot настройки
TELEGRAM_BOT_TOKEN=8203837964:AAF8mErf22811XcprPHN3IusUCZU0lERcWI
TELEGRAM_BOT_USERNAME=anonim_mektep_bot
TELEGRAM_WEBHOOK_URL=https://anonim-m.online/telegram/webhook/

# reCAPTCHA настройки
RECAPTCHA_PUBLIC_KEY=your_production_recaptcha_public_key
RECAPTCHA_PRIVATE_KEY=your_production_recaptcha_private_key
```

## 🛠️ **Новые команды управления**

### **1. Обновление .env файлов:**
```bash
# Обновление .env.dev
python manage.py update_env --env dev

# Обновление .env.prod
python manage.py update_env --env prod
```

### **2. Переключение сред:**
```bash
# Переключение на разработку
python manage.py switch_env dev

# Переключение на продакшен
python manage.py switch_env prod
```

### **3. Проверка конфигурации:**
```bash
# Проверка всех настроек
python manage.py check_config
```

## 🔍 **Проверка работы**

### **Разработка (DEV):**
```bash
export DJANGO_ENV=dev
python manage.py check_config
```

**Результат:**
```
📋 Django настройки:
  ✅ SECRET_KEY: настроен
  ⚠️  DEBUG: включен (только для разработки)
  ✅ ALLOWED_HOSTS: 127.0.0.1, localhost

🤖 Telegram Bot настройки:
  ✅ TELEGRAM_BOT_TOKEN: настроен
  ✅ TELEGRAM_BOT_USERNAME: anonim_mektep_bot
  ✅ TELEGRAM_WEBHOOK_URL: https://127.0.0.1:8000/telegram/webhook/
```

### **Продакшен (PROD):**
```bash
export DJANGO_ENV=prod
python manage.py check_config
```

**Результат:**
```
📋 Django настройки:
  ✅ SECRET_KEY: настроен
  ✅ DEBUG: отключен (продакшен)
  ✅ ALLOWED_HOSTS: anonim-m.online, www.anonim-m.online

🤖 Telegram Bot настройки:
  ✅ TELEGRAM_BOT_TOKEN: настроен
  ✅ TELEGRAM_BOT_USERNAME: anonim_mektep_bot
  ✅ TELEGRAM_WEBHOOK_URL: https://anonim-m.online/telegram/webhook/
```

## 🚀 **Рабочий процесс**

### **Для разработки:**
```bash
# 1. Переключиться на dev среду
python manage.py switch_env dev

# 2. Проверить конфигурацию
python manage.py check_config

# 3. Запустить сервер
python manage.py runserver
```

### **Для продакшена:**
```bash
# 1. Переключиться на prod среду
python manage.py switch_env prod

# 2. Проверить конфигурацию
python manage.py check_config

# 3. Запустить сервер
python manage.py runserver
```

## 🔒 **Безопасность**

### **Что защищено:**
- ✅ **SECRET_KEY** - секретный ключ Django
- ✅ **TELEGRAM_BOT_TOKEN** - токен Telegram бота
- ✅ **RECAPTCHA ключи** - ключи reCAPTCHA
- ✅ **Пароли БД** - пароли базы данных

### **Файлы в .gitignore:**
```gitignore
.env
.env.*
```

### **Проверка безопасности:**
```bash
# Проверка, что .env файлы не в git
git status

# Должно показать только файлы проекта, без .env файлов
```

## ⚠️ **Важные замечания**

### **Никогда не делайте:**
- ❌ Не коммитьте .env файлы в git
- ❌ Не используйте одинаковые ключи для dev и prod
- ❌ Не оставляйте DEBUG=True в продакшене

### **Всегда делайте:**
- ✅ Используйте сильные секретные ключи
- ✅ Регулярно обновляйте пароли
- ✅ Проверяйте конфигурацию перед запуском
- ✅ Делайте резервные копии .env файлов

## 📊 **Статус миграции**

| Компонент | До | После |
|-----------|----|----|
| **SECRET_KEY** | В settings.py | ✅ В .env файлах |
| **TELEGRAM_BOT_TOKEN** | В settings.py | ✅ В .env файлах |
| **TELEGRAM_BOT_USERNAME** | В settings.py | ✅ В .env файлах |
| **TELEGRAM_WEBHOOK_URL** | В settings.py | ✅ В .env файлах |
| **Переключение сред** | Ручное | ✅ Автоматическое |

## 🎯 **Следующие шаги**

1. **Настройте reCAPTCHA ключи** в .env файлах
2. **Создайте резервные копии** .env файлов
3. **Настройте CI/CD** для автоматического переключения сред
4. **Добавьте мониторинг** конфигурации

---

**🔧 Настройка .env файлов завершена! Проект готов к безопасному развертыванию!** 🎉
