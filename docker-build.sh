#!/bin/bash

# Скрипт для сборки и запуска Docker контейнеров

set -e

echo "🐳 Сборка и запуск Docker контейнеров для Аноним Мектеп"
echo "=================================================="

# Проверяем наличие .env файлов
if [ ! -f ".env.prod" ]; then
    echo "❌ Файл .env.prod не найден!"
    echo "Создайте файл .env.prod с настройками для продакшена"
    exit 1
fi

if [ ! -f ".env.dev" ]; then
    echo "❌ Файл .env.dev не найден!"
    echo "Создайте файл .env.dev с настройками для разработки"
    exit 1
fi

# Функция для продакшена
build_prod() {
    echo "🚀 Сборка для продакшена..."
    docker-compose build
    
    echo "📦 Запуск контейнеров..."
    docker-compose up -d
    
    echo "✅ Продакшен запущен!"
    echo "🌐 Сайт доступен по адресу: https://anonim-m.online"
    echo "📊 Логи: docker-compose logs -f"
}

# Функция для продакшена с Caddy
build_prod_caddy() {
    echo "🚀 Сборка для продакшена с Caddy..."
    docker-compose -f docker-compose.caddy.yml build
    
    echo "📦 Запуск контейнеров с Caddy..."
    docker-compose -f docker-compose.caddy.yml up -d
    
    echo "✅ Продакшен с Caddy запущен!"
    echo "🌐 Сайт доступен по адресу: https://anonim-m.online"
    echo "📊 Логи: docker-compose -f docker-compose.caddy.yml logs -f"
}

# Функция для разработки
build_dev() {
    echo "🛠️ Сборка для разработки..."
    docker-compose -f docker-compose.dev.yml build
    
    echo "📦 Запуск контейнеров для разработки..."
    docker-compose -f docker-compose.dev.yml up -d
    
    echo "✅ Разработка запущена!"
    echo "🌐 Сайт доступен по адресу: http://127.0.0.1:8000"
    echo "📊 Логи: docker-compose -f docker-compose.dev.yml logs -f"
}

# Функция остановки
stop_containers() {
    echo "🛑 Остановка контейнеров..."
    docker-compose down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    docker-compose -f docker-compose.caddy.yml down 2>/dev/null || true
    echo "✅ Контейнеры остановлены!"
}

# Функция очистки
clean_containers() {
    echo "🧹 Очистка контейнеров и образов..."
    docker-compose down --rmi all --volumes --remove-orphans 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down --rmi all --volumes --remove-orphans 2>/dev/null || true
    docker-compose -f docker-compose.caddy.yml down --rmi all --volumes --remove-orphans 2>/dev/null || true
    docker system prune -f
    echo "✅ Очистка завершена!"
}

# Функция показа логов
show_logs() {
    echo "📊 Показ логов..."
    if docker-compose ps | grep -q "Up"; then
        docker-compose logs -f
    elif docker-compose -f docker-compose.dev.yml ps | grep -q "Up"; then
        docker-compose -f docker-compose.dev.yml logs -f
    elif docker-compose -f docker-compose.caddy.yml ps | grep -q "Up"; then
        docker-compose -f docker-compose.caddy.yml logs -f
    else
        echo "❌ Нет запущенных контейнеров"
    fi
}

# Функция показа статуса
show_status() {
    echo "📊 Статус контейнеров..."
    echo "=== Продакшен (Nginx) ==="
    docker-compose ps 2>/dev/null || echo "Не запущен"
    echo ""
    echo "=== Разработка ==="
    docker-compose -f docker-compose.dev.yml ps 2>/dev/null || echo "Не запущен"
    echo ""
    echo "=== Продакшен (Caddy) ==="
    docker-compose -f docker-compose.caddy.yml ps 2>/dev/null || echo "Не запущен"
}

# Функция входа в контейнер
enter_container() {
    echo "🔧 Вход в контейнер..."
    if docker-compose ps | grep -q "Up"; then
        docker-compose exec web bash
    elif docker-compose -f docker-compose.dev.yml ps | grep -q "Up"; then
        docker-compose -f docker-compose.dev.yml exec web bash
    elif docker-compose -f docker-compose.caddy.yml ps | grep -q "Up"; then
        docker-compose -f docker-compose.caddy.yml exec web bash
    else
        echo "❌ Нет запущенных контейнеров"
    fi
}

# Функция выполнения команд Django
run_django_command() {
    echo "🐍 Выполнение Django команды: $1"
    if docker-compose ps | grep -q "Up"; then
        docker-compose exec web python manage.py $1
    elif docker-compose -f docker-compose.dev.yml ps | grep -q "Up"; then
        docker-compose -f docker-compose.dev.yml exec web python manage.py $1
    elif docker-compose -f docker-compose.caddy.yml ps | grep -q "Up"; then
        docker-compose -f docker-compose.caddy.yml exec web python manage.py $1
    else
        echo "❌ Нет запущенных контейнеров"
    fi
}

# Главное меню
case "$1" in
    "prod")
        build_prod
        ;;
    "prod-caddy")
        build_prod_caddy
        ;;
    "dev")
        build_dev
        ;;
    "stop")
        stop_containers
        ;;
    "clean")
        clean_containers
        ;;
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    "shell")
        enter_container
        ;;
    "migrate")
        run_django_command "migrate"
        ;;
    "collectstatic")
        run_django_command "collectstatic --noinput"
        ;;
    "init")
        run_django_command "init_data"
        ;;
    "help"|"")
        echo "Использование: $0 [команда]"
        echo ""
        echo "Команды:"
        echo "  prod        - Сборка и запуск для продакшена (с Nginx)"
        echo "  prod-caddy  - Сборка и запуск для продакшена (с Caddy)"
        echo "  dev         - Сборка и запуск для разработки"
        echo "  stop        - Остановка всех контейнеров"
        echo "  clean       - Очистка контейнеров и образов"
        echo "  logs        - Показ логов"
        echo "  status      - Статус контейнеров"
        echo "  shell       - Вход в контейнер"
        echo "  migrate     - Выполнить миграции"
        echo "  collectstatic - Собрать статические файлы"
        echo "  init        - Инициализировать данные"
        echo "  help        - Показать эту справку"
        echo ""
        echo "Для интеграции с существующим Caddy используйте:"
        echo "  ./caddy-integration.sh install"
        ;;
    *)
        echo "❌ Неизвестная команда: $1"
        echo "Используйте '$0 help' для справки"
        exit 1
        ;;
esac
