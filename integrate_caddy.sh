#!/bin/bash

# Скрипт для интеграции конфигурации "Аноним Мектеп" в существующий Caddyfile
# Этот скрипт добавляет конфигурацию для anonim-m.online в существующий Caddyfile

echo "Интеграция конфигурации 'Аноним Мектеп' в Caddyfile..."

# Проверяем, существует ли текущий Caddyfile
if [ ! -f "/root/Caddyfile.current" ]; then
    echo "Ошибка: Файл /root/Caddyfile.current не найден!"
    exit 1
fi

# Создаем резервную копию
cp /root/Caddyfile.current /root/Caddyfile.backup.$(date +%Y%m%d_%H%M%S)

# Добавляем конфигурацию для anonim-m.online
cat >> /root/Caddyfile.current << 'EOF'

# Конфигурация для "Аноним Мектеп"
anonim-m.online, www.anonim-m.online {
    encode zstd gzip

    # Раздача статических файлов из Docker volume
    handle_path /static/* {
        root * /var/lib/docker/volumes/anonim_static_data/_data
        file_server
        header Cache-Control "public, max-age=31536000, immutable"
    }

    # Раздача медиа файлов из Docker volume
    handle_path /media/* {
        root * /var/lib/docker/volumes/anonim_media_data/_data
        file_server
        header Cache-Control "public, max-age=31536000"
    }

    # Безопасность - блокируем доступ к служебным файлам
    @sensitive {
        path /.env* /.git* /docker-compose* /Dockerfile* /nginx.conf
    }
    respond @sensitive 404

    # Прокси на Django приложение (сервис anonim_web внутри docker-сети caddy_network)
    reverse_proxy anonim_web:8000 {
        header_up Host {host}
        header_up X-Real-IP {remote}
        header_up X-Forwarded-For {remote}
        header_up X-Forwarded-Proto {scheme}
        header_up X-Forwarded-Port {server_port}
    }

    # Логирование
    log {
        output stdout
        format console
        level INFO
    }

    # Заголовки безопасности
    header {
        # Безопасность
        X-Frame-Options "DENY"
        X-Content-Type-Options "nosniff"
        X-XSS-Protection "1; mode=block"
        Referrer-Policy "strict-origin-when-cross-origin"
        
        # HSTS для HTTPS
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        
        # Удаляем заголовки сервера
        -Server
    }

    # Ограничение размера загружаемых файлов
    request_body {
        max_size 10MB
    }
}
EOF

echo "Конфигурация успешно добавлена в Caddyfile!"
echo "Для применения изменений перезапустите Caddy:"
echo "docker restart tdp-caddy-1"
