from django.core.management.base import BaseCommand
from django.utils import translation
from core.models import EditablePage


class Command(BaseCommand):
    help = 'Инициализирует контент для новых страниц'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('📄 Инициализация контента новых страниц')
        )
        self.stdout.write('=' * 40)
        
        # Инициализируем для русского языка
        translation.activate('ru')
        self.init_pages_for_language('ru')
        
        # Инициализируем для кыргызского языка
        translation.activate('ky')
        self.init_pages_for_language('ky')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Контент новых страниц инициализирован!')
        )

    def init_pages_for_language(self, language_code):
        """Инициализирует страницы для указанного языка"""
        self.stdout.write(f'\n🌐 Инициализация для языка: {language_code}')
        
        # База знаний
        self.create_or_update_page(
            'knowledge_base',
            'База знаний' if language_code == 'ru' else 'Билим базасы',
            self.get_knowledge_base_content(language_code),
            language_code
        )
        
        # Контакты служб
        self.create_or_update_page(
            'service_contacts',
            'Контакты служб' if language_code == 'ru' else 'Кызмат байланыштары',
            self.get_service_contacts_content(language_code),
            language_code
        )
        
        # Инструкции
        self.create_or_update_page(
            'instructions',
            'Инструкции' if language_code == 'ru' else 'Көрсөтмөлөр',
            self.get_instructions_content(language_code),
            language_code
        )

    def create_or_update_page(self, page_key, title, content, language_code):
        """Создает или обновляет страницу"""
        page, created = EditablePage.objects.get_or_create(
            page=page_key,
            language=language_code,
            defaults={
                'title': title,
                'content': content
            }
        )
        
        if not created:
            page.title = title
            page.content = content
            page.save()
        
        status = 'создана' if created else 'обновлена'
        self.stdout.write(f'  ✅ {title}: {status}')

    def get_knowledge_base_content(self, language_code):
        """Контент для базы знаний"""
        if language_code == 'ru':
            return '''
            <div class="row">
                <div class="col-md-6">
                    <h4>🛡️ Безопасность в школе</h4>
                    <ul>
                        <li>Правила поведения в школе</li>
                        <li>Как защитить себя от буллинга</li>
                        <li>Что делать при конфликтах</li>
                        <li>Куда обращаться за помощью</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h4>📚 Полезные материалы</h4>
                    <ul>
                        <li>Статьи о психологии подростков</li>
                        <li>Методы разрешения конфликтов</li>
                        <li>Информация о правах детей</li>
                        <li>Ресурсы для родителей</li>
                    </ul>
                </div>
            </div>
            '''
        else:
            return '''
            <div class="row">
                <div class="col-md-6">
                    <h4>🛡️ Мектептеги коопсуздук</h4>
                    <ul>
                        <li>Мектепте жүрүш-туруш эрежелери</li>
                        <li>Буллингден кантип коргонуу</li>
                        <li>Кагылыштарда эмне кылуу</li>
                        <li>Жардамга кайда кайрылуу</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h4>📚 Пайдалуу материалдар</h4>
                    <ul>
                        <li>Өспүрүмдөрдүн психологиясы жөнүндө макалалар</li>
                        <li>Кагылыштарды чечүү ыкмалары</li>
                        <li>Балдардын укуктары жөнүндө маалымат</li>
                        <li>Ата-энелер үчүн ресурстар</li>
                    </ul>
                </div>
            </div>
            '''

    def get_service_contacts_content(self, language_code):
        """Контент для контактов служб"""
        if language_code == 'ru':
            return '''
            <div class="row">
                <div class="col-md-6">
                    <h4>🚨 Экстренные службы</h4>
                    <ul>
                        <li><strong>Полиция:</strong> 102</li>
                        <li><strong>Скорая помощь:</strong> 103</li>
                        <li><strong>Пожарная служба:</strong> 101</li>
                        <li><strong>Газовая служба:</strong> 104</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h4>👥 Службы поддержки</h4>
                    <ul>
                        <li><strong>Детский телефон доверия:</strong> 111</li>
                        <li><strong>Психологическая помощь:</strong> +996 312 123456</li>
                        <li><strong>Социальная служба:</strong> +996 312 654321</li>
                        <li><strong>Образовательная горячая линия:</strong> +996 312 789012</li>
                    </ul>
                </div>
            </div>
            '''
        else:
            return '''
            <div class="row">
                <div class="col-md-6">
                    <h4>🚨 Тез жардам кызматтары</h4>
                    <ul>
                        <li><strong>Полиция:</strong> 102</li>
                        <li><strong>Тез жардам:</strong> 103</li>
                        <li><strong>Өрт кызматы:</strong> 101</li>
                        <li><strong>Газ кызматы:</strong> 104</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h4>👥 Колдоо кызматтары</h4>
                    <ul>
                        <li><strong>Балдар ишеним телефону:</strong> 111</li>
                        <li><strong>Психологиялык жардам:</strong> +996 312 123456</li>
                        <li><strong>Социалдык кызмат:</strong> +996 312 654321</li>
                        <li><strong>Билим берүү ысык сызыгы:</strong> +996 312 789012</li>
                    </ul>
                </div>
            </div>
            '''

    def get_instructions_content(self, language_code):
        """Контент для инструкций"""
        if language_code == 'ru':
            return '''
            <div class="row">
                <div class="col-md-12">
                    <h4>📋 Как отправить сообщение</h4>
                    <ol>
                        <li>Найдите QR-код в вашей школе или перейдите по уникальной ссылке</li>
                        <li>Выберите тип проблемы из списка</li>
                        <li>Опишите ситуацию подробно</li>
                        <li>Укажите, нужна ли вам помощь</li>
                        <li>Оставьте контактную информацию (по желанию)</li>
                        <li>Нажмите "Отправить сообщение"</li>
                    </ol>
                    
                    <h4>🔒 Анонимность</h4>
                    <ul>
                        <li>Ваше сообщение полностью анонимно</li>
                        <li>Мы не сохраняем IP-адреса</li>
                        <li>Контактная информация необязательна</li>
                        <li>Ответ придет через администрацию школы</li>
                    </ul>
                </div>
            </div>
            '''
        else:
            return '''
            <div class="row">
                <div class="col-md-12">
                    <h4>📋 Билдирүү жөнөтүү</h4>
                    <ol>
                        <li>Мектебиңиздеги QR-кодду табыңыз же уникалдуу шилтеме аркылуу өтүңүз</li>
                        <li>Типти тизмеден тантаңыз</li>
                        <li>Жагдайды толук сүрөттөңүз</li>
                        <li>Жардам керекпи, көрсөтүңүз</li>
                        <li>Байланыш маалыматын калтырыңыз (каалоо боюнча)</li>
                        <li>"Билдирүү жөнөтүү" баскычын басыңыз</li>
                    </ol>
                    
                    <h4>🔒 Анонимдүүлүк</h4>
                    <ul>
                        <li>Сиздин билдирүүңүз толук анонимдүү</li>
                        <li>Биз IP-даректерди сактабайбыз</li>
                        <li>Байланыш маалыматы милдеттүү эмес</li>
                        <li>Жооп мектеп администрациясы аркылуу келет</li>
                    </ul>
                </div>
            </div>
            '''
