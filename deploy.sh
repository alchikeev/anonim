#!/bin/bash

# Скрипт для деплоя проекта "Аноним Мектеп" на сервер
# Использование: ./deploy.sh

set -e  # Остановка при ошибке

echo "🚀 Начинаем деплой проекта 'Аноним Мектеп'..."

# Проверяем наличие необходимых файлов
if [ ! -f ".env.prod" ]; then
    echo "❌ Ошибка: Файл .env.prod не найден!"
    echo "Создайте файл .env.prod на основе env.example"
    exit 1
fi

if [ ! -f "docker-compose.caddy.yml" ]; then
    echo "❌ Ошибка: Файл docker-compose.caddy.yml не найден!"
    exit 1
fi

# Создаем директорию для проекта на сервере
echo "📁 Создаем директорию проекта на сервере..."
ssh root@79.133.181.227 "mkdir -p /root/anonim-mektep"

# Копируем файлы проекта на сервер
echo "📤 Копируем файлы проекта на сервер..."
rsync -avz --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' --exclude='.env.dev' . root@79.133.181.227:/root/anonim-mektep/

# Создаем директории для volumes на сервере
echo "📂 Создаем директории для Docker volumes..."
ssh root@79.133.181.227 "mkdir -p /var/lib/docker/volumes/anonim_static_data/_data /var/lib/docker/volumes/anonim_media_data/_data"

# Собираем и запускаем контейнер
echo "🐳 Собираем и запускаем Docker контейнер..."
ssh root@79.133.181.227 "cd /root/anonim-mektep && docker-compose -f docker-compose.caddy.yml up -d --build"

# Интегрируем конфигурацию в Caddy
echo "🔧 Интегрируем конфигурацию в Caddy..."
ssh root@79.133.181.227 "cd /root/anonim-mektep && chmod +x integrate_caddy.sh && ./integrate_caddy.sh"

# Перезапускаем Caddy для применения изменений
echo "🔄 Перезапускаем Caddy..."
ssh root@79.133.181.227 "docker restart tdp-caddy-1"

# Проверяем статус контейнеров
echo "✅ Проверяем статус контейнеров..."
ssh root@79.133.181.227 "docker ps | grep anonim"

echo "🎉 Деплой завершен!"
echo "🌐 Ваш сайт должен быть доступен по адресу: https://anonim-m.online"
echo ""
echo "📋 Полезные команды:"
echo "  Просмотр логов: ssh root@79.133.181.227 'docker logs anonim-mektep_anonim_web_1'"
echo "  Перезапуск: ssh root@79.133.181.227 'cd /root/anonim-mektep && docker-compose -f docker-compose.caddy.yml restart'"
echo "  Остановка: ssh root@79.133.181.227 'cd /root/anonim-mektep && docker-compose -f docker-compose.caddy.yml down'"
