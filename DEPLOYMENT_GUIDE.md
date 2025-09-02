# Руководство по деплою проекта "Аноним Мектеп"

## Подготовка к деплою

### 1. Создайте файл .env.prod

Скопируйте `env.example` в `.env.prod` и заполните необходимые значения:

```bash
cp env.example .env.prod
```

**Обязательно заполните:**
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота
- `TELEGRAM_BOT_USERNAME` - имя пользователя бота
- `RECAPTCHA_PUBLIC_KEY` - публичный ключ reCAPTCHA
- `RECAPTCHA_PRIVATE_KEY` - приватный ключ reCAPTCHA

### 2. Настройте Telegram бота

1. Создайте бота через @BotFather в Telegram
2. Получите токен и добавьте в .env.prod
3. Настройте webhook URL: `https://anonim-m.online/telegram/webhook/`

### 3. Настройте reCAPTCHA

1. Зарегистрируйтесь на https://www.google.com/recaptcha/
2. Создайте новый сайт для домена `anonim-m.online`
3. Добавьте ключи в .env.prod

## Деплой

### Автоматический деплой

Запустите скрипт деплоя:

```bash
chmod +x deploy.sh
./deploy.sh
```

### Ручной деплой

1. **Создайте директорию на сервере:**
```bash
ssh root@79.133.181.227 "mkdir -p /root/anonim-mektep"
```

2. **Скопируйте файлы:**
```bash
rsync -avz --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' --exclude='.env.dev' . root@79.133.181.227:/root/anonim-mektep/
```

3. **Создайте volumes:**
```bash
ssh root@79.133.181.227 "mkdir -p /var/lib/docker/volumes/anonim_static_data/_data /var/lib/docker/volumes/anonim_media_data/_data"
```

4. **Запустите контейнер:**
```bash
ssh root@79.133.181.227 "cd /root/anonim-mektep && docker-compose -f docker-compose.caddy.yml up -d --build"
```

5. **Интегрируйте в Caddy:**
```bash
ssh root@79.133.181.227 "cd /root/anonim-mektep && chmod +x integrate_caddy.sh && ./integrate_caddy.sh"
```

6. **Перезапустите Caddy:**
```bash
ssh root@79.133.181.227 "docker restart tdp-caddy-1"
```

## Проверка работы

После деплоя проверьте:

1. **Статус контейнеров:**
```bash
ssh root@79.133.181.227 "docker ps | grep anonim"
```

2. **Логи приложения:**
```bash
ssh root@79.133.181.227 "docker logs anonim-mektep_anonim_web_1"
```

3. **Доступность сайта:**
- Откройте https://anonim-m.online в браузере
- Проверьте работу Telegram бота

## Управление

### Полезные команды

**Просмотр логов:**
```bash
ssh root@79.133.181.227 "docker logs anonim-mektep_anonim_web_1"
```

**Перезапуск приложения:**
```bash
ssh root@79.133.181.227 "cd /root/anonim-mektep && docker-compose -f docker-compose.caddy.yml restart"
```

**Остановка приложения:**
```bash
ssh root@79.133.181.227 "cd /root/anonim-mektep && docker-compose -f docker-compose.caddy.yml down"
```

**Обновление приложения:**
```bash
ssh root@79.133.181.227 "cd /root/anonim-mektep && docker-compose -f docker-compose.caddy.yml up -d --build"
```

## Структура на сервере

```
/root/anonim-mektep/          # Код приложения
/var/lib/docker/volumes/
├── anonim_static_data/       # Статические файлы
└── anonim_media_data/        # Медиа файлы
```

## Безопасность

- Файл `.env.prod` содержит секретные ключи - не коммитьте его в git
- Используйте HTTPS для всех соединений
- Регулярно обновляйте зависимости
- Мониторьте логи на предмет подозрительной активности

## Устранение неполадок

### Проблемы с SSL
Если SSL сертификат не создается автоматически, проверьте:
- Доступность домена anonim-m.online
- Настройки DNS
- Логи Caddy: `docker logs tdp-caddy-1`

### Проблемы с базой данных
Если возникают ошибки с базой данных:
```bash
ssh root@79.133.181.227 "cd /root/anonim-mektep && docker-compose -f docker-compose.caddy.yml exec anonim_web python manage.py migrate"
```

### Проблемы с Telegram ботом
Проверьте:
- Правильность токена в .env.prod
- Настройку webhook URL
- Логи бота в Django админке
