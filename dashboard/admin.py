
from django.contrib import admin
from .models import Message, InternalComment

class InternalCommentInline(admin.TabularInline):
	model = InternalComment
	extra = 0

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'problem', 'school', 'problem_type', 'status', 'created_at')
	list_filter = ('school', 'problem_type', 'status')
	search_fields = ('problem', 'school', 'contact')
	inlines = [InternalCommentInline]

@admin.register(InternalComment)
class InternalCommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'message', 'author', 'created_at')
