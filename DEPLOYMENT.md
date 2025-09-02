# 🚀 Инструкции по развертыванию на домене anonim-m.online

## 📋 Подготовка к развертыванию

### 1. Настройка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и зависимостей
sudo apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx -y

# Установка PostgreSQL (рекомендуется для продакшена)
sudo apt install postgresql postgresql-contrib -y
```

### 2. Клонирование проекта
```bash
# Создание директории
sudo mkdir -p /var/www/anonim-mektep
sudo chown $USER:$USER /var/www/anonim-mektep

# Клонирование (замените на ваш репозиторий)
cd /var/www/anonim-mektep
git clone <your-repo-url> .

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
```bash
# Создание .env.prod файла для продакшена
nano .env.prod
```

Содержимое `.env.prod`:
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

**⚠️ ВАЖНО:** 
- Замените `your-super-secret-production-key-here` на реальный секретный ключ
- Настройте reCAPTCHA ключи для продакшена
- Настройте базу данных PostgreSQL
- Убедитесь, что .env файлы не попадают в git (они уже в .gitignore)

### 4. Настройка базы данных
```bash
# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Загрузка начальных данных
python manage.py init_data

# Сбор статических файлов
python manage.py collectstatic --noinput
```

### 5. Настройка Gunicorn
```bash
# Установка Gunicorn
pip install gunicorn

# Создание systemd сервиса
sudo nano /etc/systemd/system/anonim-mektep.service
```

Содержимое сервиса:
```ini
[Unit]
Description=Anonim Mektep Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/anonim-mektep
Environment="PATH=/var/www/anonim-mektep/venv/bin"
ExecStart=/var/www/anonim-mektep/venv/bin/gunicorn --workers 3 --bind unix:/var/www/anonim-mektep/anonim_mektep.sock anonim_mektep.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

### 6. Настройка Nginx
```bash
# Создание конфигурации Nginx
sudo nano /etc/nginx/sites-available/anonim-mektep
```

Содержимое конфигурации:
```nginx
server {
    listen 80;
    server_name anonim-m.online www.anonim-m.online;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/anonim-mektep;
    }

    location /media/ {
        root /var/www/anonim-mektep;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/anonim-mektep/anonim_mektep.sock;
    }
}
```

### 7. Активация конфигураций
```bash
# Активация сайта
sudo ln -s /etc/nginx/sites-available/anonim-mektep /etc/nginx/sites-enabled/

# Проверка конфигурации
sudo nginx -t

# Перезапуск сервисов
sudo systemctl start anonim-mektep
sudo systemctl enable anonim-mektep
sudo systemctl restart nginx
```

### 8. Настройка SSL сертификата
```bash
# Получение SSL сертификата
sudo certbot --nginx -d anonim-m.online -d www.anonim-m.online

# Автоматическое обновление
sudo crontab -e
# Добавить строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### 9. Настройка Telegram бота
```bash
# Установка webhook
python manage.py telegram_bot set-webhook --url https://anonim-m.online/telegram/webhook/

# Проверка работы
python manage.py telegram_bot test
```

### 10. Настройка брандмауэра
```bash
# Разрешение HTTP и HTTPS
sudo ufw allow 'Nginx Full'

# Разрешение SSH
sudo ufw allow ssh

# Включение брандмауэра
sudo ufw enable
```

## 🔧 Полезные команды

### Управление сервисом
```bash
# Статус сервиса
sudo systemctl status anonim-mektep

# Перезапуск сервиса
sudo systemctl restart anonim-mektep

# Логи сервиса
sudo journalctl -u anonim-mektep -f
```

### Управление Nginx
```bash
# Перезапуск Nginx
sudo systemctl restart nginx

# Проверка конфигурации
sudo nginx -t

# Логи Nginx
sudo tail -f /var/log/nginx/error.log
```

### Управление ботом
```bash
# Информация о боте
python manage.py telegram_bot get-info

# Установка webhook
python manage.py telegram_bot set-webhook --url https://anonim-m.online/telegram/webhook/

# Удаление webhook
python manage.py telegram_bot delete-webhook
```

## 📱 QR-коды для школ

После развертывания QR-коды будут доступны по адресам:
- **Арстан**: https://anonim-m.online/send/38d5b3c2d765/
- **Школа №1**: https://anonim-m.online/send/f404dcb3ecdc/
- **Школа №2**: https://anonim-m.online/send/68c743f3e8c0/
- **Школа №3**: https://anonim-m.online/send/9a027944b808/
- **Гимназия №4**: https://anonim-m.online/send/f3adce141e48/
- **Лицей №5**: https://anonim-m.online/send/99f4f4896bf6/
- **Районный отдел**: https://anonim-m.online/send/general/

## 🔐 Безопасность

### Рекомендации:
1. **Используйте сильный SECRET_KEY**
2. **Настройте регулярные бэкапы базы данных**
3. **Мониторьте логи на предмет подозрительной активности**
4. **Обновляйте зависимости регулярно**
5. **Используйте HTTPS для всех соединений**

### Бэкапы:
```bash
# Создание бэкапа базы данных
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Восстановление из бэкапа
python manage.py loaddata backup_20250902_120000.json
```

## 📊 Мониторинг

### Логи приложения:
```bash
# Логи Django
tail -f /var/log/anonim-mektep/django.log

# Логи Gunicorn
sudo journalctl -u anonim-mektep -f

# Логи Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🚨 Устранение неполадок

### Проблемы с ботом:
```bash
# Проверка webhook
python manage.py telegram_bot get-info

# Переустановка webhook
python manage.py telegram_bot delete-webhook
python manage.py telegram_bot set-webhook --url https://anonim-m.online/telegram/webhook/
```

### Проблемы с сервисом:
```bash
# Проверка статуса
sudo systemctl status anonim-mektep

# Перезапуск
sudo systemctl restart anonim-mektep

# Проверка логов
sudo journalctl -u anonim-mektep --since "1 hour ago"
```

---

**🎉 После выполнения всех шагов ваш сайт будет доступен по адресу: https://anonim-m.online**
