# 💻 Примеры кода для дизайнеров

## 🎨 Быстрый старт

### Подключение стилей
```html
<!-- В head секции -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
<link rel="stylesheet" href="{% static 'core/style.css' %}">
```

---

## 🧩 Готовые компоненты

### Кнопки

#### Основная кнопка
```html
<button class="btn btn-primary">Отправить сообщение</button>
```

#### Outline кнопка
```html
<button class="btn btn-outline-primary">Вход в систему</button>
```

#### Кнопка с иконкой
```html
<button class="btn btn-primary">
    <i class="bi bi-send me-2"></i>Отправить
</button>
```

### Карточки

#### Базовая карточка
```html
<div class="card">
    <div class="card-header">
        <h5 class="card-title">Заголовок карточки</h5>
    </div>
    <div class="card-body">
        <p class="card-text">Содержимое карточки</p>
        <a href="#" class="btn btn-primary">Действие</a>
    </div>
</div>
```

#### Карточка с hover эффектом
```html
<div class="card features-section">
    <div class="card-body text-center">
        <i class="bi bi-shield-check text-primary mb-3" style="font-size: 3rem;"></i>
        <h5 class="card-title">Безопасность</h5>
        <p class="card-text">Ваши сообщения защищены</p>
    </div>
</div>
```

### Формы

#### Базовая форма
```html
<form>
    <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" required>
    </div>
    <div class="mb-3">
        <label for="message" class="form-label">Сообщение</label>
        <textarea class="form-control" id="message" rows="4"></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Отправить</button>
</form>
```

#### Радио-опции
```html
<div class="radio-options">
    <div class="radio-option">
        <input type="radio" id="option1" name="problem" value="bullying">
        <label for="option1">Проблема с одноклассниками</label>
    </div>
    <div class="radio-option">
        <input type="radio" id="option2" name="problem" value="teacher">
        <label for="option2">Проблема с учителем</label>
    </div>
</div>
```

### Навигация

#### Навбар
```html
<nav class="navbar navbar-expand-lg">
    <div class="container-fluid">
        <a class="navbar-brand fw-bold d-flex align-items-center" href="/">
            <img src="logo.png" alt="Логотип" height="32" class="me-2">
            Аноним Мектеп
        </a>
        <div class="navbar-nav me-auto">
            <a class="nav-link" href="/about">О проекте</a>
            <a class="nav-link" href="/faq">FAQ</a>
        </div>
        <a href="/login" class="btn btn-outline-primary">Вход</a>
    </div>
</nav>
```

### Языковой переключатель
```html
<div class="btn-group language-switcher" role="group">
    <button type="button" class="btn btn-sm language-btn active" data-lang="ru">РУС</button>
    <button type="button" class="btn btn-sm language-btn" data-lang="ky">КЫР</button>
</div>
```

---

## 🎨 Цветовые схемы

### Основные цвета в CSS
```css
:root {
    --cream: #FFFEF8;
    --white: #F5F5F5;
    --lime: #CDFF07;
    --blue: #69C5F8;
    --dark: #313642;
    --black: #262626;
    --grey: #4B5262;
}
```

### Использование в стилях
```css
.my-component {
    background-color: var(--lime);
    color: var(--dark);
    border: 2px solid var(--blue);
}
```

### Градиенты
```css
.hero-gradient {
    background: linear-gradient(135deg, var(--blue) 0%, rgba(105, 197, 248, 0.8) 100%);
}

.features-gradient {
    background: linear-gradient(135deg, rgba(205, 255, 7, 0.05) 0%, rgba(105, 197, 248, 0.05) 100%);
}
```

---

## 📐 Сетка и отступы

### Контейнер
```html
<div class="container">
    <!-- Контент с максимальной шириной 1200px -->
</div>
```

### Сетка Bootstrap
```html
<div class="row">
    <div class="col-md-6 col-lg-4">
        <!-- 1/2 на планшете, 1/3 на десктопе -->
    </div>
    <div class="col-md-6 col-lg-4">
        <!-- 1/2 на планшете, 1/3 на десктопе -->
    </div>
    <div class="col-md-12 col-lg-4">
        <!-- Полная ширина на планшете, 1/3 на десктопе -->
    </div>
</div>
```

### Отступы
```html
<!-- Стандартные отступы Bootstrap -->
<div class="mb-3">Отступ снизу</div>
<div class="mt-4">Отступ сверху</div>
<div class="p-3">Отступы со всех сторон</div>
<div class="px-4">Отступы по горизонтали</div>
```

---

## 🎭 Анимации

### Базовые анимации
```css
/* Fade in */
.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* Slide up */
.slide-up {
    animation: slideInUp 0.6s ease-out;
}

/* Pulse */
.pulse {
    animation: pulse 2s infinite;
}
```

