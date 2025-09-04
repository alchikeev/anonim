#!/bin/bash
# Скрипт для запуска в DEV режиме
echo "🚀 Запуск в DEV режиме..."
export DJANGO_ENV=dev
source venv/bin/activate
python manage.py runserver 127.0.0.1:8000
