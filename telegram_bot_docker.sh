#!/bin/bash

# Скрипт для управления Telegram ботом в Docker

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Проверка наличия Docker и Docker Compose
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker не установлен"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose не установлен"
        exit 1
    fi
}

# Функция для запуска в режиме разработки
start_dev() {
    print_header "Запуск Telegram бота в режиме разработки"
    check_dependencies
    
    if [ ! -f ".env.dev" ]; then
        print_warning "Файл .env.dev не найден. Создайте его на основе env.dev.example"
        exit 1
    fi
    
    print_message "Запуск сервисов..."
    docker-compose -f docker-compose.dev.yml up -d
    
    print_message "Проверка статуса сервисов..."
    docker-compose -f docker-compose.dev.yml ps
    
    print_message "Просмотр логов Telegram бота..."
    docker-compose -f docker-compose.dev.yml logs -f telegram-bot
}

# Функция для запуска в продакшене
start_prod() {
    print_header "Запуск Telegram бота в продакшене"
    check_dependencies
    
    if [ ! -f ".env.prod" ]; then
        print_warning "Файл .env.prod не найден. Создайте его на основе env.prod.example"
        exit 1
    fi
    
    print_message "Запуск сервисов..."
    docker-compose -f docker-compose.prod.yml up -d
    
    print_message "Проверка статуса сервисов..."
    docker-compose -f docker-compose.prod.yml ps
    
    print_message "Просмотр логов Telegram бота..."
    docker-compose -f docker-compose.prod.yml logs -f telegram-bot
}

# Функция для остановки сервисов
stop_services() {
    print_header "Остановка сервисов"
    
    if [ "$1" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml down
        print_message "Сервисы разработки остановлены"
    elif [ "$1" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml down
        print_message "Сервисы продакшена остановлены"
    else
        print_message "Остановка всех сервисов..."
        docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
        docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
        print_message "Все сервисы остановлены"
    fi
}

# Функция для просмотра логов
view_logs() {
    print_header "Просмотр логов Telegram бота"
    
    if [ "$1" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml logs -f telegram-bot
    elif [ "$1" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml logs -f telegram-bot
    else
        print_error "Укажите режим: dev или prod"
        exit 1
    fi
}

# Функция для тестирования бота
test_bot() {
    print_header "Тестирование Telegram бота"
    
    if [ "$1" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml exec telegram-bot python manage.py telegram_bot test
    elif [ "$1" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml exec telegram-bot python manage.py telegram_bot test
    else
        print_error "Укажите режим: dev или prod"
        exit 1
    fi
}

# Функция для перезапуска бота
restart_bot() {
    print_header "Перезапуск Telegram бота"
    
    if [ "$1" = "dev" ]; then
        docker-compose -f docker-compose.dev.yml restart telegram-bot
        print_message "Telegram бот перезапущен (dev)"
    elif [ "$1" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml restart telegram-bot
        print_message "Telegram бот перезапущен (prod)"
    else
        print_error "Укажите режим: dev или prod"
        exit 1
    fi
}

# Функция для показа справки
show_help() {
    echo "Использование: $0 [КОМАНДА] [РЕЖИМ]"
    echo ""
    echo "Команды:"
    echo "  start-dev     Запуск в режиме разработки"
    echo "  start-prod    Запуск в продакшене"
    echo "  stop [режим]  Остановка сервисов (dev/prod или все)"
    echo "  logs [режим]  Просмотр логов (dev/prod)"
    echo "  test [режим]  Тестирование бота (dev/prod)"
    echo "  restart [режим] Перезапуск бота (dev/prod)"
    echo "  help          Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0 start-dev"
    echo "  $0 start-prod"
    echo "  $0 stop dev"
    echo "  $0 logs prod"
    echo "  $0 test dev"
    echo "  $0 restart prod"
}

# Основная логика
case "$1" in
    "start-dev")
        start_dev
        ;;
    "start-prod")
        start_prod
        ;;
    "stop")
        stop_services "$2"
        ;;
    "logs")
        view_logs "$2"
        ;;
    "test")
        test_bot "$2"
        ;;
    "restart")
        restart_bot "$2"
        ;;
    "help"|"--help"|"-h"|"")
        show_help
        ;;
    *)
        print_error "Неизвестная команда: $1"
        show_help
        exit 1
        ;;
esac
