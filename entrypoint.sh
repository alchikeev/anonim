#!/usr/bin/env bash
set -e

# ожидание БД (если нужна) — по необходимости можно добавить wait-for-it
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# gunicorn (замени core.wsgi на фактический модуль)
exec gunicorn anonim_mektep.wsgi:application -b 0.0.0.0:8000 -w 2 --timeout 120

