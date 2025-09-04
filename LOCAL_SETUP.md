# Локальная настройка и запуск Anonim Mektep

Этот документ описывает, как настроить и запустить проект Anonim Mektep локально на вашем компьютере.

## 🚀 Быстрый старт

### 1. Подготовка

Убедитесь, что у вас установлены:
- Python 3.8+ 
- Git

### 2. Клонирование и настройка

```bash
# Клонируйте репозиторий (если еще не сделано)
git clone <repository-url>
cd anonim

# Запустите скрипт настройки
./start.sh
```

Скрипт автоматически:
- Создаст виртуальное окружение
- Установит зависимости
- Настроит базу данных
- Запустит Django сервер и Telegram бота

## 📋 Подробная настройка

### 1. Настройка переменных окружения

Создайте файл `.env.dev`:

```bash
cp env.dev.example .env.dev
```

Отредактируйте `.env.dev` и настройте необходимые переменные:

```env
# Django настройки
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

# Telegram Bot настройки (обязательно для работы бота)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_BOT_USERNAME=your_telegram_bot_username
TELEGRAM_WEBHOOK_URL=http://localhost:8000/telegram/webhook/

# reCAPTCHA настройки (тестовые ключи уже настроены)
RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
```

### 2. Получение Telegram Bot Token

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env.dev`

## 🎮 Использование скрипта start.sh

### Основные команды

```bash
# Запустить все сервисы (Django + Telegram бот)
./start.sh

# Запустить только Django сервер
./start.sh --django-only

# Запустить только Telegram бота
./start.sh --bot-only

# Запустить без Telegram бота
./start.sh --no-bot

# Запустить Django на другом порту
./start.sh --port 8080

# Показать статус сервисов
./start.sh --status

# Показать справку
./start.sh --help
```

### Что делает скрипт

1. **Проверяет виртуальное окружение** - создает если не существует
2. **Активирует виртуальное окружение** - автоматически
3. **Устанавливает зависимости** - из requirements.txt
4. **Проверяет настройки** - файл .env.dev
5. **Настраивает базу данных** - выполняет миграции
6. **Запускает сервисы** - Django сервер и/или Telegram бот
7. **Мониторит логи** - показывает все логи в реальном времени

## 🌐 Доступ к приложению

После запуска скрипта:

- **Веб-сайт**: http://localhost:8000
- **Админка**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

## 🤖 Telegram бот

### Настройка бота

1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен и username
3. Добавьте их в `.env.dev`
4. Запустите скрипт

### Тестирование бота

```bash
# Найти вашего бота в Telegram по username
# Отправить команду /start
# Следовать инструкциям для авторизации
```

### Команды бота

- `/start` - Начать работу с ботом
- Авторизация через логин/пароль
- Просмотр сообщений и статистики
- Управление статусами сообщений

## 🔧 Ручная настройка (альтернатива)

Если скрипт не работает, можете настроить вручную:

```bash
# 1. Создать виртуальное окружение
python3 -m venv venv

# 2. Активировать виртуальное окружение
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить переменные окружения
cp env.dev.example .env.dev
# Отредактировать .env.dev

# 5. Настроить базу данных
python manage.py migrate

# 6. Создать суперпользователя (опционально)
python manage.py createsuperuser

# 7. Запустить Django сервер
python manage.py runserver

# 8. В другом терминале запустить Telegram бота
python manage.py telegram_polling
```

## 🐛 Устранение неполадок

### Проблема: Скрипт не запускается

```bash
# Проверьте права на выполнение
chmod +x start.sh

# Проверьте, что вы в правильной директории
pwd
ls -la start.sh
```

### Проблема: Python не найден

```bash
# Установите Python 3.8+
# Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS:
brew install python3

# Windows:
# Скачайте с python.org
```

### Проблема: Telegram бот не отвечает

1. Проверьте токен в `.env.dev`
2. Убедитесь, что бот создан через @BotFather
3. Проверьте логи в терминале
4. Попробуйте перезапустить скрипт

### Проблема: База данных не работает

```bash
# Удалите базу данных и пересоздайте
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Проблема: Порт занят

```bash
# Используйте другой порт
./start.sh --port 8080

# Или найдите и остановите процесс на порту 8000
lsof -ti:8000 | xargs kill -9
```

## 📊 Мониторинг

### Логи в реальном времени

Скрипт автоматически показывает все логи:
- **Django** - веб-сервер, запросы, ошибки
- **Telegram** - сообщения бота, API запросы
- **База данных** - SQL запросы, миграции

### Остановка сервисов

Нажмите `Ctrl+C` в терминале где запущен скрипт. Все сервисы остановятся автоматически.

### Проверка статуса

```bash
./start.sh --status
```

## 🔄 Обновление

```bash
# Остановите скрипт (Ctrl+C)
git pull origin main
./start.sh
```

## 📝 Полезные команды Django

```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Собрать статические файлы
python manage.py collectstatic

# Запустить тесты
python manage.py test

# Django shell
python manage.py shell

# Проверить настройки
python manage.py check
```

## 🆘 Поддержка

При возникновении проблем:

1. Проверьте логи в терминале
2. Убедитесь, что все зависимости установлены
3. Проверьте настройки в `.env.dev`
4. Попробуйте перезапустить скрипт
5. Обратитесь к документации Django

## 📚 Дополнительные ресурсы

- [Django Documentation](https://docs.djangoproject.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
