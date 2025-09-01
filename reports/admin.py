from django.contrib import admin
from .models import Report, ProblemType


admin.site.register(ProblemType)
admin.site.register(Report)
