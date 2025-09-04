#!/bin/bash
# Скрипт для запуска Telegram бота в PROD режиме
echo "🤖 Запуск Telegram бота в PROD режиме..."
export DJANGO_ENV=prod
source venv/bin/activate
python manage.py telegram_polling --timeout=30
