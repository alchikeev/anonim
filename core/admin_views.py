from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import School, EditablePage
from dashboard.models import Message, InternalComment
from .forms import SendMessageForm, ProblemTypeForm
from .admin_forms import SchoolForm, UserForm

User = get_user_model()

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role in ['super_admin', 'rayon_otdel', 'teacher']:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Неверные учетные данные или недостаточно прав доступа.')
    
    return render(request, 'core/admin_login.html')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
def admin_dashboard(request):
    # Фильтрация по ролям
    if request.user.role == 'teacher':
        # Учитель видит только сообщения своей школы
        messages_queryset = Message.objects.filter(school=request.user.school)
    elif request.user.role == 'rayon_otdel':
        # Районный отдел видит все сообщения
        messages_queryset = Message.objects.all()
    else:
        # Супер-админ видит все сообщения
        messages_queryset = Message.objects.all()
    
    # Статистика
    stats = {
        'new_messages': messages_queryset.filter(status='new').count(),
        'in_progress': messages_queryset.filter(status='in_progress').count(),
        'resolved': messages_queryset.filter(status='resolved').count(),
        'total_messages': messages_queryset.count(),
    }
    
    # Для районного отдела - отдельная статистика по общим сообщениям
    rayon_stats = None
    if request.user.role == 'rayon_otdel':
        from core.models import School
        general_school = School.objects.filter(unique_code='general').first()
        if general_school:
            general_messages = Message.objects.filter(school=general_school)
            rayon_stats = {
                'general_new': general_messages.filter(status='new').count(),
                'general_in_progress': general_messages.filter(status='in_progress').count(),
                'general_resolved': general_messages.filter(status='resolved').count(),
                'general_total': general_messages.count(),
            }
    
    # Последние сообщения
    recent_messages = messages_queryset.order_by('-created_at')[:5]
    
    # Для районного отдела - последние общие сообщения
    recent_general_messages = None
    if request.user.role == 'rayon_otdel':
        from core.models import School
        general_school = School.objects.filter(unique_code='general').first()
        if general_school:
            recent_general_messages = Message.objects.filter(school=general_school).order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'rayon_stats': rayon_stats,
        'recent_messages': recent_messages,
        'recent_general_messages': recent_general_messages,
    }
    
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def admin_messages(request):
    # Фильтрация по ролям
    if request.user.role == 'teacher':
        messages_queryset = Message.objects.filter(school=request.user.school)
    else:
        messages_queryset = Message.objects.all()
    
    # Применяем фильтры
    school_filter = request.GET.get('school')
    problem_type = request.GET.get('problem_type')
    status = request.GET.get('status')
    general_only = request.GET.get('general_only')
    
    if school_filter:
        messages_queryset = messages_queryset.filter(school__name__icontains=school_filter)
    if problem_type:
        messages_queryset = messages_queryset.filter(problem_type=problem_type)
    if status:
        messages_queryset = messages_queryset.filter(status=status)
    
    # Фильтр для сообщений в районный отдел
    if general_only == 'true':
        from core.models import School
        general_school = School.objects.filter(unique_code='general').first()
        if general_school:
            messages_queryset = messages_queryset.filter(school=general_school)
    
    # Сортировка
    messages_queryset = messages_queryset.order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(messages_queryset, 20)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)
    
    context = {
        'messages': messages_page,
        'problem_type_choices': Message.PROBLEM_TYPE_CHOICES,
        'status_choices': Message.STATUS_CHOICES,
    }
    
    return render(request, 'core/admin_messages.html', context)

@login_required
def admin_message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Проверка доступа для учителей
    if request.user.role == 'teacher' and message.school != request.user.school:
        messages.error(request, 'У вас нет доступа к этому сообщению.')
        return redirect('admin_messages')
    
    if request.method == 'POST':
        # Обновление статуса
        new_status = request.POST.get('status')
        if new_status and new_status in dict(Message.STATUS_CHOICES):
            message.status = new_status
            message.save()
            messages.success(request, 'Статус обновлен.')
        
        # Добавление комментария
        comment_text = request.POST.get('comment')
        if comment_text:
            InternalComment.objects.create(
                message=message,
                author=request.user,
                text=comment_text
            )
            messages.success(request, 'Комментарий добавлен.')
        
        return redirect('admin_message_detail', message_id=message_id)
    
    context = {
        'message': message,
        'status_choices': Message.STATUS_CHOICES,
    }
    
    return render(request, 'core/admin_message_detail.html', context)

