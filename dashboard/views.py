
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Message, InternalComment
from core.models import User

def is_admin(user):
	return user.is_authenticated and user.role in ['super_admin', 'rayon_otdel', 'teacher']

@login_required
@user_passes_test(is_admin)
def dashboard(request):
	messages = Message.objects.select_related('school').order_by('-created_at')
	
	# Фильтрация по ролям
	if request.user.role == 'teacher':
		# Учитель видит только сообщения своей школы
		messages = messages.filter(school=request.user.school)
	elif request.user.role == 'rayon_otdel':
		# Районный отдел видит все сообщения (можно добавить фильтр по району)
		pass
	# Супер-админ видит все сообщения
	
	# Применяем фильтры
	school_filter = request.GET.get('school')
	problem_type = request.GET.get('problem_type')
	status = request.GET.get('status')
	
	if school_filter:
		messages = messages.filter(school__name__icontains=school_filter)
	if problem_type:
		messages = messages.filter(problem_type=problem_type)
	if status:
		messages = messages.filter(status=status)
	
	return render(request, 'dashboard/dashboard.html', {'messages': messages})

@login_required
@user_passes_test(is_admin)
def message_detail(request, pk):
	message = get_object_or_404(Message, pk=pk)
	
	# Проверка доступа для учителей
	if request.user.role == 'teacher' and message.school != request.user.school:
		return redirect('dashboard')
	
	if request.method == 'POST':
		text = request.POST.get('comment')
		if text:
			InternalComment.objects.create(message=message, author=request.user, text=text)
		status = request.POST.get('status')
		if status and status in dict(Message.STATUS_CHOICES):
			message.status = status
			message.save()
		return redirect('message_detail', pk=pk)
	return render(request, 'dashboard/message_detail.html', {'message': message})
