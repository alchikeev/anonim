#!/bin/bash
# Скрипт для запуска в PROD режиме
echo "🚀 Запуск в PROD режиме..."
export DJANGO_ENV=prod
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
