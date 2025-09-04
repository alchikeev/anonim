# Telegram Bot в Docker

Этот документ описывает, как запустить Telegram бота в Docker контейнере.

## Структура

- `docker-compose.prod.yml` - конфигурация для продакшена
- `docker-compose.dev.yml` - конфигурация для разработки
- `telegram_bot_docker.sh` - скрипт для управления ботом

## Быстрый старт

### 1. Настройка переменных окружения

Создайте файл `.env.prod` на основе `env.prod.example`:

```bash
cp env.prod.example .env.prod
```

Заполните необходимые переменные:

```env
# Telegram Bot настройки
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_BOT_USERNAME=your_telegram_bot_username
TELEGRAM_WEBHOOK_URL=https://your-domain.com/telegram/webhook/
```

### 2. Запуск в продакшене

```bash
# Используя скрипт (рекомендуется)
./telegram_bot_docker.sh start-prod

# Или напрямую через docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Запуск в режиме разработки

```bash
# Создайте .env.dev на основе env.dev.example
cp env.dev.example .env.dev

# Запустите в режиме разработки
./telegram_bot_docker.sh start-dev
```

## Управление ботом

### Основные команды

```bash
# Запуск
./telegram_bot_docker.sh start-prod    # Продакшен
./telegram_bot_docker.sh start-dev     # Разработка

# Остановка
./telegram_bot_docker.sh stop prod     # Остановить продакшен
./telegram_bot_docker.sh stop dev      # Остановить разработку
./telegram_bot_docker.sh stop          # Остановить все

# Просмотр логов
./telegram_bot_docker.sh logs prod     # Логи продакшена
./telegram_bot_docker.sh logs dev      # Логи разработки

# Тестирование
./telegram_bot_docker.sh test prod     # Тест продакшена
./telegram_bot_docker.sh test dev      # Тест разработки

# Перезапуск
./telegram_bot_docker.sh restart prod  # Перезапуск продакшена
./telegram_bot_docker.sh restart dev   # Перезапуск разработки
```

### Прямые команды Docker Compose

```bash
# Продакшен
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml logs -f telegram-bot

# Разработка
docker-compose -f docker-compose.dev.yml up -d
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml logs -f telegram-bot
```

## Мониторинг

### Проверка статуса

```bash
# Статус всех сервисов
docker-compose -f docker-compose.prod.yml ps

# Логи в реальном времени
docker-compose -f docker-compose.prod.yml logs -f telegram-bot

# Проверка здоровья бота
docker-compose -f docker-compose.prod.yml exec telegram-bot python manage.py telegram_bot test
```

### Health Check

Контейнер Telegram бота настроен с health check, который:
- Проверяет работоспособность бота каждые 30 секунд
- Использует команду `python manage.py telegram_bot test`
- Таймаут: 10 секунд
- Количество попыток: 3
- Период запуска: 40 секунд

## Режимы работы

### Polling (текущий)

Бот работает в режиме polling - постоянно опрашивает Telegram API на предмет новых сообщений.

**Преимущества:**
- Простота настройки
- Не требует внешнего домена
- Работает за NAT/firewall

**Недостатки:**
- Больше нагрузки на сервер
- Задержка в получении сообщений

### Webhook (альтернатива)

Для использования webhook режима:

1. Убедитесь, что у вас есть SSL сертификат
2. Настройте `TELEGRAM_WEBHOOK_URL` в `.env.prod`
3. Установите webhook:
   ```bash
   docker-compose -f docker-compose.prod.yml exec telegram-bot python manage.py telegram_bot set-webhook --url https://your-domain.com/telegram/webhook/
   ```

## Устранение неполадок

### Бот не отвечает

1. Проверьте логи:
   ```bash
   ./telegram_bot_docker.sh logs prod
   ```

2. Проверьте переменные окружения:
   ```bash
   docker-compose -f docker-compose.prod.yml exec telegram-bot env | grep TELEGRAM
   ```

3. Протестируйте бота:
   ```bash
   ./telegram_bot_docker.sh test prod
   ```

### Ошибки подключения к базе данных

1. Убедитесь, что веб-сервис запущен:
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

2. Проверьте, что база данных доступна:
   ```bash
   docker-compose -f docker-compose.prod.yml exec telegram-bot python manage.py check
   ```

### Проблемы с правами доступа

1. Проверьте права на файлы:
   ```bash
   ls -la /srv/data_anonim/
   ls -la /srv/media_anonim/
   ```

2. Убедитесь, что контейнер может писать в эти директории

## Логи и отладка

### Просмотр логов

```bash
# Все логи
docker-compose -f docker-compose.prod.yml logs

# Только Telegram бот
docker-compose -f docker-compose.prod.yml logs telegram-bot

# Последние 100 строк
docker-compose -f docker-compose.prod.yml logs --tail=100 telegram-bot

# В реальном времени
docker-compose -f docker-compose.prod.yml logs -f telegram-bot
```

### Отладка

```bash
# Войти в контейнер
docker-compose -f docker-compose.prod.yml exec telegram-bot bash

# Запустить Django shell
docker-compose -f docker-compose.prod.yml exec telegram-bot python manage.py shell

# Проверить настройки
docker-compose -f docker-compose.prod.yml exec telegram-bot python manage.py check
```

## Обновление

```bash
# Остановить сервисы
./telegram_bot_docker.sh stop prod

# Пересобрать образы
docker-compose -f docker-compose.prod.yml build

# Запустить снова
./telegram_bot_docker.sh start-prod
```

## Безопасность

1. **Никогда не коммитьте файлы `.env.prod` и `.env.dev`**
2. **Используйте сильные пароли и токены**
3. **Регулярно обновляйте зависимости**
4. **Мониторьте логи на предмет подозрительной активности**

## Поддержка

При возникновении проблем:

1. Проверьте логи
2. Убедитесь, что все переменные окружения настроены
3. Проверьте, что все сервисы запущены
4. Обратитесь к документации Django и Telegram Bot API
