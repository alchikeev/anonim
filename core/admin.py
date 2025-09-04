from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from django.urls import reverse  # добавлено для построения относительных ссылок
import qrcode
import io
import base64
from .models import User, School, EditablePage

@admin.register(EditablePage)
class EditablePageAdmin(admin.ModelAdmin):
	list_display = ('id', 'page', 'language', 'title')
	list_filter = ('page', 'language')
	search_fields = ('title', 'content')
	ordering = ('page', 'language')
	
	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.order_by('page', 'language')


def get_site_domain():
	return getattr(settings, 'SITE_DOMAIN', '127.0.0.1:8000')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'address', 'unique_code', 'school_link', 'school_qr')
	search_fields = ('name', 'address')

	def school_link(self, obj):
		# Полная ссылка на страницу отправки сообщения
		from django.conf import settings
		protocol = 'https' if not settings.DEBUG else 'http'
		domain = get_site_domain()
		relative_url = reverse('send_message', args=[obj.unique_code])
		full_url = f"{protocol}://{domain}{relative_url}"
		return format_html('<a href="{}" target="_blank">{}</a>', full_url, full_url)
	school_link.short_description = 'Ссылка для сообщений'

	def school_qr(self, obj):
		# QR-код на полную ссылку страницы отправки сообщения
		from django.conf import settings
		protocol = 'https' if not settings.DEBUG else 'http'
		domain = get_site_domain()
		relative_url = reverse('send_message', args=[obj.unique_code])
		full_url = f"{protocol}://{domain}{relative_url}"
		qr = qrcode.make(full_url)
		buf = io.BytesIO()
		qr.save(buf, format='PNG')
		img_b64 = base64.b64encode(buf.getvalue()).decode()
		return format_html('<img src="data:image/png;base64,{}" style="height:80px;"/>', img_b64)
	school_qr.short_description = 'QR-код'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'username', 'role', 'school', 'is_active', 'is_staff')
	list_filter = ('role', 'school', 'is_active')
	search_fields = ('username', 'email')
	actions = ['make_teacher', 'make_rayon_otdel', 'make_super_admin']

	def get_actions(self, request):
		actions = super().get_actions(request)
		# Только супер-админы могут назначать роли супер-админа
		if not (request.user.is_superuser or request.user.role == 'super_admin'):
			if 'make_super_admin' in actions:
				del actions['make_super_admin']
		return actions

	def make_teacher(self, request, queryset):
		queryset.update(role=User.TEACHER)
	make_teacher.short_description = 'Назначить роль Учитель'

	def make_rayon_otdel(self, request, queryset):
		queryset.update(role=User.RAYON_OTDEL)
	make_rayon_otdel.short_description = 'Назначить роль Районный отдел'

	def make_super_admin(self, request, queryset):
		# Только супер-админы могут назначать роль супер-админа
		if not (request.user.is_superuser or request.user.role == 'super_admin'):
			self.message_user(request, 'У вас нет прав для назначения роли супер-админа', level='ERROR')
			return
		queryset.update(role=User.SUPER_ADMIN)
	make_super_admin.short_description = 'Назначить роль Супер-админ'

# Register your models here.
