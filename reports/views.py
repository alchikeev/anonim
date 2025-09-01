from django.shortcuts import get_object_or_404, redirect, render

from schools.models import School
from .forms import ReportStep1Form, ReportStep2Form
from .models import Report


def submit_report_step1(request, key):
    school = get_object_or_404(School, submission_key=key)
    if request.method == "POST":
        form = ReportStep1Form(request.POST)
        if form.is_valid():
            request.session["report_type"] = form.cleaned_data["type"]
            return redirect("reports:submit_step2", key=key)
    else:
        form = ReportStep1Form()
    return render(
        request, "reports/submit_step1.html", {"form": form, "school": school}
    )


def submit_report_step2(request, key):
    school = get_object_or_404(School, submission_key=key)
    if "report_type" not in request.session:
        return redirect("reports:submit", key=key)
    if request.method == "POST":
        form = ReportStep2Form(request.POST)
        if form.is_valid():
            Report.objects.create(
                school=school,
                type=request.session.pop("report_type"),
                message_text=form.cleaned_data["message_text"],
            )
            return render(
                request, "reports/submit_success.html", {"school": school}
            )
    else:
        form = ReportStep2Form()
    return render(
        request, "reports/submit_step2.html", {"form": form, "school": school}
    )
