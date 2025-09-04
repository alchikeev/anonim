
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User

class Message(models.Model):
	STATUS_NEW = 'new'
	STATUS_IN_PROGRESS = 'in_progress'
	STATUS_RESOLVED = 'resolved'
	STATUS_SPAM = 'spam'
	STATUS_CHOICES = [
		(STATUS_NEW, _('Новое')),
		(STATUS_IN_PROGRESS, _('В работе')),
		(STATUS_RESOLVED, _('Решено')),
		(STATUS_SPAM, _('Спам')),
	]

	PROBLEM_TYPE_BULLYING = 'bullying'
	PROBLEM_TYPE_EXTORTION = 'extortion'
	PROBLEM_TYPE_VIOLENCE = 'violence'
	PROBLEM_TYPE_DISCRIMINATION = 'discrimination'
	PROBLEM_TYPE_ACADEMIC = 'academic'
	PROBLEM_TYPE_OTHER = 'other'
	PROBLEM_TYPE_CHOICES = [
		(PROBLEM_TYPE_BULLYING, _('Буллинг')),
		(PROBLEM_TYPE_EXTORTION, _('Вымогательство')),
		(PROBLEM_TYPE_VIOLENCE, _('Насилие')),
		(PROBLEM_TYPE_DISCRIMINATION, _('Дискриминация')),
		(PROBLEM_TYPE_ACADEMIC, _('Академические проблемы')),
		(PROBLEM_TYPE_OTHER, _('Другое')),
	]

	problem = models.TextField()
	help = models.TextField()
	contact = models.CharField(max_length=255, blank=True)
	school = models.ForeignKey('core.School', on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
	problem_type = models.CharField(max_length=32, choices=PROBLEM_TYPE_CHOICES, default=PROBLEM_TYPE_OTHER)
	status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_NEW)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.problem[:30]}... ({self.get_status_display()})"

class InternalComment(models.Model):
	message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
