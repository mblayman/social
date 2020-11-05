from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from social.users.models import User

from .forms import SendInviteForm


@login_required
@require_http_methods(["GET", "POST"])
def send_invite(request, username: str):
    """Send an invite to a new user.

    Creates a pending invite between users.
    """
    to_user = get_object_or_404(User, username=username)
    if request.method == "GET":
        form = SendInviteForm(
            data={"from_user": str(request.user.id), "to_user": str(to_user.id)}
        )
    else:
        form = SendInviteForm(data=request.POST)

    is_valid = form.is_valid()

    if request.method == "POST" and is_valid:
        form.save()
        messages.add_message(request, messages.SUCCESS, f"Invite sent to {username}.")
        return redirect("core:index")

    context: dict = {
        "form": form,
        "remaining_connections": request.user.remaining_connections,
        "to_user": to_user,
    }
    return render(request, "invites/send.html", context)