@login_required
def admin_schools(request):
    if request.user.role not in ['super_admin', 'rayon_otdel'] and not request.user.is_superuser:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('admin_dashboard')
    
    schools = School.objects.all()
    
    context = {
        'schools': schools,
    }
    
    return render(request, 'core/admin_schools.html', context)

@login_required
def add_school(request):
    if request.user.role not in ['super_admin', 'rayon_otdel'] and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Нет доступа'})
    
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save()
            return JsonResponse({
                'success': True, 
                'message': f'Школа "{school.name}" успешно добавлена',
                'school_id': school.id,
                'school_name': school.name,
                'school_code': school.unique_code
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})

@login_required
def edit_school(request, school_id):
    if request.user.role not in ['super_admin', 'rayon_otdel'] and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Нет доступа'})
    
    school = get_object_or_404(School, id=school_id)
    
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=school)
        if form.is_valid():
            school = form.save()
            return JsonResponse({
                'success': True, 
                'message': f'Школа "{school.name}" успешно обновлена',
                'school_name': school.name
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    # GET запрос - возвращаем данные школы
    return JsonResponse({
        'success': True,
        'school': {
            'id': school.id,
            'name': school.name,
            'address': school.address,
            'unique_code': school.unique_code
        }
    })

@login_required
def delete_school(request, school_id):
    if request.user.role not in ['super_admin', 'rayon_otdel'] and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Нет доступа'})
    
    school = get_object_or_404(School, id=school_id)
    
    if request.method == 'POST':
        school_name = school.name
        
        # Подсчитываем связанных пользователей
        teachers_count = User.objects.filter(school=school).count()
        messages_count = Message.objects.filter(school=school).count()
        
        # Удаляем школу (каскадное удаление настроено в модели)
        school.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Школа "{school_name}" и все связанные данные удалены. Удалено: {teachers_count} учителей, {messages_count} сообщений.'
        })
    
    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})

@login_required
def admin_users(request):
    if request.user.role not in ['super_admin', 'rayon_otdel'] and not request.user.is_superuser:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('admin_dashboard')
    
    users = User.objects.all()
    schools = School.objects.all()
    
    context = {
        'users': users,
        'schools': schools,
        'current_user': request.user,
    }
    
    return render(request, 'core/admin_users.html', context)

@login_required
def add_user(request):
    if request.user.role not in ['super_admin', 'rayon_otdel'] and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Нет доступа'})
    
    if request.method == 'POST':
        form = UserForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'success': True, 
                'message': f'Пользователь "{user.username}" успешно добавлен',
                'user_id': user.id,
                'username': user.username
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})

@login_required
def edit_user(request, user_id):
    if request.user.role not in ['super_admin', 'rayon_otdel'] and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Нет доступа'})
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user, user=request.user)
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'success': True, 
                'message': f'Пользователь "{user.username}" успешно обновлен',
                'username': user.username
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    # GET запрос - возвращаем данные пользователя
    return JsonResponse({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email or '',
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'role': user.role,
            'school': user.school.id if user.school else None,
            'is_active': user.is_active
        }
    })

@login_required
def delete_user(request, user_id):
    if request.user.role not in ['super_admin', 'rayon_otdel'] and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Нет доступа'})
    
    user = get_object_or_404(User, id=user_id)
    
    # Нельзя удалить самого себя
    if user == request.user:
        return JsonResponse({'success': False, 'error': 'Нельзя удалить самого себя'})
    
    if request.method == 'POST':
        username = user.username
        
        # Подсчитываем связанные сообщения
        messages_count = Message.objects.filter(school=user.school).count() if user.school else 0
        
        # Удаляем пользователя
        user.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Пользователь "{username}" удален. Связанных сообщений: {messages_count}.'
        })
    
    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})

@login_required
def admin_content(request):
    if request.user.role != 'super_admin' and not request.user.is_superuser:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('admin_dashboard')
    
    pages = EditablePage.objects.all()
    
    context = {
        'pages': pages,
    }
    
    return render(request, 'core/admin_content.html', context)
