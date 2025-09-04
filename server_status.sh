#!/bin/bash

# Скрипт для проверки статуса сервера и всех проектов
# Использование: ./server_status.sh

echo "🔍 Проверяем статус сервера и проектов..."
echo "=========================================="

# Проверяем статус контейнеров
echo "📦 Статус Docker контейнеров:"
ssh root@79.133.181.227 "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

echo ""
echo "🌐 Проверяем доступность сайтов:"

# Проверяем TDP
echo -n "TDP (thaidreamphuket.com): "
if curl -s -o /dev/null -w "%{http_code}" https://thaidreamphuket.com | grep -q "200"; then
    echo "✅ Работает"
else
    echo "❌ Недоступен"
fi

# Проверяем Аноним Мектеп
echo -n "Аноним Мектеп (anonim-m.online): "
if curl -s -o /dev/null -w "%{http_code}" https://anonim-m.online | grep -q "200"; then
    echo "✅ Работает"
else
    echo "❌ Недоступен"
fi

echo ""
echo "📊 Использование ресурсов:"
ssh root@79.133.181.227 "df -h / && echo '' && free -h"

echo ""
echo "📋 Последние логи:"
echo "TDP:"
ssh root@79.133.181.227 "docker logs tdp-tdp-1 --tail 3 2>/dev/null || echo 'Контейнер не найден'"

echo ""
echo "Аноним Мектеп:"
ssh root@79.133.181.227 "docker logs anonim-mektep-anonim_web-1 --tail 3 2>/dev/null || echo 'Контейнер не найден'"

echo ""
echo "Caddy:"
ssh root@79.133.181.227 "docker logs tdp-caddy-1 --tail 3 2>/dev/null || echo 'Контейнер не найден'"

