# 🎨 Цветовая палитра "Аноним Мектеп"

## Основные цвета

| Цвет | Hex | RGB | CSS Variable | Использование |
|------|-----|-----|--------------|---------------|
| ![Cream](https://via.placeholder.com/40x20/FFFEF8/000000?text=+) | `#FFFEF8` | `rgb(255, 254, 248)` | `--cream` | Фон страниц |
| ![White](https://via.placeholder.com/40x20/F5F5F5/000000?text=+) | `#F5F5F5` | `rgb(245, 245, 245)` | `--white` | Основной фон |
| ![Sky Blue](https://via.placeholder.com/40x20/80B3FF/000000?text=+) | `#80B3FF` | `rgb(128, 179, 255)` | `--sky-blue` | Навигация, футер |
| ![Teal Green](https://via.placeholder.com/40x20/58B2A6/000000?text=+) | `#58B2A6` | `rgb(88, 178, 166)` | `--teal-green` | Переходы, градиенты |
| ![Warm Orange](https://via.placeholder.com/40x20/FF9966/000000?text=+) | `#FF9966` | `rgb(255, 153, 102)` | `--warm-orange` | Акценты, кнопки |
| ![Dark](https://via.placeholder.com/40x20/313642/FFFFFF?text=+) | `#313642` | `rgb(49, 54, 66)` | `--dark` | Текст на светлом |
| ![Black](https://via.placeholder.com/40x20/262626/FFFFFF?text=+) | `#262626` | `rgb(38, 38, 38)` | `--black` | Основной текст |
| ![Grey](https://via.placeholder.com/40x20/4B5262/FFFFFF?text=+) | `#4B5262` | `rgb(75, 82, 98)` | `--grey` | Вторичный текст |

## Дополнительные цвета

| Цвет | Hex | RGB | Использование |
|------|-----|-----|---------------|
| ![Info Blue](https://via.placeholder.com/40x20/0D6EFD/FFFFFF?text=+) | `#0D6EFD` | `rgb(13, 110, 253)` | Ссылки, интерактивные элементы |
| ![Light Grey](https://via.placeholder.com/40x20/6C757D/FFFFFF?text=+) | `#6C757D` | `rgb(108, 117, 125)` | Вторичный текст |
| ![Border Grey](https://via.placeholder.com/40x20/DEE2E6/000000?text=+) | `#DEE2E6` | `rgb(222, 226, 230)` | Границы, разделители |
| ![Background Grey](https://via.placeholder.com/40x20/F8F9FA/000000?text=+) | `#F8F9FA` | `rgb(248, 249, 250)` | Заголовки карточек |

## Градиенты

### Основной градиент фона
```css
background: linear-gradient(135deg, var(--sky-blue) 0%, var(--teal-green) 50%, var(--warm-orange) 100%);
```

### Навигация градиент
```css
background: linear-gradient(135deg, var(--sky-blue) 0%, var(--teal-green) 100%);
```

### Features градиент
```css
background: linear-gradient(135deg, rgba(128, 179, 255, 0.08) 0%, rgba(88, 178, 166, 0.08) 50%, rgba(255, 153, 102, 0.08) 100%);
```

### Статистика градиент
```css
background: linear-gradient(135deg, var(--sky-blue) 0%, var(--teal-green) 50%, var(--warm-orange) 100%);
```

## Цветовые комбинации

### Основные пары
- **Warm Orange + White**: Кнопки, акценты
- **Sky Blue + Teal Green**: Навигация, футер
- **Black + White**: Основной текст
- **Grey + White**: Вторичный текст

### Hover состояния
- **Warm Orange → Light Orange**: Основные кнопки
- **White → Warm Orange**: Outline кнопки
- **Sky Blue → Teal Green**: Навигационные элементы

## CSS переменные

```css
:root {
    --cream: #FFFEF8;
    --white: #F5F5F5;
    --sky-blue: #80B3FF;
    --teal-green: #58B2A6;
    --warm-orange: #FF9966;
    --dark: #313642;
    --black: #262626;
    --grey: #4B5262;
    
    /* Legacy colors for backward compatibility */
    --lime: #FF9966; /* Warm orange as new accent */
    --blue: #80B3FF; /* Sky blue as new primary */
}
```

## Использование в коде

```css
/* Основные цвета */
.my-element {
    background-color: var(--warm-orange);
    color: var(--white);
    border: 2px solid var(--sky-blue);
}

/* Градиенты */
.hero-section {
    background: linear-gradient(135deg, var(--sky-blue) 0%, var(--teal-green) 50%, var(--warm-orange) 100%);
}

/* Hover эффекты */
.btn:hover {
    background-color: var(--white);
    color: var(--dark);
}
```

---

*Быстрый справочник для дизайнеров*
*Обновлено: 4 сентября 2025*
