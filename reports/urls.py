from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("submit/<uuid:key>/", views.submit_report_step1, name="submit"),
    path(
        "submit/<uuid:key>/confirm/",
        views.submit_report_step2,
        name="submit_step2",
    ),
]
