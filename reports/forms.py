from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models import Report


class ReportStep1Form(forms.Form):
    type = forms.ChoiceField(choices=Report.Type.choices)


class ReportStep2Form(forms.Form):
    message_text = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField(widget=ReCaptchaV3())
