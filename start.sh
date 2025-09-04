#!/bin/bash

# Скрипт для локального запуска Anonim Mektep
# Включает виртуальное окружение, запускает Django сервер и Telegram бота

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Функции для вывода сообщений
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

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_telegram() {
    echo -e "${PURPLE}[TELEGRAM]${NC} $1"
}

print_django() {
    echo -e "${CYAN}[DJANGO]${NC} $1"
}

# Переменные
VENV_DIR="venv"
ENV_FILE=".env.dev"
DJANGO_PORT=8000
TELEGRAM_PID=""
DJANGO_PID=""

# Функция для очистки при завершении
cleanup() {
    print_message "Остановка сервисов..."
    
    if [ ! -z "$TELEGRAM_PID" ]; then
        print_telegram "Остановка Telegram бота (PID: $TELEGRAM_PID)..."
        kill $TELEGRAM_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$DJANGO_PID" ]; then
        print_django "Остановка Django сервера (PID: $DJANGO_PID)..."
        kill $DJANGO_PID 2>/dev/null || true
    fi
    
    print_success "Все сервисы остановлены"
    exit 0
}

# Устанавливаем обработчик сигналов
trap cleanup SIGINT SIGTERM

# Функция проверки виртуального окружения
check_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        print_error "Виртуальное окружение не найдено в директории $VENV_DIR"
        print_message "Создаю виртуальное окружение..."
        python3 -m venv $VENV_DIR
        print_success "Виртуальное окружение создано"
    fi
}

# Функция активации виртуального окружения
activate_venv() {
    print_message "Активация виртуального окружения..."
    source $VENV_DIR/bin/activate
    print_success "Виртуальное окружение активировано"
}

# Функция установки зависимостей
install_dependencies() {
    print_message "Проверка зависимостей..."
    if [ -f "requirements.txt" ]; then
        print_message "Установка зависимостей из requirements.txt..."
        pip install -r requirements.txt
        print_success "Зависимости установлены"
    else
        print_warning "Файл requirements.txt не найден"
    fi
}

# Функция проверки файла окружения
check_env_file() {
    if [ ! -f "$ENV_FILE" ]; then
        print_warning "Файл $ENV_FILE не найден"
        if [ -f "env.dev.example" ]; then
            print_message "Создаю $ENV_FILE на основе env.dev.example..."
            cp env.dev.example $ENV_FILE
            print_warning "Пожалуйста, отредактируйте $ENV_FILE и настройте необходимые переменные"
            print_message "Особенно важно настроить TELEGRAM_BOT_TOKEN для работы бота"
        else
            print_error "Файл env.dev.example не найден"
            exit 1
        fi
    fi
}

# Функция проверки и очистки конфликтующих процессов
check_conflicting_processes() {
    print_message "Проверка конфликтующих процессов..."
    
    # Ищем процессы Telegram бота
    TELEGRAM_PIDS=$(ps aux | grep "telegram_polling" | grep -v grep | awk '{print $2}')
    
    if [ ! -z "$TELEGRAM_PIDS" ]; then
        print_warning "Найдены запущенные процессы Telegram бота: $TELEGRAM_PIDS"
        print_message "Останавливаю конфликтующие процессы..."
        
        for pid in $TELEGRAM_PIDS; do
            # Сначала пытаемся мягко завершить
            kill $pid 2>/dev/null || true
            sleep 1
            # Если процесс все еще существует, принудительно завершаем
            if kill -0 $pid 2>/dev/null; then
                kill -9 $pid 2>/dev/null || true
                print_message "Принудительно остановлен процесс PID: $pid"
            else
                print_message "Остановлен процесс PID: $pid"
            fi
        done
        
        sleep 2  # Даем время процессам завершиться
        print_success "Конфликтующие процессы Telegram бота остановлены"
    else
        print_success "Конфликтующих процессов Telegram бота не найдено"
    fi
    
    # Ищем процессы Django на том же порту (только если запускаем Django)
    if [ "$BOT_ONLY" = false ]; then
        print_message "Проверка процессов Django на порту $DJANGO_PORT..."
        DJANGO_PIDS=$(lsof -ti :$DJANGO_PORT 2>/dev/null | grep -v $$ || true)
        
        if [ ! -z "$DJANGO_PIDS" ]; then
            print_warning "Найдены процессы на порту $DJANGO_PORT: $DJANGO_PIDS"
            print_message "Останавливаю конфликтующие процессы Django..."
            
            for pid in $DJANGO_PIDS; do
                kill -9 $pid 2>/dev/null || true
                print_message "Остановлен процесс Django PID: $pid"
            done
            
            sleep 2  # Даем время процессам завершиться
            print_success "Конфликтующие процессы Django остановлены"
        else
            print_success "Конфликтующих процессов Django не найдено"
        fi
    else
        print_message "Пропускаю проверку Django процессов (режим bot-only)"
    fi
}

# Функция проверки базы данных
check_database() {
    print_message "Проверка базы данных..."
    python manage.py check --deploy
    if [ $? -eq 0 ]; then
        print_success "База данных в порядке"
    else
        print_warning "Проблемы с базой данных, выполняю миграции..."
        python manage.py migrate
        print_success "Миграции выполнены"
    fi
}

