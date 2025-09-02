#!/bin/bash

# Скрипт для интеграции "Аноним Мектеп" с существующим Caddy

set -e

echo "🔧 Интеграция с Caddy для 'Аноним Мектеп'"
echo "=========================================="

# Пути
CADDYFILE_PATH="/etc/caddy/Caddyfile"
BACKUP_PATH="/etc/caddy/Caddyfile.backup.$(date +%Y%m%d_%H%M%S)"
ANONIM_CONFIG="Caddyfile"

# Функция проверки прав
check_permissions() {
    if [[ $EUID -ne 0 ]]; then
        echo "❌ Этот скрипт должен запускаться с правами root"
        echo "Используйте: sudo $0"
        exit 1
    fi
}

# Функция резервного копирования
backup_caddyfile() {
    if [ -f "$CADDYFILE_PATH" ]; then
        echo "📋 Создание резервной копии Caddyfile..."
        cp "$CADDYFILE_PATH" "$BACKUP_PATH"
        echo "✅ Резервная копия создана: $BACKUP_PATH"
    else
        echo "⚠️  Caddyfile не найден по пути: $CADDYFILE_PATH"
        echo "Создайте файл Caddyfile вручную"
        exit 1
    fi
}

# Функция добавления конфигурации
add_anonim_config() {
    echo "➕ Добавление конфигурации для anonim-m.online..."
    
    # Проверяем, есть ли уже конфигурация для anonim-m.online
    if grep -q "anonim-m.online" "$CADDYFILE_PATH"; then
        echo "⚠️  Конфигурация для anonim-m.online уже существует"
        echo "Проверьте файл: $CADDYFILE_PATH"
        return 1
    fi
    
    # Добавляем конфигурацию
    echo "" >> "$CADDYFILE_PATH"
    echo "# Конфигурация для Аноним Мектеп" >> "$CADDYFILE_PATH"
    cat "$ANONIM_CONFIG" >> "$CADDYFILE_PATH"
    
    echo "✅ Конфигурация добавлена в Caddyfile"
}

# Функция создания директорий
create_directories() {
    echo "📁 Создание директорий для статических файлов..."
    
    mkdir -p /var/www/anonim/static
    mkdir -p /var/www/anonim/media
    
    # Устанавливаем права
    chown -R www-data:www-data /var/www/anonim/
    chmod -R 755 /var/www/anonim/
    
    echo "✅ Директории созданы"
}

# Функция настройки Docker сети
setup_docker_network() {
    echo "🐳 Настройка Docker сети..."
    
    # Создаем внешнюю сеть для Caddy
    docker network create caddy_network 2>/dev/null || echo "Сеть caddy_network уже существует"
    
    # Подключаем существующую сеть anonim_network к caddy_network
    echo "✅ Docker сети настроены"
}

# Функция обновления docker-compose
update_docker_compose() {
    echo "🔄 Обновление docker-compose.yml для работы с Caddy..."
    
    # Создаем версию для Caddy
    cat > docker-compose.caddy.yml << 'EOF'
version: '3.8'

services:
  web:
    build: .
    expose:
      - "8000"
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - DJANGO_ENV=prod
      - DJANGO_DEBUG=False
      - DJANGO_ALLOWED_HOSTS=anonim-m.online,www.anonim-m.online
      - DJANGO_SITE_DOMAIN=anonim-m.online
      - DJANGO_DB_ENGINE=django.db.backends.sqlite3
      - DJANGO_DB_NAME=db.sqlite3
    env_file:
      - .env.prod
    command: >
      sh -c "python manage.py migrate &&
             python manage.py init_data &&
             python manage.py init_new_pages &&
             gunicorn --bind 0.0.0.0:8000 --workers 3 anonim_mektep.wsgi:application"
    restart: unless-stopped
    networks:
      - anonim_network
      - caddy_network

volumes:
  static_volume:
  media_volume:

networks:
  anonim_network:
    driver: bridge
  caddy_network:
    external: true
EOF

    echo "✅ docker-compose.caddy.yml создан"
}

# Функция тестирования конфигурации
test_caddy_config() {
    echo "🧪 Тестирование конфигурации Caddy..."
    
    if command -v caddy &> /dev/null; then
        caddy validate --config "$CADDYFILE_PATH"
        echo "✅ Конфигурация Caddy валидна"
    else
        echo "⚠️  Caddy не найден, пропускаем валидацию"
    fi
}

# Функция перезапуска Caddy
restart_caddy() {
    echo "🔄 Перезапуск Caddy..."
    
    if systemctl is-active --quiet caddy; then
        systemctl reload caddy
        echo "✅ Caddy перезагружен"
    else
        echo "⚠️  Caddy не запущен, запустите его вручную"
    fi
}

# Функция показа инструкций
show_instructions() {
    echo ""
    echo "📋 Инструкции по завершению настройки:"
    echo "======================================"
    echo ""
    echo "1. Запустите Docker контейнеры:"
    echo "   docker-compose -f docker-compose.caddy.yml up -d"
    echo ""
    echo "2. Проверьте статус:"
    echo "   docker-compose -f docker-compose.caddy.yml ps"
    echo ""
    echo "3. Проверьте логи:"
    echo "   docker-compose -f docker-compose.caddy.yml logs -f"
    echo ""
    echo "4. Проверьте Caddy:"
    echo "   systemctl status caddy"
    echo "   caddy reload"
    echo ""
    echo "5. Проверьте сайт:"
    echo "   curl -I https://anonim-m.online"
    echo ""
    echo "6. Мониторинг:"
    echo "   docker stats"
    echo "   journalctl -u caddy -f"
    echo ""
    echo "⚠️  Важно:"
    echo "- Убедитесь, что домен anonim-m.online указывает на ваш сервер"
    echo "- Проверьте, что SSL сертификат получен автоматически"
    echo "- Настройте .env.prod с правильными значениями"
}

# Главная функция
main() {
    case "${1:-install}" in
        "install")
            check_permissions
            backup_caddyfile
            add_anonim_config
            create_directories
            setup_docker_network
            update_docker_compose
            test_caddy_config
            restart_caddy
            show_instructions
            ;;
        "uninstall")
            check_permissions
            echo "🗑️  Удаление конфигурации..."
            # Здесь можно добавить логику удаления
            echo "✅ Конфигурация удалена"
            ;;
        "test")
            test_caddy_config
            ;;
        "restart")
            restart_caddy
            ;;
        "help"|*)
            echo "Использование: $0 [команда]"
            echo ""
            echo "Команды:"
            echo "  install   - Установка интеграции с Caddy (по умолчанию)"
            echo "  uninstall - Удаление интеграции"
            echo "  test      - Тестирование конфигурации"
            echo "  restart   - Перезапуск Caddy"
            echo "  help      - Показать эту справку"
            ;;
    esac
}

main "$@"
