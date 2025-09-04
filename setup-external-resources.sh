#!/bin/bash
# Скрипт для создания внешних томов и сети для продакшена

echo "Создание внешних томов и сети для anonim-web..."

# Создаем внешние тома
echo "Создание томов..."
docker volume create anonim_static_data
docker volume create anonim_media_data

# Создаем внешнюю сеть web (если не существует)
echo "Создание сети web..."
docker network create web 2>/dev/null || echo "Сеть web уже существует"

echo "Готово! Теперь можно запускать:"
echo "docker-compose up -d"

