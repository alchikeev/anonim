# 📚 Документация проекта "Аноним Мектеп"

## 📋 **Содержание**

1. [Обзор проекта](#обзор-проекта)
2. [Установка и настройка](#установка-и-настройка)
3. [Docker развертывание](#docker-развертывание)
4. [Интеграция с Caddy](#интеграция-с-caddy)
5. [Администрирование](#администрирование)
6. [Безопасность](#безопасность)
7. [API и интеграции](#api-и-интеграции)
8. [Разработка](#разработка)

---

## 🎯 **Обзор проекта**

### **Описание**
"Аноним Мектеп" - это веб-платформа для сбора анонимных сообщений о проблемах в школах, включая буллинг, вымогательство и другие нарушения.

### **Основные функции**
- ✅ **Анонимная отправка сообщений** через QR-коды и уникальные ссылки
- ✅ **Многоязычная поддержка** (Кыргызский, Русский)
- ✅ **Ролевая система** (Супер-админ, Районный отдел, Учитель)
- ✅ **Telegram бот** для уведомлений
- ✅ **reCAPTCHA v3** для защиты от спама
- ✅ **Адаптивный дизайн** для всех устройств

### **Технологический стек**
- **Backend:** Django 5.2.5, Python 3.12
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **База данных:** SQLite3
- **Контейнеризация:** Docker, Docker Compose
- **Веб-сервер:** Nginx / Caddy
- **Интеграции:** Telegram Bot API, Google reCAPTCHA

---

## 🚀 **Установка и настройка**

### **Требования**
- Python 3.12+
- Docker и Docker Compose (для продакшена)
- Git

### **Быстрая установка**

#### **1. Клонирование репозитория:**
```bash
git clone https://github.com/alchikeev/anonim.git
cd anonim
```

#### **2. Создание виртуального окружения:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

#### **3. Установка зависимостей:**
```bash
pip install -r requirements.txt
```

#### **4. Настройка переменных окружения:**
```bash
# Создайте .env.dev для разработки
cp env.example .env.dev

# Отредактируйте .env.dev с вашими настройками
nano .env.dev
```

#### **5. Инициализация базы данных:**
```bash
python manage.py migrate
python manage.py init_data
python manage.py init_new_pages
python manage.py createsuperuser
```

#### **6. Запуск сервера разработки:**
```bash
python manage.py runserver
```

### **Настройка переменных окружения**

#### **Основные переменные (.env.dev/.env.prod):**
```env
# Django настройки
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True/False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,anonim-m.online

# Домен сайта
DJANGO_SITE_DOMAIN=127.0.0.1:8000  # для dev
DJANGO_SITE_DOMAIN=anonim-m.online  # для prod

# База данных
DJANGO_DB_ENGINE=django.db.backends.sqlite3
DJANGO_DB_NAME=db.sqlite3

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_BOT_USERNAME=your_telegram_bot_username
TELEGRAM_WEBHOOK_URL=https://anonim-m.online/telegram/webhook/

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=your_recaptcha_public_key
RECAPTCHA_PRIVATE_KEY=your_recaptcha_private_key
```

---

## 🐳 **Docker развертывание**

### **Быстрый старт с Docker**

#### **Для разработки:**
```bash
# Настройка Docker
python manage.py docker_setup --env dev

# Запуск
./docker-build.sh dev

# Сайт: http://127.0.0.1:8000
```

#### **Для продакшена (с Nginx):**
```bash
# Настройка
python manage.py docker_setup --env prod

# Запуск
./docker-build.sh prod

# Сайт: https://anonim-m.online
```

### **Управление Docker контейнерами**

#### **Основные команды:**
```bash
# Запуск
./docker-build.sh prod

# Остановка
./docker-build.sh stop

# Логи
./docker-build.sh logs

# Статус
./docker-build.sh status

# Вход в контейнер
./docker-build.sh shell

# Очистка
./docker-build.sh clean
```

#### **Django команды в Docker:**
```bash
# Миграции
./docker-build.sh migrate

# Сбор статических файлов
./docker-build.sh collectstatic

# Инициализация данных
./docker-build.sh init
```

### **Структура Docker файлов**

#### **Dockerfile:**
- Python 3.12-slim образ
- Установка системных зависимостей
- Создание пользователя для безопасности
- Gunicorn для продакшена

#### **docker-compose.yml (Продакшен):**
- Web сервис с Gunicorn
- Nginx сервис с SSL
- Volumes для статических файлов
- Сетевая изоляция

#### **docker-compose.dev.yml (Разработка):**
- Web сервис с runserver
- Монтирование кода для разработки
- Горячая перезагрузка

---

## 🚀 **Интеграция с Caddy**

### **Для существующих Caddy серверов**

Если у вас уже есть Caddy сервер с другими сайтами, используйте интеграцию:

#### **Автоматическая установка:**
```bash
# Запустите скрипт интеграции
sudo ./caddy-integration.sh install

# Запустите проект
docker-compose -f docker-compose.caddy.yml up -d
```

#### **Ручная настройка:**

1. **Добавьте в ваш Caddyfile:**
```caddy
anonim-m.online, www.anonim-m.online {
    encode zstd gzip

    handle_path /static/* {
        root * /var/www/anonim/static
        file_server
        header Cache-Control "public, max-age=31536000, immutable"
    }

    handle_path /media/* {
        root * /var/www/anonim/media
        file_server
        header Cache-Control "public, max-age=31536000"
    }

    @sensitive {
        path /.env* /.git* /docker-compose* /Dockerfile*
    }
    respond @sensitive 404

    reverse_proxy anonim_web:8000 {
        header_up Host {host}
        header_up X-Real-IP {remote}
        header_up X-Forwarded-For {remote}
        header_up X-Forwarded-Proto {scheme}
    }

    header {
        X-Frame-Options "DENY"
        X-Content-Type-Options "nosniff"
        X-XSS-Protection "1; mode=block"
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    }
}
```

2. **Создайте директории:**
```bash
sudo mkdir -p /var/www/anonim/static
sudo mkdir -p /var/www/anonim/media
sudo chown -R www-data:www-data /var/www/anonim/
```

3. **Создайте Docker сеть:**
```bash
docker network create caddy_network
```

4. **Запустите проект:**
```bash
docker-compose -f docker-compose.caddy.yml up -d
```

### **Преимущества интеграции с Caddy**
- ✅ **Единый сервер** для всех сайтов
- ✅ **Автоматический SSL** для всех доменов
- ✅ **Централизованное управление**
- ✅ **Оптимизированная производительность**

---

## 👨‍💼 **Администрирование**

### **Роли пользователей**

#### **Супер-админ:**
- Полный доступ ко всем функциям
- Управление школами и пользователями
- Доступ к статистике
- Настройка системы

#### **Районный отдел образования:**
- Просмотр сообщений в своем районе
- Управление школами в районе
- Создание учителей
- Комментирование сообщений

#### **Учитель:**
- Просмотр сообщений своей школы
- Комментирование сообщений
- Изменение статуса сообщений

### **Панель администратора**

#### **Доступ:**
- URL: `/staff-login/`
- Логин: `admin` (по умолчанию)
- Пароль: `1234` (по умолчанию)

#### **Основные разделы:**
- **Дашборд** - статистика и обзор
- **Сообщения** - управление сообщениями
- **Школы** - управление школами
- **Пользователи** - управление пользователями
- **Контент** - редактирование страниц

### **Управление школами**

#### **Добавление школы:**
1. Перейдите в раздел "Школы"
2. Нажмите "Добавить школу"
3. Заполните данные школы
4. Сохраните - автоматически сгенерируется QR-код

#### **QR-коды и уникальные ссылки:**
- Каждая школа получает уникальный QR-код
- QR-код ведет на специальную страницу отправки сообщений
- Ссылки генерируются автоматически при создании школы

### **Управление сообщениями**

#### **Статусы сообщений:**
- **Новое** - только что получено
- **В работе** - принято к рассмотрению
- **Решено** - проблема решена
- **Отклонено** - сообщение отклонено

#### **Типы проблем:**
- Буллинг
- Вымогательство
- Насилие
- Дискриминация
- Другие нарушения

---

## 🔒 **Безопасность**

### **Защита от спама**
- **reCAPTCHA v3** - невидимая защита
- **Ограничение по времени** между отправками
- **Валидация данных** на сервере

### **Анонимность**
- **Не сохраняются IP адреса**
- **Уникальные ссылки** для каждой школы
- **QR-коды** для физического доступа

### **Ролевая безопасность**
- **Ограниченный доступ** по ролям
- **Проверка прав** на каждом уровне
- **Защита от эскалации** привилегий

### **Заголовки безопасности**
- **X-Frame-Options: DENY**
- **X-Content-Type-Options: nosniff**
- **X-XSS-Protection**
- **Strict-Transport-Security**

### **Docker безопасность**
- **Не root пользователь** в контейнерах
- **Изолированные сети**
- **Ограниченные volumes**

---

## 🤖 **API и интеграции**

### **Telegram Bot**

#### **Настройка:**
1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Добавьте токен в `.env` файл
4. Запустите команду: `python manage.py telegram_bot`

#### **Функции бота:**
- **Уведомления** о новых сообщениях
- **Интерактивные кнопки** для изменения статуса
- **Статистика** по сообщениям
- **Аутентификация** пользователей

#### **Команды бота:**
- `/start` - начало работы
- `/login` - вход в систему
- `/stats` - статистика
- `/help` - справка

### **reCAPTCHA v3**

#### **Настройка:**
1. Зарегистрируйтесь на [Google reCAPTCHA](https://www.google.com/recaptcha/)
2. Создайте сайт с reCAPTCHA v3
3. Получите ключи
4. Добавьте в `.env` файл

#### **Использование:**
```bash
# Настройка ключей
python manage.py setup_recaptcha

# Тестирование
python manage.py test_recaptcha

# Демо с тестовыми ключами
python manage.py demo_recaptcha
```

---

## 🛠️ **Разработка**

### **Структура проекта**

```
anonim/
├── anonim_mektep/          # Основные настройки Django
├── core/                   # Основное приложение
│   ├── models.py          # Модели данных
│   ├── views.py           # Представления
│   ├── urls.py            # URL маршруты
│   ├── admin.py           # Админ панель
│   ├── forms.py           # Формы
│   ├── templates/         # Шаблоны
│   └── management/        # Команды управления
├── dashboard/             # Приложение дашборда
├── static/               # Статические файлы
├── media/                # Медиа файлы
├── requirements.txt      # Зависимости Python
├── Dockerfile           # Docker образ
├── docker-compose.yml   # Docker Compose
└── manage.py           # Управление Django
```

### **Модели данных**

#### **User (Пользователь):**
- username, email, password
- role (super_admin, rayon_otdel, teacher)
- telegram_id, telegram_username
- school (связь с школой)

#### **School (Школа):**
- name, address, district
- unique_code, qr_code
- school_link (уникальная ссылка)

#### **Message (Сообщение):**
- school, problem_type, text
- status, created_at
- is_anonymous

#### **EditablePage (Редактируемые страницы):**
- page, language, title, content

### **Команды управления**

#### **Инициализация:**
```bash
python manage.py init_data          # Начальные данные
python manage.py init_new_pages     # Новые страницы
python manage.py update_qr_codes    # Обновление QR-кодов
```

#### **Настройка:**
```bash
python manage.py setup_recaptcha    # Настройка reCAPTCHA
python manage.py test_recaptcha     # Тестирование reCAPTCHA
python manage.py docker_setup       # Настройка Docker
```

#### **Управление:**
```bash
python manage.py telegram_bot       # Запуск Telegram бота
python manage.py check_config       # Проверка конфигурации
python manage.py switch_env         # Переключение среды
```

### **Тестирование**

#### **Проверка конфигурации:**
```bash
python manage.py check_config
```

#### **Проверка Django:**
```bash
python manage.py check
python manage.py test
```

#### **Проверка Docker:**
```bash
./docker-build.sh status
docker-compose ps
```

### **Отладка**

#### **Логи Django:**
```bash
# В разработке
python manage.py runserver

# В Docker
docker-compose logs -f web
```

#### **Логи Caddy/Nginx:**
```bash
# Caddy
journalctl -u caddy -f

# Nginx
tail -f /var/log/nginx/error.log
```

#### **Вход в контейнер:**
```bash
./docker-build.sh shell
# или
docker-compose exec web bash
```

---

## 📞 **Поддержка**

### **Полезные ссылки**
- **Репозиторий:** https://github.com/alchikeev/anonim.git
- **Документация Django:** https://docs.djangoproject.com/
- **Docker документация:** https://docs.docker.com/
- **Caddy документация:** https://caddyserver.com/docs/

### **Контакты**
- **Разработчик:** alchikeev
- **GitHub:** https://github.com/alchikeev

---

**🎉 Документация проекта "Аноним Мектеп" готова!** 

**Для быстрого старта:** `python manage.py runserver`  
**Для продакшена:** `./docker-build.sh prod`  
**Для Caddy:** `sudo ./caddy-integration.sh install`
