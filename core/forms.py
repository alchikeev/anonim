from django import forms
from dashboard.models import Message

class ProblemTypeForm(forms.Form):
    PROBLEM_TYPE_CHOICES = [
        (Message.PROBLEM_TYPE_BULLYING, 'Буллинг'),
        (Message.PROBLEM_TYPE_EXTORTION, 'Вымогательство'),
        (Message.PROBLEM_TYPE_VIOLENCE, 'Насилие'),
        (Message.PROBLEM_TYPE_DISCRIMINATION, 'Дискриминация'),
        (Message.PROBLEM_TYPE_ACADEMIC, 'Академические проблемы'),
        (Message.PROBLEM_TYPE_OTHER, 'Другое'),
    ]
    
    problem_type = forms.ChoiceField(
        choices=PROBLEM_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label='Выберите тип проблемы'
    )

class SendMessageForm(forms.Form):
    problem = forms.CharField(
        label='Опишите проблему', 
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Подробно опишите ситуацию...'}),
        required=True
    )
    help = forms.CharField(
        label='Какую помощь вы ожидаете?', 
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Опишите, какая помощь вам нужна...'}),
        required=True
    )
    contact = forms.CharField(
        label='Как с вами связаться (опционально)', 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Телефон, email или другой способ связи'})
    )
