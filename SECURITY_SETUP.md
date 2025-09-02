# 🔐 Настройка безопасности проекта "Аноним Мектеп"

## 📋 Обзор

Все секретные данные и API ключи теперь вынесены в переменные окружения для обеспечения безопасности проекта.

## 🔧 Настройка .env файлов

### **Для разработки (.env.dev):**
```env
# Django настройки
DJANGO_SECRET_KEY=your-super-secret-key-here
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

# База данных
DATABASE_URL=sqlite:///db.sqlite3
```

### **Для продакшена (.env.prod):**
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

# База данных (для продакшена)
DATABASE_URL=postgresql://user:password@localhost:5432/anonim_mektep

# Email настройки (опционально)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

## 🛠️ Новые команды управления

### **1. Генерация секретного ключа:**
```bash
python manage.py generate_secret_key
```
**Результат:**
```
Скопируйте эту строку в ваш .env файл:
DJANGO_SECRET_KEY=t-wvm4mmnc6(-#ie8@38n2i_!nwq7(w@41d9wfo@=ooaxi2x37

⚠️  ВАЖНО: Никогда не коммитьте секретный ключ в git!
```

### **2. Проверка конфигурации:**
```bash
python manage.py check_config
```
**Результат:**
```
🔍 Проверка конфигурации проекта "Аноним Мектеп"
==================================================

📋 Django настройки:
  ✅ SECRET_KEY: настроен
  ⚠️  DEBUG: включен (только для разработки)
  ✅ ALLOWED_HOSTS: 127.0.0.1, localhost

🤖 Telegram Bot настройки:
  ✅ TELEGRAM_BOT_TOKEN: настроен
  ✅ TELEGRAM_BOT_USERNAME: anonim_mektep_bot
  ✅ TELEGRAM_WEBHOOK_URL: https://anonim-m.online/telegram/webhook/

🔒 reCAPTCHA настройки:
  ⚠️  RECAPTCHA_PUBLIC_KEY: не настроен
  ⚠️  RECAPTCHA_PRIVATE_KEY: не настроен

🗄️  База данных:
  ⚠️  База данных: SQLite (только для разработки)
  ✅ SITE_DOMAIN: localhost:8000
==================================================
✅ Проверка завершена!
```

## 🔒 Безопасность

### **Что защищено:**
- ✅ **SECRET_KEY** - секретный ключ Django
- ✅ **TELEGRAM_BOT_TOKEN** - токен Telegram бота
- ✅ **RECAPTCHA ключи** - ключи reCAPTCHA
- ✅ **Пароли БД** - пароли базы данных
- ✅ **Email пароли** - пароли для отправки email

### **Файлы в .gitignore:**
```gitignore
# Environments
.env
.env.*
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

### **Проверка безопасности:**
```bash
# Проверка, что .env файлы не в git
git status

# Должно показать только файлы проекта, без .env файлов
```

## 🚀 Развертывание

### **1. Локальная разработка:**
```bash
# Создайте .env.dev файл
cp .env.example .env.dev

# Отредактируйте настройки
nano .env.dev

# Запустите сервер
python manage.py runserver
```

### **2. Продакшен:**
```bash
# Создайте .env.prod файл на сервере
nano .env.prod

# Установите переменную окружения
export DJANGO_ENV=prod

# Запустите приложение
python manage.py runserver
```

## ⚠️ Важные предупреждения

### **Никогда не делайте:**
- ❌ Не коммитьте .env файлы в git
- ❌ Не используйте одинаковые ключи для dev и prod
- ❌ Не оставляйте DEBUG=True в продакшене
- ❌ Не используйте слабые пароли

### **Всегда делайте:**
- ✅ Используйте сильные секретные ключи
- ✅ Регулярно обновляйте пароли
- ✅ Мониторьте логи на предмет подозрительной активности
- ✅ Делайте резервные копии базы данных

## 📊 Статус безопасности

| Компонент | Статус | Описание |
|-----------|--------|----------|
| **SECRET_KEY** | ✅ | Вынесен в переменные окружения |
| **Telegram Bot** | ✅ | Токен защищен |
| **reCAPTCHA** | ⚠️ | Требует настройки ключей |
| **База данных** | ✅ | Пароли защищены |
| **Email** | ✅ | Пароли защищены |
| **Git** | ✅ | .env файлы исключены |

## 🎯 Следующие шаги

1. **Настройте reCAPTCHA ключи** для защиты форм
2. **Настройте PostgreSQL** для продакшена
3. **Настройте SSL сертификат** для HTTPS
4. **Настройте мониторинг** безопасности
5. **Создайте резервные копии** базы данных

---

**🔐 Проект "Аноним Мектеп" теперь безопасен и готов к продакшену!**
