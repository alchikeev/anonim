# 🏫 Аноним Мектеп

**Платформа для анонимных сообщений о проблемах в школах**

[![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 **О проекте**

"Аноним Мектеп" - это веб-платформа для сбора анонимных сообщений о проблемах в школах, включая буллинг, вымогательство и другие нарушения. Платформа обеспечивает полную анонимность и безопасность для учащихся.

### ✨ **Основные функции**
- 🔒 **Анонимная отправка сообщений** через QR-коды и уникальные ссылки
- 🌍 **Многоязычная поддержка** (Кыргызский, Русский)
- 👥 **Ролевая система** (Супер-админ, Районный отдел, Учитель)
- 🤖 **Telegram бот** для уведомлений и управления
- 🛡️ **reCAPTCHA v3** для защиты от спама
- 📱 **Адаптивный дизайн** для всех устройств

## 🚀 **Быстрый старт**

### **Локальная разработка**

```bash
# 1. Клонирование
git clone https://github.com/alchikeev/anonim.git
cd anonim

# 2. Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Настройка
cp env.example .env.dev
# Отредактируйте .env.dev

# 5. Инициализация
python manage.py migrate
python manage.py init_data
python manage.py createsuperuser

# 6. Запуск
python manage.py runserver
```

**Сайт будет доступен по адресу:** http://127.0.0.1:8000

### **Docker (рекомендуется для продакшена)**

```bash
# Настройка Docker
python manage.py docker_setup --env prod

# Запуск для разработки
./docker-build.sh dev

# Запуск для продакшена (с Nginx)
./docker-build.sh prod

# Запуск для продакшена (с Caddy)
./docker-build.sh prod-caddy
```

## 🐳 **Docker команды**

```bash
./docker-build.sh prod        # Продакшен с Nginx
./docker-build.sh prod-caddy  # Продакшен с Caddy
./docker-build.sh dev         # Разработка
./docker-build.sh stop        # Остановка
./docker-build.sh logs        # Логи
./docker-build.sh status      # Статус
./docker-build.sh shell       # Вход в контейнер
```

## 🚀 **Интеграция с Caddy**

Если у вас уже есть Caddy сервер:

```bash
# Автоматическая интеграция
sudo ./caddy-integration.sh install

# Запуск проекта
docker-compose -f docker-compose.caddy.yml up -d
```

## ⚙️ **Настройка**

### **Переменные окружения**

Создайте `.env.dev` или `.env.prod` на основе `env.example`:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True/False
DJANGO_SITE_DOMAIN=127.0.0.1:8000  # или anonim-m.online

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_BOT_USERNAME=your_bot_username

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=your_public_key
RECAPTCHA_PRIVATE_KEY=your_private_key
```

### **Telegram Bot**

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен
3. Добавьте в `.env` файл
4. Запустите: `python manage.py telegram_bot`

### **reCAPTCHA**

1. Зарегистрируйтесь на [Google reCAPTCHA](https://www.google.com/recaptcha/)
2. Создайте сайт с reCAPTCHA v3
3. Получите ключи
4. Настройте: `python manage.py setup_recaptcha`

## 📊 **Администрирование**

### **Панель администратора**
- **URL:** `/staff-login/`
- **Логин:** `admin` (по умолчанию)
- **Пароль:** `1234` (по умолчанию)

### **Роли пользователей**
- **Супер-админ:** Полный доступ ко всем функциям
- **Районный отдел:** Управление школами в районе
- **Учитель:** Просмотр сообщений своей школы

## 🛠️ **Команды управления**

```bash
# Инициализация
python manage.py init_data          # Начальные данные
python manage.py init_new_pages     # Новые страницы
python manage.py update_qr_codes    # Обновление QR-кодов

# Настройка
python manage.py setup_recaptcha    # reCAPTCHA
python manage.py test_recaptcha     # Тестирование
python manage.py docker_setup       # Docker

# Управление
python manage.py telegram_bot       # Telegram бот
python manage.py check_config       # Проверка конфигурации
python manage.py switch_env         # Переключение среды
```

## 📁 **Структура проекта**

```
anonim/
├── anonim_mektep/          # Настройки Django
├── core/                   # Основное приложение
├── dashboard/              # Приложение дашборда
├── static/                 # Статические файлы
├── media/                  # Медиа файлы
├── requirements.txt        # Зависимости
├── Dockerfile             # Docker образ
├── docker-compose.yml     # Docker Compose
├── Caddyfile              # Конфигурация Caddy
└── manage.py              # Управление Django
```

## 🔧 **Технологический стек**

- **Backend:** Django 5.2.5, Python 3.12
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **База данных:** SQLite3
- **Контейнеризация:** Docker, Docker Compose
- **Веб-сервер:** Nginx / Caddy
- **Интеграции:** Telegram Bot API, Google reCAPTCHA

## 📚 **Документация**

**Полная документация:** [DOCUMENTATION.md](DOCUMENTATION.md)

Включает:
- Подробную установку и настройку
- Docker развертывание
- Интеграцию с Caddy
- Администрирование
- Безопасность
- API и интеграции
- Разработку

## 🤝 **Вклад в проект**

1. Fork проекта
2. Создайте ветку для функции (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 **Лицензия**

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 **Поддержка**

- **GitHub Issues:** [Создать issue](https://github.com/alchikeev/anonim/issues)
- **Документация:** [DOCUMENTATION.md](DOCUMENTATION.md)
- **Разработчик:** alchikeev

---

**🎉 Спасибо за использование "Аноним Мектеп"!**

**Для быстрого старта:** `python manage.py runserver`  
**Для продакшена:** `./docker-build.sh prod`  
**Для Caddy:** `sudo ./caddy-integration.sh install`