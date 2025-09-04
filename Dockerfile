FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . /app

# Аргумент окружения: dev|prod
ARG DJANGO_ENV=dev
ENV DJANGO_ENV=${DJANGO_ENV}

# Сбор статики (OK, если в dev её ещё нет)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["gunicorn", "anonim_mektep.wsgi:application", "--bind", "0.0.0.0:8000"]