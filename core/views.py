from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import translation
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
import os

from .forms import SendMessageForm, ProblemTypeForm
from .models import School, EditablePage
from .telegram_utils import notify_admins_about_message
from .recaptcha_utils import verify_recaptcha
from dashboard.models import Message


def send_message_info(request):
    """Страница со списком школ и QR-кодами для отправки сообщений"""
    protocol = 'http' if settings.DEBUG else 'https'
    domain = settings.SITE_DOMAIN
    schools = School.objects.all()
    return render(request, 'core/send_message_info.html', {
        'schools': schools,
        'protocol': protocol,
        'domain': domain,
    })

def index(request):
    """Главная страница с статистикой платформы"""
    # Получаем статистику сообщений
    total_messages = Message.objects.count()
    pending_messages = Message.objects.filter(status='pending').count()
    in_progress_messages = Message.objects.filter(status='in_progress').count()
    resolved_messages = Message.objects.filter(status='resolved').count()
    
    # Статистика по типам проблем
    bullying_count = Message.objects.filter(problem_type='bullying').count()
    extortion_count = Message.objects.filter(problem_type='extortion').count()
    harassment_count = Message.objects.filter(problem_type='harassment').count()
    other_count = Message.objects.filter(problem_type='other').count()
    
    context = {
        'total_messages': total_messages,
        'pending_messages': pending_messages,
        'in_progress_messages': in_progress_messages,
        'resolved_messages': resolved_messages,
        'bullying_count': bullying_count,
        'extortion_count': extortion_count,
        'harassment_count': harassment_count,
        'other_count': other_count,
    }
    
    return render(request, 'core/index.html', context)

def set_language(request):
	if request.method == 'POST':
		language = request.POST.get('language')
		if language in [lang[0] for lang in settings.LANGUAGES]:
			translation.activate(language)
			request.session['django_language'] = language
	return redirect(request.META.get('HTTP_REFERER', '/'))

def about(request):
	try:
		page = EditablePage.objects.get(page='about', language=translation.get_language())
	except EditablePage.DoesNotExist:
		# Создаем дефолтную страницу если не существует
		page = EditablePage.objects.create(
			page='about',
			language=translation.get_language(),
			title='О проекте',
			content='Аноним Мектеп — это платформа, созданная для поддержки школьников, учителей и родителей. Здесь вы можете получить консультацию, поделиться проблемой или узнать полезную информацию, сохраняя анонимность.'
		)
	return render(request, 'core/about.html', {'page': page})

def faq(request):
	try:
		page = EditablePage.objects.get(page='faq', language=translation.get_language())
	except EditablePage.DoesNotExist:
		page = EditablePage.objects.create(
			page='faq',
			language=translation.get_language(),
			title='Часто задаваемые вопросы',
			content='<ul><li><strong>Как работает анонимность?</strong> Ваши сообщения не содержат личных данных и не отслеживаются.</li><li><strong>Кто может воспользоваться сервисом?</strong> Любой школьник, учитель или родитель.</li><li><strong>Как получить ответ?</strong> Ответ поступит на указанный вами способ связи или будет опубликован на сайте.</li></ul>'
		)
	return render(request, 'core/faq.html', {'page': page})

def contacts(request):
	try:
		page = EditablePage.objects.get(page='contacts', language=translation.get_language())
	except EditablePage.DoesNotExist:
		page = EditablePage.objects.create(
			page='contacts',
			language=translation.get_language(),
			title='Полезные контакты',
			content='<ul><li>Телефон доверия: <a href="tel:150">150</a></li><li>Министерство образования: <a href="https://edu.gov.kg/">edu.gov.kg</a></li><li>Психологическая помощь: <a href="tel:142">142</a></li><li>Экстренная помощь: <a href="tel:112">112</a></li></ul>'
		)
	return render(request, 'core/contacts.html', {'page': page})

