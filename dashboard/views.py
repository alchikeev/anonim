from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from .models import Comment, Message


def role_required(*allowed_roles: User.Roles):
    """Decorator restricting access to users with the given roles."""

    def check(user: User) -> bool:
        return user.is_authenticated and user.role in allowed_roles

    return user_passes_test(check)


@login_required
def message_list(request):
    """Display a list of messages with optional status filtering."""
    messages = Message.objects.all()
    status = request.GET.get("status")
    if status:
        messages = messages.filter(status=status)
    return render(request, "dashboard/message_list.html", {"messages": messages})


@role_required(User.Roles.SUPER_ADMIN, User.Roles.DISTRICT_ADMIN)
def update_status(request, pk: int):
    """Allow privileged users to update a message's status."""
    message = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in dict(Message.Status.choices):
            message.status = status
            message.save()
            return redirect("dashboard:message_list")
    return render(request, "dashboard/update_status.html", {"message": message})


@role_required(
    User.Roles.SUPER_ADMIN, User.Roles.DISTRICT_ADMIN, User.Roles.TEACHER
)
def add_comment(request, pk: int):
    """Add an internal comment to a message."""
    message = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if body:
            Comment.objects.create(message=message, author=request.user, body=body)
            return redirect("dashboard:message_list")
    return render(request, "dashboard/add_comment.html", {"message": message})