### Hover эффекты
```css
.hover-lift:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.hover-scale:hover {
    transform: scale(1.05);
}
```

### Переходы
```css
.smooth-transition {
    transition: all 0.3s ease;
}
```

---

## 📱 Адаптивность

### Медиа-запросы
```css
/* Мобильные устройства */
@media (max-width: 576px) {
    .mobile-full-width {
        width: 100%;
    }
}

/* Планшеты */
@media (max-width: 768px) {
    .tablet-stack {
        flex-direction: column;
    }
}

/* Десктопы */
@media (min-width: 992px) {
    .desktop-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
    }
}
```

### Адаптивные утилиты Bootstrap
```html
<!-- Скрыть на мобильных -->
<div class="d-none d-md-block">Только на планшетах и больше</div>

<!-- Показать только на мобильных -->
<div class="d-block d-md-none">Только на мобильных</div>

<!-- Адаптивные отступы -->
<div class="p-2 p-md-4 p-lg-5">Отступы увеличиваются с размером экрана</div>
```

---

## 🎪 Специальные эффекты

### Shimmer эффект
```css
.shimmer {
    position: relative;
    overflow: hidden;
}

.shimmer::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(205, 255, 7, 0.1), transparent);
    transition: left 0.6s ease;
}

.shimmer:hover::before {
    left: 100%;
}
```

### Градиентный текст
```css
.gradient-text {
    background: linear-gradient(45deg, var(--blue), var(--lime));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

### 3D эффекты
```css
.card-3d {
    transform-style: preserve-3d;
    transition: transform 0.3s ease;
}

.card-3d:hover {
    transform: translateY(-10px) rotateX(5deg);
}
```

---

## 🎨 Иконки

### Bootstrap Icons
```html
<!-- Базовые иконки -->
<i class="bi bi-house"></i>
<i class="bi bi-person"></i>
<i class="bi bi-envelope"></i>

<!-- Иконки с размерами -->
<i class="bi bi-shield-check" style="font-size: 2rem;"></i>
<i class="bi bi-lightning" style="font-size: 3rem;"></i>

<!-- Иконки с цветами -->
<i class="bi bi-heart text-danger"></i>
<i class="bi bi-star text-warning"></i>
```

### Специальные эффекты иконок
```css
.icon-gradient {
    background: linear-gradient(45deg, var(--blue), var(--lime));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.icon-hover:hover {
    transform: scale(1.2) rotate(5deg);
    color: var(--lime) !important;
}
```

---

## 🎯 Состояния компонентов

### Loading состояние
```html
<button class="btn btn-primary" disabled>
    <span class="spinner-border spinner-border-sm me-2"></span>
    Загрузка...
</button>
```

### Success состояние
```html
<div class="alert alert-success">
    <i class="bi bi-check-circle me-2"></i>
    Сообщение успешно отправлено!
</div>
```

### Error состояние
```html
<div class="alert alert-danger">
    <i class="bi bi-exclamation-triangle me-2"></i>
    Произошла ошибка при отправке
</div>
```

### Empty состояние
```html
<div class="text-center py-5">
    <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
    <p class="text-muted mt-3">Нет данных для отображения</p>
</div>
```

---

## 🔧 Утилиты

### Текст
```html
<p class="text-primary">Основной текст</p>
<p class="text-muted">Вторичный текст</p>
<p class="text-center">Центрированный текст</p>
<p class="text-truncate">Обрезанный текст с многоточием</p>
```

### Фоны
```html
<div class="bg-primary text-white">Синий фон</div>
<div class="bg-light">Светлый фон</div>
<div class="bg-gradient">Градиентный фон</div>
```

### Границы
```html
<div class="border">Обычная граница</div>
<div class="border-primary">Цветная граница</div>
<div class="border-0">Без границы</div>
<div class="border-dashed">Пунктирная граница</div>
```

### Тени
```css
.shadow-sm { box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); }
.shadow { box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15); }
.shadow-lg { box-shadow: 0 1rem 3rem rgba(0,0,0,0.175); }
```

---

## 📋 Чек-лист для дизайнеров

### ✅ Перед началом работы
- [ ] Изучить цветовую палитру
- [ ] Понять иерархию типографики
- [ ] Ознакомиться с компонентами
- [ ] Проверить адаптивность

### ✅ При создании макетов
- [ ] Использовать только цвета из палитры
- [ ] Соблюдать отступы и размеры
- [ ] Учитывать hover состояния
- [ ] Проверять на разных экранах

### ✅ При верстке
- [ ] Использовать готовые классы
- [ ] Добавлять анимации умеренно
- [ ] Тестировать интерактивность
- [ ] Проверять доступность

---

*Документ обновлен: 4 сентября 2025*
*Версия примеров: 1.0*
