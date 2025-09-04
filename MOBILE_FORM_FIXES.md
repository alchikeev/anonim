# 📱 Исправление полей ввода на мобильных устройствах

## ✨ Проблема

На мобильных устройствах поля ввода текста выходили за рамки карточки формы, нарушая макет.

## 🔧 **Исправления**

### **1. Общие стили для полей ввода**
```css
.form-control, .form-select, textarea {
    max-width: 100%;
    box-sizing: border-box;
    word-wrap: break-word;
    word-break: break-word;
    overflow-wrap: break-word;
}
```

### **2. Стили для textarea**
```css
textarea.form-control {
    resize: vertical;
    min-height: 100px;
    max-height: 200px;
}
```

### **3. Стили для reCAPTCHA**
```css
.g-recaptcha {
    max-width: 100%;
    overflow: hidden;
}
```

### **4. Исправление viewport для мобильных**
```css
@media (max-width: 768px) {
    body {
        overflow-x: hidden;
    }
    
    .container, .container-fluid {
        padding-left: 15px;
        padding-right: 15px;
    }
    
    .message-form-card {
        width: calc(100% - 2rem);
        max-width: calc(100vw - 2rem);
    }
}
```

### **5. Дополнительные исправления для мобильных**
```css
@media (max-width: 768px) {
    .message-form-card {
        margin: 0 1rem;
        overflow: hidden;
    }
    
    .message-form-body {
        padding: 1.5rem;
        overflow: hidden;
    }
    
    .form-control, .form-select, textarea {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    .row {
        margin: 0;
    }
    
    .col-md-8, .col-lg-6 {
        padding: 0;
    }
}
```

## 🎯 **Что исправлено**

### **Проблемы:**
- ❌ Поля ввода выходили за рамки карточки
- ❌ Текст не переносился корректно
- ❌ reCAPTCHA нарушала макет
- ❌ Горизонтальная прокрутка на мобильных

### **Решения:**
- ✅ Принудительное ограничение ширины полей
- ✅ Корректный перенос длинного текста
- ✅ Ограничение размера reCAPTCHA
- ✅ Скрытие горизонтальной прокрутки
- ✅ Правильные отступы и padding

## 📱 **Адаптивность**

### **Десктоп**
- Стандартные размеры полей
- Полная функциональность
- Корректное отображение

### **Мобильный**
- Поля ввода: 100% ширины с ограничением
- Отступы: 1rem по бокам
- Перенос текста: принудительный
- reCAPTCHA: адаптивная

## 🚀 **Результат**

Теперь формы отправки сообщений:
- **Корректно отображаются** на всех мобильных устройствах
- **Не выходят за рамки** карточки
- **Правильно переносят** длинный текст
- **Адаптивны** для всех размеров экранов

---

*Исправление мобильных форм завершено: 5 сентября 2025*
*Версия: 1.4 - Исправление полей ввода на мобильных*
