# Аноним Мектеп

Веб-платформа для анонимного сбора сообщений о буллинге, вымогательстве и других проблемах в школах.

## Особенности

- 🔒 **Полная анонимность** - не сохраняются IP-адреса и другие идентифицирующие данные
- 🌐 **Многоязычность** - поддержка русского и кыргызского языков
- 📱 **Mobile-First дизайн** - адаптивный интерфейс для всех устройств
- 🤖 **Telegram интеграция** - мгновенные уведомления администраторам
- 🛡️ **reCAPTCHA защита** - защита от спама и ботов
- 👥 **Ролевая система** - разные уровни доступа для учителей, районных отделов и супер-админов

## Технологический стек

- **Backend**: Django 5.2.5
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **База данных**: SQLite3
- **Интеграции**: Telegram Bot API, Google reCAPTCHA v3

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd anonim
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env.dev` для разработки в корне проекта:

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

Для продакшена создайте файл `.env.prod`:

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

### 5. Генерация секретного ключа

```bash
# Генерация нового секретного ключа
python manage.py generate_secret_key

# Скопируйте полученный ключ в ваш .env.dev файл
```

### 6. Переключение между средами

```bash
# Переключение на среду разработки
python manage.py switch_env dev

# Переключение на продакшен среду
python manage.py switch_env prod

# Или через переменную окружения
export DJANGO_ENV=dev    # для разработки
export DJANGO_ENV=prod   # для продакшена
```

### 7. Обновление .env файлов

```bash
# Обновление .env.dev файла
python manage.py update_env --env dev

# Обновление .env.prod файла
python manage.py update_env --env prod
```

### 8. Настройка reCAPTCHA

```bash
# Показать инструкции по настройке
python manage.py setup_recaptcha

# Настроить для разработки (тестовые ключи)
python manage.py setup_recaptcha --env dev --public-key 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI --private-key 6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe

# Настроить для продакшена (реальные ключи)
python manage.py setup_recaptcha --env prod --public-key YOUR_REAL_PUBLIC_KEY --private-key YOUR_REAL_PRIVATE_KEY

# Тестирование reCAPTCHA
python manage.py test_recaptcha
```

### 9. Проверка конфигурации

```bash
# Проверка всех настроек проекта
python manage.py check_config
```

### 10. Применение миграций

```bash
python manage.py migrate
python manage.py init_data
python manage.py createsuperuser
```

### 11. Запуск сервера

```bash
python manage.py runserver
```

## Настройка Telegram бота

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Добавьте токен в переменную `TELEGRAM_BOT_TOKEN`
4. Для каждого пользователя получите chat_id:
   - Пользователь должен написать боту `/start`
   - Используйте API Telegram для получения chat_id

## Настройка reCAPTCHA

1. Зарегистрируйтесь на [Google reCAPTCHA](https://www.google.com/recaptcha/)
2. Создайте сайт с типом reCAPTCHA v3
3. Добавьте ключи в переменные окружения

## Структура проекта

```
anonim/
├── anonim_mektep/          # Основные настройки Django
├── core/                   # Основное приложение
│   ├── models.py          # Модели данных
│   ├── views.py           # Представления
│   ├── forms.py           # Формы
│   ├── templates/         # Шаблоны
│   └── static/            # Статические файлы
├── dashboard/             # Админ-панель
│   ├── models.py         # Модели сообщений
│   ├── views.py          # Представления дашборда
│   └── templates/        # Шаблоны админки
└── requirements.txt       # Зависимости
```

## Роли пользователей

### Супер-админ
- Полный доступ ко всем функциям
- Может управлять школами и пользователями
- Доступ ко всем сообщениям

### Районный отдел образования
- Доступ ко всем сообщениям в районе
- Может управлять учителями в школах района

### Учитель
- Доступ только к сообщениям своей школы
- Может изменять статусы и добавлять комментарии

## API и интеграции

### Telegram уведомления

Система автоматически отправляет уведомления в Telegram при получении новых сообщений:

- Учителя получают уведомления только по своей школе
- Районные отделы получают уведомления по всем школам
- Супер-админы получают все уведомления

### reCAPTCHA v3

Все формы отправки сообщений защищены reCAPTCHA v3 для предотвращения спама.

## Безопасность

- Все трафик должен быть зашифрован с помощью SSL
- Уникальные URL для каждой школы содержат случайные хеш-ключи
- Система не сохраняет IP-адреса или другие идентифицирующие данные
- Используется CSRF защита Django

## Развертывание в продакшене

### 1. Настройка переменных окружения

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SITE_DOMAIN=yourdomain.com
```

### 2. Обновление QR-кодов для нового домена

```bash
python manage.py update_qr_codes --domain yourdomain.com
```

### 3. Основные шаги развертывания

1. Установите PostgreSQL или другую production БД
2. Настройте веб-сервер (Nginx + Gunicorn)
3. Получите SSL сертификат (обязательно для reCAPTCHA)
4. Настройте переменные окружения для продакшена

### 4. Важные моменты при смене домена

- **QR-коды автоматически обновляются** при изменении `DJANGO_SITE_DOMAIN`
- **Telegram уведомления** используют правильный домен
- **Все ссылки в админке** показывают полные URL
- **Не забудьте распечатать новые QR-коды** для школ
5. Запустите `python manage.py collectstatic`

## Поддержка

Для получения поддержки обращайтесь к разработчикам проекта.

## Лицензия

Проект разработан для образовательных целей.