def what_to_do(request):
	try:
		page = EditablePage.objects.get(page='what_to_do', language=translation.get_language())
	except EditablePage.DoesNotExist:
		page = EditablePage.objects.create(
			page='what_to_do',
			language=translation.get_language(),
			title='Что делать, если...',
			content='<ul><li>...вы столкнулись с буллингом — обратитесь к школьному психологу или напишите нам анонимно.</li><li>...заметили нарушение — сообщите администрации или используйте форму на сайте.</li><li>...нужна срочная помощь — позвоните на горячую линию.</li><li>...вас вымогают деньги — немедленно сообщите родителям и в полицию.</li></ul>'
		)
	return render(request, 'core/what_to_do.html', {'page': page})


def knowledge_base(request):
	"""База знаний"""
	try:
		page = EditablePage.objects.get(page='knowledge_base', language=translation.get_language())
	except EditablePage.DoesNotExist:
		page = EditablePage.objects.create(
			page='knowledge_base',
			language=translation.get_language(),
			title='База знаний',
			content='<p>База знаний по вопросам безопасности в школах, профилактике буллинга и другим темам.</p>'
		)
	return render(request, 'core/knowledge_base.html', {'page': page})


def service_contacts(request):
	"""Контакты служб"""
	try:
		page = EditablePage.objects.get(page='service_contacts', language=translation.get_language())
	except EditablePage.DoesNotExist:
		page = EditablePage.objects.create(
			page='service_contacts',
			language=translation.get_language(),
			title='Контакты служб',
			content='<p>Контактная информация служб поддержки, психологов, правоохранительных органов.</p>'
		)
	return render(request, 'core/service_contacts.html', {'page': page})


def instructions(request):
	"""Инструкции"""
	try:
		page = EditablePage.objects.get(page='instructions', language=translation.get_language())
	except EditablePage.DoesNotExist:
		page = EditablePage.objects.create(
			page='instructions',
			language=translation.get_language(),
			title='Инструкции',
			content='<p>Пошаговые инструкции по использованию платформы "Аноним Мектеп".</p>'
		)
	return render(request, 'core/instructions.html', {'page': page})


def send_message(request, unique_id):
	# Определяем школу по уникальному коду из URL
	school = get_object_or_404(School, unique_code=unique_id)
	step = request.GET.get('step', '1')
	
	# Проверяем, является ли это общим сообщением
	is_general_message = unique_id == 'general'
	
	if step == '1':
		# Первый шаг: выбор типа проблемы
		form = ProblemTypeForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid():
				request.session['problem_type'] = form.cleaned_data['problem_type']
				return redirect(f'/send/{unique_id}/?step=2')
			else:
				# Форма не валидна, показываем ошибки
				print(f"Form errors: {form.errors}")
		return render(request, 'core/send_message_step1.html', {
			'form': form, 
			'school': school,
			'is_general_message': is_general_message
		})
	
	elif step == '2':
		# Второй шаг: описание проблемы
		if 'problem_type' not in request.session:
			return redirect(f'/send/{unique_id}/?step=1')
		
		form = SendMessageForm(request.POST or None)
		if request.method == 'POST' and form.is_valid():
			# Проверка reCAPTCHA v3
			recaptcha_token = request.POST.get('recaptcha_token')
			if not verify_recaptcha(recaptcha_token, request.META.get('REMOTE_ADDR')):
				form.add_error(None, 'Проверка безопасности не пройдена. Попробуйте еще раз.')
			else:
				msg = Message.objects.create(
					problem=form.cleaned_data['problem'],
					help=form.cleaned_data['help'],
					contact=form.cleaned_data['contact'],
					school=school,
					problem_type=request.session['problem_type']
				)
				# Очищаем сессию
				del request.session['problem_type']
				notify_admins_about_message(msg)
				return redirect('message_sent')
		
		problem_type = request.session.get('problem_type')
		# Получаем отображаемое название типа проблемы
		problem_type_display = dict(Message.PROBLEM_TYPE_CHOICES).get(problem_type, 'Неизвестно')
		return render(request, 'core/send_message_step2.html', {
			'form': form, 
			'school': school,
			'problem_type': problem_type,
			'problem_type_display': problem_type_display,
			'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY,
			'is_general_message': is_general_message
		})
	
	return redirect(f'/send/{unique_id}/?step=1')

def message_sent(request):
	return render(request, 'core/message_sent.html')
