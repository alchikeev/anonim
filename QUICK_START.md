# 🚀 Быстрый старт Anonim Mektep

## Установка и запуск за 3 шага

### 1. Настройка окружения
```bash
# Скопируйте файл настроек
cp env.dev.example .env.dev

# Отредактируйте .env.dev и добавьте токен Telegram бота
nano .env.dev  # или любой другой редактор
```

### 2. Запуск
```bash
# Запустите все сервисы одной командой
./start.sh
```

### 3. Использование
- **Веб-сайт**: http://localhost:8000
- **Telegram бот**: Найдите по username в Telegram и отправьте `/start`

## 🔧 Основные команды

```bash
./start.sh                    # Запустить все
./start.sh --django-only      # Только сайт
./start.sh --no-bot           # Без бота
./start.sh --port 8080        # Другой порт
./start.sh --help             # Справка
```

## ⚙️ Настройка Telegram бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в `.env.dev`:
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_здесь
   TELEGRAM_BOT_USERNAME=ваш_username_здесь
   ```

## 🛑 Остановка

Нажмите `Ctrl+C` в терминале

## 📖 Подробная документация

Смотрите [LOCAL_SETUP.md](LOCAL_SETUP.md) для детальной информации
