from django.urls import path
from django.views.i18n import set_language
from . import views
from . import admin_views
from . import telegram_views

urlpatterns = [
    path('', views.index, name='index'),
    path('set-language/', set_language, name='set_language'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contacts/', views.contacts, name='contacts'),
    path('what-to-do/', views.what_to_do, name='what_to_do'),
    # Новые страницы
    path('knowledge-base/', views.knowledge_base, name='knowledge_base'),
    path('service-contacts/', views.service_contacts, name='service_contacts'),
    path('instructions/', views.instructions, name='instructions'),
    path('send-message/', views.send_message_info, name='send_message_info'),
    path('send/<str:unique_id>/', views.send_message, name='send_message'),
    path('message-sent/', views.message_sent, name='message_sent'),
    
    # Админ-панель
    path('staff-login/', admin_views.admin_login, name='admin_login'),
    path('staff-logout/', admin_views.admin_logout, name='admin_logout'),
    path('staff/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('staff/messages/', admin_views.admin_messages, name='admin_messages'),
    path('staff/messages/<int:message_id>/', admin_views.admin_message_detail, name='admin_message_detail'),
    path('staff/schools/', admin_views.admin_schools, name='admin_schools'),
    path('staff/schools/add/', admin_views.add_school, name='add_school'),
    path('staff/schools/<int:school_id>/edit/', admin_views.edit_school, name='edit_school'),
    path('staff/schools/<int:school_id>/delete/', admin_views.delete_school, name='delete_school'),
    path('staff/users/', admin_views.admin_users, name='admin_users'),
    path('staff/users/add/', admin_views.add_user, name='add_user'),
    path('staff/users/<int:user_id>/edit/', admin_views.edit_user, name='edit_user'),
    path('staff/users/<int:user_id>/delete/', admin_views.delete_user, name='delete_user'),
    path('staff/content/', admin_views.admin_content, name='admin_content'),
    path('staff/content/edit/<int:page_id>/', admin_views.edit_page_content, name='edit_page_content'),
    path('staff/content/create/', admin_views.create_page_content, name='create_page_content'),
    
    # Telegram Bot URLs
    path('telegram/webhook/', telegram_views.TelegramWebhookView.as_view(), name='telegram_webhook'),
    path('telegram/set-webhook/', telegram_views.set_webhook, name='telegram_set_webhook'),
    path('telegram/webhook-info/', telegram_views.get_webhook_info, name='telegram_webhook_info'),
]
