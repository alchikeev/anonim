# 📋 Инструкция по безопасному деплою

## 🚀 Для проекта "Аноним Мектеп"

### 1. Подготовка на локальной машине:
```bash
# Коммитим изменения
git add .
git commit -m "deploy: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
```

### 2. Деплой на сервер:
```bash
# Подключаемся к серверу
ssh root@79.133.181.227

# Создаем резервную копию
mkdir -p /root/backups/anonim-$(date +%Y%m%d_%H%M%S)
cp -r /root/anonim-mektep /root/backups/anonim-$(date +%Y%m%d_%H%M%S)/

# Обновляем код
cd /root/anonim-mektep


# Собираем статические файлы
docker compose -f docker-compose.caddy.yml exec anonim_web python manage.py collectstatic --noinput

# Копируем статические файлы в volume Caddy
docker cp anonim-mektep-anonim_web-1:/app/staticfiles/. /var/lib/docker/volumes/tdp_anonim_static_data/_data/

# Перезапускаем приложение
docker compose -f docker-compose.caddy.yml up -d --build
```

---

## 🚀 Для проекта TDP

### 1. Подготовка на локальной машине:
```bash
# Коммитим изменения (если это git репозиторий)
git add .
git commit -m "deploy: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
```

### 2. Деплой на сервер:
```bash
# Подключаемся к серверу
ssh root@79.133.181.227

# Создаем резервную копию
mkdir -p /root/backups/tdp-$(date +%Y%m%d_%H%M%S)
cp -r /srv/tdp /root/backups/tdp-$(date +%Y%m%d_%H%M%S)/

# Обновляем код
cd /srv/tdp
git pull origin main  # или копируем файлы вручную

# Перезапускаем приложение
docker compose up -d --build
```

---

## 🔍 Проверка статуса

### Проверяем контейнеры:
```bash
docker ps
```

### Проверяем логи:
```bash
# Логи Аноним Мектеп
docker logs anonim-mektep-anonim_web-1 --tail 20

# Логи TDP
docker logs tdp-tdp-1 --tail 20

# Логи Caddy
docker logs tdp-caddy-1 --tail 20
```

### Проверяем сайты:
```bash
curl -I https://anonim-m.online
curl -I https://thaidreamphuket.com
```

---

## ⚠️ Откат в случае проблем

### Для Аноним Мектеп:
```bash
# Останавливаем текущее приложение
cd /root/anonim-mektep
docker compose -f docker-compose.caddy.yml down

# Восстанавливаем из резервной копии
cd /root
rm -rf anonim-mektep
mv /root/backups/anonim-YYYYMMDD_HHMMSS/anonim-mektep /root/

# Запускаем восстановленную версию
cd /root/anonim-mektep
docker compose -f docker-compose.caddy.yml up -d
```

### Для TDP:
```bash
# Останавливаем текущее приложение
cd /srv/tdp
docker compose down

# Восстанавливаем из резервной копии
cd /srv
rm -rf tdp
mv /root/backups/tdp-YYYYMMDD_HHMMSS/tdp /srv/

# Запускаем восстановленную версию
cd /srv/tdp
docker compose up -d
```

---

## 🛡️ Безопасность

1. **Всегда создавайте резервные копии** перед деплоем
2. **Проверяйте статус** после каждого деплоя
3. **Тестируйте на staging** перед продакшеном
4. **Мониторьте логи** в первые минуты после деплоя
5. **Имейте план отката** готовым

---

## 📊 Мониторинг

### Проверка ресурсов:
```bash
df -h /          # Дисковое пространство
free -h          # Память
docker stats     # Использование ресурсов контейнерами
```

### Проверка сетей:
```bash
docker network ls
docker network inspect tdp_default
```

### Проверка volumes:
```bash
docker volume ls
docker volume inspect tdp_anonim_static_data
```

---

## 🆘 Экстренные команды

### Если сайт не отвечает:
```bash
# Проверяем статус всех контейнеров
docker ps -a

# Перезапускаем все сервисы
cd /srv/tdp && docker compose restart
cd /root/anonim-mektep && docker compose -f docker-compose.caddy.yml restart

# Проверяем логи Caddy
docker logs tdp-caddy-1 --tail 50
```

### Если проблемы с SSL:
```bash
# Проверяем сертификаты Caddy
docker exec tdp-caddy-1 caddy list-certificates

# Перезапускаем Caddy
docker restart tdp-caddy-1
```

### Если проблемы с базой данных:
```bash
# Проверяем миграции Аноним Мектеп
docker exec anonim-mektep-anonim_web-1 python manage.py showmigrations

# Применяем миграции
docker exec anonim-mektep-anonim_web-1 python manage.py migrate
```

---

## 📝 Полезные команды

### Создание суперпользователя:
```bash
docker exec -it anonim-mektep-anonim_web-1 python manage.py createsuperuser
```

### Очистка Docker:
```bash
# Удаление неиспользуемых контейнеров
docker container prune

# Удаление неиспользуемых образов
docker image prune

# Удаление неиспользуемых volumes
docker volume prune
```

### Просмотр использования места:
```bash
# Размер Docker данных
du -sh /var/lib/docker/

# Размер проектов
du -sh /root/anonim-mektep/
du -sh /srv/tdp/
```

---

## 🌐 Доступные сайты

- **Аноним Мектеп**: https://anonim-m.online
- **TDP**: https://thaidreamphuket.com
- **Django Admin (Аноним Мектеп)**: https://anonim-m.online/admin/

---

## 📞 Контакты для поддержки

При возникновении проблем:
1. Проверьте логи контейнеров
2. Убедитесь, что все контейнеры запущены
3. Проверьте доступность сайтов
4. При необходимости выполните откат

**Помните**: всегда делайте резервные копии перед деплоем!