# Функция проверки доступности порта
check_port_availability() {
    local port=$1
    if lsof -i :$port >/dev/null 2>&1; then
        print_warning "Порт $port занят, но это может быть наш процесс"
        return 0
    else
        print_success "Порт $port свободен"
        return 0
    fi
}

# Функция запуска Django сервера
start_django() {
    print_django "Запуск Django сервера на порту $DJANGO_PORT..."
    
    # Проверяем доступность порта
    check_port_availability $DJANGO_PORT
    
    python manage.py runserver 0.0.0.0:$DJANGO_PORT &
    DJANGO_PID=$!
    
    # Даем время серверу запуститься
    sleep 3
    
    # Проверяем, что сервер действительно запустился
    if kill -0 $DJANGO_PID 2>/dev/null; then
        print_success "Django сервер запущен (PID: $DJANGO_PID)"
        print_django "Сервер доступен по адресу: http://localhost:$DJANGO_PORT"
        
        # Тестируем доступность
        if curl -s -o /dev/null -w "%{http_code}" http://localhost:$DJANGO_PORT | grep -q "200"; then
            print_success "✅ Сайт доступен и отвечает"
        else
            print_warning "⚠️  Сайт запущен, но может быть недоступен"
        fi
    else
        print_error "❌ Не удалось запустить Django сервер"
        return 1
    fi
}

# Функция запуска Telegram бота
start_telegram_bot() {
    print_telegram "Запуск Telegram бота..."
    python manage.py telegram_polling &
    TELEGRAM_PID=$!
    print_success "Telegram бот запущен (PID: $TELEGRAM_PID)"
}

# Функция мониторинга логов
monitor_logs() {
    print_header "Мониторинг логов"
    print_message "Нажмите Ctrl+C для остановки всех сервисов"
    print_message "Логи будут отображаться в реальном времени"
    echo ""
    
    # Ждем завершения процессов
    wait
}

# Функция показа статуса
show_status() {
    print_header "Статус сервисов"
    
    if [ ! -z "$DJANGO_PID" ] && kill -0 $DJANGO_PID 2>/dev/null; then
        print_django "✅ Django сервер работает (PID: $DJANGO_PID)"
    else
        print_django "❌ Django сервер не работает"
    fi
    
    if [ ! -z "$TELEGRAM_PID" ] && kill -0 $TELEGRAM_PID 2>/dev/null; then
        print_telegram "✅ Telegram бот работает (PID: $TELEGRAM_PID)"
    else
        print_telegram "❌ Telegram бот не работает"
    fi
}

# Функция показа справки
show_help() {
    echo "Использование: $0 [ОПЦИЯ]"
    echo ""
    echo "Опции:"
    echo "  --help, -h     Показать эту справку"
    echo "  --status       Показать статус сервисов"
    echo "  --django-only  Запустить только Django сервер"
    echo "  --bot-only     Запустить только Telegram бота"
    echo "  --no-bot       Запустить без Telegram бота"
    echo "  --port PORT    Указать порт для Django (по умолчанию 8000)"
    echo "  --clean        Очистить конфликтующие процессы и выйти"
    echo ""
    echo "Примеры:"
    echo "  $0                    # Запустить все сервисы"
    echo "  $0 --django-only      # Только Django"
    echo "  $0 --port 8080        # Django на порту 8080"
    echo "  $0 --no-bot           # Без Telegram бота"
    echo "  $0 --clean            # Очистить конфликтующие процессы"
    echo ""
    echo "Устранение неполадок:"
    echo "  Если видите ошибку 409 Conflict - выполните: $0 --clean"
    echo "  Если порт занят - используйте: $0 --port 8080"
    echo "  Подробнее: см. TROUBLESHOOTING.md"
}

# Основная функция
main() {
    print_header "Anonim Mektep - Локальный запуск"
    
    # Парсинг аргументов
    DJANGO_ONLY=false
    BOT_ONLY=false
    NO_BOT=false
    CLEAN_ONLY=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                show_help
                exit 0
                ;;
            --status)
                show_status
                exit 0
                ;;
            --clean)
                CLEAN_ONLY=true
                shift
                ;;
            --django-only)
                DJANGO_ONLY=true
                shift
                ;;
            --bot-only)
                BOT_ONLY=true
                shift
                ;;
            --no-bot)
                NO_BOT=true
                shift
                ;;
            --port)
                DJANGO_PORT="$2"
                shift 2
                ;;
            *)
                print_error "Неизвестная опция: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Если только очистка
    if [ "$CLEAN_ONLY" = true ]; then
        activate_venv
        check_conflicting_processes
        exit 0
    fi
    
    # Проверки
    check_venv
    activate_venv
    install_dependencies
    check_env_file
    
    # Проверка конфликтующих процессов (всегда, если не только очистка)
    print_message "Выполняю проверку конфликтующих процессов..."
    check_conflicting_processes
    print_message "Проверка конфликтующих процессов завершена"
    
    # Проверка базы данных
    if [ "$BOT_ONLY" = false ]; then
        check_database
    fi
    
    # Запуск сервисов
    if [ "$BOT_ONLY" = false ]; then
        start_django
        sleep 2  # Даем время Django серверу запуститься
    fi
    
    if [ "$DJANGO_ONLY" = false ] && [ "$NO_BOT" = false ]; then
        start_telegram_bot
    fi
    
    # Показываем статус
    echo ""
    show_status
    echo ""
    
    # Мониторинг
    monitor_logs
}

# Запуск основной функции
main "$@"
