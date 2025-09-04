#!/bin/bash
# Скрипт для запуска Telegram бота в DEV режиме
echo "🤖 Запуск Telegram бота в DEV режиме..."
export DJANGO_ENV=dev
source venv/bin/activate
python manage.py telegram_polling --timeout=30
