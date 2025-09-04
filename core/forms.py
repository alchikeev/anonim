from django import forms
from django.utils.translation import gettext_lazy as _
from dashboard.models import Message

class ProblemTypeForm(forms.Form):
    PROBLEM_TYPE_CHOICES = [
        (Message.PROBLEM_TYPE_BULLYING, _('Буллинг')),
        (Message.PROBLEM_TYPE_EXTORTION, _('Вымогательство')),
        (Message.PROBLEM_TYPE_VIOLENCE, _('Насилие')),
        (Message.PROBLEM_TYPE_DISCRIMINATION, _('Дискриминация')),
        (Message.PROBLEM_TYPE_ACADEMIC, _('Академические проблемы')),
        (Message.PROBLEM_TYPE_OTHER, _('Другое')),
    ]
    
    problem_type = forms.ChoiceField(
        choices=PROBLEM_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label=_('Выберите тип проблемы')
    )

class SendMessageForm(forms.Form):
    problem = forms.CharField(
        label=_('Опишите проблему'), 
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': _('Подробно опишите ситуацию...')}),
        required=True
    )
    help = forms.CharField(
        label=_('Какую помощь вы ожидаете?'), 
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': _('Опишите, какая помощь вам нужна...')}),
        required=True
    )
    contact = forms.CharField(
        label=_('Если хотите чтобы с Вами связались, то оставьте контакты'), 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Телефон, email или другой способ связи')})
    )
