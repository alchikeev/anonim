from django import forms
from django.contrib.auth import get_user_model
from .models import School

User = get_user_model()

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название школы'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Адрес школы'
            }),
        }

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }),
        required=False,
        help_text='Оставьте пустым, если не хотите менять пароль'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'school', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'role': forms.Select(attrs={
                'class': 'form-select'
            }),
            'school': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Если это новый пользователь, пароль обязателен
        if not self.instance.pk:
            self.fields['password'].required = True
        
        # Ограничиваем роли в зависимости от прав пользователя
        if self.user:
            if self.user.role == 'rayon_otdel' and not self.user.is_superuser:
                # Районный отдел может создавать только учителей
                self.fields['role'].choices = [
                    ('teacher', 'Учитель'),
                ]
            elif self.user.role == 'super_admin' or self.user.is_superuser:
                # Супер-админ может создавать всех
                self.fields['role'].choices = [
                    ('super_admin', 'Супер-админ'),
                    ('rayon_otdel', 'Районный отдел'),
                    ('teacher', 'Учитель'),
                ]

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
