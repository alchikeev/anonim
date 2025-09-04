from django.core.management.base import BaseCommand
from core.models import EditablePage


class Command(BaseCommand):
    help = 'Очищает старые записи контента и создает новые для активных разделов'

    def handle(self, *args, **options):
        # Удаляем старые записи с неактивными разделами
        old_pages = EditablePage.objects.filter(page__in=['contacts', 'what_to_do'])
        deleted_count = old_pages.count()
        old_pages.delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Удалено старых записей: {deleted_count}')
        )
        
        # Создаем новые записи для service_contacts если их нет
        service_contacts_ru = EditablePage.objects.filter(page='service_contacts', language='ru').first()
        if not service_contacts_ru:
            EditablePage.objects.create(
                page='service_contacts',
                language='ru',
                title='Контакты служб',
                content='''
                <h3>Контакты служб</h3>
                
                <div class="contact-item">
                    <h4>Экстренные службы</h4>
                    <ul>
                        <li>Полиция: <a href="tel:102">102</a></li>
                        <li>Скорая помощь: <a href="tel:103">103</a></li>
                        <li>Пожарная служба: <a href="tel:101">101</a></li>
                        <li>Единый номер экстренных служб: <a href="tel:112">112</a></li>
                    </ul>
                </div>
                
                <div class="contact-item">
                    <h4>Образование и поддержка</h4>
                    <ul>
                        <li>Министерство образования: <a href="https://edu.gov.kg/">edu.gov.kg</a></li>
                        <li>Телефон доверия: <a href="tel:150">150</a></li>
                        <li>Психологическая помощь: <a href="tel:142">142</a></li>
                    </ul>
                </div>
                
                <div class="contact-item">
                    <h4>Детские службы</h4>
                    <ul>
                        <li>Детский телефон доверия: <a href="tel:150">150</a></li>
                        <li>Центр помощи детям: <a href="tel:+996312123456">+996 312 123 456</a></li>
                    </ul>
                </div>
                '''
            )
            self.stdout.write(self.style.SUCCESS('✅ Создана страница "Контакты служб" (русский)'))
        
        service_contacts_ky = EditablePage.objects.filter(page='service_contacts', language='ky').first()
        if not service_contacts_ky:
            EditablePage.objects.create(
                page='service_contacts',
                language='ky',
                title='Кызматтардын байланыштары',
                content='''
                <h3>Кызматтардын байланыштары</h3>
                
                <div class="contact-item">
                    <h4>Тез жардам кызматтары</h4>
                    <ul>
                        <li>Полиция: <a href="tel:102">102</a></li>
                        <li>Тез жардам: <a href="tel:103">103</a></li>
                        <li>Өрт кызматы: <a href="tel:101">101</a></li>
                        <li>Бирдиктүү тез жардам номери: <a href="tel:112">112</a></li>
                    </ul>
                </div>
                
                <div class="contact-item">
                    <h4>Билим берүү жана колдоо</h4>
                    <ul>
                        <li>Билим берүү министрлиги: <a href="https://edu.gov.kg/">edu.gov.kg</a></li>
                        <li>Ишеним телефону: <a href="tel:150">150</a></li>
                        <li>Психологиялык жардам: <a href="tel:142">142</a></li>
                    </ul>
                </div>
                
                <div class="contact-item">
                    <h4>Балдар кызматтары</h4>
                    <ul>
                        <li>Балдар ишеним телефону: <a href="tel:150">150</a></li>
                        <li>Балдарга жардам көрсөтүү борбору: <a href="tel:+996312123456">+996 312 123 456</a></li>
                    </ul>
                </div>
                '''
            )
            self.stdout.write(self.style.SUCCESS('✅ Создана страница "Контакты служб" (кыргызский)'))
        
        # Обновляем название FAQ
        faq_pages = EditablePage.objects.filter(page='faq')
        for page in faq_pages:
            if page.language == 'ru':
                page.title = 'Вопросы-ответы'
            else:
                page.title = 'Суроо-жооптор'
            page.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Обновлено названий FAQ: {faq_pages.count()}')
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Очистка завершена! Теперь в системе только активные разделы.')
        )
